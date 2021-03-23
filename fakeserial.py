#!/usr/bin/python3

import time, random, threading
import tkinter as tk
from tkinter.font import Font

class Fakeserial(tk.Frame):
	def __init__(self, serial, master=None):
		tk.Frame.__init__(self, master)
		if hasattr(master, 'title'): master.title('Fakeserial')
		self.pack(fill=tk.BOTH, expand=True)

		self.serial = serial

		self.font = Font(family='monospace')

		f = tk.Frame(self)

		tk.Button(f, text='push', command=self.push).pack(side='left')
		self.status = tk.Label(f, text='init')
		self.status.pack(side='left')

		f.pack(fill=tk.BOTH, expand=True)

	def push(self):
		self.serial.push = True

class Serial():
	def __init__(self, *void_args, **void_kwargs):
		self.freq = void_kwargs.get('freq', 100)

		self.peaklen = self.freq * 2  # seconds

		self.push = False
		self.last = 0
		self.index = 0
		self.peak_x = -1
		self.peak_y = -1

		self.gui_died = False
		self.guithread = threading.Thread(target=self.guithread, name='guithread', daemon=True)
		self.guithread.start()

	def peak_func(self, x):
		return -(0.42*x)**2

	def readline(self):
		if self.gui_died:
			raise Exception('fakeserial disconnected')

		if self.push:
			self.push = False
			self.peak_x = self.last + self.peak_func(-self.peaklen/2)
			self.peak_y = self.index

		if self.index > (self.peak_y + self.peaklen):  # peak finished -> reset
			self.peak_y = -1

		if self.peak_y != -1:
			center = self.peak_y + self.peaklen/2
			x = self.index - center
			self.last = -self.peak_func(x) + self.peak_x

		delta = 42
		val = self.last + random.randint(-delta, +delta)
		self.last = val
		self.index += 1

		ret = ('%d\t%d\n' % (self.index, val)).encode('utf8')
		time.sleep(1/self.freq)

		return ret

	def guithread(self):
		root = tk.Tk()
		gui = Fakeserial(self, master=root)
		gui.mainloop()

		self.gui_died = True

	def __enter__(self):
		return self

	def __exit__(self, *void_args):
		pass

if '__main__' == __name__:
	try:
		with Serial('/dev/fake', 9600, timeout=1) as s:
			while True:
				print('\r', len(s.readline().decode()), end='\r')
	except KeyboardInterrupt:
		print('')
