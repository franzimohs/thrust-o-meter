#!/usr/bin/python3
import Analyse as al
import numpy as np

def lernfortsave():
    dateiP = open('Peak.txt', 'a')
    dateiP.write(str(peakValue)+'\n')
    dateiI = open('Inzisur.txt', 'a')
    dateiI.write(str(dentValue)+'\n')
    dateiVK = open('VorspanKrft.txt', 'a')
    dateiVK.write(str(plateauValue)+'\n')
    dateiZ = open('Zeit.txt', 'a')
    dateiZ.write(str(deltaX)+'\n')
