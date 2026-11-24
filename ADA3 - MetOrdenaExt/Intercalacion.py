"""
Intercalación.

Ejercicio: dos grupos entregan sus calificaciones finales, cada lista ya
ordenada de menor a mayor. El profesor necesita una sola lista general
ordenada, sin volver a ordenar todo desde cero.

El método usa dos "cabezas" (una por lista). En cada paso compara los dos
elementos de las cabezas, pasa el menor a la lista final y avanza solo en la
lista de donde salió. Cuando una lista se acaba, el resto de la otra se copia
tal cual. Las dos listas de entrada deben estar ordenadas.
"""

from interfaz import VentanaOrdenamiento, leer_numeros, mostrar_lista, formatear


def intercalar(a, b, pasos=None):
    """Mezcla dos listas ordenadas y regresa una lista ordenada. Si se pasa
    una lista 'pasos', va anotando cada comparación."""
    resultado = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            if pasos is not None:
                pasos.append(f"{formatear(a[i])} <= {formatear(b[j])}  -> pasa {formatear(a[i])} (lista 1)")
            resultado.append(a[i])
            i += 1
        else:
            if pasos is not None:
                pasos.append(f"{formatear(a[i])} > {formatear(b[j])}  -> pasa {formatear(b[j])} (lista 2)")
            resultado.append(b[j])
            j += 1
    if i < len(a):
        if pasos is not None:
            pasos.append(f"La lista 2 se acabó -> se copia el resto de la lista 1: {mostrar_lista(a[i:])}")
        resultado.extend(a[i:])
    if j < len(b):
        if pasos is not None:
            pasos.append(f"La lista 1 se acabó -> se copia el resto de la lista 2: {mostrar_lista(b[j:])}")
        resultado.extend(b[j:])
    return resultado


def ejecutar_gui(texto1, texto2):
    lista1 = leer_numeros(texto1, "La lista 1")
    lista2 = leer_numeros(texto2, "La lista 2")

    pasos = []
    if lista1 != sorted(lista1):
        lista1 = sorted(lista1)
        pasos.append(f"La lista 1 no estaba ordenada, se ordenó primero: {mostrar_lista(lista1)}")
    if lista2 != sorted(lista2):
        lista2 = sorted(lista2)
        pasos.append(f"La lista 2 no estaba ordenada, se ordenó primero: {mostrar_lista(lista2)}")
    if pasos:
        pasos.append("")
    pasos.append(f"Lista 1: {mostrar_lista(lista1)}")
    pasos.append(f"Lista 2: {mostrar_lista(lista2)}")
    pasos.append("")

    resultado = intercalar(lista1, lista2, pasos)
    return "Lista intercalada: " + mostrar_lista(resultado), pasos


METODO = {
    "descripcion": ("Calificaciones de dos grupos, cada lista ya ordenada. La intercalación las une "
                    "en una sola lista ordenada comparando solo los primeros elementos de cada una."),
    "etiqueta_datos": "Lista 1 (números separados por comas):",
    "ejemplo_datos": "6, 7.5, 8, 9, 10",
    "etiqueta_valor": "Lista 2 (números separados por comas):",
    "ejemplo_valor": "5, 7, 8.5, 9.5",
    "ejecutar": ejecutar_gui,
}

if __name__ == "__main__":
    VentanaOrdenamiento({"Intercalación": METODO}, "Intercalación").iniciar()
