
class Pila:
    def __init__(self):
        self.elementos = []

    def apilar(self, elemento):
        self.elementos.append(elemento)

    def desapilar(self):
        if self.esta_vacia():
            return None
        return self.elementos.pop()

    def cima(self):
        if self.esta_vacia():
            return None
        return self.elementos[-1]

    def esta_vacia(self):
        return len(self.elementos) == 0


class Navegador:
    def __init__(self):
        self.atras = Pila()
        self.adelante = Pila()
        self.historial = Pila()
        self.actual = None

    def visitar(self, sitio):
        if self.actual is not None:
            self.atras.apilar(self.actual)

        self.actual = sitio
        self.historial.apilar(sitio)
        self.adelante = Pila()

        print("Visitando:", self.actual)

    def retroceder(self):
        if self.atras.esta_vacia():
            print("No hay páginas anteriores")
        else:
            self.adelante.apilar(self.actual)
            self.actual = self.atras.desapilar()
            print("Regresando a:", self.actual)

    def avanzar(self):
        if self.adelante.esta_vacia():
            print("No hay páginas siguientes")
        else:
            self.atras.apilar(self.actual)
            self.actual = self.adelante.desapilar()
            print("Avanzando a:", self.actual)

    def mostrar_actual(self):
        if self.actual is None:
            print("No hay ninguna página abierta")
        else:
            print("Página actual:", self.actual)

    def mostrar_historial(self):
        if self.historial.esta_vacia():
            print("El historial está vacío")
        else:
            print("\n--- HISTORIAL DE VISITAS ---")
            for sitio in reversed(self.historial.elementos):
                print(sitio)


def main():
    navegador = Navegador()

    while True:
        print("\n--- NAVEGADOR WEB ---")
        print("1. Visitar página")
        print("2. Retroceder")
        print("3. Avanzar")
        print("4. Mostrar página actual")
        print("5. Mostrar historial")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            sitio = input("Ingrese la URL: ").strip()
            if sitio:
                navegador.visitar(sitio)
            else:
                print("La URL no puede estar vacía")

        elif opcion == "2":
            navegador.retroceder()

        elif opcion == "3":
            navegador.avanzar()

        elif opcion == "4":
            navegador.mostrar_actual()

        elif opcion == "5":
            navegador.mostrar_historial()

        elif opcion == "6":
            print("Cerrando navegador...")
            break

        else:
            print("Opción inválida")


main()
