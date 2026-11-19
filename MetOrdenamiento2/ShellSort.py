"""
Ejercicio 1: Método de Ordenamiento ShellSort

Problema:
    Una tienda de abarrotes captura los precios de sus productos en el orden
    en que llegan del proveedor y necesita ordenarlos de MENOR a MAYOR para
    acomodar su lista de precios. El programa pide cuántos precios (números)
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


def formatear(numero):
    """Muestra 5.0 como 5 y deja 5.5 como 5.5."""
    return str(int(numero)) if float(numero).is_integer() else str(numero)


def mostrar_lista(lista):
    return "[" + ", ".join(formatear(x) for x in lista) + "]"


def shell_sort(lista, mostrar_pasos=True):
    datos = lista.copy()
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
        if mostrar_pasos:
            print(f"  Vuelta {vuelta} (salto = {salto}): {mostrar_lista(datos)}")
        salto //= 2
        vuelta += 1

    return datos


def pedir_cantidad():
    while True:
        try:
            cantidad = int(input("¿Cuántos números vas a ingresar? "))
            if cantidad > 0:
                return cantidad
            print("  La cantidad debe ser mayor que 0.")
        except ValueError:
            print("  Escribe un número entero.")


def pedir_numeros(cantidad):
    numeros = []
    for i in range(cantidad):
        while True:
            try:
                numeros.append(float(input(f"  Número {i + 1}: ")))
                break
            except ValueError:
                print("  Valor no válido, escribe un número.")
    return numeros


def menu():
    while True:
        print("\n========== MÉTODO SHELLSORT ==========")
        print("1. Ingresar números y ordenarlos")
        print("2. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            cantidad = pedir_cantidad()
            numeros = pedir_numeros(cantidad)
            print(f"\nLista original: {mostrar_lista(numeros)}")
            print("Proceso de ShellSort:")
            ordenados = shell_sort(numeros)
            print(f"\nLista ordenada: {mostrar_lista(ordenados)}")
        elif opcion == "2":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    menu()
