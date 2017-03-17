import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
import threading
import socket
import time
from matplotlib.figure import Figure
import random
import sqlite3
import ast
import scipy.ndimage

plt.ion()

class Ui_MainWindow(object):
    def __init__(self):
        self.listaX = []
        self.listaY = []
        self.vectorPromedio = []
        
        self.contadorX = 0
        self.contadorY = 0
        
        self.fig, self.ax = plt.subplots(figsize=(16,2))
        self.fig.set_size_inches(16,2)
        ax = plt.Axes(self.fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        self.fig.add_axes(ax)

        self.ax.set_xticklabels([])
        self.labels = [0]
        self.sqlDataBase()

        while True:
            averageVector = self.AveragePerRow()
            self.insertPoint(averageVector)
            time.sleep(0.2)
        
    def sqlDataBase(self):
        
        self.conn = sqlite3.connect('distribucionPresionSensorFlexible.db')
        self.c = self.conn.cursor()


    def AveragePerRow(self):

        for row in self.c.execute("SELECT * FROM sensorFlexible WHERE `id`='1'"):
            dataSensor1 = row[1]
        for row in self.c.execute("SELECT * FROM sensorFlexible WHERE `id`='2'"):
            dataSensor2 = row[1]
        
        #Sensor 1
        matrizSensor1 = ast.literal_eval(str(dataSensor1))

        #Sensor 1
        matrizSensor2 = ast.literal_eval(str(dataSensor2))
        matrizRotadaSensor2 = scipy.ndimage.rotate(matrizSensor2, -90)
        matrizConcatenada = np.concatenate((matrizSensor1,matrizRotadaSensor2), axis=1)

        averageColumn = 0
        for i in range(86):
            vectorColumna = matrizConcatenada[:,[i]]
            for j in range(43):
                averageColumn = averageColumn + vectorColumna[j]
            averageColumn = averageColumn/43
            self.vectorPromedio.append(averageColumn[0])          
        return self.vectorPromedio

    def insertPoint(self, vector):

        for i in range(86):
            self.listaX.append(i*2)
            self.listaY.append(random.randint(100, 150))

        y = np.random.random()
        plt.cla()
        plt.grid(True)
        plt.plot(self.listaX, vector,marker='o', linestyle='-', color='b', label = "Temperatura 1", markersize=3)
        
        # major ticks every 20, minor ticks every 5                                      
        major_ticks_x = np.arange(0, 194, 20)                                              
        minor_ticks_x = np.arange(0, 194, 5)

        # major ticks every 20, minor ticks every 5                                      
        major_ticks_y = np.arange(0, 255, 30)                                              
        minor_ticks_y = np.arange(0, 255, 10) 

        self.ax.set_xticks(major_ticks_x)                                                       
        self.ax.set_xticks(minor_ticks_x, minor=True)                                           
        self.ax.set_yticks(major_ticks_y)                                                       
        self.ax.set_yticks(minor_ticks_y, minor=True)


        for tick in self.ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(8)  

        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        # and a corresponding grid                                                       

        self.ax.grid(which='both')                                                            

        # or if you want differnet settings for the grids:                               
        self.ax.grid(which='minor', alpha=0.2)                                                
        self.ax.grid(which='major', alpha=0.5)  

        plt.ylabel('Presion promedio')
        plt.xlabel('Fila sensor')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.title.set_color('white')

        plt.ylim([0,150])
        plt.xlim([0,172])

        background_color = '#cdc9c9'
        plt.fill_between(self.listaX, 0, y2=vector, color = background_color)
 #       plt.fill_between(np.array(self.listaX), 0, np.array(self.listaY), where=np.array(self.listaY) >= 0, facecolor='blue', interpolate=True)
#        plt.fill_between(np.array(self.listaX), 0, np.array(self.listaY), where=np.array(self.listaY) <= 0, facecolor='red', interpolate=True)
 #       ax.fill_between(x, y1, y2, where=y2 <= y1, facecolor='red', interpolate=True)

 #       plt.fill_between(np.array(self.listaX), 0, 200, where=np.array(self.listaY) > 0.9, facecolor='green', alpha=0.5)
 #       plt.fill_between(np.array(self.listaY), 0, 200, where=np.array(self.listaY) < -0.9, facecolor='red', alpha=0.5)

        plt.savefig('../appSensorFlexibleWebLocalMatplotlib/img/GraficoPresion.png',facecolor='#222222', edgecolor='none')
        plt.pause(0.5)

        self.listaX = []
        self.listaY = []
        self.vectorPromedio = []
interfaz = Ui_MainWindow()


