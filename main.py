# TO - DO
# - Write a function to do when clicked on item take the value of that and store, then after write a function which makes taking # changed value

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QApplication, QLabel, QWidget
import sys

from registerRecording import *
from newregisters import *

from modbus import Ui_MainWindow

from pyModbusTCP.client import ModbusClient

import re

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

        # Variables
        self.writeModbus = None  # Register Value

        self.writeRModbus = None # Register Number

        self.readModbus = None # Register Number

        super().__init__(parent)

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.setMouseTracking(True)

        self.conn = sqlite3.connect('database.db')

        self.addRegisterNumberstoList()

        #self.ui._tableWrite.setItem(0, 0,  QTableWidgetItem("falan"))   # set item in 0, 0 position

        self.ui._tableWrite.setHorizontalHeaderLabels(["Register Name", "Register Value"])

        self.ui._tableRead.setHorizontalHeaderLabels(["Register Name", "Register Value"])

        item1 = self.ui._lstWrite.item(0).text()
        
        #-------------- Signal Slot --------------

        self.ui._lstWrite.itemActivated.connect(self.addRegistertoWTableFunc)

        self.ui._lstRead.itemActivated.connect(self.addRegistertoRTableFunc)

        self.ui._tableWrite.itemChanged.connect(self.modbusWriteFunction)

        #self.ui._lstWrite.itemClicked.connect(self.dragAndDroptoTable) additional features

        #self.ui.actionNew_Registers.triggered.connect(self.newRegistersWidget)
         
        self.ui._tableWrite.itemActivated.connect(self.storeData)  # past value

        self.ui._tableWrite.itemClicked.connect(self.storeData) # new value

    def storeData(self, item):
        
        # Storing the clicked data

        self.writeRModbus = item.text()

    def addRegisterNumberstoList(self): # This function does fill the list widgets with registers
        
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

        row = self.ui._tableWrite.rowCount()  #  gets table row count

        column = self.ui._tableWrite.columnCount()

        self.ui._tableWrite.setRowCount(row+1) #  increment the row count

        col = 0

        col2 = 1

        for item in row_1:  # First columns item

            cell = QTableWidgetItem(str(item))   # makes the item to be QTableWidgetItem
        
            self.ui._tableWrite.setItem(row, col, cell)  # set item to declared row and col index

        for item in row_1:   # Second columns item

            cell = QTableWidgetItem(str(item))   # makes the item to be QTableWidgetItem
        
            self.ui._tableWrite.setItem(row, col2, cell)  # set item to declared row and col index

    def addRegistertoRTableFunc(self, item):

        ipAdress = self.ui._lneIp.text() # ip adresi

        row_1 = [item.text()]

        row = self.ui._tableRead.rowCount() #  gets table row count

        self.ui._tableRead.setRowCount(row+1) #  increment the row count

        col=0

        col2 = 1

        temp = item.text()

        tempP = int(re.search(r'\d+', temp).group())

        client = ModbusClient(host=ipAdress, port = 502)

        client.open()

        readValuefromRegister = client.read_holding_registers(tempP, 1)   # column2 value must be this, change when you are doing simulation

        for item in row_1:

            cell = QTableWidgetItem(str(item))# makes the item to be QTableWidgetItem 
            self.ui._tableRead.setItem(row, col, cell)# set item to declared row and col index

        for item in row_1:

            cell = QTableWidgetItem(str(readValuefromRegister))# makes the item to be QTableWidgetItem 
            self.ui._tableRead.setItem(row, col2, cell)# set item to declared row and col index

    def modbusWriteFunction(self, item):

        ipAdress = self.ui._lneIp.text() # ip adresi
        try:
            wrnumber = int(re.search(r'\d+', self.writeRModbus).group())

            temp = item.text()

            tempP = int(re.search(r'\d+', temp).group())

            wvalues = [tempP]  # must be array type because write_multiple_registers function takes this paramater as an array

            client = ModbusClient(host=ipAdress, port = 502)

            client.open()

            client.write_multiple_registers(wrnumber, wvalues)
            self.writeRModbus = None # discharge past values
        except:
            pass
    
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