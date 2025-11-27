# stock.py
# Control de stock
from tabulate import tabulate
from productos import productos, obtener_producto_por_codigo
from persistencia import actualizar, leer, cargar, borrar, generar_reporte, limpiar_datos
from utilidades import limpiar_consola,encabezador

OPERACIONES = ("venta", "compra")

def verificar_stock():
    '''
    Lista el stock de todos los productos y alerta si hay bajo stock.
    '''
    limpiar_consola()
    limpiar_datos("stock")

    productos = []
    productos.extend(leer("productos"))
    if not productos:
        encabezador("No hay productos cargados.")
        return

    headers = ["Código", "Nombre", "Stock", "Alerta"]
    tabla = []

    for p in productos:
        alerta = "Bajo stock" if p["stock"] < 5 else "OK"
        tabla.append([p["id"], p["nombre"], p["stock"], alerta])
        if alerta == "Bajo stock":
            cargar("stock",{
                "Código": p["id"],
                "Nombre": p["nombre"],
                "Stock": p["stock"],
                "Alerta": alerta})
    
    generar_reporte("stock")
    print(tabulate(tabla, headers=headers, tablefmt="grid"))


def actualizar_stock(codigo, cantidad, operacion):
    '''
    Actualiza el stock de un producto según la operación ("venta" o "compra").
    '''
    if operacion not in OPERACIONES:
        encabezador(f"Operación inválida. Solo se permiten: {OPERACIONES}")
        return

    producto = obtener_producto_por_codigo(codigo)
    if not producto:
        encabezador(f"Producto con código {codigo} no encontrado.")
        return

    if cantidad <= 0:
        encabezador("La cantidad debe ser un número entero positivo.")
        return

    if operacion == "venta":
        if producto["stock"] >= cantidad:
            producto["stock"] -= cantidad
            actualizar("productos", producto)
            encabezador(f"Venta realizada. Nuevo stock de {producto['nombre']}: {producto['stock']}")
        else:
            encabezador(f"Stock insuficiente para vender {cantidad} unidades.")
    elif operacion == "compra":
        producto["stock"] += cantidad
        actualizar("productos", producto)
        encabezador(f"Compra registrada. Nuevo stock de {producto['nombre']}: {producto['stock']}", caracter= "+")

    if producto["stock"] < 5:
        encabezador(f"Alerta: El producto '{producto['nombre']}' tiene bajo stock ({producto['stock']} unidades).", caracter="+")


def menu_stock():
    '''
    Menú principal de control de stock con validación de inputs.
    '''
    limpiar_consola()
    while True:
        encabezador("MENU DE GESTION DE STOCK")
        print("1. Verificar stock")
        print("2. Actualizar stock")
        print("3. Regresar al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            verificar_stock()

        elif opcion == "2":
            codigo = input("Ingrese código del producto: ").strip()
            if not codigo:
                encabezador("El código no puede estar vacío.")
                continue
                
            cantidad_input = input("Ingrese cantidad: ").strip()
            if not cantidad_input.isdigit() or int(cantidad_input) <= 0:
                encabezador("La cantidad debe ser un número entero positivo.")
                continue
            cantidad = int(cantidad_input)

            operacion = input("Ingrese operación (venta/compra): ").strip().lower()
            if operacion not in OPERACIONES:
                encabezador(f"Operación inválida. Solo se permiten: {OPERACIONES}")
                continue

            actualizar_stock(codigo, cantidad, operacion)

        elif opcion == "3":
            limpiar_consola()
            break
        else:
            encabezador("Opción inválida. Intente nuevamente.", ancho = 50, caracter="*")
