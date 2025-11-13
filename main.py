from productos import menu_productos, listar_producto_buscado, crear_producto, agregar_producto, listar_productos, productos, obtener_producto_por_codigo
from stock import menu_stock, verificar_stock, actualizar_stock
from compras import menu_compras, compras
from ventas import menu_ventas, ventas
from persistencia import leer, cargar, borrar, actualizar
from utilidades import limpiar_consola
from finanzas import menuFinanzas
from analiticas import menuAnaliticas

def menu():
    '''
    Menú principal del sistema de control comercial.
    Permite acceder a la gestión de productos, stock, ventas, compras, finanzas y analíticas.
    '''
    limpiar_consola()
    
    while True:
        print("\n=== SISTEMA DE CONTROL COMERCIAL ===")
        print("1. Productos")
        print("2. Gestión de stock")
        print("3. Compras")
        print("4. Ventas")
        print("5. Finanzas")
        print("6. Analíticas")
        print("7. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            menu_productos()
        elif opcion == "2":
            menu_stock()
        elif opcion == "3":
            menu_compras()
        elif opcion == "4":
            menu_ventas()
        elif opcion == "5":
            menuFinanzas()
        elif opcion == "6":
            menuAnaliticas()
        elif opcion == "7":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    menu()