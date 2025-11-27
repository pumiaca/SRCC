import os

def limpiar_consola():
    '''
    Limpia la consola
    '''
    os.system('cls' if os.name == 'nt' else 'clear')

def encabezador(titulo, ancho=50, caracter='='):
    texto_centrado = f" {titulo.upper()} ".center(ancho - 4, ' ')
    linea_superior = caracter * ancho
    linea_media = caracter * 2 + texto_centrado + caracter * 2
    print("\n" + linea_superior)
    print(linea_media)
    print(linea_superior + "\n")