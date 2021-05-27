
import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph
import numpy as np
import pyqtgraph as pg



class App(QtGui.QMainWindow):
    def __init__(self, daten, parent=None):
        super(App, self).__init__(parent)

        self.daten = daten

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
        
        
        self.otherplot = self.canvas.addPlot()
      
        self.otherplot.setYRange(0,400)
        self.otherplot.addItem(self.target)
        self.otherplot.hideButtons()
        self.h2 = self.otherplot.plot(pen='y')
        
        self.ydata = np.zeros(1000)
       
        self.counter = 0
        self.fps = 0.
        self.lastupdate = time.time()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._update)
        self.timer.start(1000/30)  

    def _update(self):
        if self.radioL.isChecked():
            val = self.daten.l
        elif self.radioR.isChecked():
            val = self.daten.r
        else: 
            val = self.daten.r
        self.ydata[:-1] = self.ydata[1:]
        self.ydata[-1] = val*9.81
        
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
        QtCore.QTimer.singleShot(10, self._update)
        self.counter += 1
        


def main(daten):
    app = QtGui.QApplication(sys.argv)
    thisapp = App(daten)
    thisapp.show()
    app.exec_()

def open_realtimeplot3_from_main(daten):
    try:
        main(daten)
    except KeyboardInterrupt:
        pass



if __name__ == '__main__':
    open_realtimeplot3_from_main() # FIXME kaputt
