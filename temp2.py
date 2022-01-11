
from pyModbusTCP.client import ModbusClient

ip = "192.168.1.200"

client = ModbusClient(host=ip, port = 502)

client.open()

client.write_multiple_registers(4, [3])