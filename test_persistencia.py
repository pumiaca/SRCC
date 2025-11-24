import sys

sys.path.append('../')
from persistencia import *

def test_leer_datos():
    assert type(leer("test")) == type(list())

def test_cargar_datos():
    nuevo_producto = {
        "id": "9999",
        "nombre": "Producto de prueba",
        "precio": 100,
        "stock": 50
    }
    datos = cargar("test", nuevo_producto)
    datos = leer("test")

    assert any(dato["id"] == '9999' for dato in datos)

def test_modificar_datos():
    producto_modificado = {
        "id": "9999",
        "nombre": "Producto modificado",
        "precio": 150,
        "stock": 30
    }
    datos_modificados = actualizar("test", producto_modificado)
    assert any(dato["id"] == "9999" and dato["nombre"] == "Producto modificado" and dato["precio"] == 150 and dato["stock"] == 30 for dato in datos_modificados)


def test_buscar_por_id():
    dato_buscar = {"id" : '9999'}
    dato_encontrado = buscar_id("test", dato_buscar)

    assert any(dato["id"] == "9999" for dato in dato_encontrado)

def test_borrar_datos():
    producto_a_borrar = {"id": "9999"}
    datos_borrados = borrar("test", producto_a_borrar)
    assert not any(item["id"] == "9999" for item in datos_borrados)

def test_limpiar_datos():
    assert limpiar_datos("test")