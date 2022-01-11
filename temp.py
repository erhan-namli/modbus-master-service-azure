from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QApplication, QLabel, QWidget, QTableView, QHBoxLayout

class Model(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.items = ['Row0_Column0','Row0_Column1','Row0_Column2']

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def rowCount(self, parent):
        return 1      
    def columnCount(self, parent):
        return len(self.items)  

    def data(self, index, role):
        if not index.isValid(): return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()

        column=index.column()
        if column<len(self.items):
            return QVariant(self.items[column])
        else:
            return QVariant()

class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        tablemodel=Model(self)               

        self.tableview=QTableView() 
        self.tableview.setModel(tablemodel)
        self.tableview.clicked.connect(self.viewClicked)

        self.tableview.setSelectionBehavior(QTableView.SelectRows)

        layout = QHBoxLayout(self)
        layout.addWidget(self.tableview)

        self.setLayout(layout)

    def viewClicked(self, clickedIndex):
        row=clickedIndex.row()
        model=clickedIndex.model()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())