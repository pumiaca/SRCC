import re
import tabulate

# Cálculo de ingresos, egresos y balance

def calcularIngresos(ventas, desdeFecha, hastaFecha): 
    """
    Calcula el total de ingresos en un período dado y muestra
    los resultados en una tabla con tabulate, con manejo de excepciones.

    Parámetros:
        ventas (list[dict]): Lista de ventas, cada una con al menos 'fecha' y 'total'.
        desdeFecha, hastaFecha (int): Índices para hacer slicing sobre la lista ventas.
    
    Retorna:
        str: Tabla formateada con las ventas y una fila de totales.
    """

    iva = 0.21

    try:
        # Intentar extraer el rango de ventas
        detalle = ventas[desdeFecha:hastaFecha]

        if not detalle:
            raise ValueError("No se encuentran registros en el periodo seleccionado.")

        # Validar formato de fecha
        primeraFecha = detalle[0]['fecha']
        regexFecha = r"^\d{4}-\d{2}-\d{2}$"

        if not re.match(regexFecha, primeraFecha):
            raise ValueError(f"Fecha inválida: {primeraFecha}")

        # Lambda para calcular IVA
        calcularIVA = lambda total: total * iva

        # Calcular totales
        totalIngresos = sum([venta['total'] for venta in detalle])
        totalIVA = sum([calcularIVA(venta['total']) for venta in detalle])

        # Crear tabla
        headers = list(detalle[0].keys()) + ["IVA"]
        tabla = [
            [v[h] for h in detalle[0].keys()] + [calcularIVA(v['total'])] for v in detalle
        ]

        # Agregar fila total
        filaTotales = ["TOTAL", "", totalIngresos, totalIVA]
        tabla.append(filaTotales)

        return tabulate(tabla, headers=headers, tablefmt="grid")

    except IndexError:
        return "Error: los índices seleccionados están fuera del rango de la lista."
    except KeyError as e:
        return f"Error: falta la clave {e} en uno de los registros."
    except TypeError:
        return "Error: los valores de 'total' deben ser numéricos."
    except ValueError as ve:
        return f"Error de validación: {ve}"
    except Exception as e:
        return f"Ocurrió un error inesperado: {e}"

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

    try:
        # Intentar obtener el rango de compras
        detalle = compras[desdeFecha:hastaFecha]

        if not detalle:
            raise ValueError("No se encuentran registros de compras en el periodo seleccionado.")

        # Validar formato de fecha
        primeraFecha = detalle[0]['fecha']
        regexFecha = r"^\d{4}-\d{2}-\d{2}$"

        if not re.match(regexFecha, primeraFecha):
            raise ValueError(f"Fecha inválida: {primeraFecha}")

        # Lambda para calcular IVA de una compra
        calcularIVA = lambda total: total * iva

        # Calcular totales
        totalEgresos = sum([compra['total'] for compra in detalle])
        totalIVA = sum([calcularIVA(compra['total']) for compra in detalle])

        # Crear tabla
        headers = list(detalle[0].keys()) + ["IVA"]
        tabla = [
            [c[h] for h in detalle[0].keys()] + [calcularIVA(c['total'])] for c in detalle
        ]

        # Agregar fila total
        filaTotales = ["TOTAL", "", totalEgresos, totalIVA]
        tabla.append(filaTotales)

        return tabulate(tabla, headers=headers, tablefmt="grid")

    except IndexError:
        return "Error: los índices seleccionados están fuera del rango de la lista."
    except KeyError as e:
        return f"Error: falta la clave {e} en uno de los registros de compras."
    except TypeError:
        return "Error: los valores de 'total' deben ser numéricos."
    except ValueError as ve:
        return f"Error de validación: {ve}"
    except Exception as e:
        return f"Ocurrió un error inesperado: {e}"
    
def balance(ventas, compras, desdeVenta, hastaVenta, desdeCompra, hastaCompra):

    '''
    Calcula el balance financiero entre ingresos (ventas) y egresos (compras).
    
    Parámetros:
        ventas (list[dict]): Lista de ventas con 'fecha' y 'total'.
        compras (list[dict]): Lista de compras con 'fecha' y 'total'.
        desdeVenta, hastaVenta (int): Índices de rango para ventas.
        desdeCompra, hastaCompra (int): Índices de rango para compras.
    
    Retorna:
        Tabla formateada con resumen financiero del período.
    '''

    try:

        iva = 0.21
        calcularIVA = lambda total: total * iva

        detalleVentas = ventas[desdeVenta:hastaVenta]
        detalleCompras = compras[desdeCompra:hastaCompra]

        if not detalleVentas and not detalleCompras:
            return "No se encuentran registros en el periodo seleccionado."

        # Totales de ingresos
        totalIngresos = sum([v['total'] for v in detalleVentas])
        totalIVA_ing = sum([calcularIVA(v['total']) for v in detalleVentas])

        # Totales de egresos
        totalEgresos = sum([c['total'] for c in detalleCompras])
        totalIVA_egr = sum([calcularIVA(c['total']) for c in detalleCompras])

        # Resultado neto
        resultado = totalIngresos - totalEgresos
        estado = "GANANCIA" if resultado >= 0 else "PÉRDIDA"

        tabla = [
            ["Ingresos", totalIngresos, totalIVA_ing],
            ["Egresos", totalEgresos, totalIVA_egr],
            ["", "", ""],
            ["Resultado neto", resultado, estado]
        ]

        headers = ["Concepto", "Monto ($)", "IVA / Estado"]

        return tabulate(tabla, headers=headers, tablefmt="grid")

    except (KeyError, TypeError, IndexError) as e:
        return f"Error al calcular el balance: {e}"
    except Exception as e:
        return f"Ocurrió un error inesperado: {e}"