# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

#from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image, ImageDraw
import matplotlib
matplotlib.use('TKAgg')
import socket
import sys
import binascii
import threading
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process
import threading
import scipy.ndimage
import sys, struct
#import tiemposDeExposicion
#import interfazTiemposExposicionSensor1
from pylab import *
#import pusher
import time
import os
import sqlite3
import ast
import recvSensor1
import interfazTiemposExposicionSensor1
import graphicsRealTimeAverageSensor_1

ion()


maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1
print("maximo nivel de recurso")
print(maxint)
sys.setrecursionlimit(maxint)


class Ui_MainWindow(object):
    def __init__(self):

        #Socket connection
        self.ip = "192.168.0.124"
        self.port = 10005
        self.columnas = 43;
        self.filas = 43;
        
        matriz = [[0 for x in range(self.columnas)] for x in range(self.filas)] 
        #matriz[0][0] = 255
        matrizSensor2 = [[0 for x in range(self.columnas)] for x in range(self.filas)] 
        matrizCompleta = np.concatenate((matriz,matrizSensor2),axis=1)

        matrizCompleta[0][0] = 255

        self.initData = scipy.ndimage.zoom(matrizCompleta, 3)
        self.figSensor1 = plt.figure(figsize=(8,4),frameon=False)
        self.figSensor1.set_size_inches(8,4)
        ax = plt.Axes(self.figSensor1, [0., 0., 1., 1.])
        ax.set_axis_off()
        self.figSensor1.add_axes(ax)
        self.figSensor1.canvas.draw()
        self.figSensor1.canvas.set_window_title('Sensor 1')

        self.imagenSensor1 = plt.imshow(self.initData, interpolation = 'nearest')
        #self.figSensor1.tight_layout()
        
        self.vectorImagen = []
        self.vectorDatosDistribucionPresion = []
        self.vectorDesencriptado = []
        #self.vectorImagen = [255,0,45,2,0,184,3,0,107,3,0,117,2,0,112,5,0,18,7,0,7,6,0,1,12,14,2,0,3,4,0,1,2,0,9,2,0,7,9,9,47,45,26,7,0,24,10,11,15,3,0,25,7,7,14,0,62,14,0,19,3,7,6,0,7,5,0,17,10,47,54,32,0,24,5,11,49,51,0,26,5,2,0,40,255]
        #self.cronometro = tiemposDeExposicion.Cronometro()
        #self.interfazTiempos = interfazTiemposExposicionSensor1.interfazTiemposExposicion()
        self.iniciaTramaDeDatos = False

        plt.set_cmap('jet')

        self.sqlDataBase()
        self.contadorImagenes = 0

        # Sensor 1: cabeza
        self.UDP_IP_Sensor1 = "192.168.0.124"
        self.UDP_PORT_Sensor1 = 10000

        self.UDP_IP_CLIENT_Sensor1 = "192.168.0.100"
        self.UDP_PORT_CLIENT_Sensor1 = 2233

        self.idSensor_Sensor1 = "1"


        # Sensor 2: piernas
        self.UDP_IP_Sensor2 = "192.168.0.124"
        self.UDP_PORT_Sensor2 = 10001

        self.UDP_IP_CLIENT_Sensor2 = "192.168.0.101"
        self.UDP_PORT_CLIENT_Sensor2 = 2233

        self.idSensor_Sensor2 = "2"
        
        # Comunicacion sensor 1
        self.t = threading.Thread(target = recvSensor1.Ui_MainWindow, args=(self.UDP_IP_Sensor1, self.UDP_PORT_Sensor1, self.UDP_IP_CLIENT_Sensor1, self.UDP_PORT_CLIENT_Sensor1, self.idSensor_Sensor1,))
        self.t.IsBackground = True;
        self.t.start()

        # Comunicacion sensor 2
        self.s = threading.Thread(target = recvSensor1.Ui_MainWindow, args=(self.UDP_IP_Sensor2, self.UDP_PORT_Sensor2, self.UDP_IP_CLIENT_Sensor2, self.UDP_PORT_CLIENT_Sensor2, self.idSensor_Sensor2,))
        self.s.IsBackground = True;
        self.s.start()

        # Interfaz tiempos de exposicion 1
        self.u = threading.Thread(target = interfazTiemposExposicionSensor1.interfazTiemposExposicion, args=("1",))
        self.u.IsBackground = True;
        self.u.start()

        # Interfaz tiempos de exposicion 2
        self.v = threading.Thread(target = interfazTiemposExposicionSensor1.interfazTiemposExposicion, args=("2",))
        self.v.IsBackground = True;
        self.v.start()

        # Calculo de promedios de presion por zonas
        self.w = threading.Thread(target = graphicsRealTimeAverageSensor_1.Ui_MainWindow)
        self.w.IsBackground = True;
        self.w.start()

    def sqlDataBase(self):
        
        self.conn = sqlite3.connect('distribucionPresionSensorFlexible.db')
        self.c = self.conn.cursor()

        self.conn1 = sqlite3.connect('transmisionContinua.db')
        self.c1 = self.conn1.cursor()
        self.c1.execute('''CREATE TABLE IF NOT EXISTS sensorFlexibleTransmision (id text, data1 real, data2 real, hour real)''')
        self.conn1.commit()

    def printit(self):
        global vectorImagen, iniciaTramaDeDatos, vectorDatosDistribucionPresion, s
        while True:
          self.dibujarDistribucionPresionSensor1()

        
    def dibujarDistribucionPresionSensor1(self):
        try:
            maximoValor = 0
            for row in self.c.execute("SELECT * FROM sensorFlexible WHERE `id`='1'"):
                dataSensor1 = row[1]
            for row in self.c.execute("SELECT * FROM sensorFlexible WHERE `id`='2'"):
                dataSensor2 = row[1]
            
            #Sensor 1
            matrizSensor1 = ast.literal_eval(str(dataSensor1))
            #matrizSensor1 = scipy.ndimage.rotate(matrizSensor1, 0)

            #Sensor 1
            matrizSensor2 = ast.literal_eval(str(dataSensor2))

            self.contadorImagenes = self.contadorImagenes + 1
            hora = time.strftime("%H:%M:%S")

            #self.c1.execute("INSERT INTO sensorFlexibleTransmision VALUES ('%s',  '%s', '%s', '%s')" % (self.contadorImagenes, matrizSensor1, matrizSensor2 ,hora))

            matrizSensor2 = scipy.ndimage.rotate(matrizSensor2, -90)

            matrizCompleta = np.concatenate((matrizSensor1,matrizSensor2), axis=1)
            #matrizCompleta = matrizSensor1
            
            #self.conn1.commit()
            #matrizCompleta = matrizDistribucion
            #Primera interpolacion vecino mas cercano
            for k in range(2):
                for i in range(self.filas):
                    for j in range(84):
                        if i > 0 and i < 42 and j > 0 and j < 84:     
                            matrizCompleta[i][j] = (matrizCompleta[i+1][j] + matrizCompleta[i-1][j] + matrizCompleta[i][j-1] + matrizCompleta[i][j+1] + matrizCompleta[i+1][j+1] + matrizCompleta[i-1][j+1] + matrizCompleta[i-1][j-1] + matrizCompleta[i+1][j-1])/8
                            if matrizCompleta[i][j] > 240:
                                matrizCompleta[i][j] = 240

            data = scipy.ndimage.zoom(matrizCompleta, 3)
          
            plt.set_cmap('jet')

            self.imagenSensor1.set_data(data)

            self.figSensor1.canvas.draw()
            quality_val = 20
            self.figSensor1.savefig('sensor1.jpeg')
            
        except:
            pass

if __name__ == "__main__":

    ui = Ui_MainWindow()
    ui.printit()

    

