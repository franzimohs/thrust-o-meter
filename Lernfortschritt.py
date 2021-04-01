#!/usr/bin/python3
import Analyse as al
import numpy as np

def lernfortsave():
  #  rawData = np.loadtxt("./ref")
  #  analyse = al.rawData

    dateiP = open('Peak.txt', 'a')
    dateiP.write(al.analyse.peak[2] +'\n')
    dateiI = open('Inzisur.txt', 'a')
    dateiI.write(al.analyse.dent[2] +'\n')
    dateiVK = open('VorspanKrft.txt', 'a')
    dateiVK.write(al.analyse.plateau[2] +'\n')
    dateiZ = open('Zeit.txt', 'a')
    dateiZ.write(al.analyse.slope +'\n')
