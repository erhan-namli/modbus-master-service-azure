import sys       
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt

class AppDemo(QListWidget):
    def __init__(self):
        super().__init__()
        self.resize(1200, 800)
        self.setStyleSheet('font-size: 40px')

        items = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
        toDisable = [True, True, False, False]

        for item, disable in zip(items, toDisable):
            lstItem = QListWidgetItem(item)

            if disable:
                lstItem.setFlags(Qt.NoItemFlags)
            self.addItem(lstItem)
        
        self.itemPressed.connect(self.getItem)
        # self.itemClicked.connect(self.getItem)

    def getItem(self, itm):
        print(itm.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()
    
    sys.exit(app.exec_())