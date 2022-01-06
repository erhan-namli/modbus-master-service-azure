from PyQt5 import uic


with open("newMainPage.py", "w", encoding="utf-8") as fout:
    uic.compileUi(r'ui\new.ui', fout)