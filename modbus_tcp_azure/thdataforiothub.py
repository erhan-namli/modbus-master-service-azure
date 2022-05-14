from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = ""

TEMPERATURE = 20

HUMIDITY = 10

MSG_TXT = '{{"Register Id": {temperature}, "Register Value": {humidity}}}'

def iothub_client_init():

    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:

        while True:
            pass
        pass
    
    except:
        pass

if __name__ == "__main__":

    iothub_client_telemetry_sample_run()

