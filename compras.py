# compras.py
from datetime import datetime
import json, os
from productos import productos, obtener_producto_por_codigo
from stock import actualizar_stock

compras = []

#  crear producto nuevo en JSON y en memoria 
def _agregar_producto_nuevo(producto_dict, ruta="productos.json"):
    # guardar en JSON 
    data = []
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
    data.append(producto_dict)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # reflejar en la lista 'productos' en memoria (si está)
    productos.append(producto_dict)

def registrar_compra():
    """Carga una compra por consola. Crea el producto si no existe y actualiza stock (+)."""
    producto_id = input("Código de producto: ").strip()
    prod = obtener_producto_por_codigo(producto_id)

    # si no existe, ofrecer crearlo para poder comprar
    if prod is None:
        print("El producto no existe. Vamos a crearlo para poder comprarlo.")
        nombre = input("Nombre del producto: ").strip()
        precio_txt = input("Precio de venta (vacío = 0): ").strip()
        try:
            precio = float(precio_txt) if precio_txt else 0.0
        except:
            print("Precio inválido. Se usará 0.")
            precio = 0.0
        prod = {"id": producto_id, "nombre": nombre or f"Prod-{producto_id}", "precio": precio, "stock": 0}
        _agregar_producto_nuevo(prod)

    # cantidad y costo
    txt = input("Cantidad: ").strip()
    if not txt.isdigit():
        print("Cantidad inválida.")
        return None
    cantidad = int(txt)

    try:
        costo_unitario = float(input("Costo unitario: ").strip())
    except:
        print("Costo inválido.")
        return None

    if cantidad <= 0 or costo_unitario <= 0:
        print("Error: cantidad y costo deben ser > 0.")
        return None

    fecha_txt = input("Fecha (YYYY-MM-DD, vacío = hoy): ").strip()
    fecha = fecha_txt if fecha_txt else datetime.now().strftime("%Y-%m-%d")

    # actualizar stock usando el módulo de stock +
    actualizar_stock(producto_id, cantidad, "compra")

    # guardar registro en la sesión 
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
