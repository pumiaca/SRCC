# productos.py
# Manejo de productos

productos = []

def crear_producto(codigo, nombre, precio, stock):
    '''
    Crea un diccionario que representa un producto.
    - codigo: str
    - nombre: str
    - precio: float
    - stock: int
    Retorna un diccionario con la información del producto.
    '''
    return {
        "codigo": codigo,
        "nombre": nombre,
        "precio": float(precio),
        "stock": int(stock)
    }

def listar_productos():
    '''
    Imprime en consola la lista de productos.
    - Si no hay productos, indica que no hay productos cargados.
    Retorna None.
    '''
    if not productos:
        print("No hay productos cargados.")
        return
    for p in productos:
        print(p)

def agregar_producto(p):
    '''
    Agrega un producto a la lista de productos.
    - p: dict (producto)
    Retorna True si se agregó correctamente, False si ya existe un producto con el mismo código.
    '''
    if any(x["codigo"] == p["codigo"] for x in productos):
        print("Ya existe un producto con ese código.")
        return False
    productos.append(p)
    return True

def obtener_producto_por_codigo(codigo):
    '''
    Busca un producto por su código.
    - codigo: str
    Retorna el producto si lo encuentra, None si no lo encuentra.
    '''
    for p in productos:
        if p["codigo"] == codigo:
            return p
    return None