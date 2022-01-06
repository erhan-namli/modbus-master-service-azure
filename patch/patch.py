from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QApplication, QLabel, QWidget
import sys
from PyQt5.QtCore import QObject, QThread, pyqtSignal # Threading Classes

import time

import sqlite3

from newMainPage import Ui_MainWindow

from pyModbusTCP.client import ModbusClient

import re

import sqlite3

import pandas as pd

from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=modbus-tcp-iot.azure-devices.net;DeviceId=mypi;SharedAccessKey=04YUBQsaAofBwwO6uFYfx7J+noaBUWJ35JDNON0pYAE="

clientAzure = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

conn = sqlite3.connect('databasev2.db')

curs = conn.cursor()

sorguOlustur = ("""CREATE TABLE IF NOT EXISTS registers(Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                 \
 RegisterFunction TEXT NOT NULL,                      \
 RegisterNumber INTEGER NOT NULL UNIQUE)""") # Register Number is must be unique value

curs.execute(sorguOlustur)
conn.commit()

class Worker(QObject):

    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def message_handler(self, message):

        a = str(message)

        list = a.split(",")

        newlist = []

        for i in list:

            newlist.append(int(re.search(r'\d+', i).group()))
        
        print(newlist)

        client = ModbusClient(host="192.168.1.200", port = 502)

        client.open()

        client.write_multiple_registers(newlist[0], [newlist[1]])

    def run(self):

        dfRegNumbers = pd.read_csv("nope.csv")

        registers = dfRegNumbers['Registers']


        for i in range(1000):

            clientAzure.on_message_received = self.message_handler

            tempDf = pd.DataFrame()

            client = ModbusClient(host="192.168.1.200", port = 502)

            client.open()

            data = []

            for i in registers:

                readedValuefromRegister = client.read_holding_registers(i, 1)

                data.append((i, readedValuefromRegister))

            message = Message(data)

            clientAzure.send_message(str(message))
            
            time.sleep(3)


        for i in range(100):

            time.sleep(1)

            print(i)

            self.progress.emit(i + 1)
        
        self.finished.emit()

class ModbusMainWindow(QMainWindow, Ui_MainWindow, QWidget):

    def __init__(self, parent=None):

        conn = sqlite3.connect('databasev2.db')

        

        curs = conn.cursor()

        super().__init__(parent)

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        


        self.ui.table_Registers.setHorizontalHeaderLabels(["Register Name", "Register Function", "Register Value"])

        curs.execute("SELECT RegisterNumber FROM registers")

        for row in curs.fetchall():

            self.ui.list_Registers.addItem("Register " + str(row[0]))

        #----------- Signal - Slot ------------#

        self.ui.btn_Insert.clicked.connect(self.insertRegister)

        self.ui.list_Registers.itemActivated.connect(self.addRegisterstoTable)  # item activated = double click

        self.ui.btn_Delete.clicked.connect(self.deleteRegisterFromTable)

        self.ui.btn_Find.clicked.connect(self.querySingleElement)

        self.ui.btn_Recording.clicked.connect(self.runLongTask)

        self.ui.table_Registers.itemChanged.connect(self.writeRegister)


    def writeRegister(self):

        pass

    def runLongTask(self):

        self.dfTempRegisters = pd.DataFrame()
        
        data = []
        for i in range(self.ui.table_Registers.rowCount()):
            data.append(int(re.search(r'\d+', self.ui.table_Registers.item(i, 0).text()).group()))
            #data.append(self.ui.table_Registers.item(i, 0).text())
        print(data)

        self.dfTempRegisters['Registers'] = data

        self.dfTempRegisters.to_csv("nope.csv")

        #int(re.search(r'\d+', self.ui.table_Registers.item(i, 0).text()).group())

        self.thread = QThread()

        self.worker = Worker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.thread.quit)

        self.worker.finished.connect(self.worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def runWriteLongTask(self):
        
        data = []
        for i in range(self.ui.table_Registers.rowCount()):
            data.append(int(re.search(r'\d+', self.ui.table_Registers.item(i, 0).text()).group()))
            #data.append(self.ui.table_Registers.item(i, 0).text())
        print(data)

        self.dfTempRegisters['Registers'] = data

        self.dfTempRegisters.to_csv("nope.csv")

        #int(re.search(r'\d+', self.ui.table_Registers.item(i, 0).text()).group())

        self.thread = QThread()

        self.worker = Worker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.thread.quit)

        self.worker.finished.connect(self.worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()


    def querySingleElement(self):
        
        registerNumb = self.ui.lne_registerNumberAdd.text()

        # SQL QUERY
        curs.execute("SELECT * FROM registers WHERE (RegisterNumber=?)",(registerNumb, )) # we need comma after the variable because it is what is 
        conn.commit()

        ####### Adding Registers To Table Function #######

        ipAdress = self.ui._lneIp.text() # ip adresi

        for satirIndeks, satirVeri in enumerate(curs):
            row = self.ui.table_Registers.rowCount() #  gets table row count

            self.ui.table_Registers.setRowCount(row+1) #  increment the row count

            col3 = 2

            col2 = 1

            col=0


            row_1 = [satirVeri[2]]
            row_2 = [satirVeri[1]]

            # Register Name Column
            for item in row_1:

                cell = QTableWidgetItem("Register " + str(item))# makes the item to be QTableWidgetItem 
                self.ui.table_Registers.setItem(row, col, cell)# set item to declared row and col index
            
            # Register Function Column
            for item in row_2:

                cell = QTableWidgetItem(str(item))# makes the item to be QTableWidgetItem 
                self.ui.table_Registers.setItem(row, col2, cell)# set item to declared row and col index

            # Register Value Column ( modbus tcp/ip )

            try:
                client = ModbusClient(host=ipAdress, port = 502)

                client.open()

                readValuefromRegister = client.read_holding_registers(int(registerNumb), 1)

                for item in [readValuefromRegister]:
                    cell = QTableWidgetItem(str(item))# makes the item to be QTableWidgetItem 
                    self.ui.table_Registers.setItem(row, col3, cell)# set item to declared row and col index
                pass
            except:

                pass
        
        pass

    def deleteRegisterFromTable(self, item):

        #self.ui.table_Registers.removeRow()

        pass

    def insertRegister(self):

        registerFunction = self.ui.cmb_Funct.currentText()

        registerNumber = self.ui.lne_Number.text()


        if(registerNumber==""):
            pass
        else:
            
            curs.execute("""INSERT OR REPLACE INTO registers (RegisterFunction, RegisterNumber) VALUES (?, ?);""", (registerFunction, registerNumber))
            conn.commit()

            #curs.execute("SELECT RegisterNumber FROM registers")

        for row in curs.fetchall():

            self.ui.list_Registers.addItem("Register" + str(row[0]))
        
        registerNumber = self.ui.lne_Number.clear()

    def addRegisterstoTable(self, item):

        # Select unique row which has belongs to taken register number and set the first 2 column with sql query, then the 3th column has to be readed value

        

        ipAdress = self.ui._lneIp.text() # ip adresi

        register = item.text()

        onlyNumber = int(re.search(r'\d+', register).group()) # get only number from string

        # SQL QUERY
        curs.execute("SELECT * FROM registers WHERE (RegisterNumber=?)",(onlyNumber, )) # we need comma after the variable because it is what is 
        
        conn.commit()

        ####### Adding Registers To Table Function #######

        for satirIndeks, satirVeri in enumerate(curs):
            row = self.ui.table_Registers.rowCount() #  gets table row count

            self.ui.table_Registers.setRowCount(row+1) #  increment the row count

            col3 = 2

            col2 = 1

            col=0
       

            row_1 = [satirVeri[2]]
            row_2 = [satirVeri[1]]

            # Register Name Column
            for item in row_1:

                cell = QTableWidgetItem("Register " + str(item))# makes the item to be QTableWidgetItem 
                self.ui.table_Registers.setItem(row, col, cell)# set item to declared row and col index
            
            # Register Function Column
            for item in row_2:

                cell = QTableWidgetItem(str(item))# makes the item to be QTableWidgetItem 
                self.ui.table_Registers.setItem(row, col2, cell)# set item to declared row and col index

            # Register Value Column ( modbus tcp/ip )

            try:
                client = ModbusClient(host=ipAdress, port = 502)

                client.open()

                readValuefromRegister = client.read_holding_registers(onlyNumber, 1)

                for item in [readValuefromRegister]:
                    cell = QTableWidgetItem(str(item))# makes the item to be QTableWidgetItem 
                    self.ui.table_Registers.setItem(row, col3, cell)# set item to declared row and col index
                pass
            except:

                pass
    
    def registerWriteCode(self):
        
        
        
        pass
            


if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setApplicationDisplayName("Modbus")

    mainPage = ModbusMainWindow()

    mainPage.show()

    sys.exit(app.exec_())