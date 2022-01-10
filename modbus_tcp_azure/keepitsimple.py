# GETTING DATA FROM MICROSOFT AZURE CLOUD SERVICE

# 1- First thing you have to do is go Azure portal and open bash command line then write code .
# 2- Open a file thats extension must be .py
# 3- CONNECTION_STRING = "HostName=modbus-tcp-iot.azure-devices.net;SharedAccessKeyName=service;                        SharedAccessKey=5ZCPyIUC7prmgWfQueBajDqSGtMUe6YZvwiiwYovB3A="
#    DEVICE_ID = "mypi"
#    IoTHubRegistryManager(CONNECTION_STRING)
#    data ="5, 2"
#    registry_manager.send_c2d_message(DEVICE_ID, data)
# 4- then you must run your message handler code in local machine

# SENKRON

import threading
 
from azure.iot.device import IoTHubDeviceClient, Message

from pyModbusTCP.client import ModbusClient

import time
from azure.iot.device import IoTHubDeviceClient

import re

RECEIVED_MESSAGES = 0

CONNECTION_STRING = "HostName=modbus-tcp-iot.azure-devices.net;DeviceId=mypi;SharedAccessKey=04YUBQsaAofBwwO6uFYfx7J+noaBUWJ35JDNON0pYAE="

def message_handler(message):

    a = str(message)

    list = a.split(",")

    newlist = []

    for i in list:

        newlist.append(int(re.search(r'\d+', i).group()))
    
    print(newlist)

    client = ModbusClient(host="192.168.1.200", port = 502)

    client.open()

    client.write_multiple_registers(newlist[0], [newlist[1]])
  
def getDatafromAzure():
    print ("Starting the Python IoT Hub C2D Messaging device sample...")

    # Instantiate the client
    clientAzure = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    print ("Waiting for C2D messages, press Ctrl-C to exit")
    try:
        # Attach the handler to the client
        clientAzure.on_message_received = message_handler

        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        print("IoT Hub C2D Messaging device sample stopped")
    finally:
        # Graceful exit
        print("Shutting down IoT Hub Client")
        clientAzure.shutdown()

# SENDING DATA TO MICROSOFT AZURE CLOUD SERVICE

# 1- First thing you have to do is go Azure portal and open bash command line then write az iot hub monitor-events --hub-name modbus-tcp-iot --device-id mypi
# 2- this command starts monitoring your device

def sendDatatoAzure(registerNumber, distance):

    clientAzure = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    client = ModbusClient(host="192.168.1.200", port = 502)

    client.open()

    data = client.read_holding_registers(registerNumber, distance)

    message = Message(data)

    clientAzure.send_message(str(message))

if __name__ == '__main__':

    t1 = threading.Thread(target=sendDatatoAzure, daemon=True)
    t2 = threading.Thread(target=getDatafromAzure)
    t1.start()
    t2.start()