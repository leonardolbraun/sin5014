from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QFileDialog, QLineEdit, QGraphicsView, QGraphicsScene, QHBoxLayout, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QIntValidator
from PIL import Image, ImageQt
import io
import matplotlib.pyplot as plt
from edge_detection import line_direction_detector
from image_processing import gerar_imagem, gerar_array_imagem, gerar_histograma, clarear_imagem, escurecer_imagem, plotar_histograma, filtro_mediana, equalizacao, quantizacao

class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.imagem = None

        self.setWindowTitle('Image Processor')
        self.setGeometry(200, 200, 1300, 600)

        main_layout = QHBoxLayout()

        # Label to show image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(800, 600)  # Definindo um tamanho mínimo para visualização
        main_layout.addWidget(self.image_label)

        # Right column of the window
        right_layout = QVBoxLayout()

        # QGroupBox to load image
        load_groupbox = QGroupBox("Load Image")
        load_layout = QVBoxLayout()

        # Button to load the image
        self.load_btn = QPushButton("Load Image")
        self.load_btn.clicked.connect(self.load_image)
        load_layout.addWidget(self.load_btn)

        self.save_btn = QPushButton("Save Image")
        self.save_btn.clicked.connect(self.save_image)
        load_layout.addWidget(self.save_btn)

        load_groupbox.setLayout(load_layout)
        right_layout.addWidget(load_groupbox)

         # QGroupBox to analyse the image
        analyse_groupbox = QGroupBox("Image Analysis")
        analyse_layout = QVBoxLayout()

        # Button to show histogram
        self.histogram_btn = QPushButton("Show Histogram")
        self.histogram_btn.clicked.connect(self.show_histogram_window)
        analyse_layout.addWidget(self.histogram_btn)

        self.image_format_label = QLabel("Image format: ")
        analyse_layout.addWidget(self.image_format_label)

        self.image_size_label = QLabel("Image size: ")
        analyse_layout.addWidget(self.image_size_label)

        self.image_mode_label = QLabel("Image mode: ")
        analyse_layout.addWidget(self.image_mode_label)

        analyse_groupbox.setLayout(analyse_layout)
        right_layout.addWidget(analyse_groupbox)

        # QGroupBox for tone_input and buttons
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

         # QGroupBox for filters
        filters_groupbox = QGroupBox("Filters")
        filters_layout = QVBoxLayout()

        self.filter_input = QLineEdit(self)
        self.filter_input.setValidator(QIntValidator(0, 255))
        filters_layout.addWidget(self.filter_input)

        self.median_filter_btn = QPushButton("Median Filter")
        self.median_filter_btn.clicked.connect(self.median_filter)
        filters_layout.addWidget(self.median_filter_btn)

        self.equalization_filter_btn = QPushButton("Equalization Filter")
        self.equalization_filter_btn.clicked.connect(self.equalization_filter)
        filters_layout.addWidget(self.equalization_filter_btn)

        self.quantization_filter_btn = QPushButton("Quantization Filter")
        self.quantization_filter_btn.clicked.connect(self.quantization_filter)
        filters_layout.addWidget(self.quantization_filter_btn)

        filters_groupbox.setLayout(filters_layout)
        right_layout.addWidget(filters_groupbox)

        # QGroupBox for edge detection
        edge_groupbox = QGroupBox("Edge Detection")
        edge_layout = QVBoxLayout()

        self.line_detector_btn = QPushButton("Line direction detector")
        self.line_detector_btn.clicked.connect(self.line_detector)
        edge_layout.addWidget(self.line_detector_btn)

        self.line_direction_label = QLabel("Line direction: ")
        edge_layout.addWidget(self.line_direction_label)

        edge_groupbox.setLayout(edge_layout)
        right_layout.addWidget(edge_groupbox)



        # QGraphicsView to show histogram
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
            if(self.imagem.mode != "L"):
                self.imagem = self.imagem.convert('L')
            
            self.update_image_display()

            # Update labels when an image is loaded
            self.image_format_label.setText("Image format: " + str(self.imagem.format))
            self.image_size_label.setText("Image size: " + str(self.imagem.size))
            self.image_mode_label.setText("Image mode: " + self.imagem.mode)

    def save_image(self):
        # Salvar a imagem usando uma caixa de diálogo
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "JPEG (*.jpg *.jpeg)")
            
        if file_path:
            self.imagem.save(file_path)
    
    def update_image_display(self):
        qt_image = ImageQt.ImageQt(self.imagem)
        pixmap = QPixmap.fromImage(qt_image)
        pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.show_histogram()

    def show_histogram_window(self):
        if self.imagem:
            imagem_array = gerar_array_imagem(self.imagem)
            histograma = gerar_histograma(imagem_array)
            plotar_histograma(histograma, 17, 1)

    def show_histogram(self):
        if self.imagem:
            imagem_array = gerar_array_imagem(self.imagem)
            histograma = gerar_histograma(imagem_array)
            self.plot_and_update_histogram(histograma)

    def plot_and_update_histogram(self, histograma):
        plt.figure(figsize=(4, 2))
        
        plotar_histograma(histograma, 51, 0)

        # Converting the graphic in a image to show on QGraphicsView
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
            imagem_array = gerar_array_imagem(self.imagem)
            nivel = int(self.tone_input.text())
            nova_imagem_array = clarear_imagem(imagem_array, nivel)
            self.imagem = gerar_imagem(nova_imagem_array)
            self.update_image_display()

    def darken_image(self):
        if self.imagem:
            imagem_array = gerar_array_imagem(self.imagem)
            nivel = int(self.tone_input.text())
            nova_imagem_array = escurecer_imagem(imagem_array, nivel)
            self.imagem = gerar_imagem(nova_imagem_array)
            self.update_image_display()

    def median_filter(self):
        if self.imagem:
            imagem_array = gerar_array_imagem(self.imagem)
            vizinhos = int(self.filter_input.text())
            nova_imagem_array = filtro_mediana(imagem_array, vizinhos)
            self.imagem = gerar_imagem(nova_imagem_array)
            self.update_image_display()

    def equalization_filter(self):
        if self.imagem:
            imagem_array = gerar_array_imagem(self.imagem)
            largura_imagem, altura_imagem = self.imagem.size
            histograma = gerar_histograma(imagem_array)
            nova_imagem_array = equalizacao(imagem_array, largura_imagem, altura_imagem, histograma)
            self.imagem = gerar_imagem(nova_imagem_array)
            self.update_image_display()

    def quantization_filter(self):
        if self.imagem:
            imagem_array = gerar_array_imagem(self.imagem)
            tons = int(self.filter_input.text())
            histograma = gerar_histograma(imagem_array)
            nova_imagem_array = quantizacao(imagem_array, tons, histograma)
            self.imagem = gerar_imagem(nova_imagem_array)
            self.update_image_display()
    
    def show_line_direction(self, line_direction):
        self.line_direction_label.setText("Line direction: " + str(line_direction))
    
    def line_detector(self):
        if self.imagem:
            imagem_array = gerar_array_imagem(self.imagem)
            line_direction = line_direction_detector(imagem_array)
            self.show_line_direction(line_direction)
