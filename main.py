from typing import Text
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QApplication, QLabel, QWidget, QComboBox
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

import json

CONNECTION_STRING = "HostName=modbus-web-iot-hub.azure-devices.net;DeviceId=myPi;SharedAccessKey=IhFblyQplDKxIxt97iUHLBKr/vfq/HtIkaPSGjV+bqg=" # Azure IoT Hub Device Key

clientAzure = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

class Worker(QtCore.QThread):

    any_signal = QtCore.pyqtSignal(int)

    def __init__(self,parent=None, ipAdress=None, QTableWidget=None, QComboBox=None, DeviceID = None, clock=None):

        self.QTable = QTableWidget
        self.QCombo = QComboBox
        super(QtCore.QThread, self).__init__()
        self.ipAdress = ipAdress
        self.DeviceID = DeviceID
        self.is_running = True
        self.clock = clock

    def message_handler(self, message):

        a = str(message)

        list = a.split(",")

        newlist = []

        for i in list:

            newlist.append(int(re.search(r'\d+', i).group()))
        
        print(newlist)

        client = ModbusClient(host=self.ipAdress, unit_id=self.DeviceID, port = 502)

        client.open()

        client.write_multiple_registers(newlist[0], [newlist[1]])

    def run(self):

        dfRegNumbers = pd.read_csv("nope.csv")

        registersComesFromTable = dfRegNumbers['Registers']

        while True:

            clientAzure.on_message_received = self.message_handler  #When azure sends message to our client do that function

            tempDf = pd.DataFrame()

            client = ModbusClient(host=self.ipAdress, unit_id=self.DeviceID, port = 502)

            client.open()

            messageList = []

            currentRow = 0

            azureRegisterValueList = []

            azureRegisterIdList = registersComesFromTable

            for register in registersComesFromTable:

                readedValuefromRegister = client.read_holding_registers(register, 1)

                #azureRegisterValueList.append(readedValuefromRegister)

                if self.QCombo.currentText() == self.ipAdress:
                    self.QTable.item(currentRow, 2).setText(str(readedValuefromRegister))

                registerFunction = str(self.QTable.item(currentRow, 3).text())

                INDIVIDUAL_REGISTER = {"IpAdress": self.ipAdress, "RegisterId": register, "RegisterValue": readedValuefromRegister, "RegisterFunction" : registerFunction}

                messageList.append(INDIVIDUAL_REGISTER)

                currentRow +=1

            #azureRegisterIdList = ",".join([str(elem) for elem in azureRegisterIdList])

            #AZURE_MESSAGE_PURE = {"IpAdress": self.ipAdress, "RegisterIdList": azureRegisterIdList, "RegisterValueList" : str(azureRegisterValueList)}

            #AZURE_MESSAGE = Message(json.dumps(AZURE_MESSAGE_PURE))

            #print(AZURE_MESSAGE)

            #clientAzure.send_message(str(AZURE_MESSAGE))

            message = Message(json.dumps(messageList))

            clientAzure.send_message(str(message))
            
            time.sleep(self.clock)
    
    def stop(self):

        self.is_running = False

        self.terminate()

class ModbusMainWindow(QMainWindow, Ui_MainWindow, QWidget):

    def __init__(self, parent=None):

        
        client = ModbusClient(host="192.168.1.200", unit_id=1, port = 502)
        
        client.open()

        self.changedValue = None

        self.conn = sqlite3.connect('test_database.db')

        self.curs = self.conn.cursor()

        super().__init__(parent)

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.ui._lneIp.setText("192.168.1.200")

        self.addAllRegisters()

        self.ui.table_Registers.setHorizontalHeaderLabels(["Parameter No", "Description", "Register Value", " Register Function", "Register Id"])

        self.curs.execute("""SELECT ParameterNo, Description, RegisterValue, RegisterFunction, RegisterId FROM deviceRegisters ORDER BY RegisterId""")

        for row in self.curs.fetchall():

            self.ui.list_Registers.addItem("Register " + str(row[4]))

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

        self.ui.btn_ClearDevices.clicked.connect(self.clearDevices)

    def addIpToIpList(self):

        sAllItems = [self.ui.cmb_deviceList.itemText(i) for i in range(self.ui.cmb_deviceList.count())]

        print(sAllItems)

        new = self.ui._lneIp.text()

        if new not in sAllItems:

            self.ui.cmb_deviceList.addItem(new)

            #self.ui.cmb_deviceList.setItemText(self.ui.cmb_deviceList.count()+1, _translate("MainWindow", new))

    def changeRegisterValue(self, item):

        deviceID = int(self.ui.lne_IDNumber.text())

        value = item.text()

        if self.changedValue == None:
            pass
    
        else:
            client = ModbusClient(host=self.ui.cmb_deviceList.currentText(), unit_id=deviceID, port = 502)

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

        if len(self.thread)>0:

            self.stop_AllThreads()

        self.ui.table_Registers.setRowCount(0)

        self.ui.list_Registers.clear()

        self.curs.execute("""SELECT ParameterNo, Description, RegisterValue, RegisterFunction, RegisterId FROM deviceRegisters ORDER BY RegisterId""")

        for row in self.curs.fetchall():

            self.ui.list_Registers.addItem("Register" + str(row[4]))

    def addAllRegisters(self):

        ipAdress = self.ui.cmb_deviceList.currentText()

        client = ModbusClient(host=ipAdress, port = 502)

        client.open()

        def parseRegisterNumber(x):
            
            return int(re.search(r'\d+', x).group())

        items = [self.ui.list_Registers.item(x).text() for x in range(self.ui.list_Registers.count())]

        ItemList = list(map(parseRegisterNumber, items))

        print(ItemList)

        for i in ItemList:

            # SQL QUERY
            self.curs.execute("SELECT * FROM deviceRegisters WHERE (RegisterId=?)",(i, )) # we need comma after the variable because it is what is 
            self.conn.commit()

            ####### Adding Registers To Table Function #######

            for satirIndeks, satirVeri in enumerate(self.curs):
                row = self.ui.table_Registers.rowCount() #  gets table row count

                self.ui.table_Registers.setRowCount(row+1) #  increment the row count
                

                col1, col2, col3, col4, col5 = 0, 1, 2, 3, 4


                row_1, row_2, row_3, row_4 = [satirVeri[0]], [satirVeri[1]], [satirVeri[3]], [satirVeri[4]]


                # Register Name Column
                for item in row_1:

                    cell = QTableWidgetItem(str(item))# makes the item to be QTableWidgetItem 
                    self.ui.table_Registers.setItem(row, col1, cell)# set item to declared row and col index
                
                # Register Function Column
                for item in row_2:

                    cell = QTableWidgetItem(str(item))# makes the item to be QTableWidgetItem 
                    self.ui.table_Registers.setItem(row, col2, cell)# set item to declared row and col index

                for item in row_3:

                    cell = QTableWidgetItem(str(item))# makes the item to be QTableWidgetItem 
                    self.ui.table_Registers.setItem(row, col4, cell)# set item to declared row and col index

                for item in row_4:

                    cell = QTableWidgetItem(str(item))
                    self.ui.table_Registers.setItem(row, col5, cell)
                    

                # Register Value Column ( modbus tcp/ip )

                try:

                    readValuefromRegister = client.read_holding_registers(int(row_4[0]), 1)
                    
                    for item in [readValuefromRegister]:
                        cell = QTableWidgetItem(str(item))# makes the item to be QTableWidgetItem 
                        self.ui.table_Registers.setItem(row, col3, cell)# set item to declared row and col index
                    pass
                except Exception as e:
                    print("HATA CIKTI", e.__class__, "s")
                    print(e.args)
                    print(e.__cause__)
                    pass
            pass

    def runLongTask(self):

        clock = float(self.ui.cmb_Clock.currentText()) # Azure Communication Clock
        
        data = []
        for i in range(self.ui.table_Registers.rowCount()):
            data.append(int(re.search(r'\d+', self.ui.table_Registers.item(i, 4).text()).group()))
            
        self.dfTempRegisters = pd.DataFrame()
        self.dfTempRegisters['Registers'] = data

        self.dfTempRegisters.to_csv("nope.csv")

        length = [self.ui.cmb_deviceList.itemText(i) for i in range(self.ui.cmb_deviceList.count())]

        for i in range(len(length)):

            self.thread[i] = Worker(parent=None, ipAdress=length[i], QTableWidget=self.ui.table_Registers, QComboBox=self.ui.cmb_deviceList, DeviceID=int(self.ui.lne_IDNumber.text()), clock=clock)

            self.thread[i].start()

    def stop_AllThreads(self):

        length = [self.ui.cmb_deviceList.itemText(i) for i in range(self.ui.cmb_deviceList.count())]

        for i in range(len(length)):

            self.thread[i].stop()

            print("Durdu")

    def querySingleElement(self):
        
        registerNumb = self.ui.lne_registerNumberAdd.text()

        # SQL QUERY
        self.curs.execute("SELECT * FROM registers WHERE (RegisterNumber=?)",(registerNumb, )) # we need comma after the variable because it is what is 
        self.conn.commit()

        ####### Adding Registers To Table Function #######

        #ipAdress = self.ui._lneIp.text() # ip adresi

        ipAdress = self.cmb_deviceList.currentText()

        for satirIndeks, satirVeri in enumerate(self.curs):
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
                client = ModbusClient(host=ipAdress,unit_id=int(self.lne_IDNumber.text()), port = 502)

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
            
            self.curs.execute("""INSERT OR REPLACE INTO registers (RegisterFunction, RegisterNumber) VALUES (?, ?);""", (registerFunction, registerNumber))
            self.conn.commit()

            #curs.execute("SELECT RegisterNumber FROM registers")

            self.curs.execute("SELECT RegisterNumber, RegisterFunction FROM registers ORDER BY RegisterNumber")
            self.conn.commit()
            self.ui.list_Registers.clear()
            for row in self.curs.fetchall():
                
                self.ui.list_Registers.addItem("Register" + str(row[0]))
        
        registerNumber = self.ui.lne_Number.clear()

    def addRegisterstoTable(self, item):

        # Select unique row which has belongs to taken register number and set the first 2 column with sql query, then the 3th column has to be readed value

        #ipAdress = self.ui._lneIp.text() # ip adresi

        ipAdress = self.ui.cmb_deviceList.currentText()

        register = item.text()
        
        item.setFlags(Qt.NoItemFlags)

        onlyNumber = int(re.search(r'\d+', register).group()) # get only number from string

        # SQL QUERY
        self.curs.execute("SELECT * FROM deviceRegisters WHERE (RegisterId=?)",(onlyNumber, )) # we need comma after the variable because it is what is 
        
        self.conn.commit()

        ####### Adding Registers To Table Function #######

        for satirIndeks, satirVeri in enumerate(self.curs):
            row = self.ui.table_Registers.rowCount() #  gets table row count

            self.ui.table_Registers.setRowCount(row+1) #  increment the row count
            

            col1, col2, col3, col4, col5 = 0, 1, 2, 3, 4


            row_1, row_2, row_3, row_4 = [satirVeri[0]], [satirVeri[1]], [satirVeri[3]], [satirVeri[4]]


            # Register Name Column
            for item in row_1:

                cell = QTableWidgetItem(str(item))# makes the item to be QTableWidgetItem 
                self.ui.table_Registers.setItem(row, col1, cell)# set item to declared row and col index
            
            # Register Function Column
            for item in row_2:

                cell = QTableWidgetItem(str(item))# makes the item to be QTableWidgetItem 
                self.ui.table_Registers.setItem(row, col2, cell)# set item to declared row and col index

            for item in row_3:

                cell = QTableWidgetItem(str(item))# makes the item to be QTableWidgetItem 
                self.ui.table_Registers.setItem(row, col4, cell)# set item to declared row and col index

            for item in row_4:

                cell = QTableWidgetItem(str(item))
                self.ui.table_Registers.setItem(row, col5, cell)
                

            # Register Value Column ( modbus tcp/ip )

            try:
                client = ModbusClient(host=ipAdress,unit_id=int(self.ui.lne_IDNumber.text()), port = 502)

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

    
    def clearDevices(self):

        self.ui.cmb_deviceList.clear()
            
if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setApplicationDisplayName("Modbus")

    mainPage = ModbusMainWindow()

    mainPage.show()

    sys.exit(app.exec_())
