from persistencia import *

def test_leer_datos():
    assert type(leer("test")) == type(list())
    assert type(leer("test")) == type(list())
    assert type(leer("test")) == type(list())

def test_cargar_datos():
    nuevo_producto = {
        "id": "9999",
        "nombre": "Producto de prueba",
        "precio": 100,
        "stock": 50
    }
    datos = cargar("test", nuevo_producto)
    assert any(item["id"] == "9999" for item in datos)
    assert any(item["nombre"] == "Producto de prueba" for item in datos)
    assert any(item["precio"] == 100 for item in datos)
    assert any(item["stock"] == 50 for item in datos)

def test_borrar_datos():
    producto_a_borrar = {
        "id": "9999"
    }
    datos_borrados = borrar("test", producto_a_borrar)
    assert not any(item["id"] == "9999" for item in datos_borrados)

def test_modificar_datos():
    producto_modificado = {
        "id": "9998",
        "nombre": "Producto modificado",
        "precio": 150,
        "stock": 30
    }
    datos_modificados = ("test", producto_modificado)
    assert any(item["id"] == "9998" and item["nombre"] == "Producto modificado" and item["precio"] == 150 and item["stock"] == 30 for item in datos_modificados)