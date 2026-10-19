
class Pila:
    def __init__(self):
        self.elementos = []

    def apilar(self, elemento):
        self.elementos.append(elemento)

    def desapilar(self):
        if self.esta_vacia():
            raise ValueError("La pila está vacía")
        return self.elementos.pop()

    def cima(self):
        if self.esta_vacia():
            raise ValueError("La pila está vacía")
        return self.elementos[-1]

    def esta_vacia(self):
        return len(self.elementos) == 0


def calcular(a, b, operador):
    if operador == "+":
        return a + b
    elif operador == "-":
        return a - b
    elif operador == "*":
        return a * b
    elif operador == "/":
        return a / b
    elif operador == "^":
        return a ** b


def evaluar_posfija(expresion):
    pila = Pila()
    operadores = ["+", "-", "*", "/", "^"]

    for elemento in expresion.split():
        if elemento in operadores:
            b = pila.desapilar()
            a = pila.desapilar()
            resultado = calcular(a, b, elemento)
            pila.apilar(resultado)
        else:
            pila.apilar(float(elemento))

    resultado = pila.desapilar()

    if not pila.esta_vacia():
        raise ValueError("Expresión inválida")

    return resultado


def evaluar_prefija(expresion):
    pila = Pila()
    operadores = ["+", "-", "*", "/", "^"]

    elementos = expresion.split()

    for elemento in reversed(elementos):
        if elemento in operadores:
            a = pila.desapilar()
            b = pila.desapilar()
            resultado = calcular(a, b, elemento)
            pila.apilar(resultado)
        else:
            pila.apilar(float(elemento))

    resultado = pila.desapilar()

    if not pila.esta_vacia():
        raise ValueError("Expresión inválida")

    return resultado


def main():
    while True:
        print("\n--- EVALUADOR DE EXPRESIONES ---")
        print("1. Notación posfija")
        print("2. Notación prefija")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            expresion = input("Expresión posfija: ")
            try:
                resultado = evaluar_posfija(expresion)
                print("Resultado:", resultado)
            except (ValueError, ZeroDivisionError):
                print("Error: expresión inválida")

        elif opcion == "2":
            expresion = input("Expresión prefija: ")
            try:
                resultado = evaluar_prefija(expresion)
                print("Resultado:", resultado)
            except (ValueError, ZeroDivisionError):
                print("Error: expresión inválida")

        elif opcion == "3":
            print("Programa finalizado")
            break

        else:
            print("Opción inválida")


main()
