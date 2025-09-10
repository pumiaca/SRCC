import json

def leer(archivo:str):
    """
    Leer datos de un archivo JSON.
    Atributos:
    - archivo: nombre del archivo sin extensión .json
    Retorna:
        Si el archivo existe, devuelve una lista de diccionarios con los datos del archivo.
        Si el archivo no existe, devuelve una lista vacía.
    """
    datos = []
    try:
        with open(f"./src/{archivo}.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return datos
    except FileNotFoundError:
        return []

def cargar(archivo:str, dato:dict):
    """
    Cargar 1 registro de un archivo JSON.
    Atributos:
        - archivo: nombre del archivo sin extensión .json
        - dato: diccionario con el registro a cargar
    Retorna:
        Si el archivo existe, devuelve una lista de diccionarios con los datos del archivo.
        Si el archivo no existe, devuelve el error.
    """
    datos = leer(archivo)
    datos.append(dato)
    try:
        with open(f"./src/{archivo}.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo)
        print(datos)
        return datos
    except Exception as e:
        print(f"Error de Carga: {e}")
        return f"Error de Carga: {e}"

"""
def actualizar(archivo:str, dato:dict): no funca, aún.
    
    Actualizar 1 registro de un archivo JSON.
    Atributos:
        - archivo: nombre del archivo sin extensión .json
        - dato: diccionario con el registro a actualizar
    Retorna:
        Si el archivo existe, devuelve una lista de diccionarios con los datos del archivo.
        Si el archivo no existe, devuelve el error.
    
    datos = leer(archivo)
    for i, item in datos:
        if item["id"] == dato["id"]:
            datos[i] = dato
    try:
        with open(f"./src/{archivo}.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo)
        return datos
    except Exception as e:
        return f"Error de Carga: {e}"

actualizar("productos", {'id': 1, 'nombre': 'Producto 1000', 'precio': 100})

"""

def borrar(archivo:str, dato:dict):
    """
    Borrar 1 registro de un archivo JSON.
    Atributos:
        - archivo: nombre del archivo sin extensión .json
        - dato: diccionario con el registro a borrar
    Retorna:
        Si el archivo existe, devuelve una lista de diccionarios con los datos del archivo.
        Si el archivo no existe, devuelve el error.
    """
    datos = leer(archivo)
    datos = [item for item in datos if item["id"] != dato["id"]]
    try:
        with open(f"./src/{archivo}.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo)
        return datos
    except Exception as e:
        return f"Error de Carga: {e}"
