from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import serial

app = QtGui.QApplication([])

p = pg.plot()
p.setWindowTitle('live plot from serial')
curve = p.plot()
xdata = [0]
ydata = [0.0]
raw=serial.Serial('COM6', 115200)


def update():
    global curve
    line = raw.readline()
    nonl = line.strip()
    decoded = nonl.decode()
    t, val = decoded.split()
    val = float(val)/64*9.81
    xdata.append(int(t))
    ydata.append(val) 
    curve.setData(xdata, ydata)
    app.processEvents()


if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()