from PyQt5 import uic


with open("modbus.py", "w", encoding="utf-8") as fout:
    uic.compileUi(r'ui\modbus.ui', fout)