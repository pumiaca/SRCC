# Análisis de datos y generación de reportes
from persistencia import *
import pandas as pd

def productos_mas_vendidos():
    # Función que devuelve los productos más vendidos
    
    datos = leer('ventas')
    datosdf = pd.DataFrame(datos)
    productos_mas_vendidos = datosdf.groupby(by='nombre').sum(['cantidad']).sort_values(by='cantidad', ascending=False).head(10)
    print(productos_mas_vendidos)
    return productos_mas_vendidos

def productos_mas_rentable():
    # Función que devuelve los productos más rentables (venta - costo)
    ventas = leer('ventas')
    compras = leer('compras')
    vdf = pd.DataFrame(ventas)
    cdf = pd.DataFrame(compras)
    join_df = pd.merge(vdf, cdf, on='id', suffixes=('_venta', '_compra'))
    join_df['rentabilidad'] = join_df['precio'] - join_df['costo_unitario']
    join_df = join_df[['id', 'nombre_venta', 'rentabilidad']]
    join_df = join_df.sort_values(by = 'rentabilidad', ascending=False)
    join_df = join_df.drop_duplicates(subset=['id'])
    print(join_df.head(10))
    return join_df
