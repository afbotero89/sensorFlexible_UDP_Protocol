import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
import threading
import socket
import time
from matplotlib.figure import Figure
import random
import sqlite3
import ast
import scipy.ndimage
from PIL import Image

plt.ion()

class Ui_MainWindow(object):
    def __init__(self):

        self.fig, self.ax = plt.subplots(figsize=(24,8))
        self.fig.set_size_inches(24,8)

        ax = plt.Axes(self.fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        self.fig.add_axes(ax)
        
        self.ax.set_xticklabels([])
        self.labels = []

        self.variablesReset()
        self.sqlDataBase()

        while True:
            try:
                self.AveragePerRow()
                time.sleep(0.2)
            except:
                pass

    def sqlDataBase(self):
        
        self.conn = sqlite3.connect('distribucionPresionSensorFlexible.db')
        self.c = self.conn.cursor()
        
    def variablesReset(self):

        self.contadorY = 0

        self.x = []

        # Zona de presion 1
        self.p1_1 = []

        # Zona de presion 2
        self.p2_1 = []

        # Zona de presion 3
        self.p3_1 = []

        # Zona de presion 4
        self.p4_1 = []

        # Zona de presion 5
        self.p5_1 = []

        # Zona de presion 6
        self.p6_1 = []

        # Zona de presion 7
        self.p7_1 = []

        # Zona de presion 8
        self.p8_1 = []

        # Zona de presion 9
        self.p9_1 = []

        self.ax.set_xticklabels([])
        self.labels = []    


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

        averageColumn_Zona1 = 0
        averageColumn_Zona2 = 0
        averageColumn_Zona3 = 0
        averageColumn_Zona4 = 0
        averageColumn_Zona5 = 0
        averageColumn_Zona6 = 0
        for i in range(43):
            for j in range(14):
                
                averageColumn_Zona1 = averageColumn_Zona1 + matrizConcatenada[i,j]

            for j in range(14,28):

                averageColumn_Zona2 = averageColumn_Zona2 + matrizConcatenada[i,j] 

            for j in range(28,42):

                averageColumn_Zona3 = averageColumn_Zona3 + matrizConcatenada[i,j]       

            for j in range(42,56):

                averageColumn_Zona4 = averageColumn_Zona4 + matrizConcatenada[i,j]
               
            for j in range(56,70):

                averageColumn_Zona5 = averageColumn_Zona5 + matrizConcatenada[i,j]

            for j in range(70,86):

                averageColumn_Zona6 = averageColumn_Zona6 + matrizConcatenada[i,j]
                
        # Saca promedios por zonas asumiendo que el maximo de ADC puede ser cercano a 150 
        maximoPromedio = 80              
        averageColumn_Zona1 = (averageColumn_Zona1/602)*(80.0/maximoPromedio)  + 500
        averageColumn_Zona2 = (averageColumn_Zona2/602)*(80.0/maximoPromedio)  + 400
        averageColumn_Zona3 = (averageColumn_Zona3/602)*(80.0/maximoPromedio)  + 300
        averageColumn_Zona4 = (averageColumn_Zona4/602)*(80.0/maximoPromedio)  + 200
        averageColumn_Zona5 = (averageColumn_Zona5/602)*(80.0/maximoPromedio)  + 100
        averageColumn_Zona6 = (averageColumn_Zona6/602)*(80.0/maximoPromedio)

        #print("datos:", averageColumn_Zona1, averageColumn_Zona2, averageColumn_Zona3, averageColumn_Zona4, averageColumn_Zona5, averageColumn_Zona6)

        self.x.append(len(self.x)/2)

        self.p1_1.append(averageColumn_Zona1)

        self.p2_1.append(averageColumn_Zona2)

        self.p3_1.append(averageColumn_Zona3)

        self.p4_1.append(averageColumn_Zona4)

        self.p5_1.append(averageColumn_Zona5)

        self.p6_1.append(averageColumn_Zona6)

        self.realTimeGraphs()


    def realTimeGraphs(self):
        hourData = time.strftime("%H:%M")
        #print(hourData)
        self.contadorY = self.contadorY + 1

        plt.cla()
        plt.grid(True)
        plt.ylim([0,600])
        plt.xlim([0,30])

        # major ticks every 20, minor ticks every 5                                      
        major_ticks_x = np.arange(0, 30, 1)                                              
        minor_ticks_x = np.arange(0, 30, 0.1)

        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')
        
        self.ax.set_xticks(major_ticks_x)                                                       
        self.ax.set_xticks(minor_ticks_x, minor=True)  

        for tick in self.ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(8)  
        # red dashes, blue squares and green triangles
        
        self.labels.append(hourData)
        self.labels[self.contadorY - 1] = hourData
        self.ax.set_xticklabels(self.labels, rotation=70)
        plt.plot(self.x, self.p1_1, 'b-',
                 self.x, self.p2_1, 'k-',
                 self.x, self.p3_1, 'b-',
                 self.x, self.p4_1, 'k-',
                 self.x, self.p5_1, 'b-',
                 self.x, self.p6_1, 'k-', marker='o', markersize=3, linewidth=0.8)
        self.fig.canvas.draw()
        plt.savefig('GraficoPresion1.png',facecolor='#222222', edgecolor='none')
        time.sleep(0.2)
        print("graficos presion")
        if(len(self.x)==60):
            self.variablesReset()
            
        self.refreshPatientHistory()
    def refreshPatientHistory(self):
        
        if len(self.x)<5:
            img = Image.open('/Applications/XAMPP/xamppfiles/htdocs/flexible1.1/img/historial1.png')
        elif len(self.x)>=5 and len(self.x)<10:
            img = Image.open('/Applications/XAMPP/xamppfiles/htdocs/flexible1.1/img/historial1.1.png')
        elif len(self.x)>=10 and len(self.x)<15:
            img = Image.open('/Applications/XAMPP/xamppfiles/htdocs/flexible1.1/img/historial2.png')
        elif len(self.x)>=15 and len(self.x)<20:
            img = Image.open('/Applications/XAMPP/xamppfiles/htdocs/flexible1.1/img/historial2.1.png')
        elif len(self.x)>=20 and len(self.x)<25:
            img = Image.open('/Applications/XAMPP/xamppfiles/htdocs/flexible1.1/img/historial3.png')
        elif len(self.x)>=25 and len(self.x)<30:
            img = Image.open('/Applications/XAMPP/xamppfiles/htdocs/flexible1.1/img/historial3.1.png')
        elif len(self.x)>=30 and len(self.x)<35:
            img = Image.open('/Applications/XAMPP/xamppfiles/htdocs/flexible1.1/img/historial4.png')
        elif len(self.x)>=35 and len(self.x)<40:
            img = Image.open('/Applications/XAMPP/xamppfiles/htdocs/flexible1.1/img/historial4.1.png')
        elif len(self.x)>=40 and len(self.x)<45:
            img = Image.open('/Applications/XAMPP/xamppfiles/htdocs/flexible1.1/img/historial5.png')
        elif len(self.x)>=45 and len(self.x)<50:
            img = Image.open('/Applications/XAMPP/xamppfiles/htdocs/flexible1.1/img/historial5.1.png')
        elif len(self.x)>=50 and len(self.x)<55:
            img = Image.open('/Applications/XAMPP/xamppfiles/htdocs/flexible1.1/img/historial6.png')
        elif len(self.x)>=55 and len(self.x)<59:
            img = Image.open('/Applications/XAMPP/xamppfiles/htdocs/flexible1.1/img/historial6.1.png')
        elif len(self.x)>=59:
            img = Image.open('/Applications/XAMPP/xamppfiles/htdocs/flexible1.1/img/historial7.png')
           
        img.save('/Applications/XAMPP/xamppfiles/htdocs/flexible1.1/img/historial_main.png')
        #plt.show()
        
plotsInstance = Ui_MainWindow()
