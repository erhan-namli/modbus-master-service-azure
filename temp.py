import sys
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5 import QtCore
class YuTextFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self): 
        self.setWindowTitle('PyQT Table Add Row Data Dynamically')  
        vbox = QVBoxLayout()
        
        # add table 
        table = QTableWidget(self)
        table.setColumnCount(5)
        
        table.rowCount()
        #set table header
        table.setHorizontalHeaderLabels(['id','Name','Age','Sex','Address'])
    
        #add data
        row_1 = ['001', 'John', 30, 'Male', 'Street No 2']
        row_2 = ['002', 'Lily', 32, 'Female', 'Street No 1']
        row_3 = ['003', 'Kate', 20, 'Male', 'Street No 3']
        row_4 = ['004', 'Tom', 22, 'Male', 'Street No 4']
        
        vbox.addWidget(table)
        self.setLayout(vbox)
        self.setGeometry(300,400,500,400)
        self.show()
        self.addTableRow(table, row_1)
        self.addTableRow(table, row_2)
        self.addTableRow(table, row_3)
        self.addTableRow(table, row_4)

    def addTableRow(self, table, row_data):
        row = table.rowCount()
        table.setRowCount(row+1)
        col = 0
        for item in row_data:
            cell = QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = YuTextFrame()
    sys.exit(app.exec_())