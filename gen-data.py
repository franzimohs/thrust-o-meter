#!/usr/bin/python3

import numpy as np
import random, sys
from matplotlib import pyplot as plt

def mkdata(length, seed, delta=16):
	data = np.zeros((length*2,))
	data.shape = (length, 2)

	if seed is not None:
		random.seed(seed)

	offset = random.randint(0, 0xff)

	last = 0x00
	for i in range(length):
		val = last + random.randint(-delta, delta)
		data[i] = (i*42+offset, val)
		last = val

	return data

def main():
	l = 1024
	data = mkdata(l, None)

	np.savetxt(sys.argv[1], data, fmt='%d') # wird am ort gespeichert der mitgegeben wird

	return

	print(data)
	for d in data:
		plt.plot(d)
	plt.show()

if '__main__' == __name__:
	try:
		main()
	except KeyboardInterrupt:
		pass
