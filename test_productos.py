import pytest
import re
from productos import (
    productos,
    agregar_producto,
    obtener_producto_por_codigo,
    obtener_producto_por_descripcion,
    listar_productos,
    listar_producto_buscado
)

@pytest.fixture(autouse=True)
def limpiar_productos():
    """Limpia la lista global de productos antes de cada prueba."""
    productos.clear()
    yield
    productos.clear()

def test_agregar_producto_exitoso():
    p = {"id": "001", "nombre": "Pan", "precio": 10.0, "stock": 50}
    resultado = agregar_producto(p)
    assert resultado is True
    assert len(productos) == 1
    assert productos[0]["nombre"] == "Pan"

def test_agregar_producto_duplicado(capfd):
    p1 = {"id": "001", "nombre": "Pan", "precio": 10.0, "stock": 50}
    p2 = {"id": "001", "nombre": "Galletas", "precio": 5.0, "stock": 20}
    agregar_producto(p1)
    resultado = agregar_producto(p2)
    out, a = capfd.readouterr()
    assert "Ya existe un producto con ese código" in out
    assert resultado is False
    assert len(productos) == 1

def test_obtener_producto_por_codigo_encontrado():
    p = {"id": "A100", "nombre": "Leche", "precio": 20.0, "stock": 10}
    productos.append(p)
    resultado = obtener_producto_por_codigo("A100")
    assert resultado == p

def test_obtener_producto_por_codigo_no_encontrado():
    p = {"id": "A100", "nombre": "Leche", "precio": 20.0, "stock": 10}
    productos.append(p)
    resultado = obtener_producto_por_codigo("X999")
    assert resultado is None

def test_obtener_producto_por_descripcion_encontrado(capfd):
    productos.extend([
        {"id": "001", "nombre": "Pan", "precio": 10.0, "stock": 5},
        {"id": "002", "nombre": "Pan dulce", "precio": 15.0, "stock": 10},
        {"id": "003", "nombre": "Leche", "precio": 20.0, "stock": 8}
    ])
    resultado = obtener_producto_por_descripcion("Pan")
    out, a = capfd.readouterr()
    assert len(resultado) == 2
    assert all("Pan" in p["nombre"] for p in resultado)
    assert isinstance(resultado, list)

def test_obtener_producto_por_descripcion_no_encontrado(capfd):
    productos.append({"id": "001", "nombre": "Pan", "precio": 10.0, "stock": 5})
    resultado = obtener_producto_por_descripcion("Queso")
    out, a = capfd.readouterr()
    assert resultado == []
    assert "[]" in out  # se imprime la lista vacía

def test_listar_productos_vacio(capfd):
    listar_productos()
    out, a = capfd.readouterr()
    assert "No hay productos cargados" in out

def test_listar_productos_con_datos(capfd):
    productos.append({"id": "001", "nombre": "Pan", "precio": 10.0, "stock": 5})
    listar_productos()
    out, a = capfd.readouterr()
    assert "Pan" in out
    assert "Precio" not in out 

def test_listar_producto_buscado_uno(capfd):
    p = {"id": "A1", "nombre": "Pan", "precio": 10.0, "stock": 5}
    listar_producto_buscado(p)
    out, a = capfd.readouterr()
    assert "Pan" in out
    assert "Precio" not in out  
def test_listar_producto_buscado_lista(capfd):
    ps = [
        {"id": "A1", "nombre": "Pan", "precio": 10.0, "stock": 5},
        {"id": "A2", "nombre": "Leche", "precio": 15.0, "stock": 10},
    ]
    listar_producto_buscado(ps)
    out, p = capfd.readouterr()
    assert "Leche" in out and "Pan" in out