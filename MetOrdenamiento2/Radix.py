"""
Ejercicio 4: Método de Ordenamiento Radix

Problema:
    El departamento de servicios escolares tiene una lista de números de
    control (matrículas) de alumnos capturados sin ningún orden y necesita
    ordenarlos de MENOR a MAYOR para generar el listado oficial del grupo.
    El programa pide cuántos números enteros se van a capturar, los lee y
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


def radix_positivos(datos, mostrar_pasos=True, etiqueta=""):
    """Ordena una lista de enteros no negativos con Radix LSD."""
    if not datos:
        return datos
    maximo = max(datos)
    posicion = 1          # 1 = unidades, 10 = decenas, 100 = centenas...
    nombres = ["unidades", "decenas", "centenas", "unidades de millar",
               "decenas de millar", "centenas de millar"]
    pasada = 0

    while maximo // posicion > 0:
        cubetas = [[] for _ in range(10)]
        for numero in datos:
            digito = (numero // posicion) % 10
            cubetas[digito].append(numero)
        datos = [numero for cubeta in cubetas for numero in cubeta]

        if mostrar_pasos:
            nombre = nombres[pasada] if pasada < len(nombres) else f"posición {posicion}"
            print(f"  {etiqueta}Pasada por {nombre}: {datos}")
        posicion *= 10
        pasada += 1

    return datos


def radix_sort(lista, mostrar_pasos=True):
    negativos = [-x for x in lista if x < 0]
    positivos = [x for x in lista if x >= 0]

    if negativos and mostrar_pasos:
        print("  Números negativos (ordenados por su valor absoluto):")
    negativos = radix_positivos(negativos, mostrar_pasos, "(negativos) ")
    if negativos and mostrar_pasos:
        print("  Números positivos:")
    positivos = radix_positivos(positivos, mostrar_pasos)

    # El negativo con mayor valor absoluto es el más pequeño.
    return [-x for x in reversed(negativos)] + positivos


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
                numeros.append(int(input(f"  Número {i + 1}: ")))
                break
            except ValueError:
                print("  Radix solo acepta números enteros, intenta de nuevo.")
    return numeros


def menu():
    while True:
        print("\n========== MÉTODO RADIX ==========")
        print("1. Ingresar números y ordenarlos")
        print("2. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            cantidad = pedir_cantidad()
            numeros = pedir_numeros(cantidad)
            print(f"\nLista original: {numeros}")
            print("Proceso de Radix:")
            ordenados = radix_sort(numeros)
            print(f"\nLista ordenada: {ordenados}")
        elif opcion == "2":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    menu()
