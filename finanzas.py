# Cálculo de ingresos, egresos y balance

def calcularIngresos(ventas, desdeFecha, hastaFecha):
    """
    Calcula el total de ingresos en un período dado.

    Parámetros:
        ventas (list[dict(?)]): Lista de ventas, cada una con al menos 'fecha' y 'total'.
        desde (str): Fecha inicial en formato 'YYYY-MM-DD'.
        hasta (str): Fecha final en formato 'YYYY-MM-DD'.

    Devuelve:
        tuple:
            - total_ingresos
            - detalle
    """
    detalle = ventas[desdeFecha:hastaFecha]

    if not detalle:
        return print("No existen registros en ese periodo.")

    totalIngresos = 0
    for venta in detalle:
        totalIngresos += venta['total']

    fechaInicio = detalle[0]['fecha']

    return (fechaInicio, totalIngresos)



def calcularEgresos(compras, pagosProveedores, fechaInicio, fechaFin):
    """
    Calcula el total de egresos en un período dado.

    Parámetros:
        compras (list[dict]): Lista de compras registradas.
        pagosProveedores (list[dict]): Lista de pagos realizados a proveedores.
        desde (str): Fecha inicial en formato 'YYYY-MM-DD'.
        hasta (str): Fecha final en formato 'YYYY-MM-DD'.

    Devuelve:
        tuple:
            - totalEgresos (float): Suma de egresos en el rango.
            - egresosProveedor (dict): Egresos agrupados por proveedor.
    """
    pass


def calcularBalance(ventas, compras, pagosProveedores, fechaInicio, fechaFin):
    """
    Calcula el balance financiero del negocio.

    Parámetros:
        ventas (list[dict]): Lista de ventas registradas.
        compras (list[dict]): Lista de compras registradas.
        pagosProveedores (list[dict]): Lista de pagos realizados a proveedores.
        desde (str): Fecha inicial en formato 'YYYY-MM-DD'.
        hasta (str): Fecha final en formato 'YYYY-MM-DD'.

    Devuelve:
        dict: Resumen con:
            - "ingresos": total y detalle de ingresos.
            - "egresos": total y detalle de egresos.
            - "balance": diferencia entre ingresos y egresos.
            - "periodo": fechas de inicio y fin.
    """
    pass