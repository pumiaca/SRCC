from datetime import datetime as d
from tabulate import tabulate
import persistencia as p
from finanzas import validacionFechas
from utilidades import limpiar_consola

def proyectarIngresos(desdeFecha):
    """
    Si el usuario ingresa como parametro una fecha 10 dias antes del presente, se proyectaria lo estimado 10 dias en el futuro

    Parámetros:
        desdeFecha (str): Fecha de inicio en formato 'YYYY-MM-DD'.

    Return:
        dict: Datos de la proyección (promedio diario, días, proyección total).
    """
    limpiar_consola()

    try:
        # Validar formato de fecha, toma la fecha actual, usa el formato para pasarla a string para validacion quien la devuelve validada
        formato = "%Y-%m-%d"        
        fechaActual = d.now().strftime(formato)

        desde, hasta = validacionFechas(desdeFecha, fechaActual)
        ventas = p.leer('ventas')

        # Convertir a objeto date para usarlo despues y valida q sea coherente
        diasPeriodo = (hasta - desde).days

        if diasPeriodo <= 0:
            raise ValueError("La fecha de inicio debe ser anterior a la actual.")

        # Leer las ventas.json
        ventas = p.leer("ventas")
        if not ventas:
            raise ValueError("No se encontraron registros en ventas.json.")

        # Filtrar ventas dentro del rango [fechaInicio, fechaActual]
        ventasPeriodo = [
            v for v in ventas
            if "fecha" in v and
                d.strptime(v["fecha"], formato) >= desde and
                d.strptime(v["fecha"], formato) <= hasta
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
            "id": len(p.leer("proyeccionIngresos")) + 1,
            "fechaGeneracion": hasta.strftime(formato),
            "periodoHistorico": f"{desde} → {hasta.strftime(formato)}",
            "diasAnalizados": diasPeriodo,
            "promedioDiario": round(promedioDiario, 2),
            "proyeccionFutura": proyeccionFutura
        }

        # Guardar usando el modulo de persistencia
        p.actualizar("proyeccionIngresos", resultado)

        print(f"Período analizado: {diasPeriodo} días")
        print(f"Promedio diario: ${resultado['promedioDiario']}")
        print(f"Proyección para los próximos {diasPeriodo} días: ${resultado['proyeccionFutura']}")

        return resultado

    except ValueError as e:
        return f"Error: el valor {e} es invalido"
    except KeyError as e:
        return f"Error: la clave {e} no es valida"
    except TypeError as e:
        return f"Error inesperado: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

def mostrarTopVentas(desdeFecha, hastaFecha, top: int = 5):
    """
    Muestra los productos más vendidos en un período dado.
    
    Parámetros:
        desdeFecha: fecha inicio de la muestra
        hastaFecha: fecha cierre de muestra
    
    Retorna:
        None (imprime una tabla con los productos top en el período).
    """
    limpiar_consola()

    try:
        # Validar formato de fecha
        desde, hasta = validacionFechas(desdeFecha, hastaFecha)
        ventas = p.leer('ventas')
        formato = "%Y-%m-%d"

        if not ventas:
            raise FileNotFoundError("No se encontraron registros de ventas.")

        # Filtrar ventas entre fechas (incluyendolas)
        ventasFiltradas = [
            v for v in ventas
            if desde <= d.strptime(v["fecha"],formato) <= hasta
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
        totalesV = lambda item: item[1]["total"]

        topVentas = sorted(
            resumen.items(),
            key=totalesV,
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

    limpiar_consola()

    try:
        # Validacion muestras ventas
        desde, hasta = validacionFechas(desdeFecha, hastaFecha)
        ventas = p.leer('ventas')
        formato = "%Y-%m-%d"

        # Leer archivos de persistencia
        ventas = p.leer("ventas")
        compras = p.leer("compras")

        if not ventas or not compras:
            raise FileNotFoundError("No se encontraron registros de ventas.")

        # Recorrer los items de los json por fecha
        ventasPeriodo = [
            v for v in ventas
            if d.strptime(v["fecha"], formato) >= desde
            and d.strptime(v["fecha"], formato) <= hasta
        ]
        comprasPeriodo = [
            c for c in compras
            if d.strptime(c["fecha"], formato) >= desde
            and d.strptime(c["fecha"], formato) <= hasta
        ]

        if not ventasPeriodo or not comprasPeriodo:
            print("No hay suficientes registros en el período seleccionado.")
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
        print(f"Período: {desde} → {hasta}")
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

def menuAnaliticas():
    '''
    Menú principal del módulo ANALÍTICAS.
    '''

    limpiar_consola()

    while True:
        print("\n=== MENU DE ANALÍTICAS ===")
        print("1. Proyectar ingresos")
        print("2. Mostrar top ventas")
        print("3. Calcular ROI")
        print("4. Regresar al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            desde = input("Ingrese la fecha DESDE (YYYY-MM-DD): ").strip()
            resultado = proyectarIngresos(desde)
            print("\nResultado de la proyección:\n", resultado)

        elif opcion == "2":
            desde = input("Ingrese la fecha DESDE (YYYY-MM-DD): ").strip()
            hasta = input("Ingrese la fecha HASTA (YYYY-MM-DD): ").strip()
            top = int(input("¿Cuántos productos desea mostrar? (por defecto = 5): ").strip())
            mostrarTopVentas(desde, hasta, top)

        elif opcion == "3":
            desde = input("Ingrese la fecha DESDE (YYYY-MM-DD): ").strip()
            hasta = input("Ingrese la fecha HASTA (YYYY-MM-DD): ").strip()
            roi = calcularROI(desde, hasta)
            if roi is not None:
                print(f"\nROI calculado: {roi:.2f}%")

        elif opcion == "4":
            print("Regresando al menú principal...")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


calcularROI('2025-01-01', '2025-12-31')