Proyecto visualización sensor flexible.
Descripción:
Se comunica con dos sensores, pies y cabeza

Configuracion de comunicacion en archivo sensorFlexibleSQLite/plotSensores.py
  - Parametros:
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
        
Ejecucion y visualizacion:
Comunicacion, tiempos y calculo de promedio por zonas de presion: python3 plotSensores.py
Visualizacion en Qt,Flexible1_1 
