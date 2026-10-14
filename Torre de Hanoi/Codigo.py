
import time

def torre_hanoi(n, origen, auxiliar, destino):
    if n == 1:
        print(f"Mover disco 1 de {origen} a {destino}")
        return

    torre_hanoi(n - 1, origen, destino, auxiliar)

    print(f"Mover disco {n} de {origen} a {destino}")

    torre_hanoi(n - 1, auxiliar, origen, destino)

discos = int(input("Ingrese el número de discos: "))

if discos > 0:
    print("\nMovimientos de la Torre de Hanói:\n")

    inicio = time.perf_counter()

    torre_hanoi(discos, "A", "B", "C")

    fin = time.perf_counter()

    tiempo = fin - inicio
    movimientos = 2 ** discos - 1

    print(f"\nTotal de movimientos: {movimientos}")
    print(f"Tiempo de ejecución: {tiempo:.3f} segundos")
    print(f"Tiempo en milisegundos: {tiempo * 1000:.3f} ms")

else:
    print("El número de discos debe ser mayor que 0.")
