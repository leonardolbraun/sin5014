from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt

def gerar_histograma(image):
    ## Documentação numpy https://numpy.org/pt/
    image_array = np.array(image)
    histograma_array = np.zeros(256);

    # print(image_array)

    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            valor_pixel = image_array[i, j];

            histograma_array[valor_pixel] += 1 

    # for k in range(len(histograma_array)):
    #     print("Valor de " + str(k) + ": " + str(histograma_array[k]))

    return histograma_array

def plotar_histograma(histograma_array):
    # Documentação do matplotlib https://gepac.github.io/2019-05-17-intro-matplotlib/
    indices = np.arange(len(histograma_array))

    plt.bar(indices, histograma_array)
    plt.xticks(indices[::17])
    plt.xlabel('Cor')
    plt.ylabel('Frequência')
    plt.title('Histograma da Imagem')
    plt.show()

def clarear_imagem(imagem, nivel):
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
    
def escurecer_imagem(imagem, nivel):
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

def filtro_mediana(imagem, raio):
    imagem_array = np.array(imagem)
    altura, largura = imagem_array.shape[:2]

    tamanho_janela = 2 * raio + 1

    deslocamento = tamanho_janela // 2

    for i in range(imagem_array.shape[0]):
        for j in range(imagem_array.shape[1]):

            matriz_vizinhanca = imagem_array[max(0, i-deslocamento):min(i + deslocamento + 1, altura), max(0, j - deslocamento):min(j+deslocamento+1, largura)]

            imagem_array_vizinhanca = []
                      
            for k in range(matriz_vizinhanca.shape[0]):
                for a in range(matriz_vizinhanca.shape[1]):
                        #print("Vizinhos de " + str(imagem_array[i, j]))
                        #print("linha " + str(k) + "coluna" + str(a))
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
                
    
    
    imagem = Image.fromarray(imagem_array)
    return imagem
    #imagem_mediana = Image.fromarray(imagem_array)
    #imagem_mediana.save('imagem_mediana.jpg')
    #imagem_mediana.show()

   
    # imagem_array_ordenado = sorted(imagem_array_completo)        
    # #for k in imagem_array_ordenado:
    # if(len(imagem_array_ordenado) % 2 == 0 ):
    #     print("#########")
    #     #print("Indice k: " + str(k))
    #     print("Tamanho do array: " + str(len(imagem_array_ordenado)))

    #     #print("Valor: " + str(imagem_array_ordenado[k]))
    #     print("par: " + str(len(imagem_array_ordenado)/2))
    #     print (round(len(imagem_array_ordenado)/2))
    # else:
    #     print("#########")
    #     #print("Indice k: " + str(k))
    #     print("Tamanho do array: " + str(len(imagem_array_ordenado)))
    #     print("impar: " + str(len(imagem_array_ordenado)/2))
    #     indice_maior = round(len(imagem_array_ordenado)/2)
    #     indice_menor = math.floor((len(imagem_array_ordenado)/2))
    #     mediana = (imagem_array_ordenado[indice_maior] + imagem_array_ordenado[indice_menor]) / 2
    #     #print("valor maior: " + str(imagem_array_ordenado[int(round(len(imagem_array_ordenado))/2))
    #     #print("Indice: " + str(k))
    #     print ("Média entre indices: " + str(indice_maior) + " e " + str(indice_menor))
    #     print("Média dos Valores: " +  str(imagem_array_ordenado[indice_maior]) + " e " + str(imagem_array_ordenado[indice_menor]))
    #     print("Mediana: " + str(mediana))

    
    #print("teste")       
    #imagem_array_ordenado = sorted(imagem_array_completo)
    
    #print (len(imagem_array_ordenado)/2);


def equalizacao(imagem):
    imagem_array = np.array(imagem)
    largura, altura = imagem.size
    niveis_cinza = 0
    histograma_equalizado = np.zeros(256)
    acumulado = np.zeros(256)
    vetor_posicoes = []

    histograma = gerar_histograma(imagem)
    print("Tamanho da imagem: " + str(imagem.size))
    
    for i in histograma:
        if i > 0:
            niveis_cinza += 1
        
    print("niveis cinza: " + str(niveis_cinza))
    numero_ideal_pixels = (largura*altura)/niveis_cinza
    print("Número ideal de pixels em cada nível: " + str(numero_ideal_pixels))

    for index, i in enumerate(histograma):
        if index >= 0: 
            acumulado[index] = acumulado[index - 1] + i;
            q = max(0,round(acumulado[index]/numero_ideal_pixels) - 1)
            vetor_posicoes.append(q)
            histograma_equalizado[q] += i

    #for index, i in enumerate(vetor_posicoes):
        #print("index: " + str(index) + "value: " + str(i))

    for i in range(imagem_array.shape[0]):
        for j in range(imagem_array.shape[1]):
            #print("cor original: " + str( imagem_array[i, j]) + " - nova cor: " + str(vetor_posicoes[imagem_array[i, j]]))
            imagem_array[i, j] = vetor_posicoes[imagem_array[i, j]]

    imagem = Image.fromarray(imagem_array)
    return imagem

    # imagem_equalizada = Image.fromarray(imagem_array)
    # imagem_equalizada.save('imagem_equalizada.jpg')
    # imagem_equalizada.show() 


def quantizacao(imagem, tons):
    imagem_array = np.array(imagem)
    histograma = gerar_histograma(imagem)

    niveis_cinza = 0
    for i in histograma:
        if i > 0:
            niveis_cinza += 1

    niveis = round(niveis_cinza / tons)
    print("tons de cinza: " + str(niveis))

    for i in range(imagem_array.shape[0]):
        for j in range(imagem_array.shape[1]):
            cor = imagem_array[i, j]
            nivel_pixel = round(cor/niveis)
            imagem_array[i, j] = int(round((nivel_pixel * niveis) + niveis / 2))

    imagem = Image.fromarray(imagem_array)
    return imagem

#imagem = Image.open('einstein_cinza.jpg')
#filtro_mediana(imagem, 8)




# imagem = Image.open('einstein_cinza.jpg')
# equalizacao(imagem)

#imagem = Image.open('einstein_cinza.jpg')
#filtro_mediana(imagem, 8)
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
