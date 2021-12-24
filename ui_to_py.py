from PyQt5 import uic


with open("registerRecording.py", "w", encoding="utf-8") as fout:
    uic.compileUi('registerRecording.ui', fout)