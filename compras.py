from datetime import datetime
from productos import productos, obtener_producto_por_codigo, crear_producto, agregar_producto
from stock import actualizar_stock
from persistencia import leer, cargar, actualizar
from tabulate import tabulate
from utilidades import limpiar_consola

compras = []

def registrar_compra():
    '''
    Registra una compra, actualizando costo, stock y precio de venta del producto.
    '''
    limpiar_consola()
    productos_archivo = leer("productos")
    producto_id = input("Código de producto: ").strip()

    # Buscar producto en memoria o archivo
    prod_memoria = obtener_producto_por_codigo(producto_id)
    prod_archivo = next((p for p in productos_archivo if str(p.get("id")) == str(producto_id)), None)

    # Si el producto no existe, crear uno nuevo
    if prod_memoria is None and prod_archivo is None:
        print("El producto no existe. Vamos a crearlo.")
        p = crear_producto()
        if agregar_producto(p):
            print("Producto agregado.")
        else:
            print("Error al agregar producto.")
            return None
        prod_memoria = p
    elif prod_memoria is None and prod_archivo is not None:
        productos.append(prod_archivo)
        actualizar("productos", prod_archivo)
        prod_memoria = prod_archivo

    # Pedir datos de compra
    print("Registrando compra para el producto: ", prod_memoria["nombre"])
    texto = input("Cantidad a Comprar: ").strip()
    if not texto.isdigit():
        print("Cantidad inválida.")
        return None
    cantidad = int(texto)

    try:
        costo_unitario = float(input("Costo unitario (precio de compra): ").strip())
    except ValueError:
        print("Costo inválido.")
        return None

    try:
        precio_venta = float(input("Nuevo precio de venta (vacío = mantener actual): ").strip() or 0)
    except ValueError:
        print("Precio de venta inválido.")
        return None

    if cantidad <= 0 or costo_unitario <= 0:
        print("Error: cantidad y costo deben ser > 0.")
        return None

    # Fecha (vacío = hoy)
    fecha_txt = input("Fecha (YYYY-MM-DD, vacío = hoy): ").strip()
    fecha = fecha_txt if fecha_txt else datetime.now().strftime("%Y-%m-%d")

    # --- Actualización del producto ---
    prod_actual = obtener_producto_por_codigo(producto_id)
    if prod_actual:
        # Actualizar stock (suma la cantidad comprada)
        prod_actual["stock"] = prod_actual.get("stock", 0) + cantidad

        # Actualizar costo (precio de compra)
        prod_actual["costo"] = costo_unitario

        # Actualizar precio de venta si se ingresó un nuevo valor
        if precio_venta > 0:
            prod_actual["precio"] = precio_venta

        actualizar("productos", prod_actual) 

    registro = {
        "tipo": "compra",
        "fecha": fecha,
        "producto_id": producto_id,
        "cantidad": cantidad,
        "costo_unitario": float(costo_unitario),
        "precio_venta": float(precio_venta) if precio_venta else prod_actual.get("precio", 0),
        "total": float(costo_unitario) * cantidad,
    }

    compras.append(registro)
    cargar("compras", registro)
    print("Compra registrada y producto actualizado correctamente.")

    return registro

def listar_compras():
    '''
    Muestra compras en consola con nombre del producto, precios y formato de moneda.
    '''
    limpiar_consola()
    compras = []
    productos = []
    productos.extend(leer("productos"))
    compras.extend(leer("compras"))

    if not compras:
        print("No hay compras cargadas.")
        return

    compras_lista = [compras] if isinstance(compras, dict) else compras

    tabla = []
    for c in compras_lista:
        producto_id = c["producto_id"]

        # Buscar el producto en la lista por id
        producto = next((p for p in productos if str(p["id"]) == str(producto_id)), None)
        nombre_producto = producto["nombre"] if producto else f"ID {producto_id}"

        # Formatear los valores monetarios
        costo_unitario = f"${c['costo_unitario']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        precio_venta = f"${c.get('precio_venta', 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total = f"${c['total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        tabla.append([
            c["tipo"],
            c["fecha"],
            nombre_producto,
            c["cantidad"],
            costo_unitario,
            precio_venta,
            total
        ])

    headers = ["Tipo", "Fecha", "Producto", "Cantidad", "Costo Unitario", "Precio Venta", "Costo Total"]
    print(tabulate(tabla, headers=headers, tablefmt="grid"))

def menu_compras():
    '''
    Menú de compras.
    Permite registrar y listar compras.
    '''
    limpiar_consola()

    while True:
        print("\n=== COMPRAS ===")
        print("1. Registrar compra")
        print("2. Listar compras")
        print("3. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            registrar_compra()
        elif opcion == "2":
            listar_compras()
        elif opcion == "3":
            limpiar_consola()
            break
        else:
            print("Opción inválida.")
