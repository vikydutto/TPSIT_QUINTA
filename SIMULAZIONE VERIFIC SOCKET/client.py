import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 8000))

opzione = None

while opzione != 0:
    print("\n 1) Verifica se un file è presente nel DB\n",
          "2) Numero di frammenti di un file\n",
          "3) IP di un host che contiene un frammento di un file\n",
          "4) IP di tutti gli host che contengono i frammento di un file\n")

    opzione = int(input("Inserisci l'opzione: "))

    if opzione == 1:
        nomeFile = input("Inserisci il nome del file: ")
        s.sendall(f"{opzione},{nomeFile}".encode())
        msgR = s.recv(4096).decode()
        print(msgR)
    elif opzione == 2:
        nomeFile = input("Inserisci il nome del file: ")
        s.sendall(f"{opzione},{nomeFile}".encode())
        msgR = s.recv(4096).decode()
        print(msgR)
    elif opzione == 3:
        nomeFile = input("Inserisci il nome del file: ")
        id_frammento = input("Inserisci l'id del frammento: ")
        s.sendall(f"{opzione},{nomeFile},{id_frammento}".encode())
        msgR = s.recv(4096).decode()
        print(msgR)
    elif opzione == 4:
        nomeFile = input("Inserisci il nome del file: ")
        s.sendall(f"{opzione},{nomeFile}".encode())
        msgR = s.recv(4096).decode()
        print(msgR)
    elif opzione == 0:
        s.sendall(f"{opzione}".encode())
        s.close()
