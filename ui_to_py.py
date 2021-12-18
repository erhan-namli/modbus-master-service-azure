from PyQt5 import uic


with open("mainpage.py", "w", encoding="utf-8") as fout:
    uic.compileUi('mainpage.ui', fout)