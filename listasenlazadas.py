class Nodo:
    def __init__(self, info):
        self.info = info
        self.liga = None


class ListaLigada:
    def __init__(self):
        self.inicio = None

    def insertar_inicio(self, dato):
        nuevo = Nodo(dato)
        nuevo.liga = self.inicio
        self.inicio = nuevo

    def insertar_final(self, dato):
        nuevo = Nodo(dato)

        if self.inicio is None:
            self.inicio = nuevo
            return

        actual = self.inicio
        while actual.liga is not None:
            actual = actual.liga

        actual.liga = nuevo

    def insertar_posicion(self, dato, posicion):
        """Inserta antes del nodo que ocupa la posición indicada."""
        if posicion < 1:
            return False

        if posicion == 1:
            self.insertar_inicio(dato)
            return True

        anterior = self.inicio

        # Buscar el nodo anterior a la posición deseada.
        for _ in range(posicion - 2):
            if anterior is None:
                return False
            anterior = anterior.liga

        if anterior is None:
            return False

        nuevo = Nodo(dato)
        nuevo.liga = anterior.liga
        anterior.liga = nuevo
        return True

    def mostrar(self):
        if self.inicio is None:
            print("Lista vacía.")
            return

        actual = self.inicio
        while actual is not None:
            print(actual.info, end=" -> ")
            actual = actual.liga

        print("None")


def main():
    lista = ListaLigada()

    while True:
        print("\n--- MENÚ ---")
        print("1. Insertar al inicio")
        print("2. Insertar al final")
        print("3. Insertar en una posición")
        print("4. Mostrar lista")
        print("5. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            dato = input("Ingresa el dato: ")
            lista.insertar_inicio(dato)
            lista.mostrar()

        elif opcion == "2":
            dato = input("Ingresa el dato: ")
            lista.insertar_final(dato)
            lista.mostrar()

        elif opcion == "3":
            lista.mostrar()

            try:
                posicion = int(input("Posición donde insertar (desde 1): "))
            except ValueError:
                print("Debes ingresar un número entero.")
                continue

            dato = input("Ingresa el dato: ")

            if lista.insertar_posicion(dato, posicion):
                lista.mostrar()
            else:
                print("Posición inválida. Usa una posición entre 1 y "
                      "la cantidad de nodos + 1.")

        elif opcion == "4":
            lista.mostrar()

        elif opcion == "5":
            print("Programa terminado.")
            break

        else:
            print("Opción inválida. Intenta nuevamente.")


if __name__ == "__main__":
    main()