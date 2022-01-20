# Welcome to PyShine
# This is part 12 of the PyQt5 learning series
# Start and Stop Qthreads
# Source code available: www.pyshine.com
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5 import uic
import sys, time

class PyShine_THREADS_APP(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('threads.ui',self)
        self.resize(888, 200)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("PyShine.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.i = 0
        self.thread={}

        self.pushButton.clicked.connect(self.start_worker_1)
        self.pushButton_2.clicked.connect(self.start_worker_2)
        self.pushButton_3.clicked.connect(self.start_worker_3)
        self.pushButton_4.clicked.connect(self.stop_worker_1)
        self.pushButton_5.clicked.connect(self.stop_worker_2)
        self.pushButton_6.clicked.connect(self.stop_worker_3)

    def start_worker_multiply(self, i):

        self.thread[i] = ThreadClass(parent=None,index=1)
        self.thread[i].start()
        self.thread[i].any_signal.connect(self.my_function)
        self.pushButton.setEnabled(False)
        
        

    def start_worker_1(self):
        self.thread[1] = ThreadClass(parent=None,index=1)
        self.thread[1].start()
        self.thread[1].any_signal.connect(self.my_function)
        self.pushButton.setEnabled(False)
        
    def start_worker_2(self):
        self.thread[2] = ThreadClass(parent=None,index=2)
        self.thread[2].start()
        self.thread[2].any_signal.connect(self.my_function)
        self.pushButton_2.setEnabled(False)

    def start_worker_3(self):
        self.thread[3] = ThreadClass(parent=None,index=3)
        self.thread[3].start()
        self.thread[3].any_signal.connect(self.my_function)
        self.pushButton_3.setEnabled(False)
        
    def stop_worker_1(self):
        self.thread[1].stop()
        self.pushButton.setEnabled(True)

    def stop_worker_2(self):
        self.thread[2].stop()
        self.pushButton_2.setEnabled(True)

    def stop_worker_3(self):
        self.thread[3].stop()
        self.pushButton_3.setEnabled(True)

    def my_function(self,counter):
        
        cnt=counter
        index = self.sender().index
        if index==1:
            self.progressBar.setValue(cnt) 
        if index==2: 
            self.progressBar_2.setValue(cnt)  
        if index==3:
            self.progressBar_3.setValue(cnt)  
    
class ThreadClass(QtCore.QThread):
    
    any_signal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None,index=0):
        super(ThreadClass, self).__init__(parent)
        self.index=index
        self.is_running = True
    def run(self):
        print('Starting thread...',self.index)
        cnt=0
        while (True):
            cnt+=1
            if cnt==99: cnt=0
            time.sleep(0.01)
            self.any_signal.emit(cnt) 
    def stop(self):
        self.is_running = False
        print('Stopping thread...',self.index)
        self.terminate()



app = QtWidgets.QApplication(sys.argv)
mainWindow = PyShine_THREADS_APP()
mainWindow.show()
sys.exit(app.exec_())