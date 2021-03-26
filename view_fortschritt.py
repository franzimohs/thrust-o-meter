#!/usr/bin/python3
import numpy as np
from matplotlib import pyplot as plt

datei = open('Peak.txt','a')
datei.write("5\n")
datei.write('6\n')
datei.write('7\n')

y = np.loadtxt('Peak.txt')
plt.plot(y)
plt.show()
