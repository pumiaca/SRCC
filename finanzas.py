from tabulate import tabulate
import persistencia as p
from datetime import datetime as d
from utilidades import limpiar_consola

# Validacion de fechas (orden y formato)
def validacionFechas(desdeFecha,hastaFecha):

    formato = "%Y-%m-%d"
    try:
        desde = d.strptime(desdeFecha, formato)
        hasta = d.strptime(hastaFecha, formato)
    except ValueError:
        raise ValueError("Formato de fecha inválido o fecha inexistente. Use 'YYYY-MM-DD'.")
        
    if desde > hasta:
        raise ValueError("La fecha 'desde' debe ser anterior o igual a la fecha 'hasta'.")
    else:
        return desde, hasta
    
# Cálculo de ingresos, egresos y balance

def calcularIngresos(desdeFecha, hastaFecha): 
    """
    Calcula el total de ingresos en un período dado y muestra
    los resultados en una tabla con tabulate, con manejo de excepciones.

    Parámetros:
        ventas (json): archivo de ventas, cada una con al menos 'fecha' y 'total'.
        desdeFecha, hastaFecha (date): parametros de inicio y fin de la muestra.
    
    Retorna:
        str: Tabla formateada con las ventas y una fila de totales.
    """
    limpiar_consola()

    iva = 0.21

    try:
        # Intentar extraer la muestra de ventas
        desde, hasta = validacionFechas(desdeFecha, hastaFecha)
        ventas = p.leer('ventas')
        formato = "%Y-%m-%d"
        muestra = [v for v in ventas if desde <= d.strptime(v["fecha"],formato) <= hasta]

        if not muestra:
            raise ValueError("No se encuentran registros en el periodo seleccionado.")

        # Lambda para calcular IVA
        calcularIVA = lambda total: total * iva

        # Calcular totales
        totalIngresos = sum([t['total'] for t in muestra])
        totalIVA = sum([calcularIVA(t['total']) for t in muestra])

        # Crear tabla
        headers = list(muestra[0].keys()) + ["IVA"]
        tabla = [
            [v[h] for h in muestra[0].keys()] + [calcularIVA(v['total'])] for v in muestra
        ]

        # Agregar fila total
        filaTotales = ["TOTAL", "", totalIngresos, totalIVA]
        tabla.append(filaTotales)

        return tabulate(tabla, headers=headers, tablefmt="grid")

    except IndexError:
        return "Error: la muestra seleccionada está fuera del rango de la lista."
    except KeyError as e:
        return f"Error: la clave {e} no es uno de los registros."
    except TypeError:
        return "Error: los valores de 'total' deben ser numéricos."
    except ValueError as ve:
        return f"Error de validación: {ve}"
    except Exception as e:
        return f"Ocurrió un error inesperado: {e}"

def calcularEgresos(desdeFecha, hastaFecha): 
    """
    Calcula el total de EGRESOS en un período dado y muestra
    los resultados en una tabla con tabulate, con manejo de excepciones.

    Parámetros:
        ventas (json): archivo de compras, cada una con al menos 'fecha' y 'total'.
        desdeFecha, hastaFecha (date): parametros de inicio y fin de la muestra.
    
    Retorna:
        str: Tabla formateada con las compras y una fila de totales.
    """
    limpiar_consola()

    iva = 0.21

    try:
        # Intentar extraer la muestra de ventas
        desde, hasta = validacionFechas(desdeFecha, hastaFecha)
        compras = p.leer('compras')
        formato = "%Y-%m-%d"
        muestra = [c for c in compras if desde <= d.strptime(c["fecha"],formato) <= hasta]

        if not muestra:
            raise ValueError("No se encuentran registros en el periodo seleccionado.")

        # Lambda para calcular IVA
        calcularIVA = lambda total: total * iva

        # Calcular totales
        totalEgresos = sum([t['total'] for t in muestra])
        totalIVA = sum([calcularIVA(t['total']) for t in muestra])

        # Crear tabla
        headers = list(muestra[0].keys()) + ["IVA"]
        tabla = [
            [c[h] for h in muestra[0].keys()] + [calcularIVA(c['total'])] for c in muestra
        ]

        # Agregar fila total
        filaTotales = ["TOTAL", "", totalEgresos, totalIVA]
        tabla.append(filaTotales)

        return tabulate(tabla, headers=headers, tablefmt="grid")

    except IndexError:
        return "Error: la muestra seleccionada está fuera del rango de la lista."
    except KeyError as e:
        return f"Error: la clave {e} no es uno de los registros."
    except TypeError:
        return "Error: los valores de 'total' deben ser numéricos."
    except ValueError as ve:
        return f"Error de validación: {ve}"
    except Exception as e:
        return f"Ocurrió un error inesperado: {e}"

def balance(desdeVenta, hastaVenta, desdeCompra, hastaCompra):

    '''
    Calcula el balance financiero entre ingresos (ventas) y egresos (compras).
    
    Parámetros:
        ventas (json): Lista de ventas con 'fecha' y 'total'.
        compras (json): Lista de compras con 'fecha' y 'total'.
        desdeVenta, hastaVenta (str): Índices de rango para ventas.
        desdeCompra, hastaCompra (str): Índices de rango para compras.
    
    Retorna:
        Tabla formateada con resumen financiero del período.
    '''
    limpiar_consola()

    try:

        iva = 0.21
        calcularIVA = lambda total: total * iva

        # Validacion muestras ventas
        desdeV, hastaV = validacionFechas(desdeVenta, hastaVenta)
        ventas = p.leer('ventas')
        formato = "%Y-%m-%d"
        muestraVentas = [v for v in ventas if desdeV <= d.strptime(v["fecha"],formato) <= hastaV]

        #Validacion muestra compras
        desdeC, hastaC = validacionFechas(desdeCompra, hastaCompra)
        compras = p.leer('compras')
        formato = "%Y-%m-%d"
        muestraCompras = [c for c in compras if desdeC <= d.strptime(c["fecha"],formato) <= hastaC]

        if not muestraVentas and not muestraCompras:
            return "No se encuentran registros en el periodo seleccionado."

        # Totales de ingresos
        totalIngresos = sum([v['total'] for v in muestraVentas])
        totalIVAingresos = sum([calcularIVA(v['total']) for v in muestraVentas])

        # Totales de egresos
        totalEgresos = sum([c['total'] for c in muestraCompras])
        totalIVAegresos = sum([calcularIVA(c['total']) for c in muestraCompras])

        # Resultado neto
        resultado = totalIngresos - totalEgresos
        estado = "GANANCIA" if resultado >= 0 else "PÉRDIDA"

        tabla = [
            ["Ingresos", totalIngresos, totalIVAingresos],
            ["Egresos", totalEgresos, totalIVAegresos],
            ["", "", ""],
            ["Resultado neto", resultado, estado]
        ]

        headers = ["Concepto", "Monto ($)", "IVA / Estado"]

        return tabulate(tabla, headers=headers, tablefmt="grid")

    except IndexError:
        return "Error: la muestra seleccionada está fuera del rango de la lista."
    except KeyError as e:
        return f"Error: la clave {e} no es uno de los registros."
    except TypeError:
        return "Error: los valores de 'total' deben ser numéricos."
    except ValueError as ve:
        return f"Error de validación: {ve}"
    except Exception as e:
        return f"Ocurrió un error inesperado: {e}"
    
def menuFinanzas():
    '''
    Menú principal del módulo FINANZAS.
    '''
    limpiar_consola()

    while True:
        print("\n=== MENU DE FINANZAS ===")
        print("1. Calcular ingresos")
        print("2. Calcular egresos")
        print("3. Calcular balance")
        print("4. Regresar al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            desde = input("Ingrese fecha DESDE (YYYY-MM-DD): ").strip()
            hasta = input("Ingrese fecha HASTA (YYYY-MM-DD): ").strip()
            resultado = calcularIngresos(desde, hasta)
            print("\n" + str(resultado))

        elif opcion == "2":
            desde = input("Ingrese fecha DESDE (YYYY-MM-DD): ").strip()
            hasta = input("Ingrese fecha HASTA (YYYY-MM-DD): ").strip()
            resultado = calcularEgresos(desde, hasta)
            print("\n" + str(resultado))

        elif opcion == "3":
            print("\n=== BALANCE GENERAL ===")
            print("Rango de VENTAS:")
            desdeV = input("Ingrese fecha DESDE (YYYY-MM-DD): ").strip()
            hastaV = input("Ingrese fecha HASTA (YYYY-MM-DD): ").strip()
            print("\nRango de COMPRAS:")
            desdeC = input("Ingrese fecha DESDE (YYYY-MM-DD): ").strip()
            hastaC = input("Ingrese fecha HASTA (YYYY-MM-DD): ").strip()
            resultado = balance(desdeV, hastaV, desdeC, hastaC)
            print("\n" + str(resultado))

        elif opcion == "4":
            print("Regresando al menú principal...")
            break

        else:
            print("Opción inválida. Intente nuevamente.")
