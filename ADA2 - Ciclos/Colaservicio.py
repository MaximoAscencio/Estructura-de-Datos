
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


def sistema_seguros():
    cantidad_servicios = 2

    colas = {}
    turnos = {}

    for servicio in range(1, cantidad_servicios + 1):
        colas[servicio] = Cola()
        turnos[servicio] = 1

    while True:
        print("\n--- SISTEMA DE SEGUROS ---")
        print("C + numero: Registrar cliente")
        print("A + numero: Atender cliente")
        print("S: Salir")
        comando = input("Ingrese una opcion: ").strip().upper()
        print("\n*******************************\n")

        if comando == "S":
            print("Sistema finalizado.")
            break

        if len(comando) < 2 or comando[0] not in ("C", "A") or not comando[1:].isdigit():
            print("Comando no valido.")
            continue

        servicio = int(comando[1:])

        if servicio not in colas:
            print("El servicio no existe.")
            print("\n*******************************\n")
            continue
            

        if comando[0] == "C":
            numero = turnos[servicio]
            colas[servicio].encolar(numero)

            print(f"Cliente registrado en servicio {servicio}")
            print(f"Turno asignado: {numero}")

            turnos[servicio] += 1

        elif comando[0] == "A":
            if colas[servicio].esta_vacia():
                print("No hay clientes en espera.")
                print("\n*******************************\n")
            else:
                numero = colas[servicio].desencolar()
                print(f"Servicio {servicio}: Atendiendo turno {numero}")

        print("\n*******************************\n")


sistema_seguros()
