import tkinter as tk
from tkinter import ttk, messagebox


class Nodo:
    def __init__(self, identificador, dato):
        self.id = identificador
        self.info = dato
        self.liga = None


class ListaVisual:
    def __init__(self, ventana):
        self.ventana = ventana
        self.nodos = {}
        self.siguiente_id = 1

        ventana.title("Nodos y enlaces visuales")
        ventana.geometry("1000x650")

        controles = ttk.Frame(ventana, padding=10)
        controles.pack(fill="x")

        ttk.Label(controles, text="Dato:").grid(row=0, column=0)

        self.dato = ttk.Entry(controles, width=18)
        self.dato.grid(row=0, column=1, padx=5)

        ttk.Button(
            controles, text="Crear nodo", command=self.crear
        ).grid(row=0, column=2, padx=5)

        ttk.Label(controles, text="Origen:").grid(row=1, column=0)

        self.origen = ttk.Combobox(
            controles, state="readonly", width=15
        )
        self.origen.grid(row=1, column=1, padx=5, pady=10)

        ttk.Label(controles, text="Destino:").grid(row=1, column=2)

        self.destino = ttk.Combobox(
            controles, state="readonly", width=15
        )
        self.destino.grid(row=1, column=3, padx=5)

        ttk.Button(
            controles, text="Conectar", command=self.conectar
        ).grid(row=1, column=4, padx=5)

        ttk.Button(
            controles, text="Quitar enlace", command=self.desconectar
        ).grid(row=1, column=5, padx=5)

        ttk.Button(
            controles,
            text="Cambiar dato del origen",
            command=self.cambiar_dato
        ).grid(row=0, column=3, columnspan=2, padx=5)

        ttk.Label(
            ventana,
            text=(
                "Cada nodo tiene un ID fijo. Las flechas indican sus enlaces.\n"
                "Varios nodos pueden apuntar al mismo destino."
            ),
            justify="center"
        ).pack(pady=5)

        self.canvas = tk.Canvas(
            ventana, background="#f1f5f9", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.bind("<Configure>", lambda evento: self.dibujar())

        self.estado = tk.StringVar()
        ttk.Label(
            ventana, textvariable=self.estado, padding=10
        ).pack(fill="x")

        # Ejemplo inicial: N1 y N2 apuntan al mismo nodo N3.
        a = self.agregar_nodo("10")
        b = self.agregar_nodo("20")
        compartido = self.agregar_nodo("30")

        a.liga = compartido
        b.liga = compartido

        self.actualizar_opciones()
        self.estado.set("N1 y N2 comparten el nodo N3.")
        self.dibujar()

    def agregar_nodo(self, dato):
        identificador = f"N{self.siguiente_id}"
        self.siguiente_id += 1

        nodo = Nodo(identificador, dato)
        self.nodos[identificador] = nodo
        return nodo

    def actualizar_opciones(self):
        opciones = list(self.nodos)

        for selector in (self.origen, self.destino):
            selector["values"] = opciones
            if not selector.get() and opciones:
                selector.set(opciones[0])

    def crear(self):
        texto = self.dato.get().strip()
        nodo = self.agregar_nodo(texto if texto else None)

        self.actualizar_opciones()
        self.origen.set(nodo.id)
        self.dato.delete(0, tk.END)
        self.estado.set(f"Se creó el nodo {nodo.id}.")
        self.dibujar()

    def conectar(self):
        origen = self.nodos.get(self.origen.get())
        destino = self.nodos.get(self.destino.get())

        if origen is None or destino is None:
            return

        # Evitar ciclos para mantener recorridos con un final.
        actual = destino
        while actual is not None:
            if actual is origen:
                messagebox.showwarning(
                    "Conexión inválida",
                    "Ese enlace produciría un ciclo."
                )
                return
            actual = actual.liga

        origen.liga = destino
        self.estado.set(f"{origen.id} ahora apunta a {destino.id}.")
        self.dibujar()

    def desconectar(self):
        origen = self.nodos.get(self.origen.get())
        if origen is not None:
            origen.liga = None
            self.estado.set(f"{origen.id} ahora apunta a FIN.")
            self.dibujar()

    def cambiar_dato(self):
        origen = self.nodos.get(self.origen.get())
        if origen is not None:
            texto = self.dato.get().strip()
            origen.info = texto if texto else None
            self.estado.set(f"Se actualizó el dato de {origen.id}.")
            self.dibujar()

    def dibujar(self):
        self.canvas.delete("all")

        ancho = max(self.canvas.winfo_width(), 300)
        columnas = max(1, ancho // 230)
        posiciones = {}

        for indice, nodo in enumerate(self.nodos.values()):
            fila, columna = divmod(indice, columnas)
            posiciones[nodo.id] = (
                40 + columna * 230,
                45 + fila * 150
            )

        # Dibujar los enlaces detrás de los nodos.
        for nodo in self.nodos.values():
            x, y = posiciones[nodo.id]

            if nodo.liga is not None:
                dx, dy = posiciones[nodo.liga.id]

                if y == dy:
                    if dx > x:
                        inicio = (x + 150, y + 35)
                        final = (dx, dy + 35)
                    else:
                        inicio = (x, y + 35)
                        final = (dx + 150, dy + 35)
                elif dy > y:
                    inicio = (x + 75, y + 70)
                    final = (dx + 75, dy)
                else:
                    inicio = (x + 75, y)
                    final = (dx + 75, dy + 70)

                self.canvas.create_line(
                    *inicio, *final,
                    arrow=tk.LAST,
                    arrowshape=(12, 14, 6),
                    width=3,
                    fill="#2563eb"
                )

        for nodo in self.nodos.values():
            x, y = posiciones[nodo.id]
            dato = "[vacío]" if nodo.info is None else str(nodo.info)
            destino = nodo.liga.id if nodo.liga else "FIN"

            self.canvas.create_rectangle(
                x, y, x + 150, y + 70,
                fill="#ffffff", outline="#334155", width=2
            )
            self.canvas.create_text(
                x + 75, y + 19,
                text=f"{nodo.id}: {dato}",
                width=140,
                font=("Arial", 11, "bold")
            )
            self.canvas.create_text(
                x + 75, y + 51,
                text=f"liga → {destino}",
                fill="#2563eb",
                font=("Arial", 10)
            )

        limites = self.canvas.bbox("all")
        if limites:
            self.canvas.configure(scrollregion=limites)


if __name__ == "__main__":
    ventana = tk.Tk()
    ListaVisual(ventana)
    ventana.mainloop()