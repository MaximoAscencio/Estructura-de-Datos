"""
Interfaz gráfica (ventana de escritorio) para los métodos de ordenamiento.

La usan ShellSort.py, QuickSort.py, HeapSort.py, Radix.py y
MenuOrdenamiento.py. Está hecha con tkinter, que ya viene incluido con
Python, así que no hay que instalar nada.

Funcionamiento de la ventana:
    1. Se elige el método (si la ventana tiene más de uno).
    2. Se escribe la cantidad de números y se presiona "Aceptar"; aparecen
       tantas casillas como números se pidieron.
    3. Se escriben los números y se presiona "Ordenar".
    4. Se muestran el proceso paso a paso y la lista ordenada.
    5. La ventana sigue abierta hasta que el usuario presiona "Salir".
"""

import tkinter as tk
from tkinter import ttk, messagebox

MAX_NUMEROS = 50
COLUMNAS = 5


def formatear(numero):
    """Muestra 5.0 como 5 y deja 5.5 como 5.5."""
    return str(int(numero)) if float(numero).is_integer() else str(numero)


def mostrar_lista(lista):
    return "[" + ", ".join(formatear(x) for x in lista) + "]"


class VentanaOrdenamiento:
    def __init__(self, metodos, titulo):
        """
        metodos: diccionario {nombre: (funcion, solo_enteros, descripcion)}
                 donde funcion(lista) regresa (lista_ordenada, pasos).
        """
        self.metodos = metodos
        self.casillas = []

        self.raiz = tk.Tk()
        self.raiz.title(titulo)
        self.raiz.geometry("760x640")
        self.raiz.minsize(640, 560)
        self.raiz.protocol("WM_DELETE_WINDOW", self.salir)

        estilo = ttk.Style(self.raiz)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 16, "bold"))
        estilo.configure("Sub.TLabel", font=("Segoe UI", 10))
        estilo.configure("Resultado.TLabel", font=("Segoe UI", 11, "bold"))
        estilo.configure("TButton", padding=(10, 4))

        self.metodo = tk.StringVar(value=next(iter(metodos)))
        self.cantidad = tk.StringVar(value="5")

        self._crear_menu()
        self._crear_widgets()
        self._actualizar_descripcion()

    # ------------------------------------------------------------ armado
    def _crear_menu(self):
        barra = tk.Menu(self.raiz)
        archivo = tk.Menu(barra, tearoff=0)
        archivo.add_command(label="Limpiar", command=self.limpiar)
        archivo.add_separator()
        archivo.add_command(label="Salir", command=self.salir)
        barra.add_cascade(label="Archivo", menu=archivo)

        if len(self.metodos) > 1:
            menu_metodos = tk.Menu(barra, tearoff=0)
            for nombre in self.metodos:
                menu_metodos.add_radiobutton(label=nombre, value=nombre,
                                             variable=self.metodo,
                                             command=self._actualizar_descripcion)
            barra.add_cascade(label="Método", menu=menu_metodos)
        self.raiz.config(menu=barra)

    def _crear_widgets(self):
        principal = ttk.Frame(self.raiz, padding=14)
        principal.pack(fill="both", expand=True)

        self.lbl_titulo = ttk.Label(principal, style="Titulo.TLabel")
        self.lbl_titulo.pack(anchor="w")
        self.lbl_descripcion = ttk.Label(principal, style="Sub.TLabel",
                                         wraplength=700, justify="left")
        self.lbl_descripcion.pack(anchor="w", pady=(2, 10))

        # Selección del método (solo cuando hay más de uno).
        if len(self.metodos) > 1:
            marco_metodo = ttk.LabelFrame(principal, text=" Método de ordenamiento ",
                                          padding=8)
            marco_metodo.pack(fill="x", pady=(0, 8))
            for nombre in self.metodos:
                ttk.Radiobutton(marco_metodo, text=nombre, value=nombre,
                                variable=self.metodo,
                                command=self._actualizar_descripcion
                                ).pack(side="left", padx=(0, 18))

        # Cantidad de números.
        marco_cantidad = ttk.LabelFrame(principal, text=" Datos ", padding=8)
        marco_cantidad.pack(fill="x")
        fila = ttk.Frame(marco_cantidad)
        fila.pack(fill="x")
        ttk.Label(fila, text="Cantidad de números:").pack(side="left")
        caja = ttk.Spinbox(fila, from_=1, to=MAX_NUMEROS, width=6,
                           textvariable=self.cantidad)
        caja.pack(side="left", padx=6)
        caja.bind("<Return>", lambda e: self.crear_casillas())
        ttk.Button(fila, text="Aceptar", command=self.crear_casillas).pack(side="left")

        # Casillas para los números.
        self.marco_numeros = ttk.Frame(marco_cantidad)
        self.marco_numeros.pack(fill="x", pady=(8, 0))

        # Botones.
        botones = ttk.Frame(principal)
        botones.pack(fill="x", pady=10)
        ttk.Button(botones, text="Ordenar", command=self.ordenar).pack(side="left")
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=6)
        ttk.Button(botones, text="Salir", command=self.salir).pack(side="right")

        # Resultado.
        marco_resultado = ttk.LabelFrame(principal, text=" Proceso paso a paso ",
                                         padding=8)
        marco_resultado.pack(fill="both", expand=True)
        self.texto = tk.Text(marco_resultado, height=10, wrap="word",
                             font=("Consolas", 10), state="disabled",
                             relief="flat", background="#fafafa")
        barra = ttk.Scrollbar(marco_resultado, command=self.texto.yview)
        self.texto.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        self.texto.pack(side="left", fill="both", expand=True)

        self.lbl_resultado = ttk.Label(principal, style="Resultado.TLabel",
                                       wraplength=700, justify="left")
        self.lbl_resultado.pack(anchor="w", pady=(8, 0))

        self.crear_casillas()

    # ----------------------------------------------------------- acciones
    def _actualizar_descripcion(self):
        nombre = self.metodo.get()
        _, solo_enteros, descripcion = self.metodos[nombre]
        self.lbl_titulo.config(text=f"Método {nombre}")
        aviso = "  (Solo acepta números enteros.)" if solo_enteros else ""
        self.lbl_descripcion.config(text=descripcion + aviso)

    def crear_casillas(self):
        try:
            cantidad = int(self.cantidad.get())
            if not 1 <= cantidad <= MAX_NUMEROS:
                raise ValueError
        except ValueError:
            messagebox.showerror("Cantidad no válida",
                                 f"Escribe un número entero entre 1 y {MAX_NUMEROS}.")
            return

        # Se conservan los valores que ya se habían escrito.
        anteriores = [c.get() for c in self.casillas]
        for widget in self.marco_numeros.winfo_children():
            widget.destroy()
        self.casillas = []

        for i in range(cantidad):
            celda = ttk.Frame(self.marco_numeros)
            celda.grid(row=i // COLUMNAS, column=i % COLUMNAS, padx=4, pady=3, sticky="w")
            ttk.Label(celda, text=f"{i + 1}.", width=3, anchor="e").pack(side="left")
            casilla = ttk.Entry(celda, width=9)
            casilla.pack(side="left")
            if i < len(anteriores):
                casilla.insert(0, anteriores[i])
            casilla.bind("<Return>", lambda e: self.ordenar())
            self.casillas.append(casilla)
        if self.casillas:
            self.casillas[0].focus_set()

    def leer_numeros(self, solo_enteros):
        numeros = []
        for i, casilla in enumerate(self.casillas, start=1):
            valor = casilla.get().strip()
            try:
                numeros.append(int(valor) if solo_enteros else float(valor))
            except ValueError:
                tipo = "un número entero" if solo_enteros else "un número"
                messagebox.showerror("Dato no válido",
                                     f"La casilla {i} debe tener {tipo}.")
                casilla.focus_set()
                return None
        return numeros

    def ordenar(self):
        nombre = self.metodo.get()
        funcion, solo_enteros, _ = self.metodos[nombre]
        numeros = self.leer_numeros(solo_enteros)
        if numeros is None:
            return

        ordenados, pasos = funcion(numeros)

        lineas = [f"Lista original: {mostrar_lista(numeros)}", "",
                  f"Proceso de {nombre}:"]
        lineas += ["  " + paso for paso in pasos]
        lineas += ["", f"Lista ordenada: {mostrar_lista(ordenados)}"]
        self._escribir("\n".join(lineas))
        self.lbl_resultado.config(
            text=f"Resultado con {nombre}: {mostrar_lista(ordenados)}")

    def _escribir(self, contenido):
        self.texto.config(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", contenido)
        self.texto.config(state="disabled")

    def limpiar(self):
        for casilla in self.casillas:
            casilla.delete(0, "end")
        self._escribir("")
        self.lbl_resultado.config(text="")
        if self.casillas:
            self.casillas[0].focus_set()

    def salir(self):
        if messagebox.askyesno("Salir", "¿Deseas salir del programa?"):
            self.raiz.destroy()

    def iniciar(self):
        self.raiz.mainloop()
