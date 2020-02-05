import imageio
import numpy as np



def coloredPixels(im, col):
    k = []
    for i in range(len(im)):
        for j in range(len(im[0])):
            if np.allclose(im[i][j], col):
                k.append([i,j])
        print(i)
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


def main(filename):
    im = imageio.imread(filename)
    green = [0,255,0]
    colPixList = coloredPixels(im, green)
    return getWidthHeight(colPixList)                                
    


width, height = main('ol.jpeg')
print("\nWidth of the garbage is:", width)
print("\nHeight of the garbage is:", height)
