from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import serial
from pyqtgraph.ptime import time
from collections import deque



app = QtGui.QApplication([])

p = pg.plot()
p.setWindowTitle('live plot from serial')
curve = p.plot()
p.setYRange(0, 300, padding=0)
#xdata = [0]
#ydata = [0.0]
xdata = deque([0], maxlen=100)
ydata = deque([0.0], maxlen=100)
raw=serial.Serial('COM6', 115200)


def update():
    global curve
    line = raw.readline()
    nonl = line.strip()
    if 0 == len(nonl): return
    decoded = nonl.decode()
    t, val = decoded.split()
    val = float(val)/64*9.81
    xdata.append(int(t))
    ydata.append((-1)*val) 
    curve.setData(xdata, ydata)
    app.processEvents()

def update_wrapper():
    try:
         update()
    except Exception:
         pass


timer = QtCore.QTimer()
timer.timeout.connect(update_wrapper)

#timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()