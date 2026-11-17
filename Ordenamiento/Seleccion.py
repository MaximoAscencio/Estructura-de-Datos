"""
Ejercicio: Método de Ordenamiento por Selección (Selection Sort)

Problema:
    En una competencia de atletismo se registraron los tiempos (en segundos)
    de los corredores en la prueba de 100 metros. Se desea ordenar los
    resultados del MÁS RÁPIDO al MÁS LENTO para armar el podio.

Funcionamiento:
    En cada pasada se busca el elemento MÍNIMO de la parte no ordenada y se
    intercambia con el primer elemento de esa parte. Así, la parte ordenada
    crece de izquierda a derecha un elemento a la vez.

Complejidad: O(n^2) en todos los casos.
"""


def seleccion(corredores):
    """Ordena una lista de tuplas (nombre, tiempo) por tiempo ascendente."""
    datos = corredores.copy()
    n = len(datos)

    for i in range(n - 1):
        indice_min = i
        for j in range(i + 1, n):
            if datos[j][1] < datos[indice_min][1]:
                indice_min = j
        if indice_min != i:
            datos[i], datos[indice_min] = datos[indice_min], datos[i]
        print(f"Pasada {i + 1}: mínimo = {datos[i][0]} ({datos[i][1]} s) -> "
              f"{[c[1] for c in datos]}")

    return datos


if __name__ == "__main__":
    resultados = [
        ("Diego", 11.42),
        ("Valeria", 12.05),
        ("Andrés", 10.98),
        ("Fernanda", 11.73),
        ("Ricardo", 10.87),
        ("Daniela", 11.15),
    ]

    print("=== Ordenamiento por Selección: Carrera de 100 m ===")
    print(f"Tiempos originales: {[r[1] for r in resultados]}\n")

    clasificacion = seleccion(resultados)

    print("\nClasificación final:")
    for lugar, (nombre, tiempo) in enumerate(clasificacion, start=1):
        print(f"  {lugar}. {nombre:<10} {tiempo:.2f} s")

    print("\nPodio:")
    medallas = ["Oro", "Plata", "Bronce"]
    for medalla, (nombre, tiempo) in zip(medallas, clasificacion):
        print(f"  {medalla}: {nombre} ({tiempo:.2f} s)")
