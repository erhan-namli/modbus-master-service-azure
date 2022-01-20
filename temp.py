from pyModbusTCP.client import ModbusClient


client = ModbusClient(host="192.168.1.200", port = 502)

client.open()

print(client.read_holding_registers(1, 5))