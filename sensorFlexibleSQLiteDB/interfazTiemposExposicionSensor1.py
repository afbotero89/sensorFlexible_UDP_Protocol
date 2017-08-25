# forma de ejecutar interfaz tiempos de exposicion
from PIL import Image, ImageDraw
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt1
import numpy as np
import os
import tiemposDeExposicion
from pylab import *
import sys, struct
import sqlite3
import ast
import scipy.ndimage
import time
ion()


maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1
#print("maximo nivel de recurso")
#print(maxint)
#sys.setrecursionlimit(maxint)

class interfazTiemposExposicion:

    def __init__(self, idSensor):
        self.tiempo = [['00:00:00','00:00:00','00:00:00'],['00:00:00','00:00:00','00:00:00'],['00:00:00','00:00:00','00:00:00']]
        self.zona = 0

        self.cronometro = tiemposDeExposicion.Cronometro()
        

##        self.cronometro = tiemposDeExposicion.Cronometro()
##        self.fig2 = plt1.figure(figsize = (4,4))
##        self.fig2.canvas.set_window_title('Tiempos sensor 2')
##        self.fig2.canvas.draw()
##        #self.fig2.canvas.toolbar.pack_forget()
##        self.tablaSensor2 = plt1.table(cellText=self.tiempo , colWidths = [0.2]*3, cellLoc = 'center', rowLoc = 'center', bbox=[0,0,1,1])
##        
        #######  Sensor 1 #########
        self.zonasActivas = [[False,False,False],[False,False,False],[False,False,False]]
        self.zonaActivada = [[False,False,False],[False,False,False],[False,False,False]]
        self.pressureRegion = False

        #######  Sensor 2 #########
        self.zonasActivasSensor2 = [[False,False,False],[False,False,False],[False,False,False]]
        self.zonaActivadaSensor2 = [[False,False,False],[False,False,False],[False,False,False]]
        self.pressureRegionSensor2 = False

        self.campoTiemposExposicionCreado = False

        self.idSensor = idSensor    
        #plt1.show(block=False)
        print('inicia tiempos')
        self.sqlDataBase()
        self.evento()

    def sqlDataBase(self):
        self.conn = sqlite3.connect('distribucionPresionSensorFlexible.db')
        self.c = self.conn.cursor()

        self.connTiempos = sqlite3.connect('estadisticas.db')
        self.cTiempos = self.connTiempos.cursor()
        #self.c.execute("DELETE FROM `sensorSuperior` WHERE 1")
        # Crea tabla para los tiempos de exposicion
        self.cTiempos.execute('''CREATE TABLE IF NOT EXISTS tiemposExposicion (id text, exposureTimes real)''')
        # Insert a row of data
        for row in self.cTiempos.execute("SELECT * FROM tiemposExposicion WHERE '%s'" % self.idSensor):
            if row[0] == self.idSensor:
                self.campoTiemposExposicionCreado = True

        if self.campoTiemposExposicionCreado == False:
            self.campoTiemposExposicionCreado = True
            self.cTiempos.execute("INSERT INTO tiemposExposicion VALUES ('%s','initValue times 1')" % self.idSensor)
        self.connTiempos.commit()

    def evento(self):
        while True:
            try:
                for row in self.c.execute("SELECT * FROM sensorFlexible WHERE `id`='%s'" % self.idSensor):
                    dataSensor1 = row[1]

                #Sensor 1
                matrizSensor1 = ast.literal_eval(str(dataSensor1))

                #matrizSensor1 = scipy.ndimage.rotate(matrizSensor1, 90)

                matrizDistribucionPresion = matrizSensor1

                self.tiempo = self.cronometro.calculaTiempo()
                for i in range(3):
                    for j in range(3):
                        if self.zonasActivas[i][j] == True and self.zonaActivada[i][j] == False:
                            self.zonaActivada[i][j] = True
                            self.cronometro.activaZonaDePresion(i,j)
                        if self.zonasActivas[i][j] == False and self.zonaActivada[i][j] == True:
                            self.zonaActivada[i][j] = False
                            self.cronometro.desactivaZonaDePresion(i,j)
                            
                #self.zonasActivas = zonasActivas
                self.determineAreasOfGreaterPressure(matrizDistribucionPresion)
                tiemposString = str(self.tiempo[0][0]) + "," + str(self.tiempo[0][1]) + "," + str(self.tiempo[0][2]) + "," + str(self.tiempo[1][0]) + "," + str(self.tiempo[1][1]) + "," + str(self.tiempo[1][2]) + "," + str(self.tiempo[2][0]) + "," + str(self.tiempo[2][1]) + "," + str(self.tiempo[2][2])
                self.cTiempos.execute("UPDATE `tiemposExposicion` SET `exposureTimes`= '%s' WHERE `id`='%s'" % (tiemposString, self.idSensor))
                self.connTiempos.commit()
                time.sleep(0.5)
            except:
                pass


    def matrixTransformations(self, matrix):
        transformationMatrix = np.array([['00:00:00','00:00:00','00:00:00'],['00:00:00','00:00:00','00:00:00'],['00:00:00','00:00:00','00:00:00']])
           
        return transformationMatrix     
        

    def determineAreasOfGreaterPressure(self, matrizDistribucion):
        self.zona = self.zona + 1
        porcentajeSuperadoAlarma = 5
        maximaSumatoria = 43*43*75
        
        ######## Zone 1 ##############
        if self.zona == 1:
            pressureSumatoriaZone1 = 0
            for i in range(14):
                for j in range(14):
                    pressureSumatoriaZone1 = pressureSumatoriaZone1 +  matrizDistribucion[i][j]
            percentagePressureZone1 = (pressureSumatoriaZone1*1000)/maximaSumatoria
            
            if percentagePressureZone1 > porcentajeSuperadoAlarma:

                self.zonasActivas[2][0] = True
                
            else:
                self.zonasActivas[2][0] = False

        ############# Zone 2 ##############
        elif self.zona == 2:
            pressureSumatoriaZone2 = 0
            
            for i in range(14,28):
                for j in range(14):
                    pressureSumatoriaZone2 = pressureSumatoriaZone2 +  matrizDistribucion[i][j]
            percentagePressureZone2 = (pressureSumatoriaZone2*1000)/maximaSumatoria
            if percentagePressureZone2 > porcentajeSuperadoAlarma:
                self.zonasActivas[2][1] = True

            else:
                self.zonasActivas[2][1] = False

        
        #########  Zone 3 ###############
        elif self.zona == 3:
            pressureSumatoriaZone3 = 0
            for i in range(28,43):
                for j in range(14):
                    pressureSumatoriaZone3 = pressureSumatoriaZone3 +  matrizDistribucion[i][j]
            percentagePressureZone3 = (pressureSumatoriaZone3*1000)/maximaSumatoria
            if percentagePressureZone3 > porcentajeSuperadoAlarma:
                self.zonasActivas[2][2] = True
            else:
                self.zonasActivas[2][2] = False
                       
        #########  Zone 4 ##############
        elif self.zona == 4:
            pressureSumatoriaZone4 = 0
            for i in range(14):
                for j in range(14,28):
                    pressureSumatoriaZone4 = pressureSumatoriaZone4 +  matrizDistribucion[i][j]
            percentagePressureZone4 = (pressureSumatoriaZone4*1000)/maximaSumatoria
            if percentagePressureZone4 > porcentajeSuperadoAlarma:
                self.zonasActivas[1][0] = True
            else:
                self.zonasActivas[1][0] = False
              
        ######### Zone 5 #############
        elif self.zona == 5:
            pressureSumatoriaZone5 = 0
            for i in range(14,28):
                for j in range(14,28):
                    pressureSumatoriaZone5 = pressureSumatoriaZone5 +  matrizDistribucion[i][j]
            percentagePressureZone5 = (pressureSumatoriaZone5*1000)/maximaSumatoria
            
            if percentagePressureZone5 > porcentajeSuperadoAlarma:
                self.zonasActivas[1][1] = True
            else:
                self.zonasActivas[1][1] = False
                   
        ######### Zone 6 #############
        elif self.zona == 6:
            pressureSumatoriaZone6 = 0
            for i in range(28,43):
                for j in range(14,28):
                    pressureSumatoriaZone6 = pressureSumatoriaZone6 +  matrizDistribucion[i][j]
            percentagePressureZone6 = (pressureSumatoriaZone6*1000)/maximaSumatoria
            if percentagePressureZone6 > porcentajeSuperadoAlarma:
                self.zonasActivas[1][2] = True
                
            else:
                self.zonasActivas[1][2] = False
           
        ######### Zone 7 ############
        elif self.zona == 7:
            pressureSumatoriaZone7 = 0
            for i in range(14):
                for j in range(28,43):
                    pressureSumatoriaZone7 = pressureSumatoriaZone7 +  matrizDistribucion[i][j]
            percentagePressureZone7 = (pressureSumatoriaZone7*1000)/maximaSumatoria
            if percentagePressureZone7 > porcentajeSuperadoAlarma:
                self.zonasActivas[0][0] = True
            else:
                self.zonasActivas[0][0] = False
          
        ######## Zone 8 #############
        elif self.zona == 8:
            pressureSumatoriaZone8 = 0
            for i in range(14,28):
                for j in range(28,43):
                    pressureSumatoriaZone8 = pressureSumatoriaZone8 +  matrizDistribucion[i][j]
            percentagePressureZone8 = (pressureSumatoriaZone8*1000)/maximaSumatoria

            if percentagePressureZone8 > porcentajeSuperadoAlarma:
                self.zonasActivas[0][1] = True
            else:
                self.zonasActivas[0][1] = False
 
        ######### Zone 9 ############
        elif self.zona == 9:
            pressureSumatoriaZone9 = 0
            for i in range(28,43):
                for j in range(28,43):
                    pressureSumatoriaZone9 = pressureSumatoriaZone9 +  matrizDistribucion[i][j]
            percentagePressureZone9 = (pressureSumatoriaZone9*1000)/maximaSumatoria
            if percentagePressureZone9 > porcentajeSuperadoAlarma:
                self.zonasActivas[0][2] = True
            else:
                self.zonasActivas[0][2] = False
            self.zona = 0
            
        return self.zonasActivas


