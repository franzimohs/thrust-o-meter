####CC Franziska Mohs####

import threading
import numpy as np
import tkinter as tk
from tkinter.font import Font
import datetime
import os.path


class Reader(tk.Frame):
	def __init__(self, daten, callback, pfad, master=None):
		tk.Frame.__init__(self, master)
		if hasattr(master, 'title'): master.title('Aufnahme')
		self.grid()
		self.daten = daten
		self.callback = callback
		self.pfad = pfad
		self.font = Font(family='monospace')
		self.flag_update = tk.IntVar(master, 0)
		self.ref = tk.IntVar(master, 0)
		self.verhältnis = tk.IntVar(master, 0)
		outer_frame = tk.Frame(self)
		f = tk.Frame(outer_frame)
		master.iconbitmap('assets/bone.ico')

		tk.Label(f, font=self.font, text='file name').grid(row = 0, column = 0)
		self.fname = tk.Entry(f, font=self.font)
		self.fname.grid(row = 0, column = 1)
		self.timeName = datetime.datetime.now().strftime('%Y%m%d_%H%M%S%z')
		self.fname.insert(0, self.timeName)
		tk.Label(f, font=self.font, text='Maximalkraft:').grid(row = 1, column=2)
		tk.Radiobutton(f, text='Rechts!', var=self.flag_update, value=0).grid(row = 0, column = 4)
		tk.Radiobutton(f, text='Links!', var=self.flag_update, value=1).grid(row = 0, column = 5)
		tk.Radiobutton(f, text='Beide!', var=self.flag_update, value=2).grid(row = 0, column = 6)
		tk.Radiobutton(f, text='550N', var=self.ref, value=0).grid(row=1, column=3)
		tk.Radiobutton(f, text='450N', var=self.ref, value=1).grid(row=1, column=4)
		tk.Radiobutton(f, text='350N', var=self.ref, value=2).grid(row=1, column=5)
		tk.Radiobutton(f, text='250N', var=self.ref, value=3).grid(row=1, column=6)
		tk.Radiobutton(f, text='1:2,5', var=self.verhältnis, value=0).grid(row=2, column =3)
		tk.Radiobutton(f, text='1:4', var=self.verhältnis, value=1).grid(row=2, column =4)
		tk.Radiobutton(f, text='ohne Referenz', var=self.ref, value=4).grid(row=1, column=7)
		self.ref.set(0)
		self.verhältnis.set(0)
		self.flag_update.set(0)
		
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
	
	def name_update(self):
		self.timeName = datetime.datetime.now().strftime('%Y%m%d_%H%M%S%z')
		self.fname.delete(0, 'end')
		self.fname.insert(0, self.timeName)

	def start(self):
		self.recording = True
		self.btn_start.config(state='disabled')
		self.btn_stop.config(state='normal')
		threading.Thread(target=self.reader, daemon=True).start()

	def save(self):
		self.recording = False
		self.btn_start.config(state='normal')
		self.btn_stop.config(state='disabled')
		filename = os.path.join(self.pfad, self.fname.get()+'.tom'+str(self.ref.get())+str(self.verhältnis.get()))
		np.savetxt(filename, self.data, fmt='%d')
		self.data.clear()
		self.samplecount['text'] = 'gespeichert'
		self.name_update()
		

	def reader(self):
		with self.daten.lock:
			while self.recording:
				if self.flag_update.get()==0:
					self.data.append((self.daten.t, (self.daten.r * 9.81)))#g= 9,81 F= m*g
				elif self.flag_update.get()==1:
					self.data.append((self.daten.t, (self.daten.l * 9.81)))#g= 9,81 F= m*g
				else:
					self.data.append((self.daten.t, (self.daten.r * 9.81), (self.daten.l * 9.81)))#g= 9,81 F= m*g
					
					

				self.samplecount['text'] = '%d samples' % len(self.data)
				self.daten.lock.wait()
	
	def on_closing(self):
		self.callback()
		self.master.destroy()
		

def main(daten, callback, pfad):
	root = tk.Tk()
	app = Reader(daten, callback, pfad, master=root)
	root.protocol("WM_DELETE_WINDOW", app.on_closing)
	app.mainloop()

def open_reader_from_main(daten, callback, pfad):
	try:
		main(daten, callback, pfad)
	except KeyboardInterrupt:
		pass


