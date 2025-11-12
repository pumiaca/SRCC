from datetime import datetime
from productos import productos, obtener_producto_por_codigo
from stock import actualizar_stock
from persistencia import leer, actualizar

ventas = []

def registrar_venta():
    """Pide datos por consola. Verifica existencia y stock."""
    productos_archivo = leer("productos")

    producto_id = input("Código de producto: ").strip()

    prod_memoria = obtener_producto_por_codigo(producto_id)
    prod_archivo = next((p for p in productos_archivo if str(p.get("id")) == str(producto_id)), None)

    if (prod_memoria is None) and (prod_archivo is None):
        print("Error: el producto no existe. Primero registrá una compra para crearlo/stockearlo.")
        return None
    elif (prod_memoria is None) and (prod_archivo is not None):
        productos.append(prod_archivo)
        prod_memoria = prod_archivo

    texto = input("Cantidad: ").strip()
    if not texto.isdigit():
        print("Cantidad inválida.")
        return None
    cantidad = int(texto)

    try:
        precio_unitario = float(input("Precio unitario: ").strip())
    except:
        print("Precio inválido.")
        return None

    if cantidad <= 0 or precio_unitario <= 0:
        print("Error: cantidad y precio deben ser > 0.")
        return None

    stock_actual = int(prod_memoria.get("stock", 0))
    if stock_actual < cantidad:
        print("Error: stock insuficiente. Hay " + str(stock_actual) + " y se pidió " + str(cantidad))
        return None

    """Fecha (vacío = hoy)"""
    fecha_txt = input("Fecha (YYYY-MM-DD, vacío = hoy): ").strip()
    fecha = fecha_txt if fecha_txt else datetime.now().strftime("%Y-%m-%d")

    """Actualizo stock en memoria"""
    actualizar_stock(producto_id, cantidad, "venta")
    prod_actual = obtener_producto_por_codigo(producto_id)
    if prod_actual:
        actualizar("productos", prod_actual)

    """Registro de venta"""
    registro = {
        "tipo": "venta",
        "fecha": fecha,
        "producto_id": producto_id,
        "cantidad": cantidad,
        "precio_unitario": float(precio_unitario),
        "total": float(precio_unitario) * cantidad,
    }
    ventas.append(registro)
    print("Venta registrada.")
    return registro


def listar_ventas():
    """Muestra ventas en consola."""
    if len(ventas) == 0:
        print("No hay ventas.")
        return
    numero = 1
    for v in ventas:
        print(str(numero) + ". Fecha: " + str(v["fecha"]) +
              " | Producto: " + str(v["producto_id"]) +
              " | Cantidad: " + str(v["cantidad"]) +
              " | Precio: " + str(v["precio_unitario"]) +
              " | Total: " + str(v["total"]))
        numero = numero + 1

def menu_ventas():
    while True:
        print("\n--- VENTAS ---")
        print("1. Registrar venta")
        print("2. Listar ventas")
        print("0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            registrar_venta()
        elif opcion == "2":
            listar_ventas()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")
