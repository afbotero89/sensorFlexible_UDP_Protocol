import socket
import sys
import binascii
import threading
import numpy as np
import socket
import scipy.ndimage
import sys, struct
#from pylab import *
import tiemposDeExposicion
#import interfazTiemposExposicionSensor1
import time
import sqlite3
from PIL import Image

#ion()

maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1
sys.setrecursionlimit(maxint)

class Ui_MainWindow(object):
    def __init__(self, UDP_IP, UDP_PORT, UDP_IP_CLIENT, UDP_PORT_CLIENT, idSensor):
        print("init", idSensor)
        self.vectorDatosDistribucionPresion = []
        self.vectorDesencriptado = []
        self.iniciaTramaDeDatos = False
        self.columnas = 43;
        self.filas = 43;
        matriz = [[0 for x in range(self.columnas)] for x in range(self.filas)] 
        matriz[0][0] = 255
        self.angle = 0
        self.contadorImagenes = 0

        self.UDP_IP = UDP_IP
        self.UDP_PORT = UDP_PORT

        self.UDP_IP_CLIENT = UDP_IP_CLIENT
        self.UDP_PORT_CLIENT = UDP_PORT_CLIENT

        # Para esta version de la sabana, el sensor tiene dos modulos wifi, por tal razon se almacenan en bases de datos distintas su informacion id=1(cabeza), id=2(piernas)
        self.idSensor = idSensor  
        self.conectarSensor()     
        
    def socketConnection(self):
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print("escuchando",self.UDP_IP, self.UDP_PORT)
        self.s.bind((self.UDP_IP, self.UDP_PORT))
        #self.s.listen(1)
        self.campoSensor1Creado = False

        self.s.settimeout(1)
        while True:            
            time.sleep(2)
            self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
            print("envia peticion", self.idSensor)
            try:
                buf = self.s.recv(10)
                if(len(buf)>5):
                    self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
                    break
            except:
                print("Time out error")
        print("conecto", self.idSensor)
        self.s.settimeout(2)
        self.sqlDataBase()
        self.recibeDatos()
        
        
    def sqlDataBase(self):
        
        try:
            self.conn = sqlite3.connect('distribucionPresionSensorFlexible.db')
            self.c = self.conn.cursor()
            #self.c.execute("DELETE FROM `sensorSuperior` WHERE 1")
            # Create table
            self.c.execute('''CREATE TABLE IF NOT EXISTS sensorFlexible (id text, data real, connectionStatus text, angle text, exposureTimes real)''')
            # Insert a row of data
            for row in self.c.execute("SELECT * FROM sensorFlexible WHERE '%s'" % self.idSensor):
                print(row[0])
                if row[0] == self.idSensor:
                    self.campoSensor1Creado = True

            if self.campoSensor1Creado == False:
                self.campoSensor1Creado = True
                self.c.execute("INSERT INTO sensorFlexible VALUES ('%s','initValue sensor 1','True','0','initValue times 1')" % self.idSensor)
            self.conn.commit()

        except:
            pass
        
    def desencriptarVector(self,vector):
        n = len(vector);
        fil = 0;
        col = 0;
        matriz = [[0 for x in range(self.columnas)] for x in range(self.filas)];
        banderacero = 0;
        for x in range(0, n):
            datos = vector[x];
            if datos == 0:
                banderacero = 1;
            elif datos == 255:
                return matriz;
            else:
                if banderacero == 1:
                    for k in range (0, datos):
                        if col == self.columnas:
                            col = 0;
                            fil = fil + 1;
                            if fil > self.filas:
                                return matriz;
                            matriz[fil][col] = 0;
                        col = col + 1;
                else:
                    if col >= self.columnas:
                        col = 0;
                        fil = fil + 1;
                        if fil >= self.filas:
                            return matriz;
                    matriz[fil][col] = datos;
                    col = col + 1;
                banderacero = 0;
                
    def recibeDatos(self):
        try:
            while True:
                #self.sc.settimeout(None)

                buf = self.s.recv(10000)
         #       self.sc.settimeout(0)
                print(time.strftime("%H:%M:%S"))
                #print(buf)
                #print(len(buf))
                if len(buf)<10000:
                
                    info = [buf[i:i+1] for i in range(0, len(buf), 1)]
                    #try:
                    for i in info:
                        valorDecimal = int(binascii.hexlify(i),16)
                        
                        if self.iniciaTramaDeDatos == False:
                          self.vectorDatosDistribucionPresion.append(valorDecimal)
                          
                          if valorDecimal == 255:
                            #print(time.strftime("%H:%M:%S"), "angulo:", self.angle, len(self.vectorDatosDistribucionPresion))
                            self.angle = self.vectorDatosDistribucionPresion[len(self.vectorDatosDistribucionPresion) - 2]
                            #self.angle = 90-self.angle
                            self.primerByte = self.vectorDatosDistribucionPresion[len(self.vectorDatosDistribucionPresion) - 4]
                            self.segundoByte = self.vectorDatosDistribucionPresion[len(self.vectorDatosDistribucionPresion) - 3]
                            self.numeroBytes = self.primerByte*255 + self.segundoByte
                            if(self.numeroBytes == len(self.vectorDatosDistribucionPresion) - 4):
                                self.vectorDatosDistribucionPresion=self.vectorDatosDistribucionPresion[:len(self.vectorDatosDistribucionPresion)-1]
                                self.vectorDatosDistribucionPresion=self.vectorDatosDistribucionPresion[:len(self.vectorDatosDistribucionPresion)-1]
                                self.vectorDatosDistribucionPresion=self.vectorDatosDistribucionPresion[:len(self.vectorDatosDistribucionPresion)-1]
                                self.vectorDatosDistribucionPresion.append(255)
                                self.vectorDesencriptado = self.desencriptarVector(self.vectorDatosDistribucionPresion)
                                self.dibujarDistribucionPresion(self.vectorDesencriptado, self.angle)
                                #self.interfazTiempos.evento(self.vectorDesencriptado)
                                self.vectorDatosDistribucionPresion = []
                                info = []
                                self.iniciaTramaDeDatos = False
                                self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
                                #self.sc.send(('*').encode())
                                break
                            else:
                                self.vectorDatosDistribucionPresion = []
                                info = []
                                self.iniciaTramaDeDatos = False
                                self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
                                #self.sc.send(('*').encode())
                                break

                        if valorDecimal == 255 and self.iniciaTramaDeDatos == False:
                            #self.s.sendto(bytes('*','utf-8'), ("192.168.0.102", 2233))
                            #self.sc.send(('*').encode())
                            self.iniciaTramaDeDatos = True
                self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
                #time.sleep(0.2)
                    #self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))        
                    #self.sc.send(('*').encode())
                #threading.Timer(0.01, self.recibeDatos()).start()
        except:
            print('nueva conexion')
            self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
            self.recibeDatos()
            #self.sc.close()
            #self.s.close()
            #self.socketConnection()


        
    def dibujarDistribucionPresion(self, matrizDistribucion, angle):
      
      maximoValor = 0

      hora = time.strftime("%H:%M:%S")

      for i in range(self.filas):
        for j in range(self.columnas):
            matrizDistribucion[i][j] = matrizDistribucion[i][j]*25

            if matrizDistribucion[i][j] > 200:
                matrizDistribucion[i][j] = 240

      self.c.execute("UPDATE `sensorFlexible` SET `data`= '%s', `angle`= '%s' WHERE `id`='%s'" % (matrizDistribucion, angle, self.idSensor))
      self.conn.commit()


    def conectarSensor(self):
        #try:
            self.socketConnection()
            threading.Timer(0.01, self.recibeDatos()).start()
            print("conecta conecta")
        #except:
            #print("No conecta")
                      
        
    def desconectaSensor(self):
        #self.s.close()
        try:
            self.s.close()
            print("desconecta sensor")
        except:
            print("Sensor desconectado")
#import rscimagenes_rc

if __name__ == "__main__":
    import sys
    ui = Ui_MainWindow()
    ui.conectarSensor()
    #ui.recibeDatos()