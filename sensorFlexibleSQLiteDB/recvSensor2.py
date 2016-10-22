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
#import scipy.ndimage
import sys, struct
#from pylab import *
import tiemposDeExposicion
#import interfazTiemposExposicionSensor2
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
        #self.interfazTiempos = interfazTiemposExposicionSensor2.interfazTiemposExposicion()
        self.angle = 0
        self.contadorCalculaTiemposExposicion = 0
        
    def socketConnection(self):
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.s.settimeout(0.5)
        #self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        #self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.UDP_IP = "192.168.0.124"
        self.UDP_PORT = 10006

        self.UDP_IP_CLIENT = "192.168.0.101"
        self.UDP_PORT_CLIENT = 2233

        self.s.bind((self.UDP_IP,self.UDP_PORT))
        #self.s.listen(1)
        self.campoSensor1Creado = False
        print('escuchando ..', self.UDP_IP, self.UDP_PORT)
        #self.sc, self.addr = self.s.accept()
        
        for i in range(3):            
            time.sleep(1)
            #self.sc.send(('*').encode())
            self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
            print("conecto 2")
        self.sqlDataBase()
        self.recibeDatos()
        
        
    def sqlDataBase(self):
        print('sql database')
        self.conn = sqlite3.connect('distribucionPresionSensorFlexible.db')
        self.c = self.conn.cursor()
        #self.c.execute("DELETE FROM `sensorSuperior` WHERE 1")
        # Create table
        self.c.execute('''CREATE TABLE IF NOT EXISTS sensorFlexible
                     (id text, data real, connectionStatus text, angle text, exposureTimes real)''')
        # Insert a row of data
        for row in self.c.execute("SELECT * FROM sensorFlexible WHERE 1"):
            if row[0] == '2':
                self.campoSensor1Creado = True

        if self.campoSensor1Creado == False:
            self.campoSensor1Creado = True
            self.c.execute("INSERT INTO sensorFlexible VALUES ('2','initValue sensor 2','True','0','initValue times 2')")
        self.conn.commit()
        
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
                print(len(buf))
         #       self.sc.settimeout(0)
                #print(time.strftime("%H:%M:%S"))
                info = [buf[i:i+1] for i in range(0, len(buf), 1)]
                #try:
                for i in info:
                    valorDecimal = int(binascii.hexlify(i),16)
                    
                    if self.iniciaTramaDeDatos == False:
                      self.vectorDatosDistribucionPresion.append(valorDecimal)
                      
                      if valorDecimal == 255:
                        #print(time.strftime("%H:%M:%S"), "angulo:", self.angle, "longitud vector:",len(self.vectorDatosDistribucionPresion))
                        self.angle = self.vectorDatosDistribucionPresion[len(self.vectorDatosDistribucionPresion) - 2]
                        self.primerByte = self.vectorDatosDistribucionPresion[len(self.vectorDatosDistribucionPresion) - 4]
                        self.segundoByte = self.vectorDatosDistribucionPresion[len(self.vectorDatosDistribucionPresion) - 3]
                        self.numeroBytes = self.primerByte*255 + self.segundoByte
                        
                        if(self.numeroBytes == len(self.vectorDatosDistribucionPresion) - 4):

                            self.vectorDatosDistribucionPresion=self.vectorDatosDistribucionPresion[:len(self.vectorDatosDistribucionPresion)-1]
                            self.vectorDatosDistribucionPresion=self.vectorDatosDistribucionPresion[:len(self.vectorDatosDistribucionPresion)-1]
                            self.vectorDatosDistribucionPresion=self.vectorDatosDistribucionPresion[:len(self.vectorDatosDistribucionPresion)-1]
                            self.vectorDatosDistribucionPresion.append(255)
                            self.vectorDesencriptado = self.desencriptarVector(self.vectorDatosDistribucionPresion)
                            self.dibujarDistribucionPresion(self.vectorDesencriptado)
                            #self.interfazTiempos.evento(self.vectorDesencriptado)
                            self.vectorDatosDistribucionPresion = []
                            info = []
                            self.iniciaTramaDeDatos = False
                            #self.sc.send(('*').encode())
                            self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
                            break
                        else:
                            self.vectorDatosDistribucionPresion = []
                            info = []
                            self.iniciaTramaDeDatos = False
                            #self.sc.send(('*').encode())
                            self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
                            break

                    if valorDecimal == 255 and self.iniciaTramaDeDatos == False:
                        #self.sc.send(('*').encode())
                        #self.s.sendto(bytes('*','utf-8'), ("192.168.0.100", 2233))
                        self.iniciaTramaDeDatos = True
                self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
                #time.sleep(0.2)
                #self.sc.send(('*').encode())
                #threading.Timer(0.01, self.recibeDatos()).start()
        except:
            print('nueva conexion')
            self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
            self.recibeDatos()
            #self.sc.close()
            #self.s.close()
            #self.socketConnection()

        
    def dibujarDistribucionPresion(self, matrizDistribucion):
      
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
##      maximoValor = 0
##      
      for i in range(self.filas):
        for j in range(self.columnas):
            matrizDistribucion[i][j] = matrizDistribucion[i][j]*15
##
            if matrizDistribucion[i][j] > 200:
                matrizDistribucion[i][j] = 240
##            if matrizDistribucion[i][j] >= maximoValor:
##                maximoValor = matrizDistribucion[i][j]
      #print(maximoValor)
      
 #     data = scipy.ndimage.zoom(matrizDistribucion, 1)
      self.contadorCalculaTiemposExposicion = self.contadorCalculaTiemposExposicion + 1
      if self.contadorCalculaTiemposExposicion == 10:
        self.contadorCalculaTiemposExposicion = 0
        #self.interfazTiempos.evento(self.vectorDesencriptado)

      print("2")
      self.c.execute("UPDATE `sensorFlexible` SET `data`= '%s' WHERE `id`='2'" % matrizDistribucion)
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

