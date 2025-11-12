from datetime import datetime
from productos import productos, obtener_producto_por_codigo
from stock import actualizar_stock
from persistencia import leer, actualizar, cargar
from utilidades import limpiar_consola
from tabulate import tabulate
from utilidades import limpiar_consola

ventas = []

def registrar_venta():
    '''
    Registra una venta usando el precio de venta del producto
    y actualiza el stock automáticamente.
    '''

    limpiar_consola()

    productos_archivo = leer("productos")
    producto_id = input("Código de producto: ").strip()

    # Buscar producto tanto en memoria como en archivo
    prod_memoria = obtener_producto_por_codigo(producto_id)
    prod_archivo = next((p for p in productos_archivo if str(p.get("id")) == str(producto_id)), None)

    if (prod_memoria is None) and (prod_archivo is None):
        print("Error: el producto no existe. Primero registrá una compra para crearlo/stockearlo.")
        return None
    elif (prod_memoria is None) and (prod_archivo is not None):
        productos.append(prod_archivo)
        prod_memoria = prod_archivo

    # Verificar cantidad
    texto = input("Cantidad a Vender: ").strip()
    if not texto.isdigit():
        print("Cantidad inválida.")
        return None
    cantidad = int(texto)

    if cantidad <= 0:
        print("Error: la cantidad debe ser mayor que 0.")
        return None

    # Tomar el precio de venta directamente del producto
    precio_unitario = float(prod_memoria.get("precio", 0))

    if precio_unitario <= 0:
        print("El producto no tiene un precio de venta configurado.")
        return None

    # Verificar stock
    stock_actual = int(prod_memoria.get("stock", 0))
    if stock_actual < cantidad:
        print(f"Stock insuficiente. Hay {stock_actual} unidades y se pidieron {cantidad}.")
        return None

    # Fecha automática o ingresada
    fecha_txt = input("Fecha (YYYY-MM-DD, vacío = hoy): ").strip()
    fecha = fecha_txt if fecha_txt else datetime.now().strftime("%Y-%m-%d")

    # Actualizar stock en memoria y archivo
    actualizar_stock(producto_id, cantidad, "venta")
    prod_actual = obtener_producto_por_codigo(producto_id)
    if prod_actual:
        actualizar("productos", prod_actual)

    # Registrar la venta
    total = precio_unitario * cantidad
    registro = {
        "tipo": "venta",
        "fecha": fecha,
        "producto_id": producto_id,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "total": total,
    }
    cargar("ventas", registro)

    print(f"Venta registrada: {cantidad} x {prod_memoria.get('nombre', 'Desconocido')} "
          f"a ${precio_unitario:.2f} = ${total:.2f}")
    return registro

def listar_ventas():
    '''
    Muestra las ventas en formato tabular, con nombre del producto y precios formateados.
    '''
    limpiar_consola()
    ventas = []
    productos = []
    ventas = leer("ventas")
    productos = leer("productos")

    if not ventas:
        print("No hay ventas cargadas.")
        return

    # Asegurar que sea una lista de diccionarios
    ventas_lista = [ventas] if isinstance(ventas, dict) else ventas

    tabla = []
    for v in ventas_lista:
        producto_id = v["producto_id"]

        # Buscar el producto por id
        producto = next((p for p in productos if str(p["id"]) == str(producto_id)), None)
        nombre_producto = producto["nombre"] if producto else f"ID {producto_id}"

        # Formatear los precios
        precio_unitario = f"${v['precio_unitario']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total = f"${v['total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        tabla.append([
            v["fecha"],
            nombre_producto,
            v["cantidad"],
            precio_unitario,
            total
        ])

    headers = ["Fecha", "Producto", "Cantidad", "Precio Venta", "Total de Venta"]
    print(tabulate(tabla, headers=headers, tablefmt="grid"))

def menu_ventas():
    '''
    Menú de ventas.
    Permite registrar y listar ventas.
    '''
    limpiar_consola()

    while True:
        print("\n=== VENTAS ===")
        print("1. Registrar venta")
        print("2. Listar ventas")
        print("3. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            registrar_venta()
        elif opcion == "2":
            listar_ventas()
        elif opcion == "3":
            limpiar_consola()
            break
        else:
            print("Opción inválida.")
