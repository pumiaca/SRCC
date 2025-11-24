import sys
sys.path.append('../')

import stock

def producto_ejemplo(codigo="001", nombre="Pan", stock_cant=10):
    return {"id": codigo, "nombre": nombre, "stock": stock_cant}

def test_verificar_stock_sin_productos(capsys):
    stock.leer = lambda clave: []
    stock.limpiar_consola = lambda: None
    stock.tabulate = lambda *args, **kwargs: "TABLA_VACIA"

    stock.verificar_stock()
    out = capsys.readouterr().out
    assert "No hay productos cargados." in out

def test_verificar_stock_con_productos(capsys):
    productos = [producto_ejemplo("001", "Pan", 8), producto_ejemplo("002", "Leche", 2)]
    stock.leer = lambda clave: productos
    stock.limpiar_consola = lambda: None
    stock.tabulate = lambda tabla, headers=None, tablefmt=None: str(tabla)

    stock.verificar_stock()
    out = capsys.readouterr().out
    assert "001" in out
    assert "002" in out
    assert "Bajo stock" in out

def test_actualizar_stock_operacion_invalida(capsys):
    stock.obtener_producto_por_codigo = lambda codigo: None
    stock.actualizar = lambda *a, **kw: None

    stock.actualizar_stock("001", 1, "invalida")
    out = capsys.readouterr().out
    assert "Operación inválida" in out


def test_actualizar_stock_producto_no_encontrado(capsys):
    stock.obtener_producto_por_codigo = lambda codigo: None
    stock.actualizar = lambda *a, **kw: None

    stock.actualizar_stock("999", 1, "venta")
    out = capsys.readouterr().out
    assert "no encontrado" in out.lower()


def test_actualizar_stock_cantidad_no_positiva(capsys):
    prod = producto_ejemplo(stock_cant=10)
    stock.obtener_producto_por_codigo = lambda codigo: prod
    fue_actualizado = {"ok": False}
    stock.actualizar = lambda *a, **kw: fue_actualizado.update(ok=True)

    stock.actualizar_stock("001", 0, "venta")
    out = capsys.readouterr().out
    assert "número entero positivo" in out
    assert not fue_actualizado["ok"]


def test_actualizar_stock_venta_suficiente(capsys):
    prod = producto_ejemplo(stock_cant=10)
    actualizado = {}

    def fake_actualizar(nombre, producto):
        actualizado.update(producto)

    stock.obtener_producto_por_codigo = lambda codigo: prod
    stock.actualizar = fake_actualizar

    stock.actualizar_stock("001", 3, "venta")
    out = capsys.readouterr().out
    assert "Venta realizada" in out
    assert actualizado["stock"] == 7


def test_actualizar_stock_venta_insuficiente(capsys):
    prod = producto_ejemplo(stock_cant=2)
    fue_actualizado = {"ok": False}

    stock.obtener_producto_por_codigo = lambda codigo: prod
    stock.actualizar = lambda *a, **kw: fue_actualizado.update(ok=True)

    stock.actualizar_stock("001", 5, "venta")
    out = capsys.readouterr().out
    assert "Stock insuficiente" in out
    assert not fue_actualizado["ok"]


def test_actualizar_stock_compra(capsys):
    prod = producto_ejemplo(stock_cant=4)
    actualizado = {}

    def fake_actualizar(nombre, producto):
        actualizado.update(producto)

    stock.obtener_producto_por_codigo = lambda codigo: prod
    stock.actualizar = fake_actualizar

    stock.actualizar_stock("001", 6, "compra")
    out = capsys.readouterr().out
    assert "Compra registrada" in out
    assert actualizado["stock"] == 10


def test_alerta_bajo_stock_se_muestra(capsys):
    prod = producto_ejemplo(nombre="Manteca", stock_cant=6)

    stock.obtener_producto_por_codigo = lambda codigo: prod
    stock.actualizar = lambda *a, **kw: None

    stock.actualizar_stock("001", 3, "venta")
    out = capsys.readouterr().out
    assert "Alerta" in out and "bajo stock" in out.lower()