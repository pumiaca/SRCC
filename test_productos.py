import productos

def prod(id="001", nombre="Pan", precio=10.5, stock=8):
    return {"id": id, "nombre": nombre, "precio": precio, "stock": stock}

def test_listar_productos_sin_datos(capsys):
    productos.leer = lambda clave: []
    productos.limpiar_consola = lambda: None
    productos.tabulate = lambda *a, **k: "TABLA_FAKE"

    productos.listar_productos()
    out = capsys.readouterr().out
    assert "No hay productos cargados." in out

def test_listar_productos_con_datos(capsys):
    productos.leer = lambda clave: [prod("001", "Pan", 10.5, 8)]
    productos.limpiar_consola = lambda: None
    productos.tabulate = lambda tabla, headers=None, tablefmt=None: str(tabla)

    productos.listar_productos()
    out = capsys.readouterr().out
    assert "001" in out and "Pan" in out

def test_listar_producto_buscado_dict(capsys):
    productos.leer = lambda clave: [prod()]
    productos.limpiar_consola = lambda: None
    productos.tabulate = lambda *a, **k: "TABLA_FAKE"

    productos.listar_producto_buscado(prod())
    out = capsys.readouterr().out
    assert "TABLA_FAKE" in out


def test_listar_producto_buscado_vacio(capsys):
    productos.leer = lambda clave: []
    productos.limpiar_consola = lambda: None
    productos.tabulate = lambda *a, **k: "TABLA_FAKE"

    productos.listar_producto_buscado(None)
    out = capsys.readouterr().out
    assert "No hay productos cargados." in out

def test_agregar_producto_nuevo(capsys):
    productos.leer = lambda clave: []
    productos.cargar = lambda clave, p: None
    productos.limpiar_consola = lambda: None

    p = prod()
    resultado = productos.agregar_producto(p)
    assert resultado is True

def test_agregar_producto_duplicado(capsys):
    productos.leer = lambda clave: [prod("001")]
    productos.cargar = lambda clave, p: None
    productos.limpiar_consola = lambda: None

    p = prod("001")
    resultado = productos.agregar_producto(p)
    out = capsys.readouterr().out
    assert not resultado
    assert "Ya existe un producto" in out

def test_obtener_producto_por_codigo_encontrado():
    p = prod("123")
    productos.leer = lambda clave: [p]
    productos.limpiar_consola = lambda: None

    encontrado = productos.obtener_producto_por_codigo("123")
    assert encontrado == p

def test_obtener_producto_por_codigo_no_encontrado():
    productos.leer = lambda clave: [prod("001")]
    productos.limpiar_consola = lambda: None

    encontrado = productos.obtener_producto_por_codigo("999")
    assert encontrado is None


def test_obtener_producto_por_descripcion_encontrado():
    lista = [prod("001", "Pan"), prod("002", "Leche")]
    productos.leer = lambda clave: lista
    productos.limpiar_consola = lambda: None

    encontrados = productos.obtener_producto_por_descripcion("pan")
    assert len(encontrados) == 1
    assert encontrados[0]["nombre"] == "Pan"


def test_obtener_producto_por_descripcion_no_encontrado():
    lista = [prod("001", "Pan")]
    productos.leer = lambda clave: lista
    productos.limpiar_consola = lambda: None

    encontrados = productos.obtener_producto_por_descripcion("queso")
    assert encontrados == []