from productos import menu_productos, listar_producto_buscado, crear_producto, agregar_producto, listar_productos, productos, obtener_producto_por_codigo
from stock import menu_stock, verificar_stock, actualizar_stock

def menu():
    while True:
        print("\n=== SISTEMA DE CONTROL COMERCIAL ===")
        print("1. Productos")
        print("2. Gestion de stock")
        print("3. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            menu_productos()
        elif opcion == "2":
            menu_stock()
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    menu()