"""
Ejercicio 3: Método de Ordenamiento Heapsort

Problema:
    En la sala de urgencias de un hospital, a cada paciente se le asigna un
    nivel de prioridad numérico al llegar. Se necesita ordenar los niveles de
    prioridad de MENOR a MAYOR para organizar el orden de atención. La
    ventana pide cuántos niveles (números) se van a capturar, los lee y los
    ordena con Heapsort.

Funcionamiento:
    Heapsort usa una estructura llamada montículo (heap). Un montículo máximo
    es un árbol binario guardado dentro del mismo arreglo, donde cada padre
    es mayor o igual que sus hijos; por eso el mayor siempre queda en la
    raíz (posición 0). Para el nodo en la posición i, sus hijos están en
    2i + 1 y 2i + 2.
    1. Se construye el montículo máximo con todos los datos.
    2. Se intercambia la raíz (el mayor) con el último elemento, con lo que
       el mayor queda en su lugar final.
    3. Se reduce el tamaño del montículo en uno y se "hunde" la nueva raíz
       (heapify) para que vuelva a ser un montículo.
    4. Se repiten los pasos 2 y 3 hasta que el montículo queda vacío.

Complejidad: O(n log n) en el mejor, promedio y peor caso. No necesita
memoria adicional: O(1).
"""

from interfaz import VentanaOrdenamiento, mostrar_lista, formatear

DESCRIPCION = ("Acomoda los datos en un montículo máximo (el mayor queda en la "
               "raíz), lo manda al final y vuelve a acomodar el montículo.")


def heapify(datos, tamano, raiz):
    """Hunde el elemento de la posición 'raiz' hasta que se cumpla la
    propiedad de montículo máximo."""
    mayor = raiz
    izquierdo = 2 * raiz + 1
    derecho = 2 * raiz + 2

    if izquierdo < tamano and datos[izquierdo] > datos[mayor]:
        mayor = izquierdo
    if derecho < tamano and datos[derecho] > datos[mayor]:
        mayor = derecho

    if mayor != raiz:
        datos[raiz], datos[mayor] = datos[mayor], datos[raiz]
        heapify(datos, tamano, mayor)


def heap_sort(lista):
    """Regresa la lista ordenada y la lista de pasos realizados."""
    datos = lista.copy()
    pasos = []
    n = len(datos)

    # 1. Construir el montículo máximo.
    for i in range(n // 2 - 1, -1, -1):
        heapify(datos, n, i)
    pasos.append(f"Montículo máximo inicial: {mostrar_lista(datos)}")

    # 2. Sacar el mayor y volver a acomodar el montículo.
    for fin in range(n - 1, 0, -1):
        datos[0], datos[fin] = datos[fin], datos[0]
        heapify(datos, fin, 0)
        pasos.append(f"Se coloca {formatear(datos[fin])} al final: "
                     f"{mostrar_lista(datos)}")

    return datos, pasos


if __name__ == "__main__":
    VentanaOrdenamiento({"Heapsort": (heap_sort, False, DESCRIPCION)},
                        "Método de Ordenamiento Heapsort").iniciar()
