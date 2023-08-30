import sys
from tela import Window
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()