"""
Interfaz gráfica (ventana de escritorio) para los métodos de búsqueda.

La usan Secuencial.py, Binaria.py, Hash.py y MenuBusqueda.py. Está hecha con
tkinter, que ya viene incluido con Python, así que no hay que instalar nada.

Funcionamiento de la ventana:
    1. Se elige el método (si la ventana tiene más de uno).
    2. Se escriben los datos (separados por comas) y el valor a buscar.
    3. Se presiona "Buscar".
    4. Se muestran el proceso paso a paso y el resultado.
    5. La ventana sigue abierta hasta que el usuario presiona "Salir".
"""

import tkinter as tk
from tkinter import ttk, messagebox


class VentanaBusqueda:
    def __init__(self, metodos, titulo):
        """
        metodos: diccionario {nombre: datos_del_metodo} donde datos_del_metodo es
                 un diccionario con las llaves:
                   "descripcion": texto que explica el ejercicio,
                   "etiqueta_datos": texto sobre el campo de datos,
                   "etiqueta_buscar": texto sobre el campo de búsqueda,
                   "ejemplo_datos": datos que aparecen por defecto,
                   "ejemplo_buscar": valor a buscar que aparece por defecto,
                   "buscar": función(datos, valor) -> (resultado, pasos)
                             que lanza ValueError si los datos no son válidos.
        """
        self.metodos = metodos

        self.raiz = tk.Tk()
        self.raiz.title(titulo)
        self.raiz.geometry("780x640")
        self.raiz.minsize(660, 560)
        self.raiz.protocol("WM_DELETE_WINDOW", self.salir)

        estilo = ttk.Style(self.raiz)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 16, "bold"))
        estilo.configure("Sub.TLabel", font=("Segoe UI", 10))
        estilo.configure("Resultado.TLabel", font=("Segoe UI", 11, "bold"))
        estilo.configure("TButton", padding=(10, 4))

        self.metodo = tk.StringVar(value=next(iter(metodos)))
        self.datos = tk.StringVar()
        self.valor = tk.StringVar()

        self._crear_widgets()
        self._cambiar_metodo()

    # ------------------------------------------------------------------
    def _crear_widgets(self):
        marco = ttk.Frame(self.raiz, padding=14)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text="Métodos de búsqueda", style="Titulo.TLabel").pack(anchor="w")

        # Selección del método
        fila = ttk.Frame(marco)
        fila.pack(fill="x", pady=(10, 0))
        ttk.Label(fila, text="Método:", style="Sub.TLabel").pack(side="left")
        self.combo = ttk.Combobox(fila, textvariable=self.metodo, state="readonly",
                                  values=list(self.metodos), width=22)
        self.combo.pack(side="left", padx=8)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self._cambiar_metodo())
        if len(self.metodos) == 1:
            self.combo.state(["disabled"])

        self.lbl_descripcion = ttk.Label(marco, style="Sub.TLabel", wraplength=720, justify="left")
        self.lbl_descripcion.pack(anchor="w", pady=(10, 8))

        # Datos
        self.lbl_datos = ttk.Label(marco, style="Sub.TLabel")
        self.lbl_datos.pack(anchor="w")
        self.ent_datos = ttk.Entry(marco, textvariable=self.datos)
        self.ent_datos.pack(fill="x", pady=(2, 8))

        # Valor a buscar
        self.lbl_valor = ttk.Label(marco, style="Sub.TLabel")
        self.lbl_valor.pack(anchor="w")
        self.ent_valor = ttk.Entry(marco, textvariable=self.valor)
        self.ent_valor.pack(fill="x", pady=(2, 8))
        self.ent_valor.bind("<Return>", lambda e: self.buscar())

        # Botones
        botones = ttk.Frame(marco)
        botones.pack(fill="x", pady=(4, 8))
        ttk.Button(botones, text="Buscar", command=self.buscar).pack(side="left")
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=8)
        ttk.Button(botones, text="Salir", command=self.salir).pack(side="right")

        # Resultado
        self.lbl_resultado = ttk.Label(marco, text="", style="Resultado.TLabel", wraplength=720)
        self.lbl_resultado.pack(anchor="w", pady=(0, 6))

        # Proceso paso a paso
        ttk.Label(marco, text="Proceso paso a paso:", style="Sub.TLabel").pack(anchor="w")
        cuadro = ttk.Frame(marco)
        cuadro.pack(fill="both", expand=True)
        barra = ttk.Scrollbar(cuadro)
        barra.pack(side="right", fill="y")
        self.texto = tk.Text(cuadro, height=12, wrap="word", font=("Consolas", 10),
                             yscrollcommand=barra.set, state="disabled")
        self.texto.pack(side="left", fill="both", expand=True)
        barra.config(command=self.texto.yview)

    # ------------------------------------------------------------------
    def _cambiar_metodo(self):
        info = self.metodos[self.metodo.get()]
        self.lbl_descripcion.config(text=info["descripcion"])
        self.lbl_datos.config(text=info["etiqueta_datos"])
        self.lbl_valor.config(text=info["etiqueta_buscar"])
        self.datos.set(info["ejemplo_datos"])
        self.valor.set(info["ejemplo_buscar"])
        self.limpiar_resultado()

    def _escribir(self, lineas):
        self.texto.config(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert("end", "\n".join(lineas))
        self.texto.config(state="disabled")

    def limpiar_resultado(self):
        self.lbl_resultado.config(text="")
        self._escribir([])

    def limpiar(self):
        self.datos.set("")
        self.valor.set("")
        self.limpiar_resultado()
        self.ent_datos.focus_set()

    def buscar(self):
        info = self.metodos[self.metodo.get()]
        try:
            resultado, pasos = info["buscar"](self.datos.get(), self.valor.get())
        except ValueError as error:
            messagebox.showwarning("Datos no válidos", str(error))
            return
        self.lbl_resultado.config(text=resultado)
        self._escribir(pasos)

    def salir(self):
        if messagebox.askyesno("Salir", "¿Seguro que deseas salir del programa?"):
            self.raiz.destroy()

    def iniciar(self):
        self.raiz.mainloop()
