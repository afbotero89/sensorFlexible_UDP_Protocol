# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rigidoBotonesConexion.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!


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
#ion()

maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1
sys.setrecursionlimit(maxint)

class Ui_MainWindow(object):
    def __init__(self):
        print("init")
        self.vectorDatosDistribucionPresion = []
        self.vectorDesencriptado = []
        self.iniciaTramaDeDatos = False
        self.columnas = 43;
        self.filas = 43;
        matriz = [[0 for x in range(self.columnas)] for x in range(self.filas)] 
        matriz[0][0] = 255
        #self.cronometro = tiemposDeExposicion.Cronometro()
        #self.interfazTiempos = interfazTiemposExposicionSensor1.interfazTiemposExposicion()
        self.angle = 0
        self.contadorCalculaTiemposExposicion = 0
        self.contadorImagenes = 0
        
    def socketConnection(self):
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.s.settimeout(0.5)
        #self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        #self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.UDP_IP = "192.168.0.108"
        self.UDP_PORT = 10000

        self.UDP_IP_CLIENT = "192.168.0.107"
        self.UDP_PORT_CLIENT = 2233

        print("escuchando",self.UDP_IP, self.UDP_PORT)
        self.s.bind((self.UDP_IP, self.UDP_PORT))
        #self.s.listen(1)
        self.campoSensor1Creado = False
        #self.sc, self.addr = self.s.accept()
        for i in range(3):            
            time.sleep(1)
            self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
            #self.sc.send(('*').encode())
            print("conecto 1")
        self.sqlDataBase()
        self.recibeDatos()
        
        
    def sqlDataBase(self):
        
        self.conn = sqlite3.connect('distribucionPresionSensorFlexible.db')
        self.c = self.conn.cursor()
        #self.c.execute("DELETE FROM `sensorSuperior` WHERE 1")
        # Create table
        self.c.execute('''CREATE TABLE IF NOT EXISTS sensorFlexible (id text, data real, connectionStatus text, angle text, exposureTimes real)''')
        # Insert a row of data
        for row in self.c.execute("SELECT * FROM sensorFlexible WHERE 1"):
            print(row[0])
            if row[0] == '1':
                self.campoSensor1Creado = True

        if self.campoSensor1Creado == False:
            self.campoSensor1Creado = True
            self.c.execute("INSERT INTO sensorFlexible VALUES ('1','initValue sensor 1','True','0','initValue times 1')")
        self.conn.commit()

        self.conn1 = sqlite3.connect('datosSensor1Respiracion.db')
        self.c1 = self.conn1.cursor()
        self.c1.execute('''CREATE TABLE IF NOT EXISTS sensorFlexibleTransmision (id text, data real, hour real, angle text)''')
        self.conn1.commit()
        
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
      
##      for i in range(self.filas):
##        for j in range(self.columnas):
##          if matrizDistribucion[i][j] < 0:
##              matrizDistribucion[i][j] = 0
##          else:
##              matrizDistribucion[i][j] = matrizDistribucion[i][j] + 20
            
##      for i in range(self.filas-1):
##        for j in range(self.columnas-1):
##            if i > 0 and j > 0:
##                matrizDistribucion[i][j] = (matrizDistribucion[i+1][j] + matrizDistribucion[i-1][j] + matrizDistribucion[i][j-1] + matrizDistribucion[i][j+1])/8
##
      maximoValor = 0
      print("inserta datos")


      hora = time.strftime("%H:%M:%S")

      #self.contadorImagenes = self.contadorImagenes + 1
      #self.c1.execute("INSERT INTO sensorFlexibleTransmision VALUES ('%s',  '%s', '%s', '%s')" % (self.contadorImagenes, matrizDistribucion,hora,angle))
      #self.conn1.commit()
      
      
      for i in range(self.filas):
        for j in range(self.columnas):
            matrizDistribucion[i][j] = matrizDistribucion[i][j]*25

            if matrizDistribucion[i][j] > 200:
                matrizDistribucion[i][j] = 240

      self.c.execute("UPDATE `sensorFlexible` SET `data`= '%s', `angle`= '%s' WHERE `id`='1'" % (matrizDistribucion, angle))
      self.conn.commit()
      #data = scipy.ndimage.zoom(matrizDistribucion, 1)
      
      self.contadorCalculaTiemposExposicion = self.contadorCalculaTiemposExposicion + 1
      if self.contadorCalculaTiemposExposicion == 10:
        self.contadorCalculaTiemposExposicion = 0
        #self.interfazTiempos.evento(self.vectorDesencriptado)


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

