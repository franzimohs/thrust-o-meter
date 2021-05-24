
import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph
import numpy as np
import pyqtgraph as pg
# import serial



class App(QtGui.QMainWindow):
    def __init__(self, serial_list, parent=None):
        super(App, self).__init__(parent)

        self.serial_list = serial_list

        #### Create Gui Elements ###########
        self.mainbox = QtGui.QWidget()
        self.radioL = QtGui.QRadioButton()
        self.radioR = QtGui.QRadioButton()
        
       
        
        self.radioL.setText('Links!')
        self.radioR.setText('Rechts!')
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QtGui.QVBoxLayout())
        
        self.canvas = pg.GraphicsLayoutWidget()
        self.mainbox.layout().addWidget(self.canvas)
        self.mainbox.layout().addWidget(self.radioL)
        self.mainbox.layout().addWidget(self.radioR)
       
        self.target = pyqtgraph.InfiniteLine(angle = 0, pos = 300, movable = True, bounds=[100,400])
       
        self.zielhöhe = QtGui.QLabel()
        self.label = QtGui.QLabel()
        self.mainbox.layout().addWidget(self.label)
        self.mainbox.layout().addWidget(self.zielhöhe)
        
        
      
        

      
        #  line plot
        self.otherplot = self.canvas.addPlot()
      
        self.otherplot.setYRange(0,400)
        self.otherplot.addItem(self.target)
        self.otherplot.hideButtons()
        self.h2 = self.otherplot.plot(pen='y')
        
        
       
        # self.raw = serial.Serial('COM6', 115200)
       

        


        #### Set Data  #####################

        
        self.ydata = np.zeros(100)
       
        self.counter = 0
        self.fps = 0.
        self.lastupdate = time.time()

        #### Start  #####################
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._update)
        self.timer.start(1000/30)  # Hz

    def _update(self):
        # line = self.raw.readline()
        # nonl = line.strip()
        # if 0 == len(nonl): return
        # decoded = nonl.decode()
        try :
            t, val1, val2 = self.serial_list
        except: 
            val1 = 1
            val2 = 1

        if self.radioL.isChecked():
            val = val2
        elif self.radioR.isChecked():
            val = val1
        else: 
            val = val1
        self.ydata[:-1] = self.ydata[1:]
        self.ydata[-1] = -float(val)/64*9.81
        
        self.h2.setData(self.ydata)
        self.zielhöhe.setText('Zielwert: '+str(int(self.target.value()))+' N')
        
    
        now = time.time()
        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        tx = 'Mean Frame Rate:  {fps:.3f} FPS'.format(fps=self.fps )
        self.label.setText(tx)
        self.counter += 1
        


def main(serial_list):
    
    app = QtGui.QApplication(sys.argv)
    thisapp = App(serial_list)
    thisapp.show()
    sys.exit(app.exec_())

def open_realtimeplot3_from_main(serial_list):
    try:
        main(serial_list)
    except KeyboardInterrupt:
        pass
    


if __name__ == '__main__':
    open_realtimeplot3_from_main()
