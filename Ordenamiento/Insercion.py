"""
Ejercicio: Método de Ordenamiento por Inserción (Insertion Sort)

Problema:
    Una tienda registra los precios de sus productos conforme van llegando
    al inventario. Se desea mostrar el catálogo ordenado por precio de
    MENOR a MAYOR.

Funcionamiento:
    Se toma cada elemento (desde el segundo) como "clave" y se inserta en
    la posición correcta dentro de la parte izquierda, que ya está ordenada,
    desplazando hacia la derecha los elementos mayores que la clave.
    Es como ordenar cartas en la mano.

Complejidad: O(n^2) en el peor caso, O(n) en el mejor (lista ya ordenada).
"""


def insercion(productos):
    """Ordena una lista de tuplas (nombre, precio) por precio."""
    datos = productos.copy()

    for i in range(1, len(datos)):
        clave = datos[i]
        j = i - 1
        while j >= 0 and datos[j][1] > clave[1]:
            datos[j + 1] = datos[j]
            j -= 1
        datos[j + 1] = clave
        print(f"Paso {i}: se insertó {clave[0]} (${clave[1]:.2f}) -> "
              f"{[p[1] for p in datos]}")

    return datos


if __name__ == "__main__":
    inventario = [
        ("Teclado", 450.00),
        ("Mouse", 199.90),
        ("Monitor", 3200.00),
        ("USB 32GB", 120.50),
        ("Audífonos", 799.00),
        ("Webcam", 650.00),
    ]

    print("=== Ordenamiento por Inserción: Catálogo de productos ===")
    print("Inventario original:")
    for nombre, precio in inventario:
        print(f"  {nombre:<12} ${precio:>9.2f}")
    print()

    ordenado = insercion(inventario)

    print("\nCatálogo ordenado por precio:")
    for nombre, precio in ordenado:
        print(f"  {nombre:<12} ${precio:>9.2f}")
