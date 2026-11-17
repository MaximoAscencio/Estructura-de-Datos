
import customtkinter as ctk
import networkx as nx
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLOR_FONDO = "#10141F"
COLOR_PANEL = "#181F2E"
COLOR_TARJETA = "#202A3B"
COLOR_AZUL = "#3B82F6"
COLOR_VERDE = "#10B981"
COLOR_ROJO = "#F43F5E"
COLOR_TEXTO = "#F1F5F9"
COLOR_SECUNDARIO = "#94A3B8"


# ==========================================================
# CREACIÓN DEL GRAFO
# ==========================================================

def crear_grafo():

    G = nx.Graph()

    estados = [
        "CDMX", "Edomex", "Puebla",
        "Morelos", "Hidalgo",
        "Tlaxcala", "Querétaro"
    ]

    G.add_nodes_from(estados)

    conexiones = [
        ("CDMX", "Edomex"),
        ("Edomex", "Querétaro"),
        ("Querétaro", "Hidalgo"),
        ("Hidalgo", "Tlaxcala"),
        ("Tlaxcala", "Puebla"),
        ("Puebla", "Morelos"),
        ("Morelos", "CDMX"),
        ("Edomex", "Hidalgo"),
        ("Edomex", "Puebla")
    ]

    costo = 1000

    for u, v in conexiones:
        G.add_edge(u, v, weight=costo)

    return G, costo


def obtener_rutas():

    ruta_1 = [
        "CDMX",
        "Edomex",
        "Querétaro",
        "Hidalgo",
        "Tlaxcala",
        "Puebla",
        "Morelos"
    ]

    ruta_2 = [
        "CDMX",
        "Edomex",
        "Querétaro",
        "Hidalgo",
        "Tlaxcala",
        "Puebla",
        "Morelos",
        "CDMX"
    ]

    return ruta_1, ruta_2


# ==========================================================
# APLICACIÓN PRINCIPAL
# ==========================================================

class AplicacionGrafos:

    def __init__(self, root):

        self.root = root

        self.root.title("Graph Explorer | Análisis de Grafos")
        self.root.geometry("1280x800")
        self.root.minsize(1050, 700)
        self.root.configure(fg_color=COLOR_FONDO)

        self.G, self.costo_vuelo = crear_grafo()

        self.ruta_1, self.ruta_2 = obtener_rutas()

        # Ruta construida por el usuario
        self.ruta_personalizada = []

        self.ruta_actual = 1

        # Orden de los nodos para detectar clics
        self.nodos = list(self.G.nodes())

        self.pos = nx.spring_layout(
            self.G,
            seed=42,
            k=1.5
        )

        self.crear_interfaz()

        # Evento para detectar clics sobre los nodos
        self.canvas.mpl_connect(
            "pick_event",
            self.al_seleccionar_nodo
        )

        self.mostrar_ruta(1)

    # ======================================================
    # INTERFAZ
    # ======================================================

    def crear_interfaz(self):

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # PANEL LATERAL

        sidebar = ctk.CTkFrame(
            self.root,
            width=245,
            corner_radius=0,
            fg_color=COLOR_PANEL
        )

        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="◈ GRAPH EXPLORER",
            font=("Arial", 20, "bold"),
            text_color=COLOR_AZUL
        ).pack(pady=(35, 5), padx=20)

        ctk.CTkLabel(
            sidebar,
            text="ANÁLISIS DE GRAFOS",
            font=("Arial", 10, "bold"),
            text_color=COLOR_SECUNDARIO
        ).pack(pady=(0, 40))

        ctk.CTkLabel(
            sidebar,
            text="NAVEGACIÓN",
            font=("Arial", 11, "bold"),
            text_color=COLOR_SECUNDARIO,
            anchor="w"
        ).pack(fill="x", padx=25, pady=(0, 10))

        # OPCIÓN 1

        self.btn_ruta1 = ctk.CTkButton(
            sidebar,
            text="  01  Sin repetir estados",
            height=45,
            anchor="w",
            corner_radius=10,
            fg_color=COLOR_AZUL,
            hover_color="#2563EB",
            font=("Arial", 12, "bold"),
            command=lambda: self.mostrar_ruta(1)
        )

        self.btn_ruta1.pack(fill="x", padx=15, pady=5)

        # OPCIÓN 2

        self.btn_ruta2 = ctk.CTkButton(
            sidebar,
            text="  02  Con repetición",
            height=45,
            anchor="w",
            corner_radius=10,
            fg_color=COLOR_TARJETA,
            hover_color="#334155",
            font=("Arial", 12),
            command=lambda: self.mostrar_ruta(2)
        )

        self.btn_ruta2.pack(fill="x", padx=15, pady=5)

        # OPCIÓN 3: RUTA PERSONALIZADA

        self.btn_personalizada = ctk.CTkButton(
            sidebar,
            text="  03  Ruta personalizada",
            height=45,
            anchor="w",
            corner_radius=10,
            fg_color=COLOR_TARJETA,
            hover_color="#334155",
            font=("Arial", 12),
            command=lambda: self.mostrar_ruta(3)
        )

        self.btn_personalizada.pack(fill="x", padx=15, pady=5)

        # INFORMACIÓN

        ctk.CTkLabel(
            sidebar,
            text="INFORMACIÓN",
            font=("Arial", 11, "bold"),
            text_color=COLOR_SECUNDARIO,
            anchor="w"
        ).pack(fill="x", padx=25, pady=(40, 12))

        info = [
            "●  7 estados",
            "●  9 conexiones",
            "●  Costo por vuelo: $1,000",
            "●  Grafo no dirigido"
        ]

        for texto in info:

            ctk.CTkLabel(
                sidebar,
                text=texto,
                font=("Arial", 12),
                text_color=COLOR_TEXTO,
                anchor="w"
            ).pack(fill="x", padx=25, pady=8)

        # PIE DEL PANEL

        ctk.CTkLabel(
            sidebar,
            text="ESTRUCTURA DE DATOS\nProyecto de teoría de grafos",
            font=("Arial", 10),
            text_color=COLOR_SECUNDARIO,
            justify="left"
        ).pack(side="bottom", pady=25, padx=20, anchor="w")

        # ==================================================
        # ÁREA PRINCIPAL
        # ==================================================

        contenido = ctk.CTkFrame(
            self.root,
            fg_color=COLOR_FONDO,
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

        encabezado = ctk.CTkFrame(
            contenido,
            fg_color="transparent"
        )

        encabezado.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(5, 20)
        )

        self.lbl_titulo = ctk.CTkLabel(
            encabezado,
            text="Explorador de recorridos",
            font=("Arial", 27, "bold"),
            text_color=COLOR_TEXTO
        )

        self.lbl_titulo.pack(anchor="w")

        self.lbl_subtitulo = ctk.CTkLabel(
            encabezado,
            text="Visualización de conexiones entre los 7 estados",
            font=("Arial", 13),
            text_color=COLOR_SECUNDARIO
        )

        self.lbl_subtitulo.pack(anchor="w", pady=(5, 0))

        # ESTADÍSTICAS

        estadisticas = ctk.CTkFrame(
            contenido,
            fg_color="transparent"
        )

        estadisticas.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 20)
        )

        for i in range(3):
            estadisticas.grid_columnconfigure(i, weight=1)

        self.lbl_estados = self.crear_tarjeta(
            estadisticas, 0,
            "ESTADOS VISITADOS", "7",
            "Nodos del grafo", COLOR_AZUL
        )

        self.lbl_vuelos = self.crear_tarjeta(
            estadisticas, 1,
            "VUELOS REALIZADOS", "6",
            "Conexiones recorridas", COLOR_VERDE
        )

        self.lbl_costo = self.crear_tarjeta(
            estadisticas, 2,
            "COSTO TOTAL", "$6,000",
            "Costo del recorrido", COLOR_ROJO
        )

        # ==================================================
        # ÁREA DEL GRAFO
        # ==================================================

        area_grafo = ctk.CTkFrame(
            contenido,
            fg_color=COLOR_PANEL,
            corner_radius=15
        )

        area_grafo.grid(
            row=2,
            column=0,
            sticky="nsew",
            pady=(0, 15)
        )

        area_grafo.grid_rowconfigure(1, weight=1)
        area_grafo.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            area_grafo,
            text="  VISUALIZACIÓN DEL GRAFO",
            font=("Arial", 13, "bold"),
            text_color=COLOR_TEXTO,
            anchor="w"
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=15
        )

        self.fig, self.ax = plt.subplots(
            figsize=(8, 5),
            dpi=100
        )

        self.fig.patch.set_facecolor(COLOR_PANEL)
        self.ax.set_facecolor(COLOR_PANEL)

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=area_grafo
        )

        self.canvas.get_tk_widget().grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=5
        )

        # ==================================================
        # PANEL INFERIOR
        # ==================================================

        panel_inferior = ctk.CTkFrame(
            contenido,
            fg_color=COLOR_PANEL,
            corner_radius=15
        )

        panel_inferior.grid(
            row=3,
            column=0,
            sticky="ew"
        )

        panel_inferior.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel_inferior,
            text="SECUENCIA DEL RECORRIDO",
            font=("Arial", 12, "bold"),
            text_color=COLOR_TEXTO
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.lbl_recorrido = ctk.CTkLabel(
            panel_inferior,
            text="",
            font=("Arial", 12, "bold"),
            text_color=COLOR_AZUL,
            wraplength=800,
            justify="left"
        )

        self.lbl_recorrido.pack(
            anchor="w",
            padx=20,
            pady=5
        )

        # ESTADO DE LA SELECCIÓN

        self.lbl_estado = ctk.CTkLabel(
            panel_inferior,
            text="",
            font=("Arial", 11),
            text_color=COLOR_SECUNDARIO,
            wraplength=800,
            justify="left"
        )

        self.lbl_estado.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        # BOTÓN LIMPIAR

        self.btn_limpiar = ctk.CTkButton(
            panel_inferior,
            text="↻  Limpiar recorrido",
            width=170,
            height=35,
            fg_color=COLOR_ROJO,
            hover_color="#BE123C",
            font=("Arial", 11, "bold"),
            command=self.limpiar_ruta
        )

        self.btn_limpiar.pack(
            anchor="e",
            padx=20,
            pady=(0, 15)
        )

    # ======================================================
    # TARJETAS
    # ======================================================

    def crear_tarjeta(
        self,
        padre,
        columna,
        titulo,
        valor,
        descripcion,
        color
    ):

        tarjeta = ctk.CTkFrame(
            padre,
            fg_color=COLOR_TARJETA,
            corner_radius=12,
            height=115
        )

        tarjeta.grid(
            row=0,
            column=columna,
            sticky="ew",
            padx=6
        )

        tarjeta.pack_propagate(False)

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=("Arial", 10, "bold"),
            text_color=COLOR_SECUNDARIO
        ).pack(anchor="w", padx=15, pady=(12, 2))

        lbl_valor = ctk.CTkLabel(
            tarjeta,
            text=valor,
            font=("Arial", 25, "bold"),
            text_color=color
        )

        lbl_valor.pack(anchor="w", padx=15)

        ctk.CTkLabel(
            tarjeta,
            text=descripcion,
            font=("Arial", 10),
            text_color=COLOR_SECUNDARIO
        ).pack(anchor="w", padx=15, pady=(0, 10))

        return lbl_valor

    # ======================================================
    # CAMBIAR RECORRIDO
    # ======================================================

    def mostrar_ruta(self, opcion):

        self.ruta_actual = opcion

        if opcion == 1:

            ruta = self.ruta_1

            self.lbl_titulo.configure(
                text="Recorrido sin repetir estados"
            )

            self.lbl_subtitulo.configure(
                text="Camino hamiltoniano: cada estado se visita una sola vez"
            )

            self.btn_ruta1.configure(fg_color=COLOR_AZUL)
            self.btn_ruta2.configure(fg_color=COLOR_TARJETA)
            self.btn_personalizada.configure(fg_color=COLOR_TARJETA)

            self.lbl_estado.configure(
                text="Recorrido predeterminado."
            )

            color = COLOR_AZUL

        elif opcion == 2:

            ruta = self.ruta_2

            self.lbl_titulo.configure(
                text="Recorrido con repetición"
            )

            self.lbl_subtitulo.configure(
                text="Recorrido cerrado: se regresa al estado de origen"
            )

            self.btn_ruta1.configure(fg_color=COLOR_TARJETA)
            self.btn_ruta2.configure(fg_color=COLOR_VERDE)
            self.btn_personalizada.configure(fg_color=COLOR_TARJETA)

            self.lbl_estado.configure(
                text="Recorrido predeterminado."
            )

            color = COLOR_VERDE

        else:

            ruta = self.ruta_personalizada

            self.lbl_titulo.configure(
                text="Construye tu propio recorrido"
            )

            self.lbl_subtitulo.configure(
                text="Selecciona los estados directamente sobre el grafo"
            )

            self.btn_ruta1.configure(fg_color=COLOR_TARJETA)
            self.btn_ruta2.configure(fg_color=COLOR_TARJETA)
            self.btn_personalizada.configure(fg_color="#8B5CF6")

            self.lbl_estado.configure(
                text="Haz clic en cualquier estado para comenzar."
            )

            color = "#8B5CF6"

        # Actualizar estadísticas

        vuelos = len(ruta) - 1 if ruta else 0
        estados = len(set(ruta)) if ruta else 0
        costo = vuelos * self.costo_vuelo

        self.lbl_estados.configure(text=str(estados))
        self.lbl_vuelos.configure(text=str(vuelos))
        self.lbl_costo.configure(text=f"${costo:,}")

        # Actualizar secuencia

        if ruta:

            self.lbl_recorrido.configure(
                text="   →   ".join(ruta),
                text_color=color
            )

        else:

            self.lbl_recorrido.configure(
                text="Esperando selección de estados...",
                text_color=COLOR_SECUNDARIO
            )

        self.dibujar_grafo(ruta, color)

    # ======================================================
    # DETECTAR CLICS SOBRE LOS NODOS
    # ======================================================

    def al_seleccionar_nodo(self, event):

        # Solo permitir selección en modo personalizado

        if self.ruta_actual != 3:
            return

        # Comprobar que el clic pertenece a los nodos

        if event.artist != self.nodos_artist:
            return

        if len(event.ind) == 0:
            return

        # Identificar el estado seleccionado

        indice = event.ind[0]

        estado = self.nodos[indice]

        # PRIMER ESTADO SELECCIONADO

        if len(self.ruta_personalizada) == 0:

            self.ruta_personalizada.append(estado)

            self.lbl_estado.configure(
                text=f"Inicio establecido: {estado}. Selecciona el siguiente estado."
            )

        else:

            ultimo_estado = self.ruta_personalizada[-1]

            # Evitar seleccionar dos veces el mismo estado consecutivamente

            if estado == ultimo_estado:

                self.lbl_estado.configure(
                    text=f"{estado} ya es el último estado seleccionado."
                )

                return

            # COMPROBAR SI EXISTE CONEXIÓN

            if self.G.has_edge(ultimo_estado, estado):

                self.ruta_personalizada.append(estado)

                self.lbl_estado.configure(
                    text=f"Conexión agregada: {ultimo_estado} → {estado}"
                )

            else:

                self.lbl_estado.configure(
                    text=f"¡Conexión no válida! No existe una conexión entre {ultimo_estado} y {estado}.",
                    text_color=COLOR_ROJO
                )

                return

        # Actualizar interfaz

        self.actualizar_ruta_personalizada()

    # ======================================================
    # ACTUALIZAR RUTA PERSONALIZADA
    # ======================================================

    def actualizar_ruta_personalizada(self):

        ruta = self.ruta_personalizada

        vuelos = len(ruta) - 1
        estados = len(set(ruta))
        costo = vuelos * self.costo_vuelo

        self.lbl_estados.configure(text=str(estados))
        self.lbl_vuelos.configure(text=str(vuelos))
        self.lbl_costo.configure(text=f"${costo:,}")

        self.lbl_recorrido.configure(
            text="   →   ".join(ruta),
            text_color="#A78BFA"
        )

        self.dibujar_grafo(ruta, "#8B5CF6")

    # ======================================================
    # LIMPIAR RECORRIDO
    # ======================================================

    def limpiar_ruta(self):

        if self.ruta_actual != 3:
            return

        self.ruta_personalizada.clear()

        self.lbl_estados.configure(text="0")
        self.lbl_vuelos.configure(text="0")
        self.lbl_costo.configure(text="$0")

        self.lbl_recorrido.configure(
            text="Esperando selección de estados...",
            text_color=COLOR_SECUNDARIO
        )

        self.lbl_estado.configure(
            text="Recorrido eliminado. Haz clic en un estado para comenzar.",
            text_color=COLOR_SECUNDARIO
        )

        self.dibujar_grafo([], "#8B5CF6")

    # ======================================================
    # DIBUJAR GRAFO
    # ======================================================

    def dibujar_grafo(self, ruta, color):

        self.ax.clear()

        self.ax.set_facecolor(COLOR_PANEL)

        # Identificar conexiones recorridas

        aristas_ruta = set()

        for i in range(len(ruta) - 1):

            u = ruta[i]
            v = ruta[i + 1]

            if self.G.has_edge(u, v):

                aristas_ruta.add(frozenset((u, v)))

        aristas_normales = [
            (u, v)
            for u, v in self.G.edges()
            if frozenset((u, v)) not in aristas_ruta
        ]

        aristas_destacadas = [
            (u, v)
            for u, v in self.G.edges()
            if frozenset((u, v)) in aristas_ruta
        ]

        # Conexiones normales

        nx.draw_networkx_edges(
            self.G,
            self.pos,
            edgelist=aristas_normales,
            width=1.5,
            edge_color="#475569",
            style="dashed",
            alpha=0.7,
            ax=self.ax
        )

        # Conexiones seleccionadas

        nx.draw_networkx_edges(
            self.G,
            self.pos,
            edgelist=aristas_destacadas,
            width=3.5,
            edge_color=color,
            ax=self.ax
        )

        # Nodos normales

        self.nodos_artist = nx.draw_networkx_nodes(
            self.G,
            self.pos,
            nodelist=self.nodos,
            node_size=1900,
            node_color="#263B57",
            edgecolors="#64748B",
            linewidths=1.5,
            ax=self.ax
        )

        # Habilitar detección de clics

        self.nodos_artist.set_picker(8)

        # Resaltar nodos visitados

        nodos_visitados = list(dict.fromkeys(ruta))

        if nodos_visitados:

            nx.draw_networkx_nodes(
                self.G,
                self.pos,
                nodelist=nodos_visitados,
                node_size=1900,
                node_color=color,
                edgecolors="white",
                linewidths=2,
                ax=self.ax
            )

        # Etiquetas

        nx.draw_networkx_labels(
            self.G,
            self.pos,
            font_size=9,
            font_weight="bold",
            font_color="white",
            ax=self.ax
        )

        # Costos de las conexiones

        edge_labels = {
            (u, v): "$1000"
            for u, v in self.G.edges()
        }

        nx.draw_networkx_edge_labels(
            self.G,
            self.pos,
            edge_labels=edge_labels,
            font_size=8,
            font_color="#CBD5E1",
            bbox={
                "facecolor": COLOR_PANEL,
                "edgecolor": "none",
                "alpha": 0.85
            },
            ax=self.ax
        )

        # Título

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


# ==========================================================
# EJECUCIÓN
# ==========================================================

if __name__ == "__main__":

    root = ctk.CTk()

    app = AplicacionGrafos(root)

    root.mainloop()
