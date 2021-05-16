import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import UnivariateSpline

def createReference(peakHeight, plateauHeight = None, plateauLenght = None):

    if plateauHeight == None:
        plateauHeight = math.floor(peakHeight / 4)
    
    if plateauLenght == None:
        plateauLenght = 4004
    
    plaetauIndexLenght = math.floor(plateauLenght / 11)
    step = math.floor(plaetauIndexLenght / 4)

    start = (0,0)
    start2 = (10,0)
    takeoff = (25,0)
    plateau1 = (100, plateauHeight)
    plateau11 = (plateau1[0] + 0.25*step, plateauHeight)
    plateau12 = (plateau1[0] + 0.5*step, plateauHeight)
    plateau13 = (plateau1[0] + 0.75*step, plateauHeight)
    plateau2 = (plateau1[0] + step, plateauHeight)
    plateau3 = (plateau2[0] + step, plateauHeight)
    plateau4 = (plateau3[0] + step, plateauHeight)
    plateau41 = (plateau4[0] + 0.25*step, plateauHeight)
    plateau42 = (plateau4[0] + 0.5*step, plateauHeight)
    plateau43 = (plateau4[0] + 0.75*step, plateauHeight)
    plateau44 = (plateau4[0] + 0.875*step, plateauHeight)
    plateau5 = (plateau1[0] + plaetauIndexLenght, plateauHeight)
    plateau6 = (plateau5[0]+ 5, plateauHeight + 15)
    peak = (plateau5[0] + 14, peakHeight)
    coolDown = (peak[0] + 20, 0)
    end1 = (coolDown[0] + 5, 0)
    end2 = (end1[0] +5, 0)
    end3 = (end2[0] +5, 0)
    end4 = (end3[0] +5, 0)

    arrayLenght = 100 + plaetauIndexLenght + 14 + 20 + 5 + 5 + 5 + 5+5
    timeLenght = arrayLenght*11

    pointsX = np.array([start[0], start2[0], takeoff[0], plateau1[0], plateau11[0], plateau12[0], plateau13[0], plateau2[0], plateau3[0], plateau4[0],plateau41[0],plateau42[0],plateau43[0], plateau44[0],plateau5[0],plateau6[0], peak[0], coolDown[0], end1[0], end2[0], end3[0], end4[0]])
    pointsY = np.array([start[1], start2[1], takeoff[1], plateau1[1], plateau11[1], plateau12[1], plateau13[1], plateau2[1], plateau3[1], plateau4[1], plateau41[1],plateau42[1],plateau43[1],plateau44[1], plateau5[1], plateau6[1], peak[1], coolDown[1], end1[1], end2[1], end3[1], end4[1]])

    #plt.plot(pointsX,pointsY, 'rx')
    interpolation = interpolate.splrep(pointsX, pointsY)

    newX = np.arange(arrayLenght)
    
    newY = interpolate.splev(newX, interpolation, der=0)

    timeX = np.arange(0, timeLenght, 11)

    finalArr = np.zeros((arrayLenght, 2))
    finalArr[:,0] = timeX
    finalArr[:,1] = newY

    return finalArr
    

if '__main__' == __name__:
    ref = createReference(270, plateauLenght= 5000)

    plt.plot(ref[:,0], ref[:,1])
    plt.show()
