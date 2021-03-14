#!/usr/bin/python3

import serial, threading

import numpy as np
import tkinter as tk
from tkinter.font import Font

class Reader(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		if hasattr(master, 'title'): master.title('reader')
		self.pack(fill=tk.BOTH, expand=True)

		self.font = Font(family='monospace')

		f = tk.Frame(self)

		tk.Label(f, text='file name').pack(side='left')
		self.fname = tk.Entry(f)
		self.fname.pack(side='left')
		self.fname.insert(0, 'out')

		tk.Label(f, text='device').pack(side='left')
		self.dev = tk.Entry(f)
		self.dev.pack(side='left')
		self.dev.insert(0, 'COM 3')

		self.samplecount = tk.Label(f, text='samples')
		self.samplecount.pack(side='left')

		self.btn_start = tk.Button(f, text='start', command=self.start)
		self.btn_start.pack(side='left')
		self.btn_stop = tk.Button(f, text='stop&save', command=self.save, state='disabled')
		self.btn_stop.pack(side='left')

		f.pack(fill=tk.BOTH, expand=True)

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
		with serial.Serial(self.dev.get(), 115200, timeout=1) as s:
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

				# -91 == 1kg load
				self.data.append((int(t), (val / 91) * 1000))

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
