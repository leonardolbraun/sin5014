import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QFileDialog, QLineEdit, QGraphicsView, QGraphicsScene, QHBoxLayout, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QIntValidator
from PIL import Image, ImageQt
import io
import matplotlib.pyplot as plt
from exercicio_1 import gerarHistograma, clarearImagem, escurecerImagem, plotarHistograma

class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.imagem = None

        self.setWindowTitle('Image Processor')
        self.setGeometry(200, 200, 1300, 600)

        main_layout = QHBoxLayout()

       

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()