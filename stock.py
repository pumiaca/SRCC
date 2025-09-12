# stock.py
# Control de stock
from tabulate import tabulate
from persistencia import cargar, leer, actualizar, borrar

def verificar_stock(producto, cantidad):
    '''
    Verifica si hay suficiente stock para una cantidad dada.
    - producto: dict (producto)
    - cantidad: int
    Retorna True si hay suficiente stock, False si no lo hay.
    '''
    if producto["stock"] >= int(cantidad):
        return True

    return False

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