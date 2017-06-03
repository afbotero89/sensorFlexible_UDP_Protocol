import numpy as np
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
import threading
import socket
import time
import random
import sqlite3
import ast
import scipy.ndimage
from PIL import Image

class Ui_MainWindow(object):
    def __init__(self):

        self.campoPromediosCreado = False

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

        self.connPromedios = sqlite3.connect('estadisticasPromedios.db')
        self.cPromedios = self.connPromedios.cursor()
        #self.c.execute("DELETE FROM `sensorSuperior` WHERE 1")
        # Crea tabla para los tiempos de exposicion
        self.cPromedios.execute('''CREATE TABLE IF NOT EXISTS promediosPresionZonas (zoneID text, pressureAverageValue real)''')
        # Insert a row of data
        for row in self.cPromedios.execute("SELECT * FROM promediosPresionZonas WHERE '1'"):
            print(row[0])
            if row[0] == '6':
                self.campoPromediosCreado = True

        if self.campoPromediosCreado == False:
            self.campoPromediosCreado = True
            self.cPromedios.execute("INSERT INTO promediosPresionZonas VALUES ('1','initValue times 1')")
            self.cPromedios.execute("INSERT INTO promediosPresionZonas VALUES ('2','initValue times 2')")
            self.cPromedios.execute("INSERT INTO promediosPresionZonas VALUES ('3','initValue times 3')")
            self.cPromedios.execute("INSERT INTO promediosPresionZonas VALUES ('4','initValue times 4')")
            self.cPromedios.execute("INSERT INTO promediosPresionZonas VALUES ('5','initValue times 5')")
            self.cPromedios.execute("INSERT INTO promediosPresionZonas VALUES ('6','initValue times 6')")
        self.connPromedios.commit()
        
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
        averageColumn_Zona1 = (averageColumn_Zona1/602)*(80.0/maximoPromedio)  + 505
        averageColumn_Zona2 = (averageColumn_Zona2/602)*(80.0/maximoPromedio)  + 400
        averageColumn_Zona3 = (averageColumn_Zona3/602)*(80.0/maximoPromedio)  + 300
        averageColumn_Zona4 = (averageColumn_Zona4/602)*(80.0/maximoPromedio)  + 180
        averageColumn_Zona5 = (averageColumn_Zona5/602)*(80.0/maximoPromedio)  + 70
        averageColumn_Zona6 = (averageColumn_Zona6/602)*(80.0/maximoPromedio)

        #print("datos:", averageColumn_Zona1, averageColumn_Zona2, averageColumn_Zona3, averageColumn_Zona4, averageColumn_Zona5, averageColumn_Zona6)

        self.x.append(len(self.x)/2)

        self.p1_1.append(averageColumn_Zona1)

        self.p2_1.append(averageColumn_Zona2)

        self.p3_1.append(averageColumn_Zona3)

        self.p4_1.append(averageColumn_Zona4)

        self.p5_1.append(averageColumn_Zona5)

        self.p6_1.append(averageColumn_Zona6)

        zona1STR = str(self.p1_1)
        zona1STR = zona1STR[1:len(zona1STR)-1]
        self.cPromedios.execute("UPDATE `promediosPresionZonas` SET `pressureAverageValue`= '%s' WHERE `zoneID`=1" % zona1STR)
        self.connPromedios.commit()

        zona2STR = str(self.p2_1)
        zona2STR = zona2STR[1:len(zona2STR)-1]
        self.cPromedios.execute("UPDATE `promediosPresionZonas` SET `pressureAverageValue`= '%s' WHERE `zoneID`=2" % zona2STR)
        self.connPromedios.commit()

        zona3STR = str(self.p3_1)
        zona3STR = zona3STR[1:len(zona3STR)-1]        
        self.cPromedios.execute("UPDATE `promediosPresionZonas` SET `pressureAverageValue`= '%s' WHERE `zoneID`=3" % zona3STR)
        self.connPromedios.commit()

        zona4STR = str(self.p4_1)
        zona4STR = zona4STR[1:len(zona4STR)-1]          
        self.cPromedios.execute("UPDATE `promediosPresionZonas` SET `pressureAverageValue`= '%s' WHERE `zoneID`=4" % zona4STR)
        self.connPromedios.commit()

        zona5STR = str(self.p5_1)
        zona5STR = zona5STR[1:len(zona5STR)-1]         
        self.cPromedios.execute("UPDATE `promediosPresionZonas` SET `pressureAverageValue`= '%s' WHERE `zoneID`=5" % zona5STR)
        self.connPromedios.commit()

        zona6STR = str(self.p6_1)
        zona6STR = zona6STR[1:len(zona6STR)-1] 
        self.cPromedios.execute("UPDATE `promediosPresionZonas` SET `pressureAverageValue`= '%s' WHERE `zoneID`=6" % zona6STR)
        self.connPromedios.commit()

        self.refreshPatientHistory()
        if(len(self.x)==60):
            self.variablesReset()


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
