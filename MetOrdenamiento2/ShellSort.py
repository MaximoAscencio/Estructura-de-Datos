"""
Ejercicio 1: Método de Ordenamiento ShellSort

Problema:
    Una tienda de abarrotes captura los precios de sus productos en el orden
    en que llegan del proveedor y necesita ordenarlos de MENOR a MAYOR para
    acomodar su lista de precios. La ventana pide cuántos precios (números)
    se van a capturar, los lee y los ordena con ShellSort.

Funcionamiento:
    ShellSort es una mejora del método de Inserción. En lugar de comparar
    solo elementos vecinos, compara elementos separados por una distancia
    llamada "salto" (gap). Se empieza con un salto igual a la mitad de la
    lista y en cada vuelta se reduce a la mitad, hasta llegar a 1. En cada
    vuelta se hace una inserción entre los elementos separados por ese salto,
    así los números pequeños avanzan rápido hacia el inicio. Cuando el salto
    vale 1 se hace una inserción normal, pero la lista ya está casi ordenada.

Complejidad: depende de la secuencia de saltos; con saltos n/2, n/4, ..., 1
el peor caso es O(n^2) y en la práctica se comporta cerca de O(n^1.5).
No necesita memoria adicional: O(1).
"""

from interfaz import VentanaOrdenamiento, mostrar_lista

DESCRIPCION = ("Ordena comparando elementos separados por un salto que se "
               "reduce a la mitad en cada vuelta, hasta llegar a 1.")


def shell_sort(lista):
    """Regresa la lista ordenada y la lista de pasos realizados."""
    datos = lista.copy()
    pasos = []
    n = len(datos)
    salto = n // 2
    vuelta = 1

    while salto > 0:
        for i in range(salto, n):
            temporal = datos[i]
            j = i
            # Se recorren hacia la derecha los elementos mayores que están
            # a "salto" posiciones de distancia.
            while j >= salto and datos[j - salto] > temporal:
                datos[j] = datos[j - salto]
                j -= salto
            datos[j] = temporal
        pasos.append(f"Vuelta {vuelta} (salto = {salto}): {mostrar_lista(datos)}")
        salto //= 2
        vuelta += 1

    if not pasos:
        pasos.append("Solo hay un número, no hay nada que ordenar.")
    return datos, pasos


if __name__ == "__main__":
    VentanaOrdenamiento({"ShellSort": (shell_sort, False, DESCRIPCION)},
                        "Método de Ordenamiento ShellSort").iniciar()
