import os

def limpiar_consola():
    '''
    Limpia la consola
    '''
    os.system('cls' if os.name == 'nt' else 'clear')