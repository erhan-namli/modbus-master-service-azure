from typing import Text
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QApplication, QLabel, QWidget
import sys
from PyQt5.QtCore import  QObject, QThread, pyqtSignal # Threading Classes

import time

import sqlite3

from newMainPage import Ui_MainWindow

from pyModbusTCP.client import ModbusClient

import threading

import re

import sqlite3

import pandas as pd

from azure.iot.device import IoTHubDeviceClient, Message

from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtCore import Qt

CONNECTION_STRING = "HostName=modbus-tcp-iot.azure-devices.net;DeviceId=mypi;SharedAccessKey=04YUBQsaAofBwwO6uFYfx7J+noaBUWJ35JDNON0pYAE=" # Azure IoT Hub Device Key

clientAzure = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

conn = sqlite3.connect('databasev2.db')

curs = conn.cursor()

sorguOlustur = ("""CREATE TABLE IF NOT EXISTS registers(Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                 \
 RegisterFunction TEXT NOT NULL,                      \
 RegisterNumber INTEGER NOT NULL UNIQUE)""") # Register Number is must be unique value

curs.execute(sorguOlustur)
conn.commit()

class Worker(QtCore.QThread):

    any_signal = QtCore.pyqtSignal(int)

    def __init__(self,parent=None,  ipAdress=None, QTableWidget=None, clock=None):

        self.QTable = QTableWidget
        super(QtCore.QThread, self).__init__()
        self.ipAdress = ipAdress

        self.is_running = True
        self.clock = clock

    def message_handler(self, message):

        a = str(message)

        list = a.split(",")

        newlist = []

        for i in list:

            newlist.append(int(re.search(r'\d+', i).group()))
        
        print(newlist)

        client = ModbusClient(host=self.ipAdress, port = 502)

        client.open()

        client.write_multiple_registers(newlist[0], [newlist[1]])

    def run(self):

        dfRegNumbers = pd.read_csv("nope.csv")

        registers = dfRegNumbers['Registers']


        while True:

            clientAzure.on_message_received = self.message_handler  #When azure sends message to our client do that function

            tempDf = pd.DataFrame()

            client = ModbusClient(host=self.ipAdress, port = 502)

            client.open()

            data = []

            currentRow = 0

            print(currentRow)

            for i in registers:

                readedValuefromRegister = client.read_holding_registers(i, 1)

                self.QTable.item(currentRow, 2).setText(str(readedValuefromRegister))
                print(i)

                data.append((i, readedValuefromRegister))

                currentRow +=1

            message = Message(data)

            clientAzure.send_message(str(message))
            
            time.sleep(self.clock)
    
    def stop(self):

        self.is_running = False

        self.terminate()

class ModbusMainWindow(QMainWindow, Ui_MainWindow, QWidget):

    def __init__(self, parent=None):

        
        client = ModbusClient(host="192.168.1.200", port = 502)
        
        client.open()

        self.changedValue = None

        conn = sqlite3.connect('databasev2.db')

        curs = conn.cursor()

        super().__init__(parent)

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.ui._lneIp.setText("192.168.1.200")

        self.ui.table_Registers.setHorizontalHeaderLabels(["Register Name", "Register Function", "Register Value"])

        curs.execute("SELECT RegisterNumber, RegisterFunction FROM registers ORDER BY RegisterNumber")

        for row in curs.fetchall():

            self.ui.list_Registers.addItem("Register " + str(row[0]))

            ######## TEMP

        #----------- Signal - Slot ------------#

        

        self.ui.btn_Insert.clicked.connect(self.insertRegister)

        self.thread={}

        self.ui.list_Registers.itemActivated.connect(self.addRegisterstoTable)  # item activated = double click

        self.ui.btn_Delete.clicked.connect(self.deleteRegisterFromTable)

        self.ui.btn_Find.clicked.connect(self.querySingleElement)

        self.ui.btn_Recording.clicked.connect(self.runLongTask)

        self.ui.btn_AllRegisters.clicked.connect(self.addAllRegisters)

        self.ui.btn_ClearAll.clicked.connect(self.clearAllRows)

        self.ui.table_Registers.itemClicked.connect(self.getRegisterValue)

        self.ui.table_Registers.itemChanged.connect(self.changeRegisterValue)

        self.ui.btn_addiptolist.clicked.connect(self.addIpToIpList)

        self.ui.btn_StopCommunication.clicked.connect(self.stop_AllThreads)


    def addIpToIpList(self):

        sAllItems = [self.ui.cmb_deviceList.itemText(i) for i in range(self.ui.cmb_deviceList.count())]

        print(sAllItems)

        new = self.ui._lneIp.text()

        if new not in sAllItems:

            self.ui.cmb_deviceList.addItem(new)

            #self.ui.cmb_deviceList.setItemText(self.ui.cmb_deviceList.count()+1, _translate("MainWindow", new))


    def changeRegisterValue(self, item):

        value = item.text()

        if self.changedValue == None:

            pass
    
        else:

            client = ModbusClient(host=self.ui._lneIp.text(), port = 502)

            client.open()

            client.write_multiple_registers(self.changedValue, [int(value)])

        self.changedValue  = None

    def getRegisterValue(self):

        rows = {index.row() for index in self.ui.table_Registers.selectionModel().selectedIndexes()}
        output = []
        for row in rows:
            row_data = []
            for column in range(self.ui.table_Registers.model().columnCount()):
                index = self.ui.table_Registers.model().index(row, column)
                row_data.append(index.data())
            output.append(row_data)

        self.changedValue = int(re.search(r'\d+', output[0][0]).group())
        print(self.changedValue)


    def clearAllRows(self):

        self.stop_AllThreads()

        self.ui.table_Registers.setRowCount(0)

        self.ui.list_Registers.clear()

        curs.execute("SELECT RegisterNumber, RegisterFunction FROM registers ORDER BY RegisterNumber")

        for row in curs.fetchall():

            self.ui.list_Registers.addItem("Register " + str(row[0]))

        

    def addAllRegisters(self):

        def falan(x):
            
            return int(re.search(r'\d+', x).group())

        items = [self.ui.list_Registers.item(x).text() for x in range(self.ui.list_Registers.count())]

        tempItems = list(map(falan, items))

        print(tempItems)

        for i in tempItems:

            # SQL QUERY
            curs.execute("SELECT * FROM registers WHERE (RegisterNumber=?)",(i, )) # we need comma after the variable because it is what is 
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

                    readValuefromRegister = client.read_holding_registers(int(i), 1)

                    for item in [readValuefromRegister]:
                        cell = QTableWidgetItem(str(item))# makes the item to be QTableWidgetItem 
                        self.ui.table_Registers.setItem(row, col3, cell)# set item to declared row and col index
                    pass
                except:

                    pass
            
            pass

    def runLongTask(self):

        clock = float(self.ui.cmb_Clock.currentText()) # Azure Communication Clock
        
        data = []
        for i in range(self.ui.table_Registers.rowCount()):
            data.append(int(re.search(r'\d+', self.ui.table_Registers.item(i, 0).text()).group()))
            
        self.dfTempRegisters = pd.DataFrame()
        self.dfTempRegisters['Registers'] = data

        self.dfTempRegisters.to_csv("nope.csv")

        length = [self.ui.cmb_deviceList.itemText(i) for i in range(self.ui.cmb_deviceList.count())]

        for i in range(len(length)):

            self.thread[i] = Worker(parent=None, ipAdress=length[i], QTableWidget=self.ui.table_Registers, clock=clock)

            self.thread[i].start()

    def stop_AllThreads(self):

        length = [self.ui.cmb_deviceList.itemText(i) for i in range(self.ui.cmb_deviceList.count())]

        for i in range(len(length)):

            self.thread[i].stop()

            print("Durdu")

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
        
        item.setFlags(Qt.NoItemFlags)

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