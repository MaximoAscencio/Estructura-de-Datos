"""
Ejercicio 2: Método de Ordenamiento Quicksort

Problema:
    En un torneo de un videojuego se registran los puntajes de los jugadores
    conforme terminan sus partidas. Al final se necesita ordenar todos los
    puntajes de MENOR a MAYOR para armar la tabla de posiciones. La ventana
    pide cuántos puntajes (números) se van a capturar, los lee y los ordena
    con Quicksort.

Funcionamiento:
    Quicksort usa la estrategia "divide y vencerás". Se elige un elemento
    llamado pivote (en este programa, el último de la sublista) y se
    "particiona" la lista: todos los menores o iguales al pivote quedan a su
    izquierda y los mayores a su derecha. Así el pivote queda en su posición
    final. Después se repite el mismo proceso, de forma recursiva, con la
    parte izquierda y con la parte derecha, hasta que cada parte tiene uno o
    ningún elemento.

Complejidad: O(n log n) en el caso promedio y en el mejor caso; O(n^2) en
el peor caso (cuando el pivote siempre queda en un extremo, por ejemplo con
una lista ya ordenada). Usa O(log n) de memoria por la recursión.
"""

from interfaz import VentanaOrdenamiento, mostrar_lista, formatear

DESCRIPCION = ("Elige un pivote, deja los menores a su izquierda y los mayores "
               "a su derecha, y repite el proceso con cada parte (divide y vencerás).")


def particion(datos, inicio, fin):
    pivote = datos[fin]
    i = inicio - 1
    for j in range(inicio, fin):
        if datos[j] <= pivote:
            i += 1
            datos[i], datos[j] = datos[j], datos[i]
    datos[i + 1], datos[fin] = datos[fin], datos[i + 1]
    return i + 1


def _quick_sort(datos, inicio, fin, pasos):
    if inicio < fin:
        pivote = datos[fin]
        posicion = particion(datos, inicio, fin)
        pasos.append(f"Partición {len(pasos) + 1} (pivote = {formatear(pivote)}): "
                     f"{mostrar_lista(datos)}")
        _quick_sort(datos, inicio, posicion - 1, pasos)
        _quick_sort(datos, posicion + 1, fin, pasos)


def quick_sort(lista):
    """Regresa la lista ordenada y la lista de pasos realizados."""
    datos = lista.copy()
    pasos = []
    _quick_sort(datos, 0, len(datos) - 1, pasos)
    if not pasos:
        pasos.append("Solo hay un número, no hay nada que ordenar.")
    return datos, pasos


if __name__ == "__main__":
    VentanaOrdenamiento({"Quicksort": (quick_sort, False, DESCRIPCION)},
                        "Método de Ordenamiento Quicksort").iniciar()
