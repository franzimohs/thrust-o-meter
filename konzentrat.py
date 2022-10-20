#!/usr/bin/python3

import tkinter as tk

# from realtimeplot.py >>>>>
import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph

app = None

class App(QtGui.QMainWindow):
    def __init__(self, daten, callback, parent=None):
        print('pre super')
        print(super(App, self).__init__(parent))
        print('post super')

        self.daten = daten
        self.callback = callback

        self.mainbox = QtGui.QWidget()
        self.setWindowTitle('Real-Time-Plot')

        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QtGui.QVBoxLayout())

        self.canvas = pyqtgraph.GraphicsLayoutWidget()
        self.mainbox.layout().addWidget(self.canvas)

        self.target = pyqtgraph.InfiniteLine(angle = 0, pos = 300, movable = True, bounds=[100,400])

        self.label = QtGui.QLabel()
        self.mainbox.layout().addWidget(self.label)

        self.otherplot = self.canvas.addPlot()
        self.otherplot.addItem(self.target)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._update)
        self.timer.start(int(1000/30))

    def closeEvent(self, event):
        self.callback()
        event.accept()

    def _update(self):
        self.label.setText('%s' % time.time())

def main(daten, callback):
    global app
    if app is None:
        app = QtGui.QApplication(sys.argv)
        print('app', app)

    thisapp = App(daten, callback)
    thisapp.show()
    
    print('pre exec')
    print('exec', app.exec_())

def open_realtimeplot3_from_main(daten, callback):
    try:
        main(daten, callback)
    except KeyboardInterrupt:
        pass
# from realtimeplot.py <<<<<


class ThrustOMeter():
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.realtimeplot_btn = tk.Button(window, text="REALTIMEPLOT!", bd='5', command=lambda: main(0, self.callback))
        self.realtimeplot_btn.grid()

        self.window.mainloop()

    def callback(self):
        print('callback')

if __name__ == '__main__':
    ThrustOMeter(tk.Tk(), "Thrust-O-Meter")
