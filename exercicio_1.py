from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def gerarHistograma(image):
    ## Documentação numpy https://numpy.org/pt/
    image_array = np.array(image)
    histograma_array = np.zeros(256);

    print(image_array)

    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            valor_pixel = image_array[i, j];

            histograma_array[valor_pixel] += 1 

    for k in range(len(histograma_array)):
        print("Valor de " + str(k) + ": " + str(histograma_array[k]))

    return histograma_array

def plotarHistograma(histograma_array):
    # Documentação do matplotlib https://gepac.github.io/2019-05-17-intro-matplotlib/
    indices = np.arange(len(histograma_array))

    plt.bar(indices, histograma_array)
    plt.xticks(indices[::17])
    plt.xlabel('Cor')
    plt.ylabel('Frequência')
    plt.title('Histograma da Imagem')
    plt.show()

def clarearImagem(imagem, nivel):
    imagem_array = np.array(imagem)
    print("clarear")
        
    for i in range(imagem_array.shape[0]):
        for j in range(imagem_array.shape[1]):
            
            #imagem_array[i, j] = np.clip(imagem_array[i, j]  + nivel, 0, 255)
            novo_valor = imagem_array[i, j] + nivel

            if(novo_valor > 255):
                novo_valor = 255

            imagem_array[i, j] = novo_valor
    
    imagem = Image.fromarray(imagem_array)
    return imagem
    """ print(imagem_array)
    imagem_clareada = Image.fromarray(imagem_array)
    imagem_clareada.save('imagem_clareada.jpg')
    imagem_clareada.show() """
    
def escurecerImagem(imagem, nivel):
    imagem_array = np.array(imagem)
    print("escurecer")
        
    for i in range(imagem_array.shape[0]):
        for j in range(imagem_array.shape[1]):
            
            #imagem_array[i, j] = np.clip(imagem_array[i, j]  + nivel, 0, 255)
            novo_valor = imagem_array[i, j] - nivel

            if(novo_valor < 0):
                novo_valor = 0

            imagem_array[i, j] = novo_valor

    imagem = Image.fromarray(imagem_array)
    return imagem
    """print(imagem_array)
    imagem_clareada = Image.fromarray(imagem_array)
    imagem_clareada.save('imagem_escurecida.jpg')
    imagem_clareada.show() "


""" # Abre a imagem usando PIL
"""imagem = Image.open('einstein_cinza.jpg')

print("Formato da imagem: " + imagem.format)
print("Tamanho da imagem: ",  imagem.size)
print("Modo da imagem: " + imagem.mode)

##Documentação pillow https://pillow.readthedocs.io/en/stable/handbook/concepts.html
if(imagem.mode == "L"):
    plotarHistograma(gerarHistograma(imagem))
    clarearImagem(imagem,10)
    escurecerImagem(imagem,100)
else:
    print("Precisa de imagem em escala de cinza")
"""
