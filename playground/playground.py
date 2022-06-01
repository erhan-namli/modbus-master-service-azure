from pyModbusTCP.client import ModbusClient

client = ModbusClient(host="192", port = 502)

client.open()

