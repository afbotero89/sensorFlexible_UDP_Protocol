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
import binascii
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process
import threading
import scipy.ndimage
import sys, struct
from pylab import *
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
        self.columnas = 94;
        self.filas = 44;
         
        matrizCompleta = [[0 for x in range(self.columnas)] for x in range(self.filas)] 

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

        self.iniciaTramaDeDatos = False

        plt.set_cmap('jet')

        self.sqlDataBase()

        # Sensor 1: cabeza
        self.UDP_IP_Sensor1 = "192.168.0.124"
        self.UDP_PORT_Sensor1 = 10000

        self.UDP_IP_CLIENT_Sensor1 = "192.168.0.101"
        self.UDP_PORT_CLIENT_Sensor1 = 2233

        self.idSensor_Sensor1 = "1"
        
        # Comunicacion sensor 1
        self.t = threading.Thread(target = recvSensor1.Ui_MainWindow, args=(self.UDP_IP_Sensor1, self.UDP_PORT_Sensor1, self.UDP_IP_CLIENT_Sensor1, self.UDP_PORT_CLIENT_Sensor1, self.idSensor_Sensor1,))
        self.t.IsBackground = True;
        self.t.start()

        # Interfaz tiempos de exposicion zona superior
        self.u = threading.Thread(target = interfazTiemposExposicionSensor1.interfazTiemposExposicion, args=("1",))
        self.u.IsBackground = True;
        self.u.start()

        # Interfaz tiempos de exposicion zona inferior
        self.u = threading.Thread(target = interfazTiemposExposicionSensor1.interfazTiemposExposicion, args=("2",))
        self.u.IsBackground = True;
        self.u.start()

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
        #try:
        maximoValor = 0
        for row in self.c.execute("SELECT * FROM sensorFlexible WHERE `id`='1'"):
            dataSensor1 = row[1]
        for row in self.c.execute("SELECT * FROM sensorFlexible WHERE `id`='2'"):
            dataSensor2 = row[1]
        
        #Parte superior
        matrizSensor1 = ast.literal_eval(str(dataSensor1))

        #Parte inferior
        matrizSensor2 = ast.literal_eval(str(dataSensor2))

        matrizSensor1 = scipy.ndimage.rotate(matrizSensor1, 90)

        matrizSensor2 = scipy.ndimage.rotate(matrizSensor2, 90)


        hora = time.strftime("%H:%M:%S")

        #self.c1.execute("INSERT INTO sensorFlexibleTransmision VALUES ('%s',  '%s', '%s', '%s')" % (self.contadorImagenes, matrizSensor1, matrizSensor2 ,hora))

        #matrizSensor1 = scipy.ndimage.rotate(dataSensor1, 90)

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
            
        #except:
            #pass

if __name__ == "__main__":

    ui = Ui_MainWindow()
    ui.printit()

    

