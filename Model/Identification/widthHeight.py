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

def calculate(filename,dist,focal,horizfov):
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

def main(filename1,filename2,dist1,dist2,focal,horizfov):
    x,y =calculate(filename1,dist,focal,horizfov)
    z,w = calculate(filename2,dist2,focal,horizfov)
    print("\nWidth of the filename1 is:", x)
    print("\nHeight of the filename1 is:", y)
    print("\nWidth of the filename2 is:", z)
    print("\nHeight of the filename2 is:", w)
    return x * y * z

volume = main('output/s1.jpg','output/s2.jpg',1.27,1.27,3.20,59)
print("\nVolume of the garbage is:", volume)


