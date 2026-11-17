
import customtkinter as ctk
import networkx as nx
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

FONDO = "#10141F"
PANEL = "#181F2E"
TARJETA = "#202A3B"

AZUL = "#3B82F6"
VERDE = "#10B981"
MORADO = "#8B5CF6"
ROJO = "#F43F5E"

BLANCO = "#F1F5F9"
GRIS = "#94A3B8"


# ==========================================================
# CREACIÓN DE LOS GRAFOS
# ==========================================================

def crear_grafo():

    G = nx.Graph()

    estados = [
        "CDMX",
        "Edomex",
        "Querétaro",
        "Hidalgo",
        "Tlaxcala",
        "Puebla",
        "Morelos"
    ]

    G.add_nodes_from(estados)

    conexiones = [
        ("CDMX", "Edomex", 4),
        ("Edomex", "Querétaro", 3),
        ("Querétaro", "Hidalgo", 2),
        ("Hidalgo", "Tlaxcala", 5),
        ("Tlaxcala", "Puebla", 2),
        ("Puebla", "Morelos", 4),
        ("Morelos", "CDMX", 7),
        ("Edomex", "Hidalgo", 4),
        ("Edomex", "Puebla", 6)
    ]

    for u, v, peso in conexiones:
        G.add_edge(u, v, weight=peso)

    return G


# Grafo dirigido para demostrar Warshall

def crear_grafo_dirigido():

    D = nx.DiGraph()

    D.add_nodes_from([
        "CDMX",
        "Edomex",
        "Querétaro",
        "Hidalgo",
        "Tlaxcala",
        "Puebla",
        "Morelos"
    ])

    conexiones = [
        ("CDMX", "Edomex"),
        ("Edomex", "Querétaro"),
        ("Edomex", "Puebla"),
        ("Querétaro", "Hidalgo"),
        ("Hidalgo", "Tlaxcala"),
        ("Tlaxcala", "Puebla"),
        ("Puebla", "Morelos")
    ]

    D.add_edges_from(conexiones)

    return D


# ==========================================================
# ALGORITMO DE WARSHALL
# ==========================================================

def algoritmo_warshall(G):

    nodos = list(G.nodes())
    n = len(nodos)

    # Matriz inicial de alcanzabilidad

    matriz = [
        [
            1 if G.has_edge(nodos[i], nodos[j]) else 0
            for j in range(n)
        ]
        for i in range(n)
    ]

    # Cada nodo puede alcanzarse a sí mismo

    for i in range(n):
        matriz[i][i] = 1

    # Algoritmo de Warshall

    for k in range(n):

        for i in range(n):

            for j in range(n):

                matriz[i][j] = (
                    matriz[i][j] or
                    (matriz[i][k] and matriz[k][j])
                )

    return nodos, matriz


# ==========================================================
# ALGORITMO DE FLOYD-WARSHALL
# ==========================================================

def algoritmo_floyd(G):

    nodos = list(G.nodes())
    n = len(nodos)

    INF = float("inf")

    matriz = [
        [INF for _ in range(n)]
        for _ in range(n)
    ]

    # Inicializar distancias

    for i in range(n):
        matriz[i][i] = 0

    for u, v, datos in G.edges(data=True):

        i = nodos.index(u)
        j = nodos.index(v)

        peso = datos["weight"]

        matriz[i][j] = peso
        matriz[j][i] = peso

    # Algoritmo de Floyd-Warshall

    for k in range(n):

        for i in range(n):

            for j in range(n):

                nueva_distancia = (
                    matriz[i][k] + matriz[k][j]
                )

                if nueva_distancia < matriz[i][j]:

                    matriz[i][j] = nueva_distancia

    return nodos, matriz


# ==========================================================
# APLICACIÓN PRINCIPAL
# ==========================================================

class GraphExplorer:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Graph Explorer | Algoritmos de Grafos"
        )

        self.root.geometry("1350x850")
        self.root.minsize(1100, 720)

        self.root.configure(fg_color=FONDO)

        self.G = crear_grafo()

        self.D = crear_grafo_dirigido()

        self.nodos = list(self.G.nodes())

        self.pos = nx.spring_layout(
            self.G,
            seed=42,
            k=1.5
        )

        self.algoritmo_actual = "dijkstra"

        self.crear_interfaz()

        self.mostrar_algoritmo("dijkstra")

    # ======================================================
    # INTERFAZ
    # ======================================================

    def crear_interfaz(self):

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # PANEL LATERAL

        sidebar = ctk.CTkFrame(
            self.root,
            width=255,
            corner_radius=0,
            fg_color=PANEL
        )

        sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        sidebar.grid_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="◈ GRAPH EXPLORER",
            font=("Arial", 20, "bold"),
            text_color=AZUL
        ).pack(pady=(35, 5))

        ctk.CTkLabel(
            sidebar,
            text="ALGORITMOS DE GRAFOS",
            font=("Arial", 10, "bold"),
            text_color=GRIS
        ).pack(pady=(0, 40))

        ctk.CTkLabel(
            sidebar,
            text="NAVEGACIÓN",
            font=("Arial", 11, "bold"),
            text_color=GRIS,
            anchor="w"
        ).pack(fill="x", padx=22, pady=(0, 12))

        # BOTONES DE NAVEGACIÓN

        self.botones = {}

        algoritmos = [
            ("dijkstra", "01  Dijkstra"),
            ("floyd", "02  Floyd"),
            ("warshall", "03  Warshall"),
            ("kruskal", "04  Kruskal")
        ]

        for clave, nombre in algoritmos:

            boton = ctk.CTkButton(
                sidebar,
                text=nombre,
                height=45,
                anchor="w",
                corner_radius=10,
                fg_color=TARJETA,
                hover_color="#334155",
                font=("Arial", 12),
                command=lambda x=clave:
                    self.mostrar_algoritmo(x)
            )

            boton.pack(
                fill="x",
                padx=15,
                pady=5
            )

            self.botones[clave] = boton

        # INFORMACIÓN GENERAL

        ctk.CTkLabel(
            sidebar,
            text="RED DE ESTADOS",
            font=("Arial", 11, "bold"),
            text_color=GRIS,
            anchor="w"
        ).pack(fill="x", padx=22, pady=(40, 12))

        datos = [
            "●  7 estados",
            "●  9 conexiones",
            "●  Costos variables",
            "●  Grafo no dirigido"
        ]

        for dato in datos:

            ctk.CTkLabel(
                sidebar,
                text=dato,
                font=("Arial", 12),
                text_color=BLANCO,
                anchor="w"
            ).pack(fill="x", padx=22, pady=7)

        ctk.CTkLabel(
            sidebar,
            text="ESTRUCTURA DE DATOS\nProyecto de grafos",
            font=("Arial", 10),
            text_color=GRIS
        ).pack(side="bottom", pady=25)

        # ==================================================
        # CONTENIDO PRINCIPAL
        # ==================================================

        contenido = ctk.CTkFrame(
            self.root,
            fg_color=FONDO,
            corner_radius=0
        )

        contenido.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=25,
            pady=20
        )

        contenido.grid_columnconfigure(0, weight=1)
        contenido.grid_rowconfigure(2, weight=1)

        # ENCABEZADO

        self.lbl_titulo = ctk.CTkLabel(
            contenido,
            text="Algoritmo de Dijkstra",
            font=("Arial", 27, "bold"),
            text_color=BLANCO
        )

        self.lbl_titulo.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(5, 3)
        )

        self.lbl_descripcion = ctk.CTkLabel(
            contenido,
            text="Encontrar los caminos de menor costo desde un origen.",
            font=("Arial", 13),
            text_color=GRIS
        )

        self.lbl_descripcion.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(48, 15)
        )

        # CONTROLES DEL ALGORITMO

        self.controles = ctk.CTkFrame(
            contenido,
            fg_color=PANEL,
            corner_radius=12
        )

        self.controles.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        # Selector de origen para Dijkstra

        self.lbl_origen = ctk.CTkLabel(
            self.controles,
            text="Estado de origen:",
            font=("Arial", 12, "bold"),
            text_color=BLANCO
        )

        self.lbl_origen.pack(
            side="left",
            padx=(15, 8),
            pady=12
        )

        self.selector_origen = ctk.CTkOptionMenu(
            self.controles,
            values=self.nodos,
            width=160,
            fg_color=AZUL,
            button_color="#2563EB",
            command=self.actualizar_dijkstra
        )

        self.selector_origen.pack(
            side="left",
            padx=5,
            pady=12
        )

        self.lbl_control = ctk.CTkLabel(
            self.controles,
            text="Selecciona un origen para comenzar.",
            text_color=GRIS,
            font=("Arial", 11)
        )

        self.lbl_control.pack(
            side="left",
            padx=15
        )

        # ==================================================
        # ÁREA VISUAL
        # ==================================================

        area = ctk.CTkFrame(
            contenido,
            fg_color=PANEL,
            corner_radius=15
        )

        area.grid(
            row=2,
            column=0,
            sticky="nsew",
            pady=(0, 15)
        )

        area.grid_columnconfigure(0, weight=1)
        area.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            area,
            text="VISUALIZACIÓN DEL ALGORITMO",
            font=("Arial", 13, "bold"),
            text_color=BLANCO
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=15
        )

        # GRÁFICA

        self.fig, self.ax = plt.subplots(
            figsize=(7, 5),
            dpi=100
        )

        self.fig.patch.set_facecolor(PANEL)
        self.ax.set_facecolor(PANEL)

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=area
        )

        self.canvas.get_tk_widget().grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=5
        )


        # RESULTADOS REDIMENSIONABLES

        resultados = ctk.CTkFrame(
            contenido,
            fg_color=PANEL,
            corner_radius=15
        )

        resultados.grid(
            row=3,
            column=0,
            sticky="nsew"
        )

        resultados.configure(height=230)
        resultados.grid_propagate(False)

        ctk.CTkLabel(
            resultados,
            text="RESULTADOS Y EXPLICACIÓN",
            font=("Arial", 12, "bold"),
            text_color=BLANCO
        ).pack(
            anchor="w",
            padx=18,
            pady=(12, 5)
        )

        self.txt_resultados = ctk.CTkTextbox(
            resultados,
            font=("Consolas", 11),
            fg_color=TARJETA,
            text_color=BLANCO,
            corner_radius=10,
            wrap="word"
        )

        self.txt_resultados.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(5, 15)
        )

    # ======================================================
    # MOSTRAR ALGORITMO
    # ======================================================

    def mostrar_algoritmo(self, algoritmo):

        self.algoritmo_actual = algoritmo

        # Actualizar botones

        for clave, boton in self.botones.items():

            if clave == algoritmo:

                color = {
                    "dijkstra": AZUL,
                    "floyd": VERDE,
                    "warshall": MORADO,
                    "kruskal": ROJO
                }[clave]

                boton.configure(
                    fg_color=color,
                    font=("Arial", 12, "bold")
                )

            else:

                boton.configure(
                    fg_color=TARJETA,
                    font=("Arial", 12)
                )

        # Mostrar configuración correspondiente

        if algoritmo == "dijkstra":

            self.lbl_titulo.configure(
                text="01. Algoritmo de Dijkstra"
            )

            self.lbl_descripcion.configure(
                text="Calcula los caminos mínimos desde un nodo de origen."
            )

            self.mostrar_controles(True)

            self.actualizar_dijkstra(
                self.selector_origen.get()
            )

        elif algoritmo == "floyd":

            self.lbl_titulo.configure(
                text="02. Algoritmo de Floyd"
            )

            self.lbl_descripcion.configure(
                text="Calcula las distancias mínimas entre todos los pares."
            )

            self.mostrar_controles(False)

            self.ejecutar_floyd()

        elif algoritmo == "warshall":

            self.lbl_titulo.configure(
                text="03. Algoritmo de Warshall"
            )

            self.lbl_descripcion.configure(
                text="Determina si existe un camino entre dos nodos."
            )

            self.mostrar_controles(False)

            self.ejecutar_warshall()

        elif algoritmo == "kruskal":

            self.lbl_titulo.configure(
                text="04. Algoritmo de Kruskal"
            )

            self.lbl_descripcion.configure(
                text="Encuentra el árbol de expansión mínima."
            )

            self.mostrar_controles(False)

            self.ejecutar_kruskal()

    # ======================================================
    # MOSTRAR U OCULTAR CONTROLES
    # ======================================================

    def mostrar_controles(self, mostrar):

        if mostrar:

            self.lbl_origen.pack(
                side="left",
                padx=(15, 8),
                pady=12
            )

            self.selector_origen.pack(
                side="left",
                padx=5,
                pady=12
            )

            self.lbl_control.configure(
                text="Cambia el origen para recalcular."
            )

        else:

            self.lbl_origen.pack_forget()
            self.selector_origen.pack_forget()

            self.lbl_control.configure(
                text="Ejecutando algoritmo sobre la red."
            )

    # ======================================================
    # DIJKSTRA
    # ======================================================

    def actualizar_dijkstra(self, origen):

        distancias, rutas = nx.single_source_dijkstra(
            self.G,
            origen,
            weight="weight"
        )

        # Identificar las conexiones utilizadas

        aristas = set()

        for destino, ruta in rutas.items():

            for i in range(len(ruta) - 1):

                aristas.add(
                    frozenset((
                        ruta[i],
                        ruta[i + 1]
                    ))
                )

        seleccionadas = [
            (u, v)
            for u, v in self.G.edges()
            if frozenset((u, v)) in aristas
        ]

        self.dibujar_grafo(
            G=self.G,
            aristas_destacadas=seleccionadas,
            color=AZUL
        )

        # RESULTADOS

        texto = "ALGORITMO DE DIJKSTRA\n"
        texto += "=" * 48 + "\n"

        texto += f"Estado de origen: {origen}\n\n"

        texto += "RUTAS MÍNIMAS:\n\n"

        for destino in self.nodos:

            ruta = rutas[destino]

            texto += f"Destino: {destino}\n"

            texto += "Ruta: " + " → ".join(ruta) + "\n"

            texto += f"Costo mínimo: {distancias[destino]}\n"

            texto += "-" * 35 + "\n"

        self.mostrar_resultados(texto)

    # ======================================================
    # FLOYD
    # ======================================================

    def ejecutar_floyd(self):

        nodos, matriz = algoritmo_floyd(self.G)

        self.dibujar_grafo(
            G=self.G,
            aristas_destacadas=[],
            color=VERDE
        )

        texto = "ALGORITMO DE FLOYD-WARSHALL\n"
        texto += "=" * 48 + "\n\n"

        texto += "MATRIZ DE DISTANCIAS MÍNIMAS\n\n"

        texto += "Cada celda representa el costo mínimo entre dos estados.\n\n"

        ancho = 12

        texto += f"{'':{ancho}}"

        for nodo in nodos:

            texto += f"{nodo[:9]:>{ancho}}"

        texto += "\n"

        texto += "-" * (ancho * (len(nodos) + 1)) + "\n"

        for i, nodo in enumerate(nodos):

            texto += f"{nodo[:9]:<{ancho}}"

            for j in range(len(nodos)):

                valor = matriz[i][j]

                texto += f"{valor:>{ancho}.0f}"

            texto += "\n"

        texto += "\nINTERPRETACIÓN:\n"

        texto += (
            "La matriz muestra el costo mínimo para viajar "
            "entre cada par de estados, considerando "
            "todos los posibles estados intermedios.\n"
        )

        self.mostrar_resultados(texto)

    # ======================================================
    # WARSHALL
    # ======================================================

    def ejecutar_warshall(self):

        nodos, matriz = algoritmo_warshall(self.D)

        self.dibujar_grafo(
            G=self.D,
            aristas_destacadas=[],
            color=MORADO,
            dirigido=True
        )

        texto = "ALGORITMO DE WARSHALL\n"
        texto += "=" * 48 + "\n\n"

        texto += "MATRIZ DE ALCANZABILIDAD\n\n"

        texto += (
            "1 = Existe un camino\n"
            "0 = No existe un camino\n\n"
        )

        ancho = 12

        texto += f"{'':{ancho}}"

        for nodo in nodos:

            texto += f"{nodo[:9]:>{ancho}}"

        texto += "\n"

        texto += "-" * (ancho * (len(nodos) + 1)) + "\n"

        for i, nodo in enumerate(nodos):

            texto += f"{nodo[:9]:<{ancho}}"

            for j in range(len(nodos)):

                texto += f"{matriz[i][j]:>{ancho}}"

            texto += "\n"

        texto += "\nINTERPRETACIÓN:\n"

        texto += (
            "La matriz indica qué estados pueden alcanzar "
            "a otros mediante una o varias conexiones.\n"
            "No se calculan costos ni distancias mínimas.\n"
        )

        self.mostrar_resultados(texto)

    # ======================================================
    # KRUSKAL
    # ======================================================

    def ejecutar_kruskal(self):

        arbol = nx.minimum_spanning_tree(
            self.G,
            algorithm="kruskal",
            weight="weight"
        )

        seleccionadas = list(arbol.edges())

        costo_total = sum(
            datos["weight"]
            for u, v, datos in arbol.edges(data=True)
        )

        self.dibujar_grafo(
            G=self.G,
            aristas_destacadas=seleccionadas,
            color=ROJO
        )

        texto = "ALGORITMO DE KRUSKAL\n"
        texto += "=" * 48 + "\n\n"

        texto += "ÁRBOL DE EXPANSIÓN MÍNIMA\n\n"

        texto += "CONEXIONES SELECCIONADAS:\n\n"

        for u, v, datos in arbol.edges(data=True):

            texto += (
                f"{u} → {v} | "
                f"Costo: {datos['weight']}\n"
            )

        texto += "\n" + "-" * 35 + "\n"

        texto += f"Conexiones seleccionadas: {arbol.number_of_edges()}\n"

        texto += f"Nodos conectados: {arbol.number_of_nodes()}\n"

        texto += f"Costo total mínimo: {costo_total}\n"

        texto += "\nINTERPRETACIÓN:\n"

        texto += (
            "Se conectaron todos los estados con el menor "
            "costo posible, sin crear ciclos.\n"
        )

        self.mostrar_resultados(texto)

    # ======================================================
    # DIBUJAR GRAFO
    # ======================================================

    def dibujar_grafo(
        self,
        G,
        aristas_destacadas,
        color,
        dirigido=False
    ):

        self.ax.clear()

        self.ax.set_facecolor(PANEL)

        aristas_destacadas_set = {
            frozenset(e)
            for e in aristas_destacadas
        }

        aristas_normales = [
            (u, v)
            for u, v in G.edges()
            if frozenset((u, v))
            not in aristas_destacadas_set
        ]

        # Conexiones normales

        nx.draw_networkx_edges(
            G,
            self.pos,
            edgelist=aristas_normales,
            width=1.5,
            edge_color="#475569",
            style="dashed",
            alpha=0.7,
            arrows=dirigido,
            arrowsize=18,
            ax=self.ax
        )

        # Conexiones destacadas

        nx.draw_networkx_edges(
            G,
            self.pos,
            edgelist=aristas_destacadas,
            width=4,
            edge_color=color,
            arrows=dirigido,
            arrowsize=22,
            ax=self.ax
        )

        # Nodos

        nx.draw_networkx_nodes(
            G,
            self.pos,
            node_size=1750,
            node_color="#263B57",
            edgecolors=color,
            linewidths=2,
            ax=self.ax
        )

        # Etiquetas

        nx.draw_networkx_labels(
            G,
            self.pos,
            font_size=9,
            font_weight="bold",
            font_color="white",
            ax=self.ax
        )

        # Etiquetas de pesos

        if not dirigido:

            etiquetas = {
                (u, v): datos["weight"]
                for u, v, datos in G.edges(data=True)
            }

            nx.draw_networkx_edge_labels(
                G,
                self.pos,
                edge_labels=etiquetas,
                font_size=9,
                font_color="#CBD5E1",
                bbox={
                    "facecolor": PANEL,
                    "edgecolor": "none",
                    "alpha": 0.9
                },
                ax=self.ax
            )

        self.ax.set_title(
            "RED DE CONEXIONES ENTRE ESTADOS",
            color="white",
            fontsize=12,
            fontweight="bold",
            pad=15
        )

        self.ax.axis("off")

        self.fig.tight_layout()

        self.canvas.draw()

    # ======================================================
    # MOSTRAR RESULTADOS
    # ======================================================

    def mostrar_resultados(self, texto):

        self.txt_resultados.configure(state="normal")

        self.txt_resultados.delete("1.0", "end")

        self.txt_resultados.insert("1.0", texto)

        self.txt_resultados.configure(state="disabled")


# ==========================================================
# EJECUCIÓN
# ==========================================================

if __name__ == "__main__":

    root = ctk.CTk()

    app = GraphExplorer(root)

    root.mainloop()
