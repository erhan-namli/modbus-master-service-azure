from PyQt5.QtCore import  QObject, QThread, pyqtSignal

from update import Ui_Form 
from PyQt5.QtWidgets import QWidget

from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QApplication, QLabel, QWidget

from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5 import uic
import sys, time

import sys

import time

class Worker(QtCore.QThread):

    any_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, ipAdress=None):

        self.ipAdress = ipAdress
        super(QtCore.QThread, self).__init__(parent)
        
        
        self.is_running = True

    def run(self):
        

        while (True):
            
            print(self.ipAdress)
            time.sleep(0.01)

    def stop(self):
        self.is_running = False
      
        self.terminate()

class Update(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(QWidget, self).__init__()
        self.ui = Ui_Form()

        self.ui.setupUi(self)

        self.AllItems = [self.ui.comboBox.itemText(i) for i in range(self.ui.comboBox.count())]

        self.thread={}
        
        print(self.AllItems)

        self.ui.pushButton.clicked.connect(self.runLongTask)

        self.ui.stop.clicked.connect(self.stop_AllThreads)


    def runLongTask(self):

        for i in range(len(self.AllItems)):

            self.thread[i] = Worker(parent=None, ipAdress=self.AllItems[i])

            self.thread[i].start()

    def stop_AllThreads(self):

        for i in range(len(self.AllItems)):

            self.thread[i].stop()

            print("Durdu")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setApplicationDisplayName("Modbus")

    mainPage = Update()

    mainPage.show()

    sys.exit(app.exec_())