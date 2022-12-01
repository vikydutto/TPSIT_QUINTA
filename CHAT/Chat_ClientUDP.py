import socket
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
stringa = ""

s.bind(("0.0.0.0", 5000))

class Receiver(Thread):
    def __init__(self, s):
        Thread.__init__(self)
        self.s = s
        self.running = True

    def run(self):
        while self.running:
            dati, ind_client = self.s.recvfrom(4096)
            print(f"\n{dati.decode()}")

    def stop(self):
        self.running = False
      
def main():
    t1 = Receiver(s)
    t1.start()

    while True:
        dest = input("DESTINATARIO: ")
        messaggio = input("MESSAGGIO: ")

        stringa = messaggio + "|" + dest

        s.sendto(stringa.encode(), ("192.168.0.136", 5000))

    s.close()

if __name__ == "__main__":
    main()