import sys
import sqlite3

def recibeDatos():
	conn = sqlite3.connect('../sensorFlexibleSQLiteDB/distribucionPresionSensorFlexible.db')
	c = conn.cursor()
	for row in c.execute("SELECT * FROM sensorFlexible WHERE `id`='1'"):
		#Retorna ;anguloIMU;
		print(";" + str(row[3]) + ";")
recibeDatos()
