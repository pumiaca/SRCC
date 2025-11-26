import pytest
from datetime import datetime
from finanzas import validacionFechas, calcularIngresos, calcularEgresos, balance

# --- Datos Simulados para Persistencia (p.leer) ---
MOCK_DATA = {
    'ventas': [
        {'id': 1, 'fecha': '2025-10-15', 'total': 100.00},
        {'id': 2, 'fecha': '2025-10-20', 'total': 200.00},
        {'id': 3, 'fecha': '2025-11-01', 'total': 50.00},
        {'id': 4, 'fecha': '2025-11-10', 'total': 300.00},
        {'id': 5, 'fecha': '2025-11-15', 'total': 'invalido'}, 
        {'id': 6, 'fecha': '2025-11-20'}, 
    ],
    'compras': [
        {'id': 101, 'fecha': '2025-10-16', 'total': 40.00},
        {'id': 102, 'fecha': '2025-10-21', 'total': 60.00},
        {'id': 103, 'fecha': '2025-11-05', 'total': 10.00},
        {'id': 104, 'fecha': '2025-11-11', 'total': 150.00},
    ]
}

# --- Fixture para Simular Dependencias con 'mocker' ---

@pytest.fixture(autouse=True)
def setup_mocker(mocker):
    """
    Utiliza el fixture 'mocker' de pytest-mock para simular las dependencias. 
    """
    
    def mock_leer(clave):
        return MOCK_DATA.get(clave, [])
    
    mocker.patch('persistencia.leer', side_effect=mock_leer)

    mocker.patch('utilidades.limpiar_consola', return_value=None)


    def mock_tabulate(tabla, headers=None, tablefmt=None):
        return f"TABLA_FAKE_CON_DATOS: {tabla}" 

    mocker.patch('finanzas.tabulate', side_effect=mock_tabulate)

def test_validacionFechas_orden_correcto():
    """Verifica el parseo y el orden correcto."""
    desde, hasta = validacionFechas("2025-10-01", "2025-10-31")
    assert desde == datetime(2025, 10, 1)
    assert hasta == datetime(2025, 10, 31)

def test_validacionFechas_orden_incorrecto():
    """Prueba que 'desde' > 'hasta' lanza ValueError."""
    with pytest.raises(ValueError, match="La fecha 'desde' debe ser anterior o igual"):
        validacionFechas("2025-11-01", "2025-10-31")

def test_calcularIngresos_exito():
    """Verifica que el cálculo sea correcto para un rango válido."""
    resultado = calcularIngresos("2025-10-15", "2025-11-05")
    assert "TABLA_FAKE_CON_DATOS" in resultado
    assert "350.0" in resultado and "73.5" in resultado # 73.5 = 350 * 0.21

def test_calcularIngresos_sin_registros():
    """Verifica el error cuando no hay registros en el rango."""
    resultado = calcularIngresos("2026-01-01", "2026-01-31")
    assert "Error de validación: No se encuentran registros en el periodo seleccionado." in resultado

def test_calcularIngresos_type_error_total_no_numerico():
    """Verifica el manejo de TypeError (dato: 'total': 'invalido')."""
    resultado = calcularIngresos("2025-11-15", "2025-11-15")
    assert "Error: los valores de 'total' deben ser numéricos." in resultado

def test_calcularIngresos_key_error_falta_total():
    """Verifica el manejo de KeyError (falta la clave 'total')."""
    resultado = calcularIngresos("2025-11-20", "2025-11-20")
    assert "Error: la clave 'total' no es uno de los registros." in resultado



def test_calcularEgresos_exito():
    """Verifica que el cálculo de egresos sea correcto."""
    # Total esperado: 260.00
    resultado = calcularEgresos("2025-10-16", "2025-11-11")
    assert "TABLA_FAKE_CON_DATOS" in resultado
    assert "260.0" in resultado and "54.6" in resultado 

def test_calcularEgresos_sin_registros():
    """Verifica el error cuando no hay registros de egresos en el rango."""
    resultado = calcularEgresos("2026-01-01", "2026-01-31")
    assert "Error de validación: No se encuentran registros en el periodo seleccionado." in resultado

def test_balance_ganancia():
    """Verifica el balance con resultado positivo (GANANCIA)."""
    # Resultado neto esperado: 350.00 - 110.00 = 240.00
    resultado = balance("2025-10-15", "2025-11-01", "2025-10-16", "2025-11-05")
    assert "TABLA_FAKE_CON_DATOS" in resultado
    assert "240.0" in resultado
    assert "GANANCIA" in resultado

def test_balance_perdida():
    """Verifica el balance con resultado negativo (PÉRDIDA)."""
    # Resultado neto esperado: 50.00 - 150.00 = -100.00
    resultado = balance("2025-11-01", "2025-11-01", "2025-11-11", "2025-11-11")
    assert "TABLA_FAKE_CON_DATOS" in resultado
    assert "-100.0" in resultado
    assert "PÉRDIDA" in resultado

def test_balance_sin_registros_ambos():
    """Verifica el error si no hay registros en ninguno de los rangos."""
    resultado = balance("2026-01-01", "2026-01-31", "2026-01-01", "2026-01-31")
    assert "No se encuentran registros en el periodo seleccionado." in resultado