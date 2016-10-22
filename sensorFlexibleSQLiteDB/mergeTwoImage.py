from PIL import Image, ImageDraw
import time
import sys
import struct

maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1
sys.setrecursionlimit(maxint)

while True:   
    try:
        img = Image.open('../appSensorFlexibleWebLocalMatplotlib/img/tablaTiemposExposicionSensor1.png')
        img.putalpha(40)
        img.save('../appSensorFlexibleWebLocalMatplotlib/img/foreground100.png')
    except:
        pass
    try:
        img = Image.open('../appSensorFlexibleWebLocalMatplotlib/img/tablaTiemposExposicionSensor2.png')
        img.putalpha(40)
        img.save('../appSensorFlexibleWebLocalMatplotlib/img/foreground101.png')
    except:
        pass

    try:
        foreground = Image.open("../appSensorFlexibleWebLocalMatplotlib/img/foreground100.png")
        foreground1 = Image.open("../appSensorFlexibleWebLocalMatplotlib/img/foreground101.png")

        backgroundSensor1 = Image.open("../appSensorFlexibleWebLocalMatplotlib/img/sensor1.jpg")
        backgroundSensor1.paste(foreground, (0, 0), foreground)
        backgroundSensor1.paste(foreground1, (800, 0), foreground1)
        #backgroundSensor1.save("sensorCompleto.jpg")
        
        width, height = backgroundSensor1.size   # Get dimensions
        left = 0
        top = 0
        right = width/2
        bottom = height

        left1 = width/2
        top1 = 0
        right1 = width
        bottom1 = height

        crop = backgroundSensor1.crop((left, top, right, bottom))
        crop.save("../appSensorFlexibleWebLocalMatplotlib/img/sensor1.jpeg","jpeg")

        crop1 = backgroundSensor1.crop((left1, top1, right1, bottom1))
        crop1.save("../appSensorFlexibleWebLocalMatplotlib/img/sensor2.jpeg","jpeg")

        
    except:
        pass

             
print("merge sensor completo")


 


