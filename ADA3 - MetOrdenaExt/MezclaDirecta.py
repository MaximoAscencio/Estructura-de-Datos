"""
Mezcla directa (ordenamiento externo).

Ejercicio: una empresa tiene un archivo muy grande de folios de factura sin
ordenar, que no cabe completo en la memoria. Se ordena usando dos archivos
auxiliares (F1 y F2), leyendo y escribiendo los datos poco a poco.

En cada pasada se hacen dos fases:
    1. Distribución: el archivo original se reparte, de forma alternada, en
       bloques de longitud fija entre F1 y F2.
    2. Mezcla: se toma un bloque de F1 y uno de F2, se intercalan y el bloque
       resultante (del doble de longitud) se escribe de vuelta en el original.
La longitud de los bloques empieza en 1 y se duplica en cada pasada (1, 2, 4,
8...) hasta que todo el archivo queda como un solo bloque ordenado.
"""

from interfaz import VentanaOrdenamiento, leer_numeros, mostrar_lista, mostrar_bloques
from Intercalacion import intercalar


def mezcla_directa(datos):
    """Regresa (lista_ordenada, pasos). Los archivos se simulan con listas."""
    pasos = []
    original = list(datos)
    n = len(original)
    longitud = 1
    pasada = 1
    while longitud < n:
        pasos.append(f"Pasada {pasada} (longitud de cada bloque = {longitud})")
        bloques = [original[i:i + longitud] for i in range(0, n, longitud)]
        f1 = bloques[0::2]
        f2 = bloques[1::2]
        pasos.append("  Distribución:")
        pasos.append(f"    F1: {mostrar_bloques(f1)}")
        pasos.append(f"    F2: {mostrar_bloques(f2)}")

        mezclado = []
        pasos.append("  Mezcla:")
        for k in range(len(f1)):
            b1 = f1[k]
            b2 = f2[k] if k < len(f2) else []
            unido = intercalar(b1, b2)
            pasos.append(f"    {mostrar_lista(b1)} + {mostrar_lista(b2)} -> {mostrar_lista(unido)}")
            mezclado.extend(unido)
        original = mezclado
        pasos.append(f"  Archivo original: {mostrar_lista(original)}")
        pasos.append("")
        longitud *= 2
        pasada += 1
    if pasada == 1:
        pasos.append("Solo hay un dato, ya está ordenado.")
    return original, pasos


def ejecutar_gui(texto, _no_se_usa):
    datos = leer_numeros(texto, "La lista de folios")
    ordenada, pasos = mezcla_directa(datos)
    return "Archivo ordenado: " + mostrar_lista(ordenada), pasos


METODO = {
    "descripcion": ("Archivo de folios de factura sin ordenar. La mezcla directa lo ordena con dos "
                    "archivos auxiliares, mezclando bloques de longitud 1, 2, 4, 8..."),
    "etiqueta_datos": "Folios (números separados por comas):",
    "ejemplo_datos": "34, 7, 52, 18, 3, 41, 26, 9",
    "ejecutar": ejecutar_gui,
}

if __name__ == "__main__":
    VentanaOrdenamiento({"Mezcla Directa": METODO}, "Mezcla Directa").iniciar()
