from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=modbus-tcp-iot.azure-devices.net;DeviceId=mypi;SharedAccessKey=04YUBQsaAofBwwO6uFYfx7J+noaBUWJ35JDNON0pYAE=" # Azure IoT Hub Device Key

clientAzure = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

def message_handler(message) :

    print(message)


while True:

    clientAzure.on_message_received = message_handler

