#!/usr/bin/python3

import pyaudio
import numpy as np
import threading
import serial

class Fiep():
	def __init__(self):
		self.samplerate = 44100
		self.buf = np.zeros(self.samplerate//10, dtype=np.float32) # 10Hz segments

		self.i = 0

		self.thread = threading.Thread(target=self.feed, daemon=True)
		self.die = True

	def __enter__(self):
		self.p = pyaudio.PyAudio()

		self.stream = self.p.open(
			format = pyaudio.paFloat32,
			channels = 1,
			rate = self.samplerate,
			output = True
		)

		self.die = False
		self.thread.start()

		self.debug = None #open('debug', 'wb')

		return self

	def play(self, freq=440.0, volume=1.0):
		for i, s in enumerate(self.buf):
			self.buf[i] = np.sin(
				2 * np.pi * (i+self.i) * freq / self.samplerate
			) * volume

		self.i += i +1

		if self.debug:
			self.debug.write(self.buf.astype(np.float32))
			self.debug.write(self.buf.astype(np.float32))

	def feed(self):
		while not self.die:
			self.stream.write(self.buf) # blocking

		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()

		if self.debug:
			self.debug.close()

	def __exit__(self, *args):
		self.die = True

demo_offset = 0
freq_update = 200.0

def update():
	global freq_update
	raw = serial.Serial('COM6', 115200)
	line = raw.readline()
	nonl = line.strip()
	try:
		decoded = nonl.decode()
		t, val1, val2 = decoded.split()
		# if self.flag_update.get():
		#     val = float(val1)
		# else: val = float(val2)
		val = -float(val1)
		freq_update = (val/64*9.81-200)
		time.sleep(0.5)
	except:
		print('e') 
		pass
	return freq_update


def demo():
	global demo_offset

	freq = (
		440.000,
		466.164,
		493.883,
		523.251,
		554.365,
		587.330,
		440*2**0,
		440*2**1,
		440*2**2,
		440*2**3,
		440*2**4,
	)

	time.sleep(0.5)
	demo_offset += 1
	if demo_offset >= len(freq):
		demo_offset = 0

	return freq[demo_offset]


if '__main__' == __name__:
	import time
	with Fiep() as f:
		while True:
			freq = update()
			f.play(freq=freq, volume=0.5)
