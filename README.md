#Proyecto Comercial - Algoritmos y Estructuras de Datos I

##Descripción
Este proyecto implementa un **sistema de registro y control comercial en Python**, desarrollado como trabajo práctico para la materia **Algoritmos y Estructuras de Datos I**.  
Permite gestionar productos, ventas y compras, calcular ingresos/egresos y mantener persistencia de datos en **JSON**.

---

##Objetivos
- Registrar productos.
- Registrar ventas y compras.
- Controlar y actualizar stock.
- Calcular ingresos, egresos y balance.
- Persistir datos en archivos **JSON** y exportarlos a otros formatos.
- Aplicar los contenidos vistos en la materia: funciones, listas, diccionarios, modularización, manejo de archivos, excepciones y pruebas unitarias.

---

##Estructura del proyecto
```
SRCC/
│── main.py              # Punto de entrada
│── productos.py         # ABM de productos
│── ventas.py            # Manejo de ventas y compras
│── stock.py             # Control de stock
│── finanzas.py          # Cálculo de ingresos y egresos
│── persistencia.py      # Guardado y carga de datos (JSON)
│── README.md            # Documentación del proyecto
│── .gitignore           # Archivos a ignorar en Git
```

---

##Ejecución
Para ejecutar el sistema, simplemente correr en consola:

```bash
python main.py
```

Se abrirá un menú interactivo con las siguientes opciones:
1. Agregar producto  
2. Listar productos  
3. Registrar venta  
4. Registrar compra  
5. Finanzas (ingresos, egresos, balance)   
6. Guardar datos  
7. Salir  

---

##Persistencia
El sistema guarda los datos en archivos JSON:
- `productos.json`
- `ventas.json`
- `compras.json`

De esta forma, la información se mantiene disponible entre ejecuciones.

---

##Tecnologías utilizadas
- Lenguaje: **Python 3**
- Paradigmas: programación estructurada y modular
- Estructuras de datos: listas, diccionarios, tuplas, conjuntos
- Persistencia: **JSON**
- Control de versiones: **Git/GitHub**
- Metodología: **SCRUM**

---

##Cronograma de entregas
- **Fase 1:** Definición de estructura JSON (10%)  
- **Fase 2:** Registro de productos y transacciones (20%)  
- **Fase 3:** Verificación de stock (40%)  
- **Fase 4:** Cálculo de finanzas (60%)  
- **Fase 5:** Persistencia en JSON/Excel (80%)  
- **Fase 6:** Pruebas y validación final (100%)  

---

##Autores
**Alexis José Salazar Pumiaca** 
**Guillermo Nicolas Rodriguez** 
**Lucas Jorge Garcia** 
**Thomas Lagruta** 
Facultad de Ingeniería - FAIN  
Departamento de Tecnología Informática

