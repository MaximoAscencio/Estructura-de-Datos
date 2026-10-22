
class Cola:
    def __init__(self):
        self.elementos = []

    def encolar(self, numero):
        self.elementos.append(numero)

    def desencolar(self):
        if not self.esta_vacia():
            return self.elementos.pop(0)
        return None

    def esta_vacia(self):
        return len(self.elementos) == 0

def sumar_colas(cola_a, cola_b):
    cola_resultado = Cola()

    if len(cola_a.elementos) != len(cola_b.elementos):
        print("Las colas deben tener el mismo tamaño")
        return None

    while not cola_a.esta_vacia():
        numero_a = cola_a.desencolar()
        numero_b = cola_b.desencolar()

        suma = numero_a + numero_b

        cola_resultado.encolar(suma)

    return cola_resultado
cola_a = Cola()



cola_a = Cola()
cola_b = Cola()

for numero in [3, 4, 2, 8, 12]:
    cola_a.encolar(numero)

for numero in [6, 2, 9, 11, 3]:
    cola_b.encolar(numero)

print("Cola A:", cola_a.elementos)
print("Cola B:", cola_b.elementos)

resultado = sumar_colas(cola_a, cola_b)

if resultado is not None:
    print("Cola R:", resultado.elementos)





