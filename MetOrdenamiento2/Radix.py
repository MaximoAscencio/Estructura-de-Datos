"""
Ejercicio 4: Método de Ordenamiento Radix

Problema:
    El departamento de servicios escolares tiene una lista de números de
    control (matrículas) de alumnos capturados sin ningún orden y necesita
    ordenarlos de MENOR a MAYOR para generar el listado oficial del grupo.
    La ventana pide cuántos números enteros se van a capturar, los lee y
    los ordena con Radix.

Funcionamiento:
    Radix (ordenamiento por residuos o por dígitos) no compara los números
    entre sí. Los ordena dígito por dígito, empezando por las unidades, luego
    las decenas, las centenas, etc. (LSD: dígito menos significativo). En
    cada pasada los números se reparten en 10 "cubetas", una por cada dígito
    del 0 al 9, y después se juntan en orden de cubeta. Como cada pasada
    respeta el orden de la anterior (es estable), al terminar con el dígito
    más significativo la lista queda ordenada.
    Radix solo trabaja con números enteros. Si hay negativos, este programa
    los ordena aparte usando su valor absoluto, los invierte y los coloca
    antes de los positivos.

Complejidad: O(d * (n + b)), donde d es la cantidad de dígitos del número
más grande, n la cantidad de números y b la base (10). Usa O(n + b) de
memoria adicional por las cubetas.
"""

from interfaz import VentanaOrdenamiento

DESCRIPCION = ("Ordena dígito por dígito (unidades, decenas, centenas...) "
               "repartiendo los números en 10 cubetas, sin compararlos entre sí.")

NOMBRES = ["unidades", "decenas", "centenas", "unidades de millar",
           "decenas de millar", "centenas de millar"]


def radix_positivos(datos, pasos, etiqueta=""):
    """Ordena una lista de enteros no negativos con Radix LSD."""
    if not datos:
        return datos
    maximo = max(datos)
    posicion = 1          # 1 = unidades, 10 = decenas, 100 = centenas...
    pasada = 0

    while True:
        cubetas = [[] for _ in range(10)]
        for numero in datos:
            digito = (numero // posicion) % 10
            cubetas[digito].append(numero)
        datos = [numero for cubeta in cubetas for numero in cubeta]

        nombre = NOMBRES[pasada] if pasada < len(NOMBRES) else f"posición {posicion}"
        pasos.append(f"{etiqueta}Pasada por {nombre}: {datos}")
        posicion *= 10
        pasada += 1
        if maximo // posicion == 0:
            break

    return datos


def radix_sort(lista):
    """Regresa la lista ordenada y la lista de pasos realizados."""
    pasos = []
    negativos = [-x for x in lista if x < 0]
    positivos = [x for x in lista if x >= 0]

    if negativos:
        pasos.append("Números negativos (se ordenan por su valor absoluto):")
        negativos = radix_positivos(negativos, pasos, "  ")
        pasos.append("Números positivos:")
        positivos = radix_positivos(positivos, pasos, "  ")
    else:
        positivos = radix_positivos(positivos, pasos)

    # El negativo con mayor valor absoluto es el más pequeño.
    return [-x for x in reversed(negativos)] + positivos, pasos


if __name__ == "__main__":
    VentanaOrdenamiento({"Radix": (radix_sort, True, DESCRIPCION)},
                        "Método de Ordenamiento Radix").iniciar()
