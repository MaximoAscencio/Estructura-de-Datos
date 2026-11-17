"""Arreglo POSTRES con una lista enlazada simple de ingredientes por postre.

Ejecutar: python postres.py
Ejemplo de eliminación de repetidos: python postres.py --demo
No requiere bibliotecas externas. Python 3.10 o posterior.
"""

from dataclasses import dataclass
from typing import Iterable, Iterator, Optional
import sys
import unicodedata


def limpiar_texto(texto: str) -> str:
    """Quita espacios sobrantes y rechaza nombres vacíos."""
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("El nombre debe ser un texto no vacío.")
    return unicodedata.normalize("NFC", " ".join(texto.split()))


def clave(texto: str) -> str:
    """Compara sin distinguir mayúsculas ni espacios sobrantes."""
    return limpiar_texto(texto).casefold()


def orden_alfabetico(texto: str) -> tuple[str, str]:
    """Orden español básico: vocales acentuadas como vocales; ñ después de n."""
    normal = clave(texto)
    base = normal.translate(str.maketrans("áéíóúü", "aeiouu"))
    return base.replace("ñ", "n~"), normal


@dataclass
class Nodo:
    ingrediente: str
    siguiente: Optional["Nodo"] = None


class ListaIngredientes:
    def __init__(self, ingredientes: Iterable[str] = ()) -> None:
        self.cabeza: Optional[Nodo] = None
        self.cola: Optional[Nodo] = None
        for ingrediente in ingredientes:
            self.agregar(ingrediente)

    def __iter__(self) -> Iterator[str]:
        actual = self.cabeza
        while actual is not None:
            yield actual.ingrediente
            actual = actual.siguiente

    def agregar(self, ingrediente: str) -> None:
        nuevo = Nodo(limpiar_texto(ingrediente))
        if self.cola is None:
            self.cabeza = nuevo
        else:
            self.cola.siguiente = nuevo
        self.cola = nuevo

    def eliminar(self, ingrediente: str) -> bool:
        """Elimina la primera aparición; devuelve False si no existe."""
        buscado = clave(ingrediente)
        anterior = None
        actual = self.cabeza
        while actual is not None:
            if clave(actual.ingrediente) == buscado:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                if actual is self.cola:
                    self.cola = anterior
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def eliminar_repetidos(self) -> int:
        """Conserva la primera aparición y vuelve a enlazar los nodos."""
        vistos: set[str] = set()
        eliminados = 0
        anterior = None
        actual = self.cabeza
        while actual is not None:
            identificador = clave(actual.ingrediente)
            if identificador in vistos:
                # anterior existe: el primer nodo siempre se conserva.
                anterior.siguiente = actual.siguiente
                if actual is self.cola:
                    self.cola = anterior
                eliminados += 1
            else:
                vistos.add(identificador)
                anterior = actual
            # No se avanza anterior al quitar un nodo: puede haber
            # varios repetidos consecutivos.
            actual = actual.siguiente
        return eliminados


@dataclass
class Postre:
    nombre: str
    ingredientes: ListaIngredientes


class CatalogoPostres:
    def __init__(self, datos: Iterable[tuple[str, Iterable[str]]] = ()) -> None:
        # La carga permite datos repetidos para resolver el ejercicio 2.
        # Cada registro recibe su propia lista; no se comparten nodos.
        self.POSTRES = [
            Postre(limpiar_texto(nombre), ListaIngredientes(ingredientes))
            for nombre, ingredientes in datos
        ]
        self.POSTRES.sort(key=lambda postre: orden_alfabetico(postre.nombre))

    def buscar(self, nombre: str) -> Optional[Postre]:
        buscado = clave(nombre)
        for postre in self.POSTRES:
            if clave(postre.nombre) == buscado:
                return postre
        return None

    def exigir_postre(self, nombre: str) -> Postre:
        postre = self.buscar(nombre)
        if postre is None:
            raise LookupError(f"No existe el postre: {limpiar_texto(nombre)}.")
        return postre

    # a) Obtener todos los ingredientes de un postre.
    def consultar_ingredientes(self, nombre: str) -> list[str]:
        return list(self.exigir_postre(nombre).ingredientes)

    # b) Insertar uno o varios ingredientes al final de su lista.
    def insertar_ingredientes(self, nombre: str, ingredientes: Iterable[str]) -> None:
        postre = self.exigir_postre(nombre)
        # Valida todo antes de cambiar la lista.
        nuevos = [limpiar_texto(ingrediente) for ingrediente in ingredientes]
        for ingrediente in nuevos:
            postre.ingredientes.agregar(ingrediente)

    # c) Eliminar una aparición de un ingrediente.
    def eliminar_ingrediente(self, nombre: str, ingrediente: str) -> bool:
        return self.exigir_postre(nombre).ingredientes.eliminar(ingrediente)

    # d) Dar de alta un postre sin romper el orden del arreglo.
    def alta(self, nombre: str, ingredientes: Iterable[str]) -> None:
        nombre = limpiar_texto(nombre)
        if self.buscar(nombre) is not None:
            raise ValueError("Ese postre ya existe; use insertar ingredientes.")
        nuevo = Postre(nombre, ListaIngredientes(ingredientes))
        posicion = 0
        while (posicion < len(self.POSTRES)
               and orden_alfabetico(self.POSTRES[posicion].nombre)
               < orden_alfabetico(nombre)):
            posicion += 1
        self.POSTRES.insert(posicion, nuevo)

    # e) Dar de baja un postre y su asociación con los ingredientes.
    def baja(self, nombre: str) -> None:
        buscado = clave(nombre)
        for posicion, postre in enumerate(self.POSTRES):
            if clave(postre.nombre) == buscado:
                del self.POSTRES[posicion]
                return
        raise LookupError(f"No existe el postre: {limpiar_texto(nombre)}.")

    # Ejercicio 2: limpiar tanto postres como ingredientes repetidos.
    def eliminar_repetidos(self) -> tuple[int, int]:
        conservados: dict[str, Postre] = {}
        unicos: list[Postre] = []
        postres_eliminados = 0
        for postre in self.POSTRES:
            identificador = clave(postre.nombre)
            if identificador not in conservados:
                conservados[identificador] = postre
                unicos.append(postre)
            else:
                destino = conservados[identificador].ingredientes
                for ingrediente in postre.ingredientes:
                    destino.agregar(ingrediente)
                postres_eliminados += 1
        # Se reemplaza el contenido después del recorrido.
        self.POSTRES[:] = unicos
        ingredientes_eliminados = sum(
            postre.ingredientes.eliminar_repetidos() for postre in self.POSTRES
        )
        return postres_eliminados, ingredientes_eliminados

    def mostrar(self) -> None:
        if not self.POSTRES:
            print("El arreglo POSTRES está vacío.")
        for postre in self.POSTRES:
            ingredientes = ", ".join(postre.ingredientes) or "sin ingredientes"
            print(f"{postre.nombre}: {ingredientes}")


def leer_ingredientes() -> list[str]:
    entrada = input("Ingredientes separados por coma (Enter para lista vacía): ")
    if not entrada.strip():
        return []
    return [limpiar_texto(parte) for parte in entrada.split(",")]


def demostracion() -> None:
    catalogo = CatalogoPostres([
        ("Flan", ["Leche", "Huevo", "Leche"]),
        ("flan", ["Azúcar", "Huevo"]),
        ("Gelatina", []),
        ("Pastel", ["Harina", "Harina", "Chocolate"]),
    ])
    print("ANTES:")
    catalogo.mostrar()
    postres, ingredientes = catalogo.eliminar_repetidos()
    print("\nDESPUÉS:")
    catalogo.mostrar()
    print(f"\nEliminados: {postres} postre(s) y {ingredientes} ingrediente(s).")
    print("Segunda limpieza:", catalogo.eliminar_repetidos())


def menu() -> None:
    catalogo = CatalogoPostres([
        ("Flan", ["Leche", "Huevo", "Azúcar"]),
        ("Gelatina", []),
        ("Pastel", ["Harina", "Huevo", "Chocolate"]),
    ])
    while True:
        print("\n1. Consultar ingredientes\n2. Insertar ingredientes"
              "\n3. Eliminar un ingrediente\n4. Dar de alta un postre"
              "\n5. Dar de baja un postre\n6. Eliminar todos los repetidos"
              "\n7. Mostrar POSTRES\n0. Salir")
        try:
            opcion = input("Opción: ").strip()
            if opcion == "0":
                return
            if opcion == "7":
                catalogo.mostrar()
            elif opcion == "6":
                postres, ingredientes = catalogo.eliminar_repetidos()
                print(f"Se eliminaron {postres} postre(s) y "
                      f"{ingredientes} ingrediente(s) repetidos.")
            elif opcion in {"1", "2", "3", "4", "5"}:
                nombre = input("Nombre del postre: ")
                if opcion == "1":
                    ingredientes = catalogo.consultar_ingredientes(nombre)
                    print(", ".join(ingredientes) or "Lista de ingredientes vacía.")
                elif opcion == "2":
                    catalogo.exigir_postre(nombre)
                    catalogo.insertar_ingredientes(nombre, leer_ingredientes())
                    print("Ingredientes procesados.")
                elif opcion == "3":
                    catalogo.exigir_postre(nombre)
                    eliminado = catalogo.eliminar_ingrediente(
                        nombre, input("Ingrediente que desea eliminar: "))
                    print("Ingrediente eliminado." if eliminado
                          else "Ese ingrediente no está en la lista.")
                elif opcion == "4":
                    catalogo.alta(nombre, leer_ingredientes())
                    print("Postre dado de alta.")
                else:
                    catalogo.baja(nombre)
                    print("Postre dado de baja.")
            else:
                print("Opción inválida.")
        except (ValueError, LookupError) as error:
            print(f"Aviso: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma finalizado.")
            return


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demostracion()
    else:
        menu()
