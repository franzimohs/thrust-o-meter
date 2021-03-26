#!/usr/bin/python3

import serial, threading
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
		self.dev.insert(0, 'COM6')

		self.samplecount = tk.Label(f, text='samples')
		self.samplecount.pack(side='left')

		self.btn_start = tk.Button(f, text='start', command=self.start)
		self.btn_start.pack(side='left')
		self.btn_stop = tk.Button(f, text='stop&save', command=self.save, state='disabled')
		self.btn_stop.pack(side='left')

		f.pack(fill=tk.BOTH, expand=True)

		self.data = []
		self.recording = False
		self.fig = plt.figure() 
		self.ax = self.fig.add_subplot(1, 1, 1)

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

	def animate (self, t, val_in_N):
		ax.clear()
		ax.plot(t, val_in_N)
		plt.xticks(rotation=45, ha='right')
		plt.subplots_adjust(bottom=0.30)
		plt.title('Kraft-Zeit-Verlauf')
		plt.ylabel('Kraft in N')
		plt.legend()
		plt.axis([1, None, 0, 1.1])

	def reader(self):
		
		with serial.Serial(self.dev.get(), 115200, timeout=1) as s:
			while self.recording:
				try:
					line = s.readline()
					nonl = line.strip()
					decoded = nonl.decode()
					t, val = decoded.split()
					val = float(val)
					val_in_N = (val/91*1000*9,81)
					self.data.append((int(t), val_in_N))
					self.samplecount['text'] = '%d samples' % len(self.data)
					ani = animation.FuncAnimation(self.fig, self.animate, fargs=(t, val_in_N), interval=1000)
					plt.show()
				except Exception as e:
					print(e)
					continue

				# -91 == 1kg load
				

def main():
	root = tk.Tk()
	app = Reader(master=root)
	app.mainloop()

if '__main__' == __name__:
	try:
		main()
	except KeyboardInterrupt:
		pass
