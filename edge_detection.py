import numpy as np
import pandas as pd
import cv2
from PIL import Image, ImageOps


def line_direction_detector(image_array):

    # Definindo os kernels de Sobel
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