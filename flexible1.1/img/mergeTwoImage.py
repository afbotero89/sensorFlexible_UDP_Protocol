from PIL import Image, ImageDraw
import time
import sys
import struct

maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1
sys.setrecursionlimit(maxint)

while True:   

    try:
        
        img = Image.open('tablaTiemposExposicionSensor1.png')
        img.putalpha(40)
        img.save('foreground100.png')
    except:
        pass
        
    
    try:
        foreground = Image.open("foreground100.png")

    except:
        pass
    
    try:
        
        img1 = Image.open('tablaTiemposExposicionSensor2.png')
        img1.putalpha(40)
        img1.save('foreground101.png')
    except:
        pass

    try:
        foreground1 = Image.open("foreground101.png")

    except:
        pass
    

    try:
        backgroundSensor1 = Image.open("sensor1.jpg")
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
        crop.save("sensor1.jpeg","jpeg")

        crop1 = backgroundSensor1.crop((left1, top1, right1, bottom1))
        crop1.save("sensor2.jpeg","jpeg")
        #backgroundSensor1 = Image.open("sensor1SinTiempos.jpeg")
        #backgroundSensor2 = Image.open("sensor2SinTiempos.jpeg")

        #backgroundSensor1.save("sensor1SinTiempos.jpg")
        #backgroundSensor2.save("sensor2SinTiempos.jpg")

        #backgroundSensor1 = Image.open("sensor1SinTiempos.jpg")
        #backgroundSensor2 = Image.open("sensor2SinTiempos.jpg")


        #backgroundSensor1.paste(foreground, (0, 0), foreground)
        #backgroundSensor2.paste(foreground1, (0, 0), foreground1)
        
        #backgroundSensor1.save("sensor1.jpeg")
        #backgroundSensor2.save("sensor2.jpeg")
        print("merge image !!!!!!!!!!!!!!!")
    except:
        pass
             
print("merge sensor completo")


 


