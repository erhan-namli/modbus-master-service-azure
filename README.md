# Modbus TCP/IP - IoT - GUI
  
 
 ## Libraries
 - GUI library : https://pypi.org/project/PyQt5/
 - Database : https://www.sqlite.org/index.html
 - Modbus Protocol Library : https://pypi.org/project/pymodbus/
 - Azure Communication Library : https://github.com/Azure/azure-sdk-for-python

 ## Azure Communication
 
 - Send data to Azure IoT hub from device : https://docs.microsoft.com/en-us/azure/iot-develop/quickstart-send-telemetry-iot-hub?pivots=programming-language-python
 - Send cloud-to-device messages with IoT Hub : https://docs.microsoft.com/en-gb/azure/iot-hub/iot-hub-python-python-c2d
 
 ### Code Examples
 ```python
 # SENDING DATA TO MICROSOFT AZURE CLOUD SERVICE

# 1- First thing you have to do is go Azure portal and open bash command line then write az iot hub monitor-events --hub-name modbus-tcp-iot --device-id mypi
# 2- this command starts monitoring for your device

def sendDatatoAzure(registerNumber, distance):

    clientAzure = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    client = ModbusClient(host="192.168.1.200", port = 502)

    client.open()

    data = client.read_holding_registers(registerNumber, distance)

    message = Message(data)

    clientAzure.send_message(str(message))
    
if __name__ == '__main__':

    sendDatatoAzure()
    #getDatafromAzure()
 ```
 ## Work Principle
