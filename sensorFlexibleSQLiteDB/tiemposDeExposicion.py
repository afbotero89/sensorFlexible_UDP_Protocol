#Tiempos de exposicion

from datetime import datetime

class Cronometro:
    def __init__(self):
        print("inicia el timer")
        # Variables sensor 1
        self.FMT = '%H:%M:%S'
        self.matrizZonasActivadas = [[False,False,False],[False,False,False],[False,False,False]]
        self.matrizHorasDeActivacion = [['0:00:00','0:00:00','0:00:00'],['0:00:00','0:00:00','0:00:00'],['0:00:00','0:00:00','0:00:00']]
        self.matrizTiempoTranscurrido = [['0:00:00','0:00:00','0:00:00'],['0:00:00','0:00:00','0:00:00'],['0:00:00','0:00:00','0:00:00']]

        # Variables sensor 2

        self.matrizZonasActivadasSensor2 = [[False,False,False],[False,False,False],[False,False,False]]
        self.matrizHorasDeActivacionSensor2 = [['0:00:00','0:00:00','0:00:00'],['0:00:00','0:00:00','0:00:00'],['0:00:00','0:00:00','0:00:00']]
        self.matrizTiempoTranscurridoSensor2 = [['0:00:00','0:00:00','0:00:00'],['0:00:00','0:00:00','0:00:00'],['0:00:00','0:00:00','0:00:00']]

        self.matrizZonasFilas = 3
        self.matrizZonasColumnas = 3
    
################ Sensor 1 ###########################

    def activaZonaDePresion(self,x,y):
        now = datetime.now()
        self.matrizZonasActivadas[x][y] = True
        self.matrizHorasDeActivacion[x][y] = str(now.hour) + ":" + str(now.minute) +":"+ str(now.second) 

    def desactivaZonaDePresion(self,x,y):
        self.matrizZonasActivadas[x][y] = False
        self.matrizHorasDeActivacion[x][y] = '0:00:00'
        self.matrizTiempoTranscurrido[x][y] = '0:00:00'
                
    def calculaTiempo(self):
        now = datetime.now()
        horaActual = str(now.hour) + ":" + str(now.minute) +":"+ str(now.second)
        for i in range(0,(self.matrizZonasFilas)):
            for j in range(0,(self.matrizZonasColumnas)):
                if self.matrizZonasActivadas[i][j] == True:
                    tdelta = datetime.strptime(horaActual, self.FMT) - datetime.strptime(self.matrizHorasDeActivacion[i][j], self.FMT)
                    self.matrizTiempoTranscurrido[i][j] = tdelta
        return self.matrizTiempoTranscurrido

################ Sensor 2 ###########################

    def activaZonaDePresionSensor2(self,x,y):
        now = datetime.now()
        self.matrizZonasActivadasSensor2[x][y] = True
        self.matrizHorasDeActivacionSensor2[x][y] = str(now.hour) + ":" + str(now.minute) +":"+ str(now.second) 

    def desactivaZonaDePresionSensor2(self,x,y):
        self.matrizZonasActivadasSensor2[x][y] = False
        self.matrizHorasDeActivacionSensor2[x][y] = '0:00:00'
        self.matrizTiempoTranscurridoSensor2[x][y] = '0:00:00'
                
    def calculaTiempoSensor2(self):
        now = datetime.now()
        horaActual = str(now.hour) + ":" + str(now.minute) +":"+ str(now.second)
        for i in range(0,(self.matrizZonasFilas)):
            for j in range(0,(self.matrizZonasColumnas)):
                if self.matrizZonasActivadasSensor2[i][j] == True:
                    tdelta = datetime.strptime(horaActual, self.FMT) - datetime.strptime(self.matrizHorasDeActivacionSensor2[i][j], self.FMT)
                    self.matrizTiempoTranscurridoSensor2[i][j] = tdelta
        return self.matrizTiempoTranscurridoSensor2    
    


