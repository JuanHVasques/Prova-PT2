import cv2
import numpy as np
import matplotlib.pyplot as plt

# Constante pega o caminho da imagem sam_final.jpg
IMAGEM = "sam_final.jpg"

# Carrega a imagem para os filtros
def carregar_imagem():
    foto = cv2.imread(IMAGEM, 0) # Pegará a imagem em preto e branco 

    if foto is None:
        print(f"Não foi possivel encontrar a {IMAGEM}")
    return foto

# ------------------Aplicar os Filtros-------------------
# ------------------Passa Baixa-------------------
def filtro_passa_baixa():
    # Selecionando a imagem
    foto = carregar_imagem()

    # Transformada de fourier e centraliza as frequências
    fft = np.fft.fft2(foto)
    fshift = np.fft.fftshift(fft)

    # Criação do filtro passa-baixa
    linhas, colunas = foto.shape # pega linhas e colunas da imagem
    clinha, ccoluna = linhas // 2, colunas // 2 # Centraliza os pixels

    # Criação circulo do filtro
    mascara = np.zeros((linhas, colunas), np.uint8)
    raio = 30
    y, x = np.ogrid[:linhas, :colunas]
    mascara[((y - clinha) ** 2 + (x - ccoluna) ** 2) <= raio**2] = 1

    # Aplicação do filtro
    fshift_filtrado = fshift * mascara

    # Aplicando a fourier invertida 
    fft_invertido = np.abs(
        np.fft.ifft2(np.fft.ifftshift(fshift_filtrado))
    )

    # Criando o espectro da imagem original
    espectro_original = 20 * np.log(np.abs(fshift) + 1)

    # Plotando as 4 imagens 
    plt.figure(figsize=(10, 7))
    plt.subplot(221)
    plt.imshow(foto, cmap="gray")
    plt.title("Imagem Original")
    plt.axis("off")

    plt.subplot(222)
    plt.imshow(espectro_original, cmap="gray")
    plt.title("Espectro de Fourier")
    plt.axis("off")

    plt.subplot(223)
    plt.imshow(mascara, cmap="gray")
    plt.title("Filtro Passa-Baixa")
    plt.axis("off")

    plt.subplot(224)
    plt.imshow(fft_invertido, cmap="gray")
    plt.title("Imagem Filtrada")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

# ------------------Passa Banda-------------------
def filtro_passa_banda():
    # Selecionando a imagem
    foto = carregar_imagem()

    # Transformada de fourier e centraliza as frequências
    fft = np.fft.fft2(foto)
    fshift = np.fft.fftshift(fft)

    # Criação do filtro passa-baixa
    linhas, colunas = foto.shape # pega linhas e colunas da imagem
    clinha, ccoluna = linhas // 2, colunas // 2 # Centraliza os pixels

    # Criação dos dois circulos
    mascara = np.zeros((linhas, colunas), np.uint8)

    raio_interno = 20
    raio_externo = 60

    y, x = np.ogrid[:linhas, :colunas]
    dist = (y - clinha) ** 2 + (x - ccoluna) ** 2

    mascara[(dist > raio_interno**2) & (dist < raio_externo**2)] = 1

    # Aplicar o filtro
    fshift_filtrado = fshift * mascara

    # Transformar em fourier invertida 
    fft_invertido = np.abs(
        np.fft.ifft2(np.fft.ifftshift(fshift_filtrado))
    )

    # Criação do espectro da imagem original
    espectro_original = 20 * np.log(np.abs(fshift) + 1)

    # Plotando as 4 imagens geradas
    plt.figure(figsize=(10, 7))
    plt.subplot(221)
    plt.imshow(foto, cmap="gray")
    plt.title("Imagem Original")
    plt.axis("off")

    plt.subplot(222)
    plt.imshow(espectro_original, cmap="gray")
    plt.title("Espectro de Fourier")
    plt.axis("off")

    plt.subplot(223)
    plt.imshow(mascara, cmap="gray")
    plt.title("Filtro Passa-Banda")
    plt.axis("off")

    plt.subplot(224)
    plt.imshow(fft_invertido, cmap="gray")
    plt.title("Imagem Filtrada")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

# ------------------Filtro transformada de fourier-------------------
def filtro_fft():
    # criação da imagem a ser usada 
    foto = carregar_imagem()

    linhas, colunas = foto.shape

    # Pegando as coordenadas e criando a grade 
    x = np.arange(colunas)
    y = np.arange(linhas)
    X, Y = np.meshgrid(x, y)

    # Cria o ruido(frequencia mostra quantas)
    frequencia = 0.15
    ruido = 50 * np.sin(2 * np.pi * frequencia * (X + Y))

    # Adicionar ruído à imagem
    img_ruido = foto + ruido

    # Limitação dos valores entre 0 e 255
    foto_ruido = np.clip(img_ruido, 0, 255).astype(np.uint8)

    # Transforma a imagem com ruido em fourier
    f = np.fft.fft2(foto_ruido)
    fshift = np.fft.fftshift(f)

    # Criando o espectro da imagem original
    espectro_original = 20 * np.log(np.abs(fshift) + 1)

    mask = np.ones((linhas, colunas), np.uint8)

    clinha, ccoluna = linhas // 2, colunas // 2

    # Pegando coordenadas para criar buracos no espectro
    pontos = [
        (clinha - 80, ccoluna - 80),
        (clinha - 60, ccoluna - 60),
        (clinha - 40, ccoluna - 40),
        (clinha - 20, ccoluna - 20),
        (clinha + 20, ccoluna + 20),
        (clinha + 40, ccoluna + 40),
        (clinha + 60, ccoluna + 60),
        (clinha + 80, ccoluna + 80),
    ]

    raio = 8 # Tamanho da remoção

    y, x = np.ogrid[:linhas, :colunas]

    # Trata o ruido(buracos no espectro)
    for px, py in pontos:
        mask[((y - px) ** 2 + (x - py) ** 2) <= raio**2] = 0

    fshift_filtrado = fshift * mask

    # Cria o espectro filtrado da imagem 
    espectro_filtrado = 20 * np.log(
        np.abs(fshift_filtrado) + 1
    )

    # Transformar em fourier invertida 
    fft_invertida = np.abs(
        np.fft.ifft2(np.fft.ifftshift(fshift_filtrado))
    )

    # Plota as 4 imagens
    plt.figure(figsize=(10, 7))

    plt.subplot(221)
    plt.imshow(foto_ruido, cmap="gray")
    plt.title("Imagem com Ruído")
    plt.axis("off")

    plt.subplot(222)
    plt.imshow(fft_invertida, cmap="gray")
    plt.title("Imagem Final")
    plt.axis("off")

    plt.subplot(223)
    plt.imshow(espectro_original, cmap="gray")
    plt.title("Espectro Original")
    plt.axis("off")

    plt.subplot(224)
    plt.imshow(espectro_filtrado, cmap="gray")
    plt.title("Espectro Filtrado")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

# ------------------Passa Alta-------------------
def filtro_passa_alta():
    # Selecionando a imagem
    foto = carregar_imagem()

    # Transformada de fourier e centraliza as frequências
    fft = np.fft.fft2(foto)
    fshift = np.fft.fftshift(fft)

    # Criação do filtro passa-baixa
    linhas, colunas = foto.shape # pega linhas e colunas da imagem
    clinha, ccoluna = linhas // 2, colunas // 2 # Centraliza os pixels

    # Criação circulo do filtro()
    mascara = np.ones((linhas, colunas), np.uint8)# Cria tela branca
    raio = 30
    y, x = np.ogrid[:linhas, :colunas]
    mascara[((y - clinha) ** 2 + (x - ccoluna) ** 2) <= raio**2] = 0

    # Aplicação do filtro
    fshift_filtrado = fshift * mascara

    # Aplicando a fourier invertida 
    fft_invertido = np.abs(
        np.fft.ifft2(np.fft.ifftshift(fshift_filtrado))
    )

    # Criando o espectro da imagem original
    espectro_original = 20 * np.log(np.abs(fshift) + 1)

    # Plotando as 4 imagens 
    plt.figure(figsize=(10, 7))
    plt.subplot(221)
    plt.imshow(foto, cmap="gray")
    plt.title("Imagem Original")
    plt.axis("off")

    plt.subplot(222)
    plt.imshow(espectro_original, cmap="gray")
    plt.title("Espectro de Fourier")
    plt.axis("off")

    plt.subplot(223)
    plt.imshow(mascara, cmap="gray")
    plt.title("Filtro Passa-Alta")
    plt.axis("off")

    plt.subplot(224)
    plt.imshow(fft_invertido, cmap="gray")
    plt.title("Imagem Filtrada")
    plt.axis("off")

    plt.tight_layout()
    plt.show()


# ------------------Codigo Main-------------------

# Cria um menu para escolher qual filtro quer 
while True:
    print("1 - Filtro Passa-Alta")
    print("2 - Filtro Passa-Banda")
    print("3 - Filtro Passa-Baixa")
    print("4 - Filtro FFT")
    print("5 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        filtro_passa_alta()
    elif opcao == "2":
        filtro_passa_banda()
    elif opcao == "3":
        filtro_passa_baixa()
    elif opcao == "4":
        filtro_fft()
    elif opcao == "5":
        print("Saindo do programa")
        break
    else:
        print("Opção inválida.")
