from PyQt5 import uic


with open("update.py", "w", encoding="utf-8") as fout:
    uic.compileUi('update.ui', fout)