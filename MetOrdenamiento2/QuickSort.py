"""
Ejercicio 2: Método de Ordenamiento Quicksort

Problema:
    En un torneo de un videojuego se registran los puntajes de los jugadores
    conforme terminan sus partidas. Al final se necesita ordenar todos los
    puntajes de MENOR a MAYOR para armar la tabla de posiciones. El programa
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


def formatear(numero):
    """Muestra 5.0 como 5 y deja 5.5 como 5.5."""
    return str(int(numero)) if float(numero).is_integer() else str(numero)


def mostrar_lista(lista):
    return "[" + ", ".join(formatear(x) for x in lista) + "]"


def particion(datos, inicio, fin):
    pivote = datos[fin]
    i = inicio - 1
    for j in range(inicio, fin):
        if datos[j] <= pivote:
            i += 1
            datos[i], datos[j] = datos[j], datos[i]
    datos[i + 1], datos[fin] = datos[fin], datos[i + 1]
    return i + 1


def _quick_sort(datos, inicio, fin, mostrar_pasos, contador):
    if inicio < fin:
        pivote = datos[fin]
        posicion = particion(datos, inicio, fin)
        if mostrar_pasos:
            contador[0] += 1
            print(f"  Partición {contador[0]} (pivote = {formatear(pivote)}): "
                  f"{mostrar_lista(datos)}")
        _quick_sort(datos, inicio, posicion - 1, mostrar_pasos, contador)
        _quick_sort(datos, posicion + 1, fin, mostrar_pasos, contador)


def quick_sort(lista, mostrar_pasos=True):
    datos = lista.copy()
    _quick_sort(datos, 0, len(datos) - 1, mostrar_pasos, [0])
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
        print("\n========== MÉTODO QUICKSORT ==========")
        print("1. Ingresar números y ordenarlos")
        print("2. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            cantidad = pedir_cantidad()
            numeros = pedir_numeros(cantidad)
            print(f"\nLista original: {mostrar_lista(numeros)}")
            print("Proceso de Quicksort:")
            ordenados = quick_sort(numeros)
            print(f"\nLista ordenada: {mostrar_lista(ordenados)}")
        elif opcion == "2":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    menu()
