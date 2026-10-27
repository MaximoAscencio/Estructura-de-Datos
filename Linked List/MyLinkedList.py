"""Biblioteca MyLinkedList: nodos y listas simplemente enlazadas.

Uso:
    from MyLinkedList import ListaLigada

Las posiciones empiezan en 1. Insertar en una posición posterior al final
crea automáticamente nodos de relleno cuyo dato es None.
"""

__all__ = ["Nodo", "ListaLigada"]


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
        if posicion < 1:
            return False

        if posicion == 1:
            self.insertar_inicio(dato)
            return True

        if self.inicio is None:
            self.inicio = Nodo(None)

        anterior = self.inicio

        # Crear nodos vacíos hasta llegar al anterior.
        for _ in range(posicion - 2):
            if anterior.liga is None:
                anterior.liga = Nodo(None)

            anterior = anterior.liga

        nuevo = Nodo(dato)
        nuevo.liga = anterior.liga
        anterior.liga = nuevo

        return True

    def obtener_nodo(self, posicion):
        if posicion < 1:
            return None

        actual = self.inicio

        for _ in range(posicion - 1):
            if actual is None:
                return None

            actual = actual.liga

        return actual

    def rellenar_vacio(self, posicion, dato):
        nodo = self.obtener_nodo(posicion)

        if nodo is None:
            return "Esa posición no existe."

        if nodo.info is not None:
            return "Ese nodo ya contiene un dato."

        nodo.info = dato
        return "Nodo rellenado correctamente."

    def buscar(self, dato):
        posiciones = []
        actual = self.inicio
        posicion = 1

        while actual is not None:
            if actual.info == dato:
                posiciones.append(posicion)

            actual = actual.liga
            posicion += 1

        return posiciones

    def eliminar_posicion(self, posicion):
        if posicion < 1 or self.inicio is None:
            return False

        if posicion == 1:
            self.inicio = self.inicio.liga
            return True

        anterior = self.obtener_nodo(posicion - 1)

        if anterior is None or anterior.liga is None:
            return False

        anterior.liga = anterior.liga.liga
        return True

    def eliminar_dato(self, dato):
        # Elimina la primera coincidencia.
        anterior = None
        actual = self.inicio

        while actual is not None:
            if actual.info == dato:
                if anterior is None:
                    self.inicio = actual.liga
                else:
                    anterior.liga = actual.liga

                return True

            anterior = actual
            actual = actual.liga

        return False

    def mostrar(self):
        if self.inicio is None:
            print("\nLista vacía: INICIO -> FIN")
            return

        partes = ["INICIO"]
        actual = self.inicio

        while actual is not None:
            valor = "[vacío]" if actual.info is None else actual.info
            partes.append(str(valor))
            actual = actual.liga

        partes.append("FIN")
        print("\n" + " -> ".join(partes))

    def mostrar_posiciones(self):
        if self.inicio is None:
            print("\nLa lista está vacía.")
            return

        print("\nPosición | Dato")
        print("-" * 25)

        actual = self.inicio
        posicion = 1

        while actual is not None:
            valor = "[vacío]" if actual.info is None else actual.info
            print(f"{posicion:8} | {valor}")

            actual = actual.liga
            posicion += 1
