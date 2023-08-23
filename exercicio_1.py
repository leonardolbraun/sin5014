from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def analisaImagemEmEscalaCinza(image):
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


# Abre a imagem usando PIL
image = Image.open('einstein_cinza.jpg')

print("Formato da imagem: " + image.format)
print("Tamanho da imagem: ",  image.size)
print("Modo da imagem: " + image.mode)

##Documentação pillow https://pillow.readthedocs.io/en/stable/handbook/concepts.html
if(image.mode == "L"):
    plotarHistograma(analisaImagemEmEscalaCinza(image))
else:
    print("Precisa de imagem em escala de cinza")