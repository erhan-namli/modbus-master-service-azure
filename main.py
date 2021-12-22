from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
import sys


from modbus import Ui_MainWindow


#-------------- Database --------------#
import sqlite3
conn = sqlite3.connect('database.db')
curs = conn.cursor()

sorguOlustur = ("""CREATE TABLE IF NOT EXISTS registers(Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                 \
 RegisterFunction TEXT NOT NULL,                      \
 RegisterNumber INTEGER NOT NULL)""")

curs.execute(sorguOlustur)
conn.commit()


#   one time function
#for i in range(250):
#
#    a= f"Register{i}"
#
#    curs.execute("""INSERT INTO registers (RegisterFunction, RegisterNumber) VALUES (?, ?);""",(a, i))
#    
#    conn.commit()
#-------------------------------------#

class Modbus(QMainWindow, Ui_MainWindow):


    def __init__(self, parent=None):

        super().__init__(parent)

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.conn = sqlite3.connect('database.db')

        self.addRegisterNumberstoList()

        self.ui._tableWrite.setItem(0, 0,  QTableWidgetItem("text1"))


    def addRegisterNumberstoList(self):
        
        curs = self.conn.cursor()

        curs.execute("SELECT RegisterFunction FROM registers")

        for row in curs.fetchall():

            self.ui._lstWrite.addItem(row[0])
            self.ui._lstRead.addItem(row[0])


if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setApplicationDisplayName("Modbus")

    mainPage = Modbus()

    mainPage.show()

    sys.exit(app.exec_())

