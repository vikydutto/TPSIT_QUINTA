import socket
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
stringa=""
while stringa!="exit":
    stringa=input("Dammi il messaggio: ")
    indirizzo_server=(("192.168.0.138",5000))
    indirizzo_client=(("0.0.0.0",5000))
    s.sendto(stringa.encode(), indirizzo_server)