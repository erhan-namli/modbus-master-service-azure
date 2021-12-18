import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from mainpage import*

from pyModbusTCP.client import ModbusClient

#-------------Ana Fonskiyonumuz------------#
#------------------------------------------#

Uygulama = QApplication(sys.argv)
anaPencere = QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(anaPencere)
anaPencere.show()

#-------------Kullanıcı İşlemleri------------#
#--------------------------------------------#

def ReadFunction():

    ipAdress = ui.lne_ip.text()   # ip adresi

    rnumber1 = ui.lne_customreadnum1.text()

    rnumber2 = ui.lne_customreadnum1.text()

    client = ModbusClient(host=ipAdress, port = 502)

    client.open()

    temp = client.read_holding_registers(rnumber1, rnumber2)

    ui.lne_customreadvalue.setText(temp)
    

def WriteFunction():

    ipAdress = ui.lne_ip.text()   # ip adresi

    client = ModbusClient(host=ipAdress, port = 502)

    wrnumber = ui.lne_customwritenum.text()  

    wvalues = ui.lne_customwritevalue.text()

    client.write_multiple_registers(wrnumber, wvalues)


#-----------------Deneme---------------#
#--------------------------------------#




#-----------------Sinyal Slot---------------#
#-------------------------------------------#

ui.btn_read.clicked.connect(ReadFunction)
ui.btn_write.clicked.connect(WriteFunction)


sys.exit(Uygulama.exec_())

