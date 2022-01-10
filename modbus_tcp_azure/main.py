import time

import threading

import pandas as pd

from azure.iot.device import IoTHubDeviceClient, Message

from pyModbusTCP.client import ModbusClient

from PyQt5.QtCore import QObject, QThread, pyqtSignal # Threading Classes

class Worker(QObject):

    
    finished = pyqtSignal()
    progress = pyqtSignal(int)


    def __init__(self):

        CONNECTION_STRING = "HostName=modbus-tcp-iot.azure-devices.net;DeviceId=mypi;SharedAccessKey=04YUBQsaAofBwwO6uFYfx7J+noaBUWJ35JDNON0pYAE="

        self.clientAzure = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

        self.client = ModbusClient(host="192.168.1.200", port = 502)

        self.client.open()

    def run(self):
        for i in range(100):

            data = self.client.read_holding_registers(1, 1)

            message = Message(data)

            self.clientAzure.send_message(str(message))

            time.sleep(1)



def write():

    for i in range(10):
        print(i)
        time.sleep(1)
    

AB = Worker()
t1 = threading.Thread(target=AB.run, daemon=True)
t2 = threading.Thread(target=write)

t1.start()
t2.start()

# ipAdress = "192.168.1.200"

# clientModbus = ModbusClient(host=ipAdress, port = 502)

# clientModbus.open()

# registers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# #a = clientModbus.read_holding_registers(1, 9)

# #message = Message(a)

# #clientAzure.send_message(str(message))

# def read():
    

#     while True:
#         CONNECTION_STRING = "HostName=modbus-tcp-iot.azure-devices.net;DeviceId=mypi;SharedAccessKey=04YUBQsaAofBwwO6uFYfx7J+noaBUWJ35JDNON0pYAE="

#         clientAzure = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
#         output = []

#         for i in registers:

#            output.append((i, clientModbus.read_holding_registers(i, 1)))

#         message = Message(output)

#         clientAzure.send_message(str(message))

#         time.sleep(2)

#         output= []

        
# def write():

#     for i in range(20):
#         print("Ana Fonksiyon Çalışıyor")
#         i=i+1
#         time.sleep(2)

# #         registerNumber = input("Register Number : ")
# #         registerValue = input("Register Value : ")
# #         clientModbus.write_multiple_registers(int(registerNumber), [int(registerValue)])


# t1 = threading.Thread(target=read, daemon=True)
# t2 = threading.Thread(target=write)

# t1.start()
# t2.start()