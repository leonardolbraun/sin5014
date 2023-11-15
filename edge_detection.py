import numpy as np
import pandas as pd
import cv2
from PIL import Image, ImageOps


def line_direction_detector(image_array):

    # Definindo os kernels de Sobel. Utilizando esses kernels não é necessário calcular a derivada da função da imagem.
    sobel_x = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])
    
    sobel_y = np.array([
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ])

    height, width  = image_array.shape

    # Vetor para gradiente x e y
    Gx = np.zeros((height, width))
    Gy = np.zeros((height, width))

    # Percorre a imagem para aplicar a convolução
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # Para cada pixel, calcula a convolução de x e y
            Gx[y, x] = np.sum(sobel_x * image_array[y-1:y+2, x-1:x+2])
            Gy[y, x] = np.sum(sobel_y * image_array[y-1:y+2, x-1:x+2])


    # Calcula a magnitude e direção do gradiente
    magnitude = np.sqrt(Gx**2 + Gy**2)
    direction = np.arctan2(Gy, Gx) # Retorna valores entre -pi e pi
    
    #Esse trecho é necessário para desconsiderar os 0 no array, ou seja, fora do objeto da imagem. 
    #Nesse caso será considerado apenas as bordas.
    threshold = 0.5 * magnitude.max()
    strong_edges = magnitude > threshold

    # Determina a orientação usando as strong_edges e o gradiente 
    vertical_count = np.sum(strong_edges & ((direction == 0) ))
    horizontal_count = np.sum(strong_edges & ((direction == np.pi/2)))

    #Para a reta inclinada é preciso retirar pi/2 da contagem para não chocar com uma reta horizontal.
    inclined_count = np.sum(strong_edges & ((direction > 0) & (direction < np.pi) & (direction != np.pi/2)))

    print("Número de bordas horizontais:", horizontal_count)
    print("Número de bordas verticais:", vertical_count)
    print("Número de bordas inclinadas:", inclined_count)

    df = pd.DataFrame(direction)
    df.to_excel(excel_writer="test.xlsx")

    if horizontal_count > vertical_count and horizontal_count > inclined_count:
        return("horizontal")
    elif vertical_count > horizontal_count and vertical_count > inclined_count:
        return("vertical")
    else:
        return("inclinada")
    

def is_homogeneous(region, threshold=40):
    # Função que determina se uma região é homogênea com base em um limiar
    return np.std(region) < threshold

def split_and_merge(img, min_size=10):
    width, height = img.size
    
    print(is_homogeneous(np.array(img)))

    # Se a imagem for muito pequena ou homogênea, retorne a própria imagem
    if height <= min_size or width <= min_size or is_homogeneous(np.array(img)):
        return img
    
    # divide a imagem em quatro quadrantes
    r1 = img.crop((0, 0, width//2, height//2))
    r2 = img.crop((width//2, 0, width, height//2))
    r3 = img.crop((0, height//2, width//2, height))
    r4 = img.crop((width//2, height//2, width, height))
    
    # split and merge em cada quadrante
    r1 = split_and_merge(r1, min_size)
    r2 = split_and_merge(r2, min_size)
    r3 = split_and_merge(r3, min_size)
    r4 = split_and_merge(r4, min_size)
    
    # Mesclar os quadrantes em uma única imagem e retorna
    merged = Image.new("L", (width, height))
    merged.paste(r1, (0, 0))
    merged.paste(r2, (width//2, 0))
    merged.paste(r3, (0, height//2))
    merged.paste(r4, (width//2, height//2))
    
    return merged

def count_objects(binary_data):
    # teste de detecção dos componentes

    #Esse código converte todos os valores em 0 e 1 
    #binary_image = (binary_data == 0).astype(np.uint8)

    num_labels, _ = cv2.connectedComponents(binary_data)
    print(f' {num_labels} objetos')

    #Necessário descontar o fundo pois o cv2 detecta componente
    num_labels -= 1
    return num_labels # retorna o número de componentes conectados


def prepare_image(image):
    # Segmentação da imagem usando o método "split and merge"
    segmented = split_and_merge(image)
   
    # Binarização da imagem segmentada
    threshold = 200
    binary_data = np.array(segmented)
    
    #Essa parte impacta na algoritmo de detecção de componentes conectados (cv2.connectedComponents(binary_data))
    #Importante converter para 1 e 0 para o algortimo detectar corretamente
    binary_data[binary_data <= threshold] = 1
    binary_data[binary_data > threshold] = 0
    
    df = pd.DataFrame(binary_data)
    df.to_excel(excel_writer="test2.xlsx")

    return binary_data