import imageio
import numpy as np
import math


def coloredPixels(im, col):
    k = []
    for i in range(len(im)):
        for j in range(len(im[0])):
            if np.allclose(im[i][j], col):
                k.append([i,j])
        #print(i)
    return k



def getWidthHeight(k):
    maxY = maxX = 0
    minY = minX = 300
    for i in k:
        if i[1] > maxX:
            maxX = i[1]
        if i[1] < minX:
            minX = i[1]
        if i[0] > maxY:
            maxY = i[0]
        if i[0] < minY:
            minY = i[0]
    print(minX, minY)
    print(maxX, maxY)

    width = abs(maxX - minX)
    height = abs(maxY - minY)
    return width, height

def getSensorWidth(horzifov,focal):
    return math.tan(math.radians(horzifov/2))*2*focal

def pixelTomm(pixel,dpi):
    return pixel*25.4/dpi
    
def getActualWidth(width,dist,focal):
    actualWidth=(width*dist)/focal
    return actualWidth

def getActualHeight(actualWidth,pixwidth,pixheight):
    pixelPerMetric = pixwidth/actualWidth
    return pixheight/pixelPerMetric

def main(filename,dist,focal,horizfov):
    im = imageio.imread(filename)
    green = [0,255,0]
    colPixList = coloredPixels(im, green)
    pixwidth, pixheight =getWidthHeight(colPixList)
    print(pixwidth,pixheight)
    sensorw = getSensorWidth(horizfov,focal)
    widthmm=pixwidth*sensorw/im.shape[1]
    actualWidth=getActualWidth(widthmm,dist,focal)
    actualHeight=getActualHeight(actualWidth,pixwidth,pixheight)
    return actualWidth,actualHeight

width, height = main('output/ol.jpeg',2.5,3.20,59)
print("\nWidth of the garbage is:", width)
print("\nHeight of the garbage is:", height)

