import pytest
from productos import productos
from stock import verificar_stock, actualizar_stock

@pytest.fixture(autouse=True)
def limpiar_productos():
    """Limpia la lista global de productos antes de cada prueba."""
    productos.clear()
    yield
    productos.clear()

def test_verificar_stock_sin_productos(capfd):
    verificar_stock()
    out, s = capfd.readouterr()
    assert "No hay productos cargados" in out

def test_verificar_stock_con_productos_y_alerta(capfd):
    productos.extend([
        {"id": "001", "nombre": "Pan", "precio": 10.0, "stock": 2},
        {"id": "002", "nombre": "Leche", "precio": 15.0, "stock": 8},
    ])
    verificar_stock()
    out, s = capfd.readouterr()
    assert "Pan" in out
    assert "Leche" in out
    assert "Bajo stock" in out
    assert "OK" in out

def test_actualizar_stock_operacion_invalida(capfd):
    productos.append({"id": "001", "nombre": "Pan", "precio": 10.0, "stock": 10})
    actualizar_stock("001", 5, "donacion")
    out, s = capfd.readouterr()
    assert "Operación inválida" in out
    assert productos[0]["stock"] == 10

def test_actualizar_stock_producto_no_encontrado(capfd):
    productos.append({"id": "001", "nombre": "Pan", "precio": 10.0, "stock": 10})
    actualizar_stock("999", 5, "venta")
    out, s = capfd.readouterr()
    assert "Producto con código 999 no encontrado" in out
    assert productos[0]["stock"] == 10

def test_actualizar_stock_cantidad_invalida(capfd):
    productos.append({"id": "001", "nombre": "Pan", "precio": 10.0, "stock": 10})
    actualizar_stock("001", 0, "venta")
    out, s = capfd.readouterr()
    assert "La cantidad debe ser un número entero positivo" in out
    assert productos[0]["stock"] == 10

def test_actualizar_stock_venta_exitosa(capfd):
    productos.append({"id": "001", "nombre": "Pan", "precio": 10.0, "stock": 10})
    actualizar_stock("001", 4, "venta")
    out, s = capfd.readouterr()
    assert "Venta realizada" in out
    assert productos[0]["stock"] == 6
    assert "OK" not in out  # No imprime el estado de stock general

def test_actualizar_stock_venta_insuficiente(capfd):
    productos.append({"id": "001", "nombre": "Pan", "precio": 10.0, "stock": 3})
    actualizar_stock("001", 5, "venta")
    out, s = capfd.readouterr()
    assert "Stock insuficiente" in out
    assert productos[0]["stock"] == 3  # No cambia

def test_actualizar_stock_compra_exitosa(capfd):
    productos.append({"id": "001", "nombre": "Leche", "precio": 15.0, "stock": 5})
    actualizar_stock("001", 10, "compra")
    out, s = capfd.readouterr()
    assert "Compra registrada" in out
    assert productos[0]["stock"] == 15

def test_actualizar_stock_dispara_alerta_bajo_stock(capfd):
    productos.append({"id": "001", "nombre": "Pan", "precio": 10.0, "stock": 6})
    actualizar_stock("001", 2, "venta")
    out, s = capfd.readouterr()
    assert "Alerta: El producto 'Pan' tiene bajo stock" in out
    assert productos[0]["stock"] == 4