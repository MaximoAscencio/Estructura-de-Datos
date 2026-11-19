"""
Menú general de Métodos de Ordenamiento 2

Permite elegir el método (ShellSort, Quicksort, Heapsort o Radix), pide la
cantidad de números y los números, y los ordena con el método elegido.
El programa se repite hasta que el usuario elige la opción Salir.

Este archivo usa las funciones de ShellSort.py, QuickSort.py, HeapSort.py
y Radix.py, por lo que deben estar en la misma carpeta.
"""

import ShellSort
import QuickSort
import HeapSort
import Radix

METODOS = {
    "1": ("ShellSort", ShellSort.shell_sort, ShellSort.pedir_numeros),
    "2": ("Quicksort", QuickSort.quick_sort, QuickSort.pedir_numeros),
    "3": ("Heapsort", HeapSort.heap_sort, HeapSort.pedir_numeros),
    "4": ("Radix", Radix.radix_sort, Radix.pedir_numeros),
}


def mostrar(lista):
    return ShellSort.mostrar_lista(lista)


def menu():
    while True:
        print("\n======= MÉTODOS DE ORDENAMIENTO 2 =======")
        print("1. ShellSort")
        print("2. Quicksort")
        print("3. Heapsort")
        print("4. Radix (solo números enteros)")
        print("5. Salir")
        opcion = input("Elige el método de ordenamiento: ").strip()

        if opcion in METODOS:
            nombre, ordenar, pedir_numeros = METODOS[opcion]
            print(f"\n--- {nombre} ---")
            cantidad = ShellSort.pedir_cantidad()
            numeros = pedir_numeros(cantidad)
            print(f"\nLista original: {mostrar(numeros)}")
            print(f"Proceso de {nombre}:")
            ordenados = ordenar(numeros)
            print(f"\nLista ordenada con {nombre}: {mostrar(ordenados)}")
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    menu()
