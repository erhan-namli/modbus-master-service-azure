from PyQt5.QtCore import  QObject, QThread, pyqtSignal

from update import Ui_Form 
from PyQt5.QtWidgets import QWidget

from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QApplication, QLabel, QWidget

from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5 import uic
import sys, time


import sys

import time


class Update(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(QWidget, self).__init__()
        self.ui = Ui_Form()

        self.ui.setupUi(self)

        self.AllItems = [self.ui.comboBox.itemText(i) for i in range(self.ui.comboBox.count())]

        self.thread={}
        self.i = 0
        print(self.AllItems)

        self.ui.pushButton.clicked.connect(self.runLongTask)


    def runLongTask(self):

        self.thread[self.i] = Worker(parent=None,index =self.i, ipAdress=self.AllItems[self.i])

        self.thread[self.i].start()

        self.thread[self.i].any_signal.connect(self.run)

        self.i +=1


        pass
class Worker(QObject):

    any_signal = QtCore.pyqtSignal(int)

    def __init__(self, ipAdress, parent=None, index=0):
        super(QObject, self).__init__(parent)
        self.ipAdress = ipAdress
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


if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setApplicationDisplayName("Modbus")

    mainPage = Update()

    mainPage.show()

    sys.exit(app.exec_())