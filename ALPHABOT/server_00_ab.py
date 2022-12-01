from imaplib import Int2AP
import socket
from threading import Thread
import time, sqlite3
import RPi.GPIO as GPIO

"""f|1.1 == 1 metro"""
meter = 1.7
curva90 = 0.45

def readDB():
    """returns the dictionary of the commands (names)"""
    connection = sqlite3.connect("./MOVIMENTI.db")
    cursor = connection.cursor()
    list = cursor.execute("SELECT * FROM MOVIMENTI")
    movementsListDB = list.fetchall()
    ####################################################
    commandNames = {}
    for m in movementsListDB:
        commandNames[m[0]] = m[0] # name command = duration time
    return commandNames

class AlphaBot(object):
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26, time=1):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 50
        self.PB  = 50

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stopNoT()

    def forward(self): # va "indietro": la sinistra gira di meno
        self.PWMA.ChangeDutyCycle(50) # guardandolo quando va avanti: ruota sx
        self.PWMB.ChangeDutyCycle(58.7)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def stopNoT(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def stop(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def backward(self): # va "avanti"
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def left(self, speed=30): # 
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def right(self, speed=30): # 
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

class Ricevitore(Thread):
    def __init__(self,connection,ad):
        Thread.__init__(self)    
        self.running=True
        self.connection, self.address=connection,ad
        self.connection.sendall("Ti sei connesso".encode()) # manda il messaggio e lo stampa sullo schermo del computer
        print(f"{self.address} si è connesso\n")

    def run(self):
        while self.running:
            dati=self.connection.recv(4096) # riceve dalla sua connection
            self.connection.sendall(dati.encode()) # l'invio dei dati sempre sulla connessione

    def stop(self, time):
        self.running=False
        time.sleep(time)

def contaTempo(tempoComando, start):
    timeMesured = 0
    while timeMesured < tempoComando:
        now = time.time()
        timeMesured = now - start
        
def main():
    dictMov = readDB()
    print(dictMov)
    Ab = AlphaBot()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ipv4, tcp
    s.bind(("0.0.0.0", 5000)) #.136
    s.listen() # permette al server di allocare risorse: si prepara a ricevere dati
    conn, add = s.accept() # qui invece sta in attesa: aspetta la connessione
        
    while True:
        data = conn.recv(4096)
        data = data.decode()
        print(data) # sapere cosa ho inviato
        #listaStringhe = data.split(";") # la stringa dovrebbe essere: "comando|tempo;comando2|tempo2"
        listaComandi = data.split("|")
        comando = listaComandi[0]
        tempoComando = float(listaComandi[1])
        print(f"print del comando e del tempo: {comando}, {tempoComando} {type(tempoComando)}")
        # al posto di mettere le if si può fare un dizionario
        start = time.time()
        if comando == "f": 
            Ab.forward()
            contaTempo(tempoComando, start)
        elif comando == "b": 
            Ab.backward()
            contaTempo(tempoComando, start)
        elif comando == "r":
            Ab.right()
            contaTempo(tempoComando, start) # gira a dx
        elif comando == "l": 
            Ab.left()
            contaTempo(tempoComando, start)
        elif comando == 's': 
            Ab.forward()
            contaTempo(meter, start) # va avanti un metro
            start = time.time() # riprende il time
            Ab.right()
            contaTempo(curva90, start) # gira e va avanti
            start = time.time()
            Ab.forward()
            contaTempo(meter, start) # finisce di andare avanti
            start = time.time()
            Ab.left()
            contaTempo(curva90, start) # gira a sinistra
            start = time.time() # riprende il time
            Ab.forward()
            contaTempo(curva90, start) # va avanti un metro
            #time.sleep(tempoComando)
        elif comando == 'c': # dobbiamo cambiare le misure
            Ab.forward()
            contaTempo(meter*2, start) # va avanti un metro
            start = time.time() # riprende il time
            Ab.left()
            contaTempo(curva90, start) # gira e va avanti
            start = time.time()
            Ab.forward()
            contaTempo(meter*2, start) # finisce di andare avanti
            start = time.time()
            Ab.right()
            contaTempo(0.2, start) # gira a sinistra
            start = time.time() # riprende il time
            Ab.forward()
            contaTempo(meter*2, start) # va avanti un metro
        conn.sendall(data.encode())
        Ab.stop()
    conn.close()
    
if __name__ == "__main__":
    main()

# C:\Users\paola\Documents\SCUOLA\FRANCY\V!!!\SIS\AB
