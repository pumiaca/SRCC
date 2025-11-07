import re
from datetime import datetime
import tabulate
import persistencia as p

def proyectarIngresos(desdeFecha):
    """
    Si el usuario ingresa como parametro una fecha 10 dias antes del presente, se proyectaria lo estimado 10 dias en el futuro

    Parámetros:
        desdeFecha (str): Fecha de inicio en formato 'YYYY-MM-DD'.

    Return:
        dict: Datos de la proyección (promedio diario, días, proyección total).
    """

    try:
        # Validar formato de fecha
        formatoFecha = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(formatoFecha, desdeFecha):
            raise ValueError("Formato de fecha inválido. Use 'YYYY-MM-DD'.")

        # Convertir a objeto datetime para usarlo despues y valida q sea coherente
        fechaInicio = datetime.strptime(desdeFecha, "%Y-%m-%d")
        fechaActual = datetime.now()
        diasPeriodo = (fechaActual - fechaInicio).days

        if diasPeriodo <= 0:
            raise ValueError("La fecha de inicio debe ser anterior a la actual.")

        # Leer las ventas.json
        ventas = p.leer("ventasFakeParaTest")
        if not ventas:
            raise ValueError("No se encontraron registros en ventas.json.")

        # Filtrar ventas dentro del rango [fechaInicio, fechaActual]
        ventasPeriodo = [
            v for v in ventas
            if "fecha" in v and
                datetime.strptime(v["fecha"], "%Y-%m-%d") >= fechaInicio and
                datetime.strptime(v["fecha"], "%Y-%m-%d") <= fechaActual
        ]

        if not ventasPeriodo:
            raise ValueError("No se encontraron ventas en el periodo seleccionado.")

        # Calcular promedio diario
        totales = [v["total"] for v in ventasPeriodo]
        promedioDiario = sum(totales) / diasPeriodo

        # Lambda para calcular proyección
        calcularProyeccion = lambda promedio, dias: round(promedio * dias, 2)
        proyeccionFutura = calcularProyeccion(promedioDiario, diasPeriodo)

        # Generar item del diccionario de resultados
        resultado = {
            "id": len(p.leer("proyeccion_ingresos")) + 1,
            "fechaGeneracion": fechaActual.strftime("%Y-%m-%d"),
            "periodoHistorico": f"{desdeFecha} → {fechaActual.strftime('%Y-%m-%d')}",
            "diasAnalizados": diasPeriodo,
            "promedioDiario": round(promedioDiario, 2),
            "proyeccionFutura": proyeccionFutura
        }

        # Guardar usando el modulo de persistencia
        p.cargar("proyeccionIngresos", resultado)

        print(f"Período analizado: {diasPeriodo} días")
        print(f"Promedio diario: ${resultado['promedio_diario']}")
        print(f"Proyección para los próximos {diasPeriodo} días: ${resultado['proyeccion_futura']}")

        return resultado

    except (ValueError, KeyError, TypeError) as e:
        print(f"Error en proyectarIngresos(): {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

def mostrarTopVentas(desdeFecha, hastaFecha, top: int = 5):
    """
    Muestra los productos más vendidos en un período dado.
    
    Parámetros:
        desdeFecha: fecha inicio de la muestra
        hastaFecha: fecha cierre de muestra
    
    Retorna:
        None (imprime una tabla con los productos top en el período).
    """
    try:
        formatoFecha = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(formatoFecha, desdeFecha) or not re.match(formatoFecha, hastaFecha):
            raise ValueError("Formato de fecha inválido. Use 'YYYY-MM-DD'.")
        
        if desdeFecha > hastaFecha:
            raise ValueError("La fecha 'desde' debe ser anterior o igual a la fecha 'hasta'.")


        # Leer JSON
        ventas = p.leer("ventasFakeParaTest")

        if not ventas:
            raise FileNotFoundError("No se encontraron registros de ventas.")

        # Filtrar ventas entre fechas (incluyendolas)
        ventasFiltradas = [
            v for v in ventas
            if desdeFecha <= v["fecha"] <= hastaFecha
        ]

        if not ventasFiltradas:
            print("No hay ventas registradas en el período seleccionado.")
            return

        # Agrupar por producto
        resumen = {}
        for v in ventasFiltradas:
            pid = v["producto_id"]
            if pid not in resumen:
                resumen[pid] = {"cantidad": 0, "total": 0.0}
            resumen[pid]["cantidad"] += v["cantidad"]
            resumen[pid]["total"] += v["total"]

        # Ordenar productos por total vendido (descendente) con una lambda como criterio (?)
        topVentas = sorted(
            resumen.items(),
            key=lambda item: item[1]["total"],
            reverse=True
        )[:top]

        # Preparar datos para la tabla
        tabla = [
            [producto, datos["cantidad"], f"${datos['total']:.2f}"]
            for producto, datos in topVentas
        ]

        headers = ["Producto ID", "Cantidad Vendida", "Total Ingresos"]

        print("TOP VENTAS")
        print(tabulate(tabla, headers=headers, tablefmt="grid"))

    except FileNotFoundError as e:
        print(f"Error de archivo: {e}")
    except ValueError as e:
        print(f"Error de validación: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def calcularROI(desdeFecha, hastaFecha):
    """
    Calcula el ROI: El ROI (Return on Investment) 
    mide la rentabilidad de una inversión, es decir, cuánto se ganó o perdió respecto al costo total de inversión.

    Parámetros:
        desdeFecha: comienzo de la muestra
        hastaFecha: fin de la muestra

    Retorna:
        float: ROI expresado en porcentaje (%).
    """
    try:
        # Validación del formato de fecha
        formatoFecha = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(formatoFecha, desdeFecha) or not re.match(formatoFecha, hastaFecha):
            raise ValueError("Formato de fecha inválido. Use 'YYYY-MM-DD'.")

        # Conversión a datetime para comparar orden
        fechaDesde = datetime.strptime(desdeFecha, "%Y-%m-%d")
        fechaHasta = datetime.strptime(hastaFecha, "%Y-%m-%d")

        if fechaDesde > fechaHasta:
            raise ValueError("La fecha 'desde' debe ser anterior o igual a la fecha 'hasta'.")

        # Leer archivos de persistencia
        ventas = p.leer("ventasFakesParaTest")
        compras = p.leer("comprasFakesParaTest")

        if not ventas:
            raise FileNotFoundError("No se encontraron registros de ventas.")
        if not compras:
            raise FileNotFoundError("No se encontraron registros de compras.")

        # Recorrer los items de los json por fecha <=
        ventasPeriodo = [
            v for v in ventas
            if datetime.strptime(v["fecha"], "%Y-%m-%d") >= fechaDesde
            and datetime.strptime(v["fecha"], "%Y-%m-%d") <= fechaHasta
        ]
        comprasPeriodo = [
            c for c in compras
            if datetime.strptime(v["fecha"], "%Y-%m-%d") >= fechaDesde
            and datetime.strptime(v["fecha"], "%Y-%m-%d") <= fechaHasta
        ]

        if not ventasPeriodo or not comprasPeriodo:
            print("No hay suficientes datos en el período seleccionado.")
            return None

        # Calcular ingresos y egresos totales y el famoso dividir por cero
        totalIngresos = sum([v["total"] for v in ventasPeriodo])
        totalEgresos = sum([c["total"] for c in comprasPeriodo])

        if totalEgresos == 0:
            raise ZeroDivisionError("Los egresos son cero, no se puede calcular ROI.")

        # Calcular ROI en una lambda ;)
        calcularROI = lambda ingresos, egresos: ((ingresos - egresos) / egresos) * 100
        roi = calcularROI(totalIngresos, totalEgresos)

        # Mostrar resultados
        print(f"ANÁLISIS DE RENTABILIDAD (ROI)")
        print(f"Período: {desdeFecha} → {hastaFecha}")
        print(f"Ingresos Totales: ${totalIngresos:,.2f}")
        print(f"Egresos Totales:  ${totalEgresos:,.2f}")
        print(f"ROI: {roi:.2f}%")

        return roi

    except FileNotFoundError as e:
        print(f"Error de archivo: {e}")
    except ValueError as e:
        print(f"Error de validación: {e}")
    except ZeroDivisionError as e:
        print(f"Error matemático: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")


calcularROI("2025-10-25", "2025-11-05")