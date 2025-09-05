# stock.py
# Control de stock

def verificar_stock(producto, cantidad):
    '''
    Verifica si hay suficiente stock para una cantidad dada.
    - producto: dict (producto)
    - cantidad: int
    Retorna True si hay suficiente stock, False si no lo hay.
    '''
    return producto["stock"] >= int(cantidad)

def actualizar_stock(producto, cantidad, operacion="venta"):
    '''
    Actualiza el stock de un producto según la operación.
    - producto: dict (producto)
    - cantidad: int
    - operacion: str ("venta" o "compra")
    Retorna None. Modifica el diccionario del producto directamente.
    '''
    cantidad = int(cantidad)
    if operacion == "venta":
        producto["stock"] -= cantidad
    elif operacion == "compra":
        producto["stock"] += cantidad