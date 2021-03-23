#!/usr/bin/python3

import sys
import numpy as np
import tkinter as tk
from tkinter.font import Font
from matplotlib import pyplot

class View(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		if hasattr(master, 'title'): master.title('view')
		self.pack(fill=tk.BOTH, expand=True)

		self.font = Font(family='monospace')

		f = tk.Frame(self)

		self.plotters = {}
		for i in range(2):
			self.plotters[i] = Plotter(f)
			self.plotters[i].pack()

		self.pyplot_line = None

		tk.Button(text='load', command=self.load).pack(side='left')
		tk.Button(text='shift rechts', command=self.shift).pack(side='left') #shift rechts = shift
		tk.Button(text='shift links', command=self.unshift).pack(side='left') #shift links = unshift
		tk.Button(text='plot', command=self.plot).pack(side='left')
		self.flag_update = tk.IntVar()
		tk.Checkbutton(text='update plot after shift', var=self.flag_update).pack(side='left')
		tk.Button(text='autoshift', command=self.autoshift).pack(side='left')

		try:
			file_out, file_ref = sys.argv[1:3]
		except Exception:
			file_out, file_ref = 'out', 'ref'

		tk.Label(f, text='out file').pack(side='left')
		self.f_out = tk.Entry(f)
		self.f_out.pack(side='left')
		self.f_out.insert(0, file_out)

		tk.Label(f, text='ref file').pack(side='left')
		self.f_ref = tk.Entry(f)
		self.f_ref.pack(side='left')
		self.f_ref.insert(0, file_ref)

		f.pack(fill=tk.BOTH, expand=True)

		self.offset = 0

		self.load()

	def load(self):
		self.data = [
			np.loadtxt(self.f_out.get()),
			np.loadtxt(self.f_ref.get()),
		]

		l = min(len(self.data[0]), len(self.data[1]))

		self.data[0] = self.data[0][:l] #bis zur kürzeren länge schneiden
		self.data[1] = self.data[1][:l]

		pyplot.close()
		self.pyplot_line = None

		self.show()

	def show(self):
		#d = self.data[0] - self.data[1]

		self.plotters[0].set(self.data[0], title=self.f_out.get())
		self.plotters[1].set(self.data[1], title=self.f_ref.get())
		#self.plotters[2].set(d, title='%s - %s' % tuple(sys.argv[1:3]))

	def plot(self):
		d = self.data[0][:,1:] - self.data[1][:,1:] #alle spalten nach der 1. spalte erste [] welcher plot oben unten 2.[] welche spalte in datei
		if self.pyplot_line:
			self.pyplot_line.set_ydata(d)
		else:
			self.pyplot_line, = pyplot.plot(d)
		pyplot.show()

	def shift(self):
		return self._shift(1)

	def unshift(self):
		return self._shift(-1)

	def autoshift(self):
		out = self.data[0][:,1]
		ref = self.data[1][:,1]
		out_min_ind = np.argmin(out)
		ref_min_ind = np.argmin(ref)

		return self._shift(out_min_ind-ref_min_ind)

	def _shift(self, offset):
		self.offset += offset

		self.data[1][:,1] = np.concatenate((self.data[1][:,1][-offset:], self.data[1][:,1][:-offset]))

		self.show()

		if self.flag_update.get():
			self.plot()

class Cache():
	def __init__(self, canvas, args, width):
		self.ptr = self.last_x = self.last_y = 0
		self.lines = [
			canvas.create_line(i, 0, i, 0, **args) for i in range(width)
		]

class Plotter(tk.Frame):
	WIDTH = 800
	HEIGHT = 600
	data = np.array([])
	title = None

	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		if hasattr(master, 'title'): master.title('plotter')
		self.pack(fill=tk.BOTH, expand=True)

		self.font = Font(family='monospace')

		self.init_gui()

	def init_gui(self):
		f = tk.Frame(self)
		self.canvas = tk.Canvas(f)
		self.canvas.pack(fill=tk.BOTH, expand=True, side='left')
		self.canvas.bind("<Configure>", self.update_canvas)
		self.canvas.bind('<Motion>', self.motion)
		self.canvas.bind('<Leave>', self.leave)

		'''
		options = tk.Frame(f)

		tk.Label(options, text='y min').pack()
		self.spin_y_min = tk.Spinbox(options, from_=0, to=42000, width=6)
		self.spin_y_min.pack()

		tk.Label(options, text='y max').pack()
		self.spin_y_max = tk.Spinbox(options, from_=0, to=42000, width=6)
		self.spin_y_max.pack()

		tk.Label(options, text='x min').pack()
		self.spin_x_min = tk.Spinbox(options, from_=0, to=42000, width=6)
		self.spin_x_min.pack()

		tk.Label(options, text='x max').pack()
		self.spin_x_max = tk.Spinbox(options, from_=0, to=42000, width=6)
		self.spin_x_max.pack()

		options.pack()
		'''

		f.pack(fill=tk.BOTH, expand=True)

	def motion(self, event):
		self.canvas.coords(self.cursorline_x, event.x, 0, event.x, self.HEIGHT)
		self.canvas.coords(self.cursorline_y, 0, event.y, self.WIDTH, event.y)

		x = event.x * self.scale_x
		#y = -self.scale_y * (event.y / self.HEIGHT)
		y = event.y * self.scale_y - (self.bounds_y_min - self.bounds_y_max) // 2

		self.canvas.itemconfig(self.cursor_x, text='%d' % x)
		self.canvas.itemconfig(self.cursor_y, text='%.2f' % y)

	def leave(self, event):
		self.canvas.coords(self.cursorline_x, 0, 0, 0, 0)
		self.canvas.coords(self.cursorline_y, 0, 0, 0, 0)

		self.canvas.itemconfig(self.cursor_x, text='')
		self.canvas.itemconfig(self.cursor_y, text='')

	def update_canvas(self, event):
		self.WIDTH = event.width
		self.HEIGHT = event.height

		self.update()

	def gen_cache(self):
		self.canvas.delete(tk.ALL)

		self.background = self.canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill='black')
		self.centerline = self.canvas.create_line(0, 0, 0, 0, fill='green')
		self.cursorline_x = self.canvas.create_line(0, 0, 0, 0, fill='yellow')
		self.cursorline_y = self.canvas.create_line(0, 0, 0, 0, fill='yellow')

		self.cursor_x = self.canvas.create_text(self.WIDTH//2, self.HEIGHT-10, anchor='s', font=self.font, fill='yellow')
		self.cursor_y = self.canvas.create_text(self.WIDTH-10, self.HEIGHT//2+10, anchor='ne', font=self.font, fill='yellow')


		self.label_title = self.canvas.create_text(self.WIDTH // 2, 10, anchor='n', font=self.font, fill='white')

		labelargs = { 'font': self.font, 'fill': 'green'}
		self.label_x_min = self.canvas.create_text(20, self.HEIGHT-10, anchor='sw', **labelargs)
		self.label_x_max = self.canvas.create_text(self.WIDTH - 20, self.HEIGHT-10, anchor='se', **labelargs)
		self.label_y_min = self.canvas.create_text(10, self.HEIGHT-20, anchor='sw', **labelargs)
		self.label_y_max = self.canvas.create_text(10, 20, anchor='nw', **labelargs)

		self.label_peak = self.canvas.create_text(0, 0, anchor='n', justify='center', font=self.font, fill='yellow')

		self.cache = Cache(self.canvas, args={'fill': 'red'}, width=len(self.data))

	def draw(self):
		peak = 1e42
		peak_id = None

		for i, (j, d) in enumerate(self.data):
			x = j / self.scale_x
			y = -d / self.scale_y + self.HEIGHT // 2

			if d < peak:
				peak = d
				peak_pos = x, y + 10

			if i != 0:
				self.canvas.coords(self.cache.lines[i], self.cache.last_x, self.cache.last_y, x, y)
			self.cache.last_x = x
			self.cache.last_y = y

		self.canvas.coords(self.label_peak, *peak_pos)
		self.canvas.itemconfig(self.label_peak, text=u'\u21e7\n%d' % -peak)

	def update(self):
		if 0 == len(self.data):
			self.canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill='black')
			self.canvas.create_text(self.WIDTH//2, self.HEIGHT//2, fill='green', text='init')
			return

		self.draw()
		center = self.HEIGHT // 2

		self.canvas.coords(self.background, 0, 0, self.WIDTH, self.HEIGHT)
		self.canvas.coords(self.centerline, 0, center, self.WIDTH, center)

		self.canvas.itemconfig(self.label_x_min, text=u'\u2190 %s' % self.bounds_x_min)
		self.canvas.itemconfig(self.label_x_max, text=u'%s \u2192' % self.bounds_x_max)
		self.canvas.itemconfig(self.label_y_min, text=u'%s\n\u21a7' % self.bounds_y_min)
		self.canvas.itemconfig(self.label_y_max, text=u'\u21a5\n%s' % self.bounds_y_max)

		self.canvas.itemconfig(self.label_title, text='' if self.title is None else self.title)

	def set(self, data, title=None):
		self.bounds_x_min = 0
		self.bounds_x_max = data[-1][0]

		self.bounds_y_min = -20000
		self.bounds_y_max = -self.bounds_y_min
		self.scale_x = (self.bounds_x_max - self.bounds_x_min) / (self.WIDTH - 20)
		self.scale_y = (self.bounds_y_max - self.bounds_y_min) / -self.HEIGHT 

		self.data = data
		self.title = title

		self.gen_cache()
		self.update()

class Point():
	def __init__(self, x, y, color, ref=None, center=None):
		self.x = x
		self.y = y
		self.color = color
		self.ref = ref
		self.center = center


if '__main__' == __name__:
	root = tk.Tk()
	app = View(master=root)
	app.mainloop()
