#!/usr/bin/python3

import threading, sys

import numpy as np
import tkinter as tk
from tkinter.font import Font
import datetime

class Reader(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		if hasattr(master, 'title'): master.title('reader')
		self.grid()

		self.font = Font(family='monospace')

		outer_frame = tk.Frame(self)
		f = tk.Frame(outer_frame)

		tk.Label(f, font=self.font, text='file name').grid(row = 0, column = 0)
		self.fname = tk.Entry(f, font=self.font)
		self.fname.grid(row = 0, column = 1)
		self.timeName = datetime.datetime.now().strftime('%Y%m%d_%H%M%S%z')
		self.fname.insert(0, self.timeName)
		self.flag_update = tk.IntVar()
		tk.Checkbutton(f, text='Rechts!', var=self.flag_update).grid(row = 0, column = 4)
		
		try:
			port = sys.argv[1]
		except Exception:
			port = 'COM6'

		tk.Label(f, font=self.font, text='device').grid(row = 0, column = 2)
		self.dev = tk.Entry(f, font=self.font)
		self.dev.grid(row = 0, column = 3)
		self.dev.insert(0, port)

		self.samplecount = tk.Label(f, font=self.font, text='samples')
		self.samplecount.grid(row = 0, column = 5)

		self.btn_start = tk.Button(f, font=self.font, text='start', command=self.start)
		self.btn_start.grid(row = 0, column = 6)
		self.btn_stop = tk.Button(f, font=self.font, text='stop&save', command=self.save, state='disabled')
		self.btn_stop.grid(row = 0, column = 7)

		f.grid()

		self.frame_fakeserial = tk.Frame(outer_frame)
		self.frame_fakeserial.grid(row = 0, column = 8)

		outer_frame.grid()

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
					t, val1, val2 = decoded.split()
					if self.flag_update.get():
						val = float(val1)
					else: val = float(val2)
				
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

def open_reader_from_main():
	try:
		main()
	except KeyboardInterrupt:
		pass

if '__main__' == __name__:
	open_reader_from_main()
