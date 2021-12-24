from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QApplication, QLabel, QWidget
import sys

from registerRecording import *
from newregisters import *

from modbus import Ui_MainWindow

from pyModbusTCP.client import ModbusClient

#-------------- Database --------------#
import sqlite3
conn = sqlite3.connect('database.db')
curs = conn.cursor()

sorguOlustur = ("""CREATE TABLE IF NOT EXISTS registers(Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                 \
 RegisterFunction TEXT NOT NULL,                      \
 RegisterNumber INTEGER NOT NULL)""")

curs.execute(sorguOlustur)
conn.commit()

# one time function
#for i in range(250):
#
#    a= f"Register{i}"
#
#    curs.execute("""INSERT INTO registers (RegisterFunction, RegisterNumber) VALUES (?, ?);""",(a, i))
#    
#    conn.commit()
#-------------------------------------#

class ModbusMainWindow(QMainWindow, Ui_MainWindow, QWidget):


    def __init__(self, parent=None):

        super().__init__(parent)

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.setMouseTracking(True)

        self.conn = sqlite3.connect('database.db')

        self.addRegisterNumberstoList()

        self.ui._tableWrite.setItem(0, 0,  QTableWidgetItem("falan"))   # set item in 0, 0 position

        self.ui._tableWrite.setHorizontalHeaderLabels(["Register Name", "Register Value"])

        self.ui._tableRead.setHorizontalHeaderLabels(["Register Name", "Register Value"])

        item1 = self.ui._lstWrite.item(0).text()

        
        #-------------- Signal Slot --------------

        self.ui._lstWrite.itemActivated.connect(self.addRegistertoWTableFunc)

        self.ui._lstRead.itemActivated.connect(self.addRegistertoRTableFunc)

        self.ui._tableWrite.itemChanged.connect(self.modbusWriteFunction)



        #self.ui._lstWrite.itemClicked.connect(self.dragAndDroptoTable) additional features

        #self.ui.actionNew_Registers.triggered.connect(self.newRegistersWidget)
        
    def addRegisterNumberstoList(self):
        
        curs = self.conn.cursor()

        curs.execute("SELECT RegisterFunction FROM registers")

        for row in curs.fetchall():

            self.ui._lstWrite.addItem(row[0])
            self.ui._lstRead.addItem(row[0])

    # This function provide us to drag and drop list item to table widget 
    def dragAndDroptoTable(self, item):

        pass

    
    def addRegistertoWTableFunc(self, item):

        row_1 = [item.text()]

        row = self.ui._tableWrite.rowCount()

        self.ui._tableWrite.setRowCount(row+1)

        col = 0

        for item in row_1:

            cell = QTableWidgetItem(str(item))
            self.ui._tableWrite.setItem(row, col, cell)
            col += 1

        
    def addRegistertoRTableFunc(self, item):

        row_1 = [item.text()]

        row = self.ui._tableRead.rowCount()

        self.ui._tableRead.setRowCount(row+1)

        col = 0

        for item in row_1:

            cell = QTableWidgetItem(str(item))
            self.ui._tableRead.setItem(row, col, cell)
            col += 1

        pass

    def modbusWriteFunction(self, item):

        ipAdress = self.ui._lneIp.text() # ip adresi

        print(item.text())


        #client = ModbusClient(host=ipAdress, port = 502)

        #client.write_multiple_registers(wrnumber, wvalues)
    

    # Drag and Drop helper function
    # def mouseMoveEvent(self, event):
        #print("Erhan2")
        #return [event.x(), event.y()]
        #print('Mouse coords: ( %d : %d )' % (event.x(), event.y()))


class RecordingRegisters(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()

        self.ui.setupUi(self)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setApplicationDisplayName("Modbus")

    mainPage = ModbusMainWindow()

    mainPage.show()

    sys.exit(app.exec_())