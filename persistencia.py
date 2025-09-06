# Guardado y carga de datos en JSON
import json, os

def cargar_productos(id_producto: int, nombre: str, descripcion: str, precio: float):
    '''
    Cargar productos en archivo json
    Parámetros:
    - id_producto: ID del producto
    - nombre: Nombre del producto
    - descripción: Descripción del producto
    - precio: Precio del producto
    Return:
    - Confirmación
    '''
    try:
        file_location = os.path.dirname(__file__)
        file_path = file_location + "\src\database.json"

        with open(file_path, 'r', encoding='utf-8') as file:
            print(file)

    except Exception as e:
        print("Error al leer el archivo", e)


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

cargar_productos(2, "Maria", "Mate y Bombilla", 99.99)