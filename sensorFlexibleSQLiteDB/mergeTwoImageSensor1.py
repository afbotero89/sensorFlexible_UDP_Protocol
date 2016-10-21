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
        
    
