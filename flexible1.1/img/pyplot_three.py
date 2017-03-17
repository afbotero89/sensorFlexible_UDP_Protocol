import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
import threading
import socket
import time
from matplotlib.figure import Figure
import random

plt.ion()

class RealTimePlots(object):
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12,4))
        self.fig.set_size_inches(12,4)

        ax = plt.Axes(self.fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        self.fig.add_axes(ax)
        
        self.ax.set_xticklabels([])
        self.labels = []

        self.variablesReset()
        
        while True:
            self.insertPoint()
            time.sleep(0.5)
        
    def variablesReset(self):
        
        self.contadorY = 0
        
        self.x = []

        # Zona de presion 1
        self.p1_1 = []
        self.p1_2 = []

        # Zona de presion 2
        self.p2_1 = []
        self.p2_2 = []

        # Zona de presion 3
        self.p3_1 = []
        self.p3_2 = []

        # Zona de presion 4
        self.p4_1 = []
        self.p4_2 = []
        
        # Zona de presion 5
        self.p5_1 = []
        self.p5_2 = []

        # Zona de presion 6
        self.p6_1 = []
        self.p6_2 = []

        # Zona de presion 7
        self.p7_1 = []
        self.p7_2 = []

        # Zona de presion 8
        self.p8_1 = []
        self.p8_2 = []

        # Zona de presion 9
        self.p9_1 = []
        self.p9_2 = []

        self.ax.set_xticklabels([])
        self.labels = []
       
    def insertPoint(self):
        self.x.append(len(self.x))
        self.p1_1.append(random.randint(10, 11))
        self.p1_2.append(random.randint(11, 12) + 1)

        self.p2_1.append(random.randint(10, 11) + 10)
        self.p2_2.append(random.randint(11, 12) + 11)

        self.p3_1.append(random.randint(10, 11) + 20)
        self.p3_2.append(random.randint(11, 12) + 21)

        self.p4_1.append(random.randint(10, 11) + 30)
        self.p4_2.append(random.randint(11, 12) + 31)

        self.p5_1.append(random.randint(10, 11) + 40)
        self.p5_2.append(random.randint(11, 12) + 41)

        self.realTimeGraphs()
           
    def realTimeGraphs(self):
        hourData = time.strftime("%H:%M")
        print(hourData)
        self.contadorY = self.contadorY + 1

        img = Image.open('historial3.png')
        img.putalpha(40)
        img.save('historial_main.png')

        plt.cla()
        plt.grid(True)
        plt.ylim([0,60])
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
        plt.plot(self.x, self.p1_1, 'g-',
                 self.x, self.p1_2, 'b-',
                 self.x, self.p2_1, 'g-',
                 self.x, self.p2_2, 'b-',
                 self.x, self.p3_1, 'g-',
                 self.x, self.p3_2, 'b-',
                 self.x, self.p4_1, 'g-',
                 self.x, self.p4_2, 'b-',
                 self.x, self.p5_1, 'g-',
                 self.x, self.p5_2, 'b-',marker='o', markersize=3, linewidth=1)
        plt.savefig('GraficoPresion.jpg',facecolor='#222222', edgecolor='none')
        plt.pause(0.01)
        if(len(self.x)==30):
            self.variablesReset()
    def refreshPatientHistory(self):
        img = Image.open('historial.png')
        img.save('foreground100.png')

        #plt.show()
        
plotsInstance = RealTimePlots()
