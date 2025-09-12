# productos.py
# Manejo de productos
from tabulate import tabulate
from persistencia import cargar, leer, actualizar, borrar

productos = []

def crear_producto():
    '''
    Crea un diccionario que representa un producto.
    Retorna un diccionario con la información del producto.
    '''
    codigo = input("Código: ").strip()
    nombre = input("Nombre: ").strip()
    try:
        precio = float(input("Precio: "))
        stock = int(input("Stock: "))
    except ValueError:
        print("Valores inválidos.")
    
    datos = {
        "id": codigo,
        "nombre": nombre,
        "precio": float(precio),
        "stock": int(stock)
    }
    return datos

def listar_productos():
    '''
    Imprime en consola la lista de productos.
    - Si no hay productos, indica que no hay productos cargados.
    Retorna None.
    '''
    if not productos:
        print("No hay productos cargados.")
        return

    headers = list(productos[0].keys())
    tabla = [[p["id"], p["nombre"], p["precio"], p["stock"]] for p in productos]

    print(tabulate(tabla, headers=headers, tablefmt="grid"))

def listar_producto_buscado(Producto):
    '''
    Imprime en consola la lista de productos buscados.
    - p: dict (producto)
    - Si no hay productos, indica que no hay productos cargados.
    Retorna None.
    '''
    if not Producto:
        print("No hay productos cargados.")
        return
    
    headers = list(Producto.keys())
    tabla = [[Producto[h] for h in headers]]
    print(tabulate(tabla, headers=headers, tablefmt="grid"))

def agregar_producto(p):
    '''
    Agrega un producto a la lista de productos.
    - p: dict (producto)
    Retorna True si se agregó correctamente, False si ya existe un producto con el mismo código.
    '''
    if any(x["id"] == p["id"] for x in productos):
        print("Ya existe un producto con ese código.")
        return False
    productos.append(p)
    cargar("productos", p)
    return True

def obtener_producto_por_codigo(codigo):
    '''
    Busca un producto por su código.
    - codigo: str
    Retorna el producto si lo encuentra, None si no lo encuentra.
    '''
    for p in productos:
        if p["id"] == codigo:
            return p
            
    return None