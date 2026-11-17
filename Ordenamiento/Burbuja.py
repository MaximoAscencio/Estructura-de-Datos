"""
Ejercicio: Método de Ordenamiento Burbuja (Bubble Sort)

Problema:
    Un profesor tiene las calificaciones finales de sus alumnos y quiere
    ordenarlas de MENOR a MAYOR para identificar rápidamente quiénes
    necesitan regularización.

Funcionamiento:
    Se recorre la lista comparando elementos adyacentes; si están en el
    orden incorrecto se intercambian. En cada pasada el elemento más
    grande "sube" (como una burbuja) hasta su posición final.
    Si en una pasada no hubo intercambios, la lista ya está ordenada.

Complejidad: O(n^2) en el peor caso, O(n) en el mejor (lista ya ordenada).
"""


def burbuja(lista):
    datos = lista.copy()
    n = len(datos)

    for i in range(n - 1):
        hubo_intercambio = False
        for j in range(n - 1 - i):
            if datos[j] > datos[j + 1]:
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
                hubo_intercambio = True
        print(f"Pasada {i + 1}: {datos}")
        if not hubo_intercambio:
            break

    return datos


if __name__ == "__main__":
    alumnos = ["Ana", "Luis", "Carlos", "María", "Jorge", "Sofía", "Pedro"]
    calificaciones = [85, 62, 94, 70, 58, 99, 77]

    print("=== Ordenamiento Burbuja: Calificaciones ===")
    print(f"Calificaciones originales: {calificaciones}\n")

    ordenadas = burbuja(calificaciones)

    print(f"\nCalificaciones ordenadas: {ordenadas}")
    print(f"Calificación más baja: {ordenadas[0]}")
    print(f"Calificación más alta: {ordenadas[-1]}")

    print("\nAlumnos que necesitan regularización (< 70):")
    for alumno, calif in zip(alumnos, calificaciones):
        if calif < 70:
            print(f"  - {alumno}: {calif}")
