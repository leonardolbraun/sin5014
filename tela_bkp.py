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

        # Label para exibir a imagem
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(800, 600)  # Definindo um tamanho mínimo para visualização
        main_layout.addWidget(self.image_label)

        # Coluna à direita
        right_layout = QVBoxLayout()

        # QGroupBox para carregamento
        load_groupbox = QGroupBox("Load Image")
        load_layout = QVBoxLayout()

        # Botão para carregar imagem
        self.load_btn = QPushButton("Load Image")
        self.load_btn.clicked.connect(self.load_image)
        load_layout.addWidget(self.load_btn)

        load_groupbox.setLayout(load_layout)
        right_layout.addWidget(load_groupbox)

         # QGroupBox para analise
        analyse_groupbox = QGroupBox("Image Analysis")
        analyse_layout = QVBoxLayout()

        # Botão para mostrar histograma
        self.histogram_btn = QPushButton("Show Histogram")
        self.histogram_btn.clicked.connect(self.show_histogram_window)
        analyse_layout.addWidget(self.histogram_btn)

        self.load_image_label = QLabel("Formato da imagem:", self)
        analyse_layout.addWidget(self.load_image_label)

        self.load_image_label = QLabel("Tamanho da imagem:", self)
        analyse_layout.addWidget(self.load_image_label)

        self.load_image_label = QLabel("Modo da imagem:", self)
        analyse_layout.addWidget(self.load_image_label)

        analyse_groupbox.setLayout(analyse_layout)
        right_layout.addWidget(analyse_groupbox)


        # QGroupBox para tones_input e botões
        tones_groupbox = QGroupBox("Adjustment Controls")
        tones_layout = QVBoxLayout()

        self.tone_input = QLineEdit(self)
        self.tone_input.setValidator(QIntValidator(0, 255))
        tones_layout.addWidget(self.tone_input)

        self.brighten_btn = QPushButton("Brighten Image")
        self.brighten_btn.clicked.connect(self.brighten_image)
        tones_layout.addWidget(self.brighten_btn)

        self.darken_btn = QPushButton("Darken Image")
        self.darken_btn.clicked.connect(self.darken_image)
        tones_layout.addWidget(self.darken_btn)

        tones_groupbox.setLayout(tones_layout)
        right_layout.addWidget(tones_groupbox)

        # QGraphicsView para exibir o histograma
        self.histogram_view = QGraphicsView(self)
        self.histogram_scene = QGraphicsScene(self)
        self.histogram_view.setScene(self.histogram_scene)
        right_layout.addWidget(self.histogram_view)

        main_layout.addLayout(right_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_image(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)")
        if filepath:
            self.imagem = Image.open(filepath)
            self.update_image_display()

    def update_image_display(self):
        qt_image = ImageQt.ImageQt(self.imagem)
        pixmap = QPixmap.fromImage(qt_image)
        pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.show_histogram()

    def show_histogram_window(self):
        if self.imagem:
            histograma = gerarHistograma(self.imagem)
            plotarHistograma(histograma)

    def show_histogram(self):
        if self.imagem:
            histograma = gerarHistograma(self.imagem)
            self.plot_and_update_histogram(histograma)

    def plot_and_update_histogram(self, histograma):
        # Criando o histograma com matplotlib
        plt.figure(figsize=(4, 2))
        
        indices = range(len(histograma))
        plt.bar(indices, histograma)
        plt.xticks(indices[::51])
        plt.xlabel('Cor')
        plt.ylabel('Frequência')
        plt.title('Histograma da Imagem')
        plt.tight_layout()

        # Convertendo o gráfico em uma imagem para ser exibida no QGraphicsView
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)

        qt_image = QImage.fromData(buf.getvalue())
        pixmap = QPixmap.fromImage(qt_image)

        self.histogram_scene.clear()
        self.histogram_scene.addPixmap(pixmap)
        self.histogram_view.setScene(self.histogram_scene)

        plt.close()

    def brighten_image(self):
        if self.imagem:
            nivel = int(self.tones_input.text())
            self.imagem = clarearImagem(self.imagem, nivel)
            self.update_image_display()

    def darken_image(self):
        if self.imagem:
            nivel = int(self.tones_input.text())
            self.imagem = escurecerImagem(self.imagem, nivel)
            self.update_image_display()

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()