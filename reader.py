#!/usr/bin/python3

import threading, sys

import numpy as np
import tkinter as tk
from tkinter.font import Font
import datetime

class Reader(tk.Frame):
	def __init__(self, serial_list, master=None):
		tk.Frame.__init__(self, master)
		if hasattr(master, 'title'): master.title('reader')
		self.grid()
		self.serial_list= serial_list
		self.font = Font(family='monospace')

		outer_frame = tk.Frame(self)
		f = tk.Frame(outer_frame)

		tk.Label(f, font=self.font, text='file name').grid(row = 0, column = 0)
		self.fname = tk.Entry(f, font=self.font)
		self.fname.grid(row = 0, column = 1)
		self.timeName = datetime.datetime.now().strftime('%Y%m%d_%H%M%S%z')
		self.fname.insert(0, self.timeName)
		self.flag_update = tk.IntVar()
		tk.Radiobutton(f, text='Rechts!', var=self.flag_update, value=True).grid(row = 0, column = 4)
		tk.Radiobutton(f, text='Links!', var=self.flag_update, value=False).grid(row = 0, column = 5)

		self.samplecount = tk.Label(f, font=self.font, text='samples')
		self.samplecount.grid(row = 0, column = 6)

		self.btn_start = tk.Button(f, font=self.font, text='start', command=self.start)
		self.btn_start.grid(row = 0, column = 7)
		self.btn_stop = tk.Button(f, font=self.font, text='stop&save', command=self.save, state='disabled')
		self.btn_stop.grid(row = 0, column = 8)

		f.grid()

		self.frame_fakeserial = tk.Frame(outer_frame)
		self.frame_fakeserial.grid(row = 0, column = 9)

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
		
		
		while self.recording:
			t, val1, val2 = self.serial_list 
			if self.flag_update.get():
				val = float(val1)
			else: val = float(val2)
			
			

			# -64 == 1kg load g= 9,81 F= m*g
			self.data.append((int(t), (val/64*9.81)))

			self.samplecount['text'] = '%d samples' % len(self.data)

def main(serial_list):
	root = tk.Tk()
	app = Reader(serial_list, master=root)
	app.mainloop()

def open_reader_from_main(serial_list):
	try:
		main(serial_list)
	except KeyboardInterrupt:
		pass

if '__main__' == __name__:
	open_reader_from_main([10,10.0,10.0])
