# Guardado y carga de datos en JSON

async def cargar_productos(id_producto, nombre, descripción, precio):
    '''
    Cargar productos en archivo json
    tipo: async def
    Parámetros:
    - id_producto: ID del producto
    - nombre: Nombre del producto
    - descripción: Descripción del producto
    - precio: Precio del producto
    Return:
    - Confirmación
    '''

async def cargar_ventas(id_venta, id_cliente, id_producto, cantidad, precio):
    '''
    Cargar ventas en archivo json
    tipo: async def
    Parámetros:
    - id_venta: ID de la venta
    - id_cliente: ID del cliente
    - id_producto: ID del producto
    - cantidad: Cantidad vendida
    - precio: Precio de venta
    Return:
    - Confirmación
    '''

async def cargar_compras(id_compra, id_proveedor, id_producto, cantidad, precio):
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

async def cargar_proveedor(id_proveedor, nombre, contacto):
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

async def cargar_clientes(id_cliente, nombre, email, telefono):
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

async def eliminar_elemento(lista, id_elemento):
    '''
    Eliminar un elemento de una lista
    tipo: async def
    Parámetros:
    - lista: La lista de la que se eliminará el elemento (proveedores, clientes, productos, ventas, compras)
    - id_elemento: El ID del elemento a eliminar
    Return:
    - Confirmación
    '''