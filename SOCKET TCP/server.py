import socket
import sqlite3
from threading import Thread


def caricaDati():
    connectionDB = sqlite3.connect('file.db')
    cursor = connectionDB.cursor()
    res = cursor.execute('SELECT * FROM files')
    files = res.fetchall()
    print(files)
    res = cursor.execute('SELECT * FROM frammenti')
    frammenti = res.fetchall()
    print(frammenti)
    connectionDB.close()

    return files, frammenti


def isPresente(files, nomeFile):
    nomiFile = [file[1] for file in files]
    if nomeFile in nomiFile:
        return True
    else:
        return False


def numeroFrammenti(files, nomeFile):
    file_frammenti = {}
    for file in files:
        file_frammenti[file[1]] = file[2]
    return file_frammenti[nomeFile]


def ipHost(nomeFile, id_frammento):
    connenctionDB = sqlite3.connect('file.db')
    cursor = connenctionDB.cursor()
    query = f'SELECT host FROM files, frammenti WHERE files.id_file = frammenti.id_file AND files.nome = "{nomeFile}" AND n_frammento = {id_frammento}'
    # print(query)
    res = cursor.execute(query)
    host = res.fetchone()
    connenctionDB.close()
    return host[0]


def allIpHosts(nomeFile):
    connenctionDB = sqlite3.connect('file.db')
    cursor = connenctionDB.cursor()
    res = cursor.execute(
        f'SELECT host FROM frammenti,files WHERE files.nome = "{nomeFile}" AND files.id_file = frammenti.id_file')
    hosts = res.fetchall()
    hosts = [host[0] for host in hosts]
    stringa = ''
    for host in hosts:
        stringa += host + '\n'
    connenctionDB.close()
    return stringa


class Client(Thread):
    def __init__(self, connection):
        Thread.__init__(self)
        self.running = True
        self.connection = connection

        self.files, self.frammenti = caricaDati()

    def run(self):
        while self.running:
            # codOperazione,nomeFile(,id_frammento)
            msgR = self.connection.recv(4096)
            msgR = msgR.decode()
            msgR = msgR.split(',')
            if int(msgR[0]) == 1:
                if isPresente(self.files, msgR[1]):
                    self.connection.sendall("Il file è presente".encode())
                else:
                    self.connection.sendall("Il file non è presente".encode())
            elif int(msgR[0]) == 2:
                numero = numeroFrammenti(self.files, msgR[1])
                self.connection.sendall(
                    ("numero frammenti: "+str(numero)).encode())
            elif int(msgR[0]) == 3:
                host = ipHost(msgR[1], msgR[2])
                self.connection.sendall(
                    ("host contentente il frammento: "+str(host)).encode())
            elif int(msgR[0]) == 4:
                stringa = allIpHosts(msgR[1])
                self.connection.sendall(
                    ("host che contengo i frammenti del file:\n"+stringa).encode())
            elif int(msgR[0]) == 0:
                self.stop()

    def stop(self):
        self.running = False


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listaThread = []

s.bind(("127.0.0.1", 8000))
s.listen()

while True:
    connection, address = s.accept()
    print(f"Connesso con {address}")
    client = Client(connection)
    client.start()
    listaThread.append(client)

    for thread in listaThread:
        if not thread.running:
            thread.join()
            listaThread.remove(thread)
