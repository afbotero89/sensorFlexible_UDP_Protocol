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
ion()



maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1
#print("maximo nivel de recurso")
#print(maxint)
#sys.setrecursionlimit(maxint)

class interfazTiemposExposicion:

    def __init__(self):
        self.tiempo = [['00:00:00','00:00:00','00:00:00'],['00:00:00','00:00:00','00:00:00'],['00:00:00','00:00:00','00:00:00']]
        self.zona = 0
        #plt1.gca().invert_yaxis()
        axis = plt.gca()
        axis.get_xaxis().set_visible(False)
        axis.get_yaxis().set_visible(False)

        self.cronometro = tiemposDeExposicion.Cronometro()
        self.fig1 = plt1.figure(figsize=(8,8))
        self.fig1.canvas.set_window_title('Tiempos sensor 1')
        self.fig1.set_size_inches(8,8)
        ax = plt.Axes(self.fig1, [0., 0., 1., 1.])
        ax.set_axis_off()
        self.fig1.add_axes(ax)

        self.fig1.canvas.draw()
        #self.fig1.canvas.toolbar.pack_forget()
        self.tablaSensor1 = plt1.table(cellText=self.tiempo , colWidths = [0.2]*3, cellLoc = 'center', rowLoc = 'center', bbox=[0,0,1,1])

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
        
        #plt1.show(block=False)
        print('inicia tiempos')
        self.sqlDataBase()
        self.evento()

    def sqlDataBase(self):
        self.conn = sqlite3.connect('distribucionPresionSensorFlexible.db')
        self.c = self.conn.cursor()

    def evento(self):
        while True:
            for row in self.c.execute("SELECT * FROM sensorFlexible WHERE `id`='1'"):
                dataSensor1 = row[1]


            #Sensor 1
            matrizSensor1 = ast.literal_eval(str(dataSensor1))

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
            self.dibujaMatriz()
        #print(self.tiempo[0][0],self.tiempo[0][1],self.tiempo[0][2],self.tiempo[1][0],self.tiempo[1][1],self.tiempo[2][0],self.tiempo[2][1],self.tiempo[2][2])

    def dibujaMatriz(self):
        global pressureRegion
        #figure(2)
 #       the_table = plt1.table(cellText=tiempo , colWidths = [0.2]*3, cellLoc = 'center', rowLoc = 'center', bbox=[0,0,1,1])
        #self.tablaSensor1.cell.set_text_props(tiempo)
        axis = plt1.gca()
        axis.get_xaxis().set_visible(False)
        axis.get_yaxis().set_visible(False)
        
        for j in range(0,3):
            for i in range(0,3):
                
                self.tablaSensor1.get_celld()[i,j].set_fontsize(40)

                # Se hace espejo con respecto a la diagonal principal
                
                if i == j:
                    cell = self.tablaSensor1.get_celld()[i,j]
                else:
                    cell = self.tablaSensor1.get_celld()[j,i]
                #invertedMatrix = self.matrixTransformations(self.tiempo)


                #activeZones = self.matrixTransformationsActiveZones(self.zonasActivas)

                cell.set_text_props(text = '0' + str(self.tiempo[i][j]))
                
                try:
                    tiempo = self.tiempo[i][j]
                    if int(tiempo.total_seconds()) > 0 and int(tiempo.total_seconds()) < 10 :
                        cell._text.set_color('black')

                    if int(tiempo.total_seconds()) > 100:
                        
                        if self.zonasActivas[i][j] == True:
                            #cell.set_color('r')
                            pass
                            #cell._text.set_color('white')
                            #if self.pressureRegion == False:
                             #   cell.set_color('r')
                            #else:
                             #   cell.set_color('w')
                        #else:
                         #   cell.set_color('w')
                except:
                    pass
                if self.zonasActivas[i][j] == False:
                    cell.set_color('w')
                    cell._text.set_color('white')
                cell.set_edgecolor('k')

        
        self.fig1.savefig('../appSensorFlexibleWebLocalMatplotlib/img/tablaTiemposExposicionSensor1.png')
        #figure(2).tight_layout()                
        #figure(2).canvas.draw()
        #plt1.cla()
        #plt1.clf()
        
        #if self.pressureRegion == False:
         #   self.pressureRegion = True
        #else:
         #   self.pressureRegion = False            

    # Funcion para hacer espejo sobre la diagonal principal

    def matrixTransformations(self, matrix):
        transformationMatrix = np.array([['00:00:00','00:00:00','00:00:00'],['00:00:00','00:00:00','00:00:00'],['00:00:00','00:00:00','00:00:00']])
        for i in range(3):
            for j in range(3):
                if i == j:
                    transformationMatrix[i][j] = matrix[i][j]
                else:
                    transformationMatrix[j][i] = matrix[i][j]
           
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

                self.zonasActivas[0][0] = True
                
            else:
                self.zonasActivas[0][0] = False

        ############# Zone 2 ##############
        elif self.zona == 2:
            pressureSumatoriaZone2 = 0
            
            for i in range(14,28):
                for j in range(14):
                    pressureSumatoriaZone2 = pressureSumatoriaZone2 +  matrizDistribucion[i][j]
            percentagePressureZone2 = (pressureSumatoriaZone2*1000)/maximaSumatoria
            if percentagePressureZone2 > porcentajeSuperadoAlarma:
                self.zonasActivas[0][1] = True

            else:
                self.zonasActivas[0][1] = False

        
        #########  Zone 3 ###############
        elif self.zona == 3:
            pressureSumatoriaZone3 = 0
            for i in range(28,43):
                for j in range(14):
                    pressureSumatoriaZone3 = pressureSumatoriaZone3 +  matrizDistribucion[i][j]
            percentagePressureZone3 = (pressureSumatoriaZone3*1000)/maximaSumatoria
            if percentagePressureZone3 > porcentajeSuperadoAlarma:
                self.zonasActivas[0][2] = True
            else:
                self.zonasActivas[0][2] = False
                       
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
                self.zonasActivas[2][0] = True
            else:
                self.zonasActivas[2][0] = False
          
        ######## Zone 8 #############
        elif self.zona == 8:
            pressureSumatoriaZone8 = 0
            for i in range(14,28):
                for j in range(28,43):
                    pressureSumatoriaZone8 = pressureSumatoriaZone8 +  matrizDistribucion[i][j]
            percentagePressureZone8 = (pressureSumatoriaZone8*1000)/maximaSumatoria

            if percentagePressureZone8 > porcentajeSuperadoAlarma:
                self.zonasActivas[2][1] = True
            else:
                self.zonasActivas[2][1] = False
 
        ######### Zone 9 ############
        elif self.zona == 9:
            pressureSumatoriaZone9 = 0
            for i in range(28,43):
                for j in range(28,43):
                    pressureSumatoriaZone9 = pressureSumatoriaZone9 +  matrizDistribucion[i][j]
            percentagePressureZone9 = (pressureSumatoriaZone9*1000)/maximaSumatoria
            if percentagePressureZone9 > porcentajeSuperadoAlarma:
                self.zonasActivas[2][2] = True
            else:
                self.zonasActivas[2][2] = False
            self.zona = 0
            
        return self.zonasActivas
interfazTiemposExposicion()

