def registrar_venta(ventas, producto_id, cantidad, precio_unitario):
    """Registra una venta"""
    registro = {
        "tipo": "venta",
        "producto_id": producto_id,
        "cantidad": cantidad,
        "precio_unitario": float(precio_unitario),
        "total": float(precio_unitario) * cantidad,
    }
    ventas.append(registro)
    return registro