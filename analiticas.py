import re
from datetime import datetime
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

import re
from tabulate import tabulate
from persistencia import leer

def mostrarTopVentas(desdeFecha: str, hastaFecha: str, top: int = 5):
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

        # Leer JSON
        ventas = leer("ventasFakeParaTest")

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

mostrarTopVentas("2025-10-10", "2025-11-05")
