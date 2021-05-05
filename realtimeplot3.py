import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import serial


class App(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        #### Create Gui Elements ###########
        self.mainbox = QtGui.QWidget()
        self.radio = QtGui.QRadioButton()
        self.radio.setText('Links!')
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QtGui.QVBoxLayout())
        
        self.canvas = pg.GraphicsLayoutWidget()
        self.mainbox.layout().addWidget(self.canvas)
        self.mainbox.layout().addWidget(self.radio)

        self.label = QtGui.QLabel()
        self.mainbox.layout().addWidget(self.label)
        

        
        

      
        #  line plot
        self.otherplot = self.canvas.addPlot()
        self.otherplot.addLine(y=300)
        self.otherplot.setYRange(0,400)

        self.h2 = self.otherplot.plot(pen='y')
        
        
       
        self.raw = serial.Serial('COM6', 115200)


        


        #### Set Data  #####################

        
        self.ydata = np.zeros(100)
       
        self.counter = 0
        self.fps = 0.
        self.lastupdate = time.time()

        #### Start  #####################
        self._update()
        

    def _update(self):

        line = self.raw.readline()
        nonl = line.strip()
        if 0 == len(nonl): return
        decoded = nonl.decode()
        try :
            t, val1, val2 = decoded.split()
        except: 
            val1 = 1
            val2 = 1

        if self.radio.isChecked():
            val = val2
        else: val = val1
        self.ydata[:-1] = self.ydata[1:]
        self.ydata[-1] = -float(val)/64*9.81
        
        self.h2.setData(self.ydata)
        
    
        now = time.time()
        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        tx = 'Mean Frame Rate:  {fps:.3f} FPS'.format(fps=self.fps )
        self.label.setText(tx)
        QtCore.QTimer.singleShot(1, self._update)
        self.counter += 1


def main():
    app = QtGui.QApplication(sys.argv)
    thisapp = App()
    thisapp.show()
    sys.exit(app.exec_())

def open_realtimeplot3_from_main():
    try:
        main()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    open_realtimeplot3_from_main()
