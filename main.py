from productos import listar_producto_buscado, crear_producto, agregar_producto, listar_productos, productos, obtener_producto_por_codigo
from persistencia import leer, cargar, actualizar, borrar
from stock import verificar_stock, actualizar_stock


def cargar_datos_iniciales():
    productos.extend(leer("productos"))

def menu():
    while True:
        print("\n=== SISTEMA DE CONTROL COMERCIAL ===")
        print("1. Productos")
        print("2. Compras")
        print("3. Ventas")
        print("4. Gestion de stock")
        print("5. Proveedores")
        print("6. Finanzas")
        print("7. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            menu_productos()
        elif opcion == "7":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")

def menu_productos():
    cargar_datos_iniciales()
    while True:
        print("\n=== MENU DE PRODUCTOS ===")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Borrar producto")
        print("4. Listar productos")
        print("5. Regresar al menú principal")

        opcion_p = input("Seleccione una opción: ").strip()

        if opcion_p == "1":
            p = crear_producto()
            if agregar_producto(p):
                print("Producto agregado.")
        elif opcion_p == "2":
            codigo = input("Ingrese Código del Producto: ").strip()
            p = obtener_producto_por_codigo(codigo)
            if p == None:
                print("Producto no Encontrado.")
            else:
                listar_producto_buscado(p)
        elif opcion_p == "3":
            codigo = input("Ingrese Código del Producto a Borrar: ").strip()
            p = obtener_producto_por_codigo(codigo)
            if p is None:
                print("Producto no Encontrado.")
            else:
                productos.remove(p)
                borrar("productos", p)
                print("Producto Borrado.")
        elif opcion_p == "4":
            print(productos)
            listar_productos()
        elif opcion_p == "5":
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    menu()