# productos.py
# Manejo de productos
import re
from tabulate import tabulate
from persistencia import cargar, leer, actualizar, borrar

productos = []

def menu_productos():
    '''
    Menú para la gestión de productos.
    Permite agregar, buscar, borrar y listar productos.
    '''

    while True:
        print("\n=== MENU DE PRODUCTOS ===")
        print("1. Agregar producto")
        print("2. Buscar producto por codigo")
        print("3. Buscar producto por Descripción")
        print("4. Borrar producto")
        print("5. Listar todos los productos")
        print("6. Regresar al menú principal")

        opcion_p = input("Seleccione una opción: ").strip()

        if opcion_p == "1":
            p = crear_producto()
            if agregar_producto(p):
                print("Producto agregado.")
        elif opcion_p == "2":
            codigo = input("Ingrese Código del Producto: ").strip()
            p = obtener_producto_por_codigo(codigo)
            if p == None:
                print("Producto no Encontrado.")
            else:
                listar_producto_buscado(p)
        elif opcion_p == "3":
            descripcion = input("Ingrese Nombre del Producto: ").strip()
            p = obtener_producto_por_descripcion(descripcion)
            if p == None:
                print("Producto no Encontrado.")
            else:
                listar_producto_buscado(p)
        elif opcion_p == "4":
            codigo = input("Ingrese Código del Producto a Borrar: ").strip()
            p = obtener_producto_por_codigo(codigo)
            if p is None:
                print("Producto no Encontrado.")
            else:
                productos.remove(p)
                print("Producto Borrado.")
        elif opcion_p == "5":
            listar_productos()
        elif opcion_p == "6":
            break
        else:
            print("Opción inválida")

def crear_producto():
    '''
    Crea un diccionario que representa un producto.
    Retorna un diccionario con la información del producto.
    Incluye validaciones de entrada.
    '''
    while True:
        codigo = input("Código: ").strip()
        if not codigo:
            print("El código no puede estar vacío.")
            continue
        if any(p["id"] == codigo for p in productos):
            print("Ya existe un producto con ese código. Intente con otro.")
            continue
        break

    while True:
        nombre = input("Nombre: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío.")
            continue
        break

    while True:
        try:
            precio = float(input("Precio: ").strip())
            if precio <= 0:
                print("El precio debe ser mayor a 0.")
                continue
            break
        except ValueError:
            print("Ingrese un número válido para el precio.")

    while True:
        try:
            stock = int(input("Stock: ").strip())
            if stock < 0:
                print("El stock no puede ser negativo.")
                continue
            break
        except ValueError:
            print("Ingrese un número entero válido para el stock.")

    datos = {
        "id": codigo,
        "nombre": nombre,
        "precio": precio,
        "stock": stock
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
    - Producto: dict (un producto) o list[dict] (varios productos)
    - Si no hay productos, indica que no hay productos cargados.
    Retorna None.
    '''
    if not Producto:
        print("No hay productos cargados.")
        return

    if isinstance(Producto, dict):
        productos_lista = [Producto]
    else:
        productos_lista = Producto

    headers = list(productos_lista[0].keys())
    tabla = [[p[h] for h in headers] for p in productos_lista]

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

def obtener_producto_por_descripcion(descripcion):
    '''
    Busca productos por su descripción usando expresiones regulares.
    - descripcion: str (patrón de búsqueda)
    Retorna una lista con los productos encontrados.
    Si no encuentra nada, retorna una lista vacía.
    '''
    encontrados = []
    for p in productos:
        if re.search(descripcion, p["nombre"], re.IGNORECASE):
            encontrados.append(p)
    
    print(encontrados)
    
    return encontrados