from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt
from numba import jit, cuda

def gerar_array_imagem(imagem):
    image_array = np.array(imagem)
    return image_array

def gerar_imagem(imagem_array):
    imagem = Image.fromarray(imagem_array)
    return imagem 

@jit(nopython=True)
def gerar_histograma(image_array):
    ## Documentação numpy https://numpy.org/pt/
    histograma_array = np.zeros(256)

    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            valor_pixel = image_array[i, j]

            histograma_array[valor_pixel] += 1 

    return histograma_array

def plotar_histograma(histograma_array, qtde_indices, show_window):
    # Documentação do matplotlib https://gepac.github.io/2019-05-17-intro-matplotlib/
    indices = np.arange(len(histograma_array))

    plt.bar(indices, histograma_array)
    plt.xticks(indices[::int(qtde_indices)])
    plt.xlabel('Cor')
    plt.ylabel('Frequência')
    plt.title('Histograma da Imagem')
    plt.tight_layout()
    if show_window:
        plt.show()

@jit(nopython=True)
def clarear_imagem(imagem_array, nivel):
        
    for i in range(imagem_array.shape[0]):
        for j in range(imagem_array.shape[1]):
            
            novo_valor = imagem_array[i, j] + nivel

            if(novo_valor > 255):
                novo_valor = 255

            imagem_array[i, j] = novo_valor
    
    return imagem_array

@jit(nopython=True) 
def escurecer_imagem(imagem_array, nivel):
        
    for i in range(imagem_array.shape[0]):
        for j in range(imagem_array.shape[1]):

            novo_valor = imagem_array[i, j] - nivel

            if(novo_valor < 0):
                novo_valor = 0

            imagem_array[i, j] = novo_valor

    return imagem_array

@jit(nopython=True)
def filtro_mediana(imagem_array, raio):
    altura, largura = imagem_array.shape[:2]

    tamanho_janela = 2 * raio + 1
    deslocamento = tamanho_janela // 2

    for i in range(imagem_array.shape[0]):
        for j in range(imagem_array.shape[1]):

            matriz_vizinhanca = imagem_array[max(0, i-deslocamento):min(i + deslocamento + 1, altura), max(0, j - deslocamento):min(j+deslocamento+1, largura)]

            imagem_array_vizinhanca = []
                      
            for k in range(matriz_vizinhanca.shape[0]):
                for a in range(matriz_vizinhanca.shape[1]):
                        
                        imagem_array_vizinhanca.append(matriz_vizinhanca[k, a])

            imagem_array_ordenado = sorted(imagem_array_vizinhanca)  
            if len(imagem_array_ordenado) % 2 != 0:
                mediana = imagem_array_ordenado[len(imagem_array_ordenado) // 2]
                imagem_array[i, j] = mediana
            else:
                indice_maior = round(len(imagem_array_ordenado)/2)
                indice_menor = math.floor((len(imagem_array_ordenado)/2))
                mediana = (int(imagem_array_ordenado[indice_maior]) + int(imagem_array_ordenado[indice_menor])) / 2
                imagem_array[i, j] = int(mediana)
                
    return imagem_array

@jit(nopython=True)
def equalizacao(imagem_array, largura_imagem, altura_imagem, histograma):
    niveis_cinza = 0
    histograma_equalizado = np.zeros(256)
    acumulado = np.zeros(256)
    vetor_posicoes = []
    
    for i in histograma:
        if i > 0:
            niveis_cinza += 1
        
    numero_ideal_pixels = (largura_imagem*altura_imagem)/niveis_cinza

    for index, i in enumerate(histograma):
        if index >= 0: 
            acumulado[index] = acumulado[index - 1] + i
            q = max(0,round(acumulado[index]/numero_ideal_pixels) - 1)
            vetor_posicoes.append(q)
            histograma_equalizado[q] += i

    for i in range(imagem_array.shape[0]):
        for j in range(imagem_array.shape[1]):

            imagem_array[i, j] = vetor_posicoes[imagem_array[i, j]]

    return imagem_array

@jit(nopython=True)
def quantizacao(imagem_array, tons, histograma):

    niveis_cinza = 0
    for i in histograma:
        if i > 0:
            niveis_cinza += 1

    niveis = round(niveis_cinza / (tons-1))

    for i in range(imagem_array.shape[0]):
        for j in range(imagem_array.shape[1]):
            cor = imagem_array[i, j]
            nivel_pixel = round(cor/niveis)
            novo_valor = int(round((nivel_pixel * niveis) + niveis / 2))
            
            if(novo_valor < 0):
                novo_valor = 0
            
            if(novo_valor > 255):
                novo_valor = 255

            imagem_array[i, j] = novo_valor

    return imagem_array

"""imagem = Image.open('einstein_cinza.jpg')

print("Formato da imagem: " + imagem.format)
print("Tamanho da imagem: ",  imagem.size)
print("Modo da imagem: " + imagem.mode)

##Documentação pillow https://pillow.readthedocs.io/en/stable/handbook/concepts.html
if(imagem.mode == "L"):
    plotar_histograma(gerar_histograma(imagem))
    clarear_imagem(imagem,10)
    escurecer_imagem(imagem,100)
else:
    print("Precisa de imagem em escala de cinza")
"""
