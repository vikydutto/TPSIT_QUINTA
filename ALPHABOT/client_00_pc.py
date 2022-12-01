import socket
from threading import Thread

class Ricevitore(Thread):
    def __init__(self,socket):
        Thread.__init__(self)
        self.socket = socket
        self.running = True

    def run(self):
        while self.running:
            while True:
                dati = self.socket.recv(4096)
                inf = dati.decode()
                print(f"\t{inf}")
            self.stop()

    def stop(self):
        self.running = False

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.0.137", 5000))
    #s.connect(("192.168.0.138", 8000)) # .136 -> bot, 138 -> pc

    while True:
        messaggio = input("Comando AB: ")
        s.sendall(messaggio.encode())

if __name__ == "__main__":
    main()

# C:\Users\paola\Documents\SCUOLA\FRANCY\V!!!\SIS\AB
