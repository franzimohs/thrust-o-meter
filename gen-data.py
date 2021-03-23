#!/usr/bin/python3

import numpy as np
import random, sys
from matplotlib import pyplot as plt

def mkdata(length, seed, delta=16):
	data = np.zeros((length, 2))

	if seed is not None:
		random.seed(seed)

	last = 0x00
	for i in range(length):
		val = last + random.randint(-delta, delta)
		data[i][0] = i
		data[i][1] = val
		last = val

	return data

def main():
	for arg in sys.argv[1:]:
		data = mkdata(length=1024, seed=None, delta=256)

		np.savetxt(arg, data, fmt='%d') # wird am ort gespeichert der mitgegeben wird

	return

if '__main__' == __name__:
	try:
		main()
	except KeyboardInterrupt:
		pass
