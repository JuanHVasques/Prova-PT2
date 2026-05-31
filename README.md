# Prova

## Tecnologias utilizadas
- Python: linguagem principal utilizada no código
- OpenCV(cv2): Biblioteca utilizada para processar a imagen sam_final.jpg
- Numpy(np): Usado principalmente para coordenadas pegas no matplotlib
- matplotlib(plt): Usado para mostar os filtros feitos

## O que é espectro de fourier
O espectro de fourier é uma representação da imagem original convertida do domínio espacial (pixels) para o domínio da frequência, sendo o que mostra nas fotos no Resultado obtido. O centro do espectro(baixa frequência) representa as regiões da imagem onde passa cores tons que mudam de forma lenta e suave, como fundos homogêneos e iluminação geral, já a borda do espectro(alta frequência) representa transições buscas de intensidade na imagem. Isso inclui bordas nítidas, contornos, detalhes finos, texturas e ruídos

## O que é e o que faz cada filtro utilizado
- Passa-baixa: Um filtro que deixa passar as menores frequências(somente o que está no centro), sendo o resultado que os detalhes finos, como os fios de cabelo do personagem e as texturas do traje de proteção, são eliminados, restando apenas as formas e luz global
- Passa-banda:Um filtro que deixa passar frequências médias(Em formato de anel), sendo o resultado que exibe contornos e texturas de escala média, eliminando tanto o borrão das superfícies planas quanto o ruído excessivamente agudo das bordas mais finas
- Passa-alta: O oposto da passa-baixa, ele deixa passar as maiores frequências(somente o que está no centro que não), sendo o resultado que os detalhes que foram retirados do passa-baixa, são mais realcados
- Notch(FFT): Filtro que é utilizado quando a imagem está severamente corrompida por linhas diagonais periódicas (ruído senoidal). Eliminando com pontos pretos os pontos brilhantes no espectro de Fourier

## Resultado obtidos
1- Passa baixa:
<img width="991" height="644" alt="Passa_baixa" src="https://github.com/user-attachments/assets/39676c59-c552-4680-86d1-0b6661bd5f22" />

2- Passa banda:
<img width="992" height="638" alt="Passa_banda" src="https://github.com/user-attachments/assets/53dce457-f1a4-49ad-b1ef-40f2cb5a7081" />

3- Passa alta:
<img width="983" height="644" alt="Passa_alta" src="https://github.com/user-attachments/assets/2f2b50fd-c1a1-4bb0-b217-f26944fe3c67" />

4- Notch(FFT):
<img width="986" height="651" alt="FFT" src="https://github.com/user-attachments/assets/760235fc-8de4-4b45-82fb-e812343f4a68" />

## Qual foi o melhor nesse caso?
O filtro que teve o melhor resultado foi o Notch(FFT), pois os filtros anterioes(passa-baixa e passa-alta) destruiram detalhes na imagem deixando ela menos nitida, enquanto o Notch ele arrumou as linhas senoidal e manteve os detalhes dela 
