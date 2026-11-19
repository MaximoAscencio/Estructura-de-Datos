"""
Menú general de Métodos de Ordenamiento 2

Abre una ventana donde se elige el método (ShellSort, Quicksort, Heapsort o
Radix), se escribe la cantidad de números y los números, y se ordenan con el
método elegido. La ventana sigue abierta para hacer más ordenamientos hasta
que el usuario presiona "Salir".

Este archivo usa las funciones de ShellSort.py, QuickSort.py, HeapSort.py,
Radix.py e interfaz.py, por lo que deben estar en la misma carpeta.
"""

import ShellSort
import QuickSort
import HeapSort
import Radix
from interfaz import VentanaOrdenamiento

METODOS = {
    "ShellSort": (ShellSort.shell_sort, False, ShellSort.DESCRIPCION),
    "Quicksort": (QuickSort.quick_sort, False, QuickSort.DESCRIPCION),
    "Heapsort": (HeapSort.heap_sort, False, HeapSort.DESCRIPCION),
    "Radix": (Radix.radix_sort, True, Radix.DESCRIPCION),
}


if __name__ == "__main__":
    VentanaOrdenamiento(METODOS, "Métodos de Ordenamiento 2").iniciar()
