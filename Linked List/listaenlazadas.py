"""Menú original que utiliza la biblioteca MyLinkedList."""

from MyLinkedList import ListaLigada


def leer_posicion():
    while True:
        try:
            posicion = int(input("Ingresa la posición (desde 1): "))

            if posicion >= 1:
                return posicion

            print("La posición debe ser mayor o igual a 1.")

        except ValueError:
            print("Debes ingresar un número entero.")


def leer_dato():
    while True:
        dato = input("Ingresa el dato: ").strip()

        if dato:
            return dato

        print("Escribe un dato. Los nodos de relleno se crean automáticamente.")


def main():
    lista = ListaLigada()

    while True:
        print("\n========== MENÚ ==========")
        print("1. Insertar al inicio")
        print("2. Insertar al final")
        print("3. Insertar en una posición")
        print("4. Mostrar lista")
        print("5. Rellenar un nodo vacío")
        print("6. Buscar un dato")
        print("7. Eliminar por posición")
        print("8. Eliminar por dato (primera coincidencia)")
        print("9. Mostrar posiciones")
        print("0. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            lista.insertar_inicio(leer_dato())
            lista.mostrar()

        elif opcion == "2":
            lista.insertar_final(leer_dato())
            lista.mostrar()

        elif opcion == "3":
            lista.mostrar_posiciones()
            posicion = leer_posicion()
            dato = leer_dato()

            lista.insertar_posicion(dato, posicion)
            print("Nodo insertado correctamente.")
            lista.mostrar()

        elif opcion == "4":
            lista.mostrar()

        elif opcion == "5":
            lista.mostrar_posiciones()
            posicion = leer_posicion()
            dato = leer_dato()

            print(lista.rellenar_vacio(posicion, dato))
            lista.mostrar()

        elif opcion == "6":
            dato = leer_dato()
            posiciones = lista.buscar(dato)

            if posiciones:
                resultado = ", ".join(map(str, posiciones))
                print(f"Dato encontrado en las posiciones: {resultado}")
            else:
                print("El dato no se encuentra en la lista.")

            lista.mostrar()

        elif opcion == "7":
            lista.mostrar_posiciones()
            posicion = leer_posicion()

            if lista.eliminar_posicion(posicion):
                print("Nodo eliminado correctamente.")
            else:
                print("Esa posición no existe.")

            lista.mostrar()

        elif opcion == "8":
            dato = leer_dato()

            if lista.eliminar_dato(dato):
                print("Se eliminó la primera coincidencia.")
            else:
                print("El dato no se encuentra en la lista.")

            lista.mostrar()

        elif opcion == "9":
            lista.mostrar_posiciones()

        elif opcion == "0":
            print("Programa terminado.")
            break

        else:
            print("Opción inválida. Intenta nuevamente.")


if __name__ == "__main__":
    main()