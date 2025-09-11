# Guardado y carga de datos en JSON
import json

def cargar_productos(id_producto: int, nombre: str = "", descripcion: str = "", precio: float = 0.0):
    '''
        Cargar productos en archivo json
        Parámetros:
        - id_producto: ID de la producto
        - nombre: nombre del producto
        - descripcion: descripción del producto
        - precio: precio del producto
        Return:
        - Confirmación
    '''
    try:
        with open("./src/productos.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        
        all_ids = [item["id_producto"] for item in datos]

        if id_producto not in all_ids :
            
            max_id = max(all_ids)

        nuevo_producto = {
            "id": max_id + 1,
            "id_producto": id_producto,
            "nombre": nombre,
            "descripcion": descripcion,
            "precio": precio
        }

        if(nuevo_producto["id_producto"] in [items["id_producto"] for items in datos]):
            print("El producto ya existe.")
            return "El producto ya existe."
        else:
            datos.append(nuevo_producto)
            print("Producto agregado.")

        with open("./src/productos.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo)
        
    except FileNotFoundError:
        print("No hay un archivo aún, se creará uno nuevo.")
        datos = []
        datos.append({
            "id": 1,
            "id_producto": id_producto,
            "nombre": nombre,
            "descripcion": descripcion,
            "precio": precio
        })
        with open("./src/productos.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo)
    finally:
        print(datos)





def cargar_stock(id_producto, descripcion, cantidad):
    '''
        Cargar stock en archivo json
        Parámetros:
        - id_producto: ID del producto
        - descripcion: descripción del producto
        - cantidad: Cantidad en stock
        Return:
        - Confirmación
    '''
    try:
        with open("./src/stock.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        datos.append({
            "id_producto": id_producto,
            "descripcion": descripcion,
            "cantidad": cantidad
        })
        with open("./src/stock.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo)
        
    except FileNotFoundError:
        print("No hay un archivo aún, se creará uno nuevo.")
        datos = []
        datos.append({
            "id_producto": id_producto,
            "descripcion": descripcion,
            "cantidad": cantidad
        })
        with open("./src/stock.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo)
    
    finally:
        print(datos)

def eliminar_stock(id_producto, cantidad):
    '''
        Eliminar stock en archivo json
        Parámetros:
        - id_producto: ID del producto
        - cantidad: Cantidad en stock
        Return:
        - Confirmación
    '''
    try:
        with open("./src/stock.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        for item in datos:
            if item["id_producto"] == id_producto:
                item["cantidad"] -= cantidad
                print("Stock Restado")

        with open("./src/stock.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo)
        
    except FileNotFoundError:
        print("No hay un archivo aún.")
    
    finally:
        print(datos)

def cargar_ventas(id_venta, id_cliente, id_producto, cantidad, precio):
    '''
    Cargar ventas en archivo json
    Parámetros:
    - id_venta: ID de la venta
    - id_cliente: ID del cliente
    - id_producto: ID del producto
    - cantidad: Cantidad vendida
    - precio: Precio de venta
    Return:
    - Confirmación
    '''

def cargar_compras(id_compra, id_proveedor, id_producto, cantidad, precio):
    '''
    Cargar compras en archivo json
    tipo: async def
    Parámetros:
    - id_compra: ID de la compra
    - id_proveedor: ID del proveedor
    - id_producto: ID del producto
    - cantidad: Cantidad comprada
    - precio: Precio de compra
    Return:
    - Confirmación
    '''

def cargar_proveedor(id_proveedor, nombre, contacto):
    '''
    Cargar proveedores en archivo json
    tipo: async def
    Parámetros:
    - id_proveedor: ID del proveedor
    - nombre: Nombre del proveedor
    - contacto: Información de contacto del proveedor
    Return:
    - Confirmación
    '''

def cargar_clientes(id_cliente, nombre, email, telefono):
    '''
    Cargar clientes en archivo json
    tipo: async def
    Parámetros:
    - id_cliente: ID del cliente
    - nombre: Nombre del cliente
    - email: Email del cliente
    - telefono: Teléfono del cliente
    Return:
    - Confirmación
    '''

def eliminar_elemento(lista, id_elemento):
    '''
    Eliminar un elemento de una lista
    tipo: async def
    Parámetros:
    - lista: La lista de la que se eliminará el elemento (proveedores, clientes, productos, ventas, compras)
    - id_elemento: El ID del elemento a eliminar
    Return:
    - Confirmación
    '''


