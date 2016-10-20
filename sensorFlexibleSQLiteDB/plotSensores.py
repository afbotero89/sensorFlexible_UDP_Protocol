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
import tiemposDeExposicion
import interfazTiemposExposicionSensor1
from pylab import *
#import pusher
import time
import os
import sqlite3
import ast
ion()


maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1
print("maximo nivel de recurso")
print(maxint)
sys.setrecursionlimit(maxint)


class Ui_MainWindow(object):
    def __init__(self):
        print("init")
        #Socket connection
        self.ip = "192.168.0.124"
        self.port = 10005
        self.columnas = 43;
        self.filas = 43;
        
        matriz = [[0 for x in range(self.columnas)] for x in range(self.filas)] 
        #matriz[0][0] = 255
        matrizSensor2 = [[0 for x in range(self.columnas)] for x in range(self.filas)] 
        #matrizSensor2[0][0] = 255
        matrizCompleta = np.concatenate((matriz,matrizSensor2),axis=1)
        #matrizCompleta = matriz
        matrizCompleta[0][0] = 255

        #matrizCompleta[0][0] = 255
        self.initData = scipy.ndimage.zoom(matrizCompleta, 3)
        self.figSensor1 = plt.figure(figsize=(16,8),frameon=False)
        self.figSensor1.set_size_inches(16,8)
        ax = plt.Axes(self.figSensor1, [0., 0., 1., 1.])
        ax.set_axis_off()
        self.figSensor1.add_axes(ax)
        #self.figSensor1.set_size_inches(9,9)
        self.figSensor1.canvas.draw()
        #self.figSensor1.canvas.toolbar.pack_forget()
        #self.figSensor1.suptitle('Sensor 1', fontsize = 14, fontweight = 'light')
        self.figSensor1.canvas.set_window_title('Sensor 1')
        
        #axis = plt.gca()
        #axis.get_xaxis().set_visible(True)
        #axis.get_yaxis().set_visible(True)

        self.imagenSensor1 = plt.imshow(self.initData, interpolation = 'nearest')
        #self.figSensor1.tight_layout()
        
        self.vectorImagen = []
        self.vectorDatosDistribucionPresion = []
        self.vectorDesencriptado = []
        #self.vectorImagen = [255,0,45,2,0,184,3,0,107,3,0,117,2,0,112,5,0,18,7,0,7,6,0,1,12,14,2,0,3,4,0,1,2,0,9,2,0,7,9,9,47,45,26,7,0,24,10,11,15,3,0,25,7,7,14,0,62,14,0,19,3,7,6,0,7,5,0,17,10,47,54,32,0,24,5,11,49,51,0,26,5,2,0,40,255]
        self.cronometro = tiemposDeExposicion.Cronometro()
        self.interfazTiempos = interfazTiemposExposicionSensor1.interfazTiemposExposicion()
        self.iniciaTramaDeDatos = False

        plt.set_cmap('jet')

        self.sqlDataBase()
        #plt.gca().invert_yaxis()
    def sqlDataBase(self):
        self.conn = sqlite3.connect('distribucionPresionSensorFlexible.db')
        self.c = self.conn.cursor()


    def printit(self):
        global vectorImagen, iniciaTramaDeDatos, vectorDatosDistribucionPresion, s
        while True:
          self.dibujarDistribucionPresionSensor1()
          time.sleep(0.05)

        
    def dibujarDistribucionPresionSensor1(self):
        try:
            maximoValor = 0
            for row in self.c.execute("SELECT * FROM sensorFlexible WHERE `id`='1'"):
                dataSensor1 = row[1]
            for row in self.c.execute("SELECT * FROM sensorFlexible WHERE `id`='2'"):
                dataSensor2 = row[1]
            
            #      for i in range(self.filas):
            #         for j in range(self.columnas):
            #            if (matrizDistribucion[i][j] > maximoValor):
            #               maximoValor = matrizDistribucion[i][j]

            #Sensor 1
            matrizSensor1 = ast.literal_eval(str(dataSensor1))


            #Sensor 1
            matrizSensor2 = ast.literal_eval(str(dataSensor2))
            matrizSensor2 = scipy.ndimage.rotate(matrizSensor2, -90)

            matrizCompleta = np.concatenate((matrizSensor1,matrizSensor2), axis=1)
            #matrizCompleta = matrizDistribucion
            #Primera interpolacion vecino mas cercano
            for k in range(2):
                for i in range(self.filas):
                    for j in range(84):
                        if i > 0 and i < 42 and j > 0 and j < 84:     
                            matrizCompleta[i][j] = (matrizCompleta[i+1][j] + matrizCompleta[i-1][j] + matrizCompleta[i][j-1] + matrizCompleta[i][j+1] + matrizCompleta[i+1][j+1] + matrizCompleta[i-1][j+1] + matrizCompleta[i-1][j-1] + matrizCompleta[i+1][j-1])/8
                            if matrizCompleta[i][j] > 240:
                                matrizCompleta[i][j] = 240
            #Segunda interpolacion vecino mas cercano

            #      if i > 0 and i < 42 and j > 0 and j < 42:
                      
             #         matrizDistribucion[i][j] = (matrizDistribucion[i+1][j] + matrizDistribucion[i-1][j] + matrizDistribucion[i][j-1] + matrizDistribucion[i][j+1] + matrizDistribucion[i+1][j+1] + matrizDistribucion[i-1][j+1] + matrizDistribucion[i-1][j-1] + matrizDistribucion[i+1][j-1])/8
              #        if(i > 40 or j < 4):
               #         matrizDistribucion[i][j] = (matrizDistribucion[i+1][j] + matrizDistribucion[i-1][j] + matrizDistribucion[i][j-1] + matrizDistribucion[i][j+1] + matrizDistribucion[i+1][j+1] + matrizDistribucion[i-1][j+1] + matrizDistribucion[i-1][j-1] + matrizDistribucion[i+1][j-1])/8
                  

            # Correccion de frontera, vecino mas cercano, para i = 48    

            #for i in range(self.filas):
            # for j in range(self.columnas):
                # Correccion para i
                # Para i = 0
            #  if (i == 0) and (j != 0) and (j != self.columnas - 1):
                #matrizDistribucion[i][j] = (matrizDistribucion[i][j-1] + matrizDistribucion[i+1][j-1] + matrizDistribucion[i+1][j] + matrizDistribucion[i+1][j+1] + matrizDistribucion[i][j+1])/5
             #   matrizDistribucion[i][j] =  (matrizDistribucion[i+1][j] + matrizDistribucion[i+2][j] + matrizDistribucion[i+3][j] + matrizDistribucion[i][j])/3
                # Para i = 48  
              #if (i == self.filas - 1) and (j != 0) and (j != self.columnas - 1):
                #matrizDistribucion[i][j] = (matrizDistribucion[i][j-1] + matrizDistribucion[i-1][j-1] + matrizDistribucion[i-1][j] + matrizDistribucion[i-1][j+1] + matrizDistribucion[i][j+1])/5
               # matrizDistribucion[i][j] = (matrizDistribucion[i-1][j] + matrizDistribucion[i-2][j] + matrizDistribucion[i-3][j] + matrizDistribucion[i][j])/3
                # Correccion para j
                # Para j = 48
              #if j == (self.columnas - 1) and i != (self.filas - 1) and i != 0:
                #matrizDistribucion[i][j] = (matrizDistribucion[i-1][j] + matrizDistribucion[i-1][j-1] + matrizDistribucion[i][j-1] + matrizDistribucion[i+1][j-1] + matrizDistribucion[i+1][j])/5
               # matrizDistribucion[i][j] = (matrizDistribucion[i][j-1] + matrizDistribucion[i][j-2] + matrizDistribucion[i][j-3] + matrizDistribucion[i][j])/3
                # Para j = 0
              #if j == 0 and i != (self.filas - 1) and i != 0:
                #matrizDistribucion[i][j] = (matrizDistribucion[i-1][j] + matrizDistribucion[i-1][j+1] + matrizDistribucion[i][j+1] + matrizDistribucion[i+1][j+1] + matrizDistribucion[i+1][j])/5
               # matrizDistribucion[i][j] = (matrizDistribucion[i][j+1] + matrizDistribucion[i][j+2] + matrizDistribucion[i][j+3] + matrizDistribucion[i][j])/3


            #for i in range(self.filas):
              
            #   for j in range(self.columnas):
                
            #      if matrizDistribucion[i][j] < 0:
             #       matrizDistribucion[i][j] = 0

            #              if matrizDistribucion[i][j] > 0:
                      
            #                 matrizDistribucion[i][j] = matrizDistribucion[i][j]*4
            ##              if matrizDistribucion[i][j] < 100:
            ##                  
            ##                  matrizDistribucion[i][j] = matrizDistribucion[i][j]*2
            #              if matrizDistribucion[i][j] > 200:
                      
            #                 matrizDistribucion[i][j] = 230
            ##              if matrizDistribucion[i][j] >= maximoValor:
            ##                  maximoValor = matrizDistribucion[i][j]

            #rotate_img = scipy.ndimage.rotate(matrizDistribucion, 0)
            #rotate_img = scipy.ndimage.rotate(matrizDistribucion, -90)
            data = scipy.ndimage.zoom(matrizCompleta, 3)
    ##        except:
    ##          print("except")
    ##          data = scipy.ndimage.zoom(self.initData, 3)
            #for i in range(len(data)):
                #for j in range(len(data[1])):
                    #data[i][j]=data[i][j] + 18
            #plt.contour(data, linewidths=1)
            #plt.imshow(data, interpolation = 'bilinear')
          
            plt.set_cmap('jet')

            self.imagenSensor1.set_data(data)

            self.figSensor1.canvas.draw()
            quality_val = 20
            self.figSensor1.savefig('../appSensorFlexibleWebLocalMatplotlib/img/sensor1.jpg')
            sensorCompleto = Image.open("../appSensorFlexibleWebLocalMatplotlib/img/sensor1.jpg")

            width, height = sensorCompleto.size   # Get dimensions

            left = 0
            top = 0
            right = width/2
            bottom = height

            left1 = width/2
            top1 = 0
            right1 = width
            bottom1 = height

            crop = sensorCompleto.crop((left, top, right, bottom))
            crop.save("../appSensorFlexibleWebLocalMatplotlib/img/sensor1SinTiempos.jpeg","jpeg")

            crop1 = sensorCompleto.crop((left1, top1, right1, bottom1))
            crop1.save("../appSensorFlexibleWebLocalMatplotlib/img/sensor2SinTiempos.jpeg","jpeg")
            #sensorCompleto.save('/Applications/XAMPP/xamppfiles/htdocs/apps_rigido_flexible1/appSensorFlexibleWebLocalMatplotlib/img/sensor1.jpg')
        except:
            pass

      

if __name__ == "__main__":

    ui = Ui_MainWindow()
    ui.printit()

    

