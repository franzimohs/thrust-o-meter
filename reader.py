#!/usr/bin/python3

import threading, sys

import numpy as np
import tkinter as tk
from tkinter.font import Font

class Reader(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		if hasattr(master, 'title'): master.title('reader')
		self.pack(fill=tk.BOTH, expand=True)

		self.font = Font(family='monospace')

		outer_frame = tk.Frame(self)
		f = tk.Frame(outer_frame)

		tk.Label(f, font=self.font, text='file name').pack(side='left')
		self.fname = tk.Entry(f, font=self.font)
		self.fname.pack(side='left')
		self.fname.insert(0, 'out')

		try:
			port = sys.argv[1]
		except Exception:
			port = 'COM 3'

		tk.Label(f, font=self.font, text='device').pack(side='left')
		self.dev = tk.Entry(f, font=self.font)
		self.dev.pack(side='left')
		self.dev.insert(0, port)

		self.samplecount = tk.Label(f, font=self.font, text='samples')
		self.samplecount.pack(side='left')

		self.btn_start = tk.Button(f, font=self.font, text='start', command=self.start)
		self.btn_start.pack(side='left')
		self.btn_stop = tk.Button(f, font=self.font, text='stop&save', command=self.save, state='disabled')
		self.btn_stop.pack(side='left')

		f.pack()

		self.frame_fakeserial = tk.Frame(outer_frame)
		self.frame_fakeserial.pack(side='left')

		outer_frame.pack(fill=tk.BOTH, expand=True)

		self.data = []
		self.recording = False

	def start(self):
		self.recording = True
		self.btn_start.config(state='disabled')
		self.btn_stop.config(state='normal')
		threading.Thread(target=self.reader, daemon=True).start()

	def save(self):
		self.recording = False
		self.btn_start.config(state='normal')
		self.btn_stop.config(state='disabled')
		np.savetxt(self.fname.get(), self.data, fmt='%d')
		self.data = []
		self.samplecount['text'] = 'saved'

	def reader(self):
		port = self.dev.get()

		kwargs = {}
		if 'fake' == port:
			import fakeserial
			kwargs['master'] = self.frame_fakeserial
			serial_class = fakeserial
		else:
			import serial
			serial_class = serial

		with serial_class.Serial(self.dev.get(), 115200, timeout=1, **kwargs) as s:
			while self.recording:
				try:
					line = s.readline()
					nonl = line.strip()
					decoded = nonl.decode()
					t, val = decoded.split()
					val = float(val)
				except Exception as e:
					print(e)
					continue

				# -64 == 1kg load g= 9,81 F= m*g
				self.data.append((int(t), (val/64*9.81)))

				self.samplecount['text'] = '%d samples' % len(self.data)

def main():
	root = tk.Tk()
	app = Reader(master=root)
	app.mainloop()

if '__main__' == __name__:
	try:
		main()
	except KeyboardInterrupt:
		pass
