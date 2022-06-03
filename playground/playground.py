from pyModbusTCP.client import ModbusClient

client = ModbusClient(host="192.168.1.201", port = 502)

print(client.open())


