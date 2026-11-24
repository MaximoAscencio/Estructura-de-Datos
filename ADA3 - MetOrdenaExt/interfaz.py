"""
Interfaz gráfica (ventana de escritorio) para los métodos de ordenamiento externo.

La usan Intercalacion.py, MezclaDirecta.py, MezclaEquilibrada.py y
MenuOrdenamientoExt.py. Está hecha con tkinter, que ya viene incluido con
Python, así que no hay que instalar nada.

Funcionamiento de la ventana:
    1. Se elige el método (si la ventana tiene más de uno).
    2. Se escriben los números separados por comas (algunos métodos piden dos listas).
    3. Se presiona "Ordenar".
    4. Se muestran el proceso paso a paso y el resultado.
    5. La ventana sigue abierta hasta que el usuario presiona "Salir".
"""

import tkinter as tk
from tkinter import ttk, messagebox


def formatear(numero):
    """Muestra 5.0 como 5 y deja 5.5 como 5.5."""
    return str(int(numero)) if float(numero).is_integer() else str(numero)


def mostrar_lista(lista):
    return "[" + ", ".join(formatear(x) for x in lista) + "]"


def mostrar_bloques(bloques):
    """Muestra una lista de bloques como  [1, 4] [2, 9] [7]"""
    return " ".join(mostrar_lista(b) for b in bloques) if bloques else "(vacío)"


def leer_numeros(texto, nombre="La lista"):
    """Convierte 'a, b, c' en una lista de números. Lanza ValueError si hay un error."""
    partes = [t.strip() for t in texto.split(",") if t.strip()]
    if not partes:
        raise ValueError(f"{nombre} está vacía. Escribe números separados por comas.")
    numeros = []
    for parte in partes:
        try:
            numeros.append(float(parte))
        except ValueError:
            raise ValueError(f"'{parte}' no es un número válido en {nombre.lower()}.")
    return numeros


class VentanaOrdenamiento:
    def __init__(self, metodos, titulo):
        """
        metodos: diccionario {nombre: datos_del_metodo} donde datos_del_metodo es
                 un diccionario con las llaves:
                   "descripcion":    texto que explica el ejercicio,
                   "etiqueta_datos": texto sobre el primer campo,
                   "ejemplo_datos":  valor que aparece por defecto en el primer campo,
                   "etiqueta_valor": (opcional) texto sobre el segundo campo; si no
                                     está, el segundo campo se oculta,
                   "ejemplo_valor":  (opcional) valor por defecto del segundo campo,
                   "ejecutar": función(datos, valor) -> (resultado, pasos)
                               que lanza ValueError si los datos no son válidos.
        """
        self.metodos = metodos

        self.raiz = tk.Tk()
        self.raiz.title(titulo)
        self.raiz.geometry("800x660")
        self.raiz.minsize(680, 580)
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

        ttk.Label(marco, text="Métodos de ordenamiento externo",
                  style="Titulo.TLabel").pack(anchor="w")

        fila = ttk.Frame(marco)
        fila.pack(fill="x", pady=(10, 0))
        ttk.Label(fila, text="Método:", style="Sub.TLabel").pack(side="left")
        self.combo = ttk.Combobox(fila, textvariable=self.metodo, state="readonly",
                                  values=list(self.metodos), width=24)
        self.combo.pack(side="left", padx=8)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self._cambiar_metodo())
        if len(self.metodos) == 1:
            self.combo.state(["disabled"])

        self.lbl_descripcion = ttk.Label(marco, style="Sub.TLabel", wraplength=740, justify="left")
        self.lbl_descripcion.pack(anchor="w", pady=(10, 8))

        self.lbl_datos = ttk.Label(marco, style="Sub.TLabel")
        self.lbl_datos.pack(anchor="w")
        self.ent_datos = ttk.Entry(marco, textvariable=self.datos)
        self.ent_datos.pack(fill="x", pady=(2, 8))

        # Segundo campo (solo lo usan los métodos que piden dos listas)
        self.marco_valor = ttk.Frame(marco)
        self.lbl_valor = ttk.Label(self.marco_valor, style="Sub.TLabel")
        self.lbl_valor.pack(anchor="w")
        self.ent_valor = ttk.Entry(self.marco_valor, textvariable=self.valor)
        self.ent_valor.pack(fill="x", pady=(2, 8))
        self.ent_valor.bind("<Return>", lambda e: self.ejecutar())

        self.botones = ttk.Frame(marco)
        self.botones.pack(fill="x", pady=(4, 8))
        ttk.Button(self.botones, text="Ordenar", command=self.ejecutar).pack(side="left")
        ttk.Button(self.botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=8)
        ttk.Button(self.botones, text="Salir", command=self.salir).pack(side="right")

        self.lbl_resultado = ttk.Label(marco, text="", style="Resultado.TLabel", wraplength=740)
        self.lbl_resultado.pack(anchor="w", pady=(0, 6))

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
        self.datos.set(info["ejemplo_datos"])
        if "etiqueta_valor" in info:
            self.lbl_valor.config(text=info["etiqueta_valor"])
            self.valor.set(info.get("ejemplo_valor", ""))
            self.marco_valor.pack(fill="x", before=self.botones)
        else:
            self.valor.set("")
            self.marco_valor.pack_forget()
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

    def ejecutar(self):
        info = self.metodos[self.metodo.get()]
        try:
            resultado, pasos = info["ejecutar"](self.datos.get(), self.valor.get())
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
