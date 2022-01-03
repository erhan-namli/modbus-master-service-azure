from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QApplication, QLabel, QWidget
import sys

import sqlite3

from newMainPage import Ui_MainWindow

from pyModbusTCP.client import ModbusClient

import re

import sqlite3

conn = sqlite3.connect('databasev2.db')

curs = conn.cursor()

sorguOlustur = ("""CREATE TABLE IF NOT EXISTS registers(Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                 \
 RegisterFunction TEXT NOT NULL,                      \
 RegisterNumber INTEGER NOT NULL UNIQUE)""") # Register Number is must be unique value

curs.execute(sorguOlustur)
conn.commit()

class ModbusMainWindow(QMainWindow, Ui_MainWindow, QWidget):

    def __init__(self, parent=None):

        conn = sqlite3.connect('databasev2.db')

        curs = conn.cursor()

        super().__init__(parent)

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.ui.table_Registers.setHorizontalHeaderLabels(["Register Name", "Register Function", "Register Value"])

        for row in curs.fetchall():

            self.ui.list_Registers.addItem("Register " + str(row[0]))

        #----------- Signal - Slot ------------#

        self.ui.btn_Insert.clicked.connect(self.insertRegister)

    def insertRegister(self):

        registerFunction = self.ui.cmb_Funct.currentText()

        registerNumber = self.ui.lne_Number.text()


        if(registerNumber==""):
            pass
        else:

            curs.execute("""INSERT OR REPLACE INTO registers (RegisterFunction, RegisterNumber) VALUES (?, ?);""", (registerFunction, registerNumber))
            conn.commit()

            curs.execute("SELECT RegisterNumber FROM registers")

        for row in curs.fetchall():

            

            self.ui.list_Registers.addItem("Register " + str(row[0]))
        
        registerNumber = self.ui.lne_Number.clear()
           

        

if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setApplicationDisplayName("Modbus")

    mainPage = ModbusMainWindow()

    mainPage.show()

    sys.exit(app.exec_())