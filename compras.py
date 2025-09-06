def registrar_compra(compras, producto_id, cantidad, costo_unitario):
    """Registra una compra"""
    registro = {
        "tipo": "compra",
        "producto_id": producto_id,
        "cantidad": cantidad,
        "costo_unitario": float(costo_unitario),
        "total": float(costo_unitario) * cantidad,
    }
    compras.append(registro)
    return registro