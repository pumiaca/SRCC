from datetime import datetime
from productos import productos, obtener_producto_por_codigo
from stock import actualizar_stock
from persistencia import leer, cargar, actualizar

compras = []

def registrar_compra():
    """Pide datos por consola. Si el producto no existe, lo crea."""
    productos_archivo = leer("productos") 

    producto_id = input("Código de producto: ").strip()

    
    prod_memoria = obtener_producto_por_codigo(producto_id)
    prod_archivo = next((p for p in productos_archivo if str(p.get("id")) == str(producto_id)), None)

    if (prod_memoria is None) and (prod_archivo is None):
        print("El producto no existe. Crealo.")
        nombre = input("Nombre del producto: ").strip()
        precio_txt = input("Precio de venta (vacío = 0): ").strip()
        try:
            precio = float(precio_txt) if precio_txt else 0.0
        except:
            print("Precio inválido. Se usará 0.")
            precio = 0.0
        nuevo = {"id": producto_id, "nombre": (nombre or f"Prod-{producto_id}"), "precio": precio, "stock": 0}
        cargar("productos", nuevo)
        productos.append(nuevo)
        prod_memoria = nuevo
    elif (prod_memoria is None) and (prod_archivo is not None):
        productos.append(prod_archivo)
        prod_memoria = prod_archivo

    texto = input("Cantidad: ").strip()
    if not texto.isdigit():
        print("Cantidad inválida.")
        return None
    cantidad = int(texto)

    try:
        costo_unitario = float(input("Costo unitario: ").strip())
    except:
        print("Costo inválido.")
        return None

    if cantidad <= 0 or costo_unitario <= 0:
        print("Error: cantidad y costo deben ser > 0.")
        return None

    """Fecha (vacío = hoy)"""
    fecha_txt = input("Fecha (YYYY-MM-DD, vacío = hoy): ").strip()
    fecha = fecha_txt if fecha_txt else datetime.now().strftime("%Y-%m-%d")

    """Actualizo stock en memoria"""
    actualizar_stock(producto_id, cantidad, "compra")
    prod_actual = obtener_producto_por_codigo(producto_id)
    if prod_actual:
        actualizar("productos", prod_actual)

    registro = {
        "tipo": "compra",
        "fecha": fecha,
        "producto_id": producto_id,
        "cantidad": cantidad,
        "costo_unitario": float(costo_unitario),
        "total": float(costo_unitario) * cantidad,
    }
    compras.append(registro)
    print("Compra registrada.")
    return registro

def listar_compras():
    """Muestra compras en consola."""
    if len(compras) == 0:
        print("No hay compras.")
        return
    numero = 1
    for c in compras:
        print(str(numero) + ". Fecha: " + str(c["fecha"]) +
              " | Producto: " + str(c["producto_id"]) +
              " | Cantidad: " + str(c["cantidad"]) +
              " | Costo: " + str(c["costo_unitario"]) +
              " | Total: " + str(c["total"]))
        numero = numero + 1

def menu_compras():
    while True:
        print("\n--- COMPRAS ---")
        print("1. Registrar compra")
        print("2. Listar compras")
        print("0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            registrar_compra()
        elif opcion == "2":
            listar_compras()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")
