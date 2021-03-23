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

		tk.Button(f, font=self.font, text='insert peak', command=self.new_peak).pack(side='left')
		self.status = tk.Label(f, text='', font=self.font)
		self.status.pack(side='left')

		f.pack(fill=tk.BOTH, expand=True)

	def new_peak(self):
		self.serial.new_peak = True
		self.status['text'] = 'inserting peak starting at %d for %d samples' % (self.serial.index, self.serial.peaklen)

class Serial():
	def __init__(self, *void_args, **void_kwargs):
		self.freq = void_kwargs.get('freq', 100)
		master = void_kwargs.get('master')

		self.peaklen = self.freq * 4  # seconds

		self.new_peak = False
		self.last = 0
		self.index = 0
		self.peak_x = -1
		self.peak_y = -1

		self.gui_died = False
		self.gui = None

		if master is None:
			self.guithread = threading.Thread(target=self.guithread, name='guithread', daemon=True)
			self.guithread.start()
		else:
			self.gui = Fakeserial(self, master=master)

	def peak_func(self, x):
		return -(42*x/420)**2

	def readline(self):
		if self.gui_died:
			raise Exception('fakeserial disconnected')

		if self.new_peak:
			self.new_peak = False
			# remember start coords
			self.peak_x = self.last + self.peak_func(-self.peaklen/2)
			self.peak_y = self.index

		if self.index > (self.peak_y + self.peaklen):  # peak finished -> reset
			self.peak_y = -1

		if self.peak_y != -1:
			center = self.peak_y + self.peaklen/2
			x = self.index - center
			self.last = -self.peak_func(x) + self.peak_x

		delta = 42
		val = self.last + random.randint(-delta, +delta) // 10
		self.last = val
		self.index += 1

		ret = ('%d\t%d\n' % (self.index, val)).encode('utf8')
		time.sleep(1/self.freq)

		return ret

	def guithread(self):
		root = tk.Tk()
		self.gui = Fakeserial(self, master=root)
		self.gui.mainloop()

		self.gui_died = True

	def __enter__(self):
		return self

	def __exit__(self, *void_args):
		if self.gui is not None:
			self.gui.destroy()

if '__main__' == __name__:
	try:
		with Serial('/dev/fake', 9600, timeout=1) as s:
			f = open('out', 'w')
			while True:
				print(s.readline().decode().strip(), file=f)
	except KeyboardInterrupt:
		print('')
