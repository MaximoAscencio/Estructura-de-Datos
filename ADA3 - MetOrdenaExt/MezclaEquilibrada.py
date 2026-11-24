"""
Mezcla equilibrada (ordenamiento externo, mezcla natural).

Ejercicio: una biblioteca registra los números de adjudicación de los libros
devueltos. Los registros llegan en tandas que ya traen cierto orden (por
ejemplo, lo que devolvió cada carrito). Se aprovechan esas tandas para ordenar
todo con cuatro archivos auxiliares.

Diferencia con la mezcla directa: en lugar de bloques de longitud fija, se
usan los bloques "naturales" (secuencias que ya vienen en orden ascendente), y
se trabaja con cuatro archivos balanceados: dos de entrada y dos de salida.
    1. Distribución inicial: los bloques naturales del archivo original se
       reparten de forma alternada entre F1 y F2.
    2. Mezcla: se intercalan un bloque de F1 con uno de F2 y el resultado se
       escribe de forma alternada en F3 y F4.
    3. Los archivos de salida pasan a ser de entrada y se repite hasta que
       queda un solo bloque.
"""

from interfaz import VentanaOrdenamiento, leer_numeros, mostrar_lista, mostrar_bloques
from Intercalacion import intercalar


def bloques_naturales(datos):
    """Separa la lista en secuencias ascendentes consecutivas."""
    bloques = []
    actual = [datos[0]]
    for x in datos[1:]:
        if x >= actual[-1]:
            actual.append(x)
        else:
            bloques.append(actual)
            actual = [x]
    bloques.append(actual)
    return bloques


def mezcla_equilibrada(datos):
    """Regresa (lista_ordenada, pasos). Los archivos se simulan con listas."""
    pasos = []
    bloques = bloques_naturales(datos)
    pasos.append(f"Bloques naturales del archivo original: {mostrar_bloques(bloques)}")
    entrada = [bloques[0::2], bloques[1::2]]
    nombres_entrada = ("F1", "F2")
    nombres_salida = ("F3", "F4")
    pasos.append("")
    pasos.append("Distribución inicial:")
    pasos.append(f"  F1: {mostrar_bloques(entrada[0])}")
    pasos.append(f"  F2: {mostrar_bloques(entrada[1])}")
    pasos.append("")

    pasada = 1
    while len(entrada[0]) + len(entrada[1]) > 1:
        a, b = entrada
        pasos.append(f"Pasada {pasada}: se mezcla {nombres_entrada[0]} y {nombres_entrada[1]} "
                     f"hacia {nombres_salida[0]} y {nombres_salida[1]}")
        salida = [[], []]
        for k in range(max(len(a), len(b))):
            b1 = a[k] if k < len(a) else []
            b2 = b[k] if k < len(b) else []
            unido = intercalar(b1, b2)
            destino = k % 2
            pasos.append(f"  {mostrar_lista(b1)} + {mostrar_lista(b2)} -> {mostrar_lista(unido)}"
                         f"  (se escribe en {nombres_salida[destino]})")
            salida[destino].append(unido)
        pasos.append(f"  {nombres_salida[0]}: {mostrar_bloques(salida[0])}")
        pasos.append(f"  {nombres_salida[1]}: {mostrar_bloques(salida[1])}")
        pasos.append("")
        entrada = salida
        nombres_entrada, nombres_salida = nombres_salida, nombres_entrada
        pasada += 1

    ordenada = entrada[0][0] if entrada[0] else entrada[1][0]
    if pasada == 1:
        pasos.append("Todo el archivo ya formaba un solo bloque ordenado.")
    return ordenada, pasos


def ejecutar_gui(texto, _no_se_usa):
    datos = leer_numeros(texto, "La lista de números de adjudicación")
    ordenada, pasos = mezcla_equilibrada(datos)
    return "Archivo ordenado: " + mostrar_lista(ordenada), pasos


METODO = {
    "descripcion": ("Libros devueltos que llegan en tandas ya parcialmente ordenadas. La mezcla "
                    "equilibrada aprovecha esos bloques naturales y usa cuatro archivos (2 de "
                    "entrada y 2 de salida)."),
    "etiqueta_datos": "Números de adjudicación (separados por comas):",
    "ejemplo_datos": "5, 12, 20, 3, 9, 15, 2, 8, 30, 1, 14",
    "ejecutar": ejecutar_gui,
}

if __name__ == "__main__":
    VentanaOrdenamiento({"Mezcla Equilibrada": METODO}, "Mezcla Equilibrada").iniciar()
