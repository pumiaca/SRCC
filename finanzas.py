import re
import tabulate

# Cálculo de ingresos, egresos y balance

def calcularIngresos(ventas, desdeFecha, hastaFecha):
    """
    Calcula el total de ingresos en un período dado.

    Parámetros:
        ventas (dict): Lista de ventas, cada una con al menos 'fecha' y 'total'.
        inicio, fin: INDICES para hacer slicing sobre la lista ventas
        desdeFecha, hastaFecha (str): Fecha final en formato 'YYYY-MM-DD'.
    
    Retorna:
        
    """

    iva = 0.21
    detalle = ventas[desdeFecha:hastaFecha]

    if not detalle:
        return print("No se encuentran registros en el periodo seleccionado.")

    # validar fecha con regex
    desdeFecha = detalle[0]['fecha']
    
    regexFecha = r"^\d{4}-\d{2}-\d{2}$"

    if not re.match(regexFecha, desdeFecha):
        raise ValueError(f"Fecha inválida: {desdeFecha}")

    # función lambda para calcular IVA de una venta
    calcularIVA = lambda total: total * iva

    # list comprehension + sum para ingresos
    totalIngresos = sum([venta['total'] for venta in detalle])

    # sumatoria de impuestos
    totalIVA = sum([calcularIVA(venta['total']) for venta in detalle])

    headers = list(detalle[0].keys()) + ['IVA']
    tabla = [[v[h] for h in detalle[0].keys()] + [calcularIVA(v['total'])] for v in detalle]

    listaTotales = ['TOTAL','',totalIngresos,totalIVA]
    tabla.append(listaTotales)

    return tabulate.tabulate(tabla, headers=headers, tablefmt="grid")



def calcularEgresos(compras, desdeFecha, hastaFecha):
    """
    Calcula el total de egresos en un período dado.

    Parámetros:
        compras (dict): Lista de compras, cada una con al menos 'fecha' y 'total'.
        desdeFecha, hastaFecha (int): Índices para hacer slicing sobre la lista de compras.
    
    Retorna:
        tuple: (fecha_inicio, totalEgresos, totalIVA)
            - fechaInicio (str): Fecha de la primera compra en el rango.
            - totalEgresos (float): Suma total de los egresos en el período.
            - totalIVA (float): Total de IVA pagado en las compras.
    """

    iva = 0.21
    detalle = compras[desdeFecha:hastaFecha]

    if not detalle:
        return print("No se encuentran registros de compras en el periodo seleccionado.")

    # validar fecha con regex
    desdeFecha = detalle[0]['fecha']
    
    regexFecha = "^\d{4}-\d{2}-\d{2}$"

    if not re.match(regexFecha, desdeFecha):
        raise ValueError(f"Fecha inválida: {desdeFecha}")

    # función lambda para calcular IVA de una compra
    calcularIVA = lambda total: total * iva

    # list comprehension + sum para egresos
    totalEgresos = sum([compra['total'] for compra in detalle])

    # sumatoria de impuestos
    totalIVA = sum([calcularIVA(compra['total']) for compra in detalle])

    return (desdeFecha, totalEgresos, totalIVA)


def calcularBalance(ventas, compras, pagosProveedores, fechaInicio, fechaFin):
    pass


ventas = [
    {"id": "V1", "fecha": "2025-09-01", "total": 1000},
    {"id": "V2", "fecha": "2025-09-05", "total": 500},
    {"id": "V3", "fecha": "2025-09-10", "total": 2000}
]

print(calcularIngresos(ventas, 0,3))