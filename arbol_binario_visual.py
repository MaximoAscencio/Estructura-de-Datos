import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Árboles binarios", page_icon="🌳", layout="wide")
st.title("🌳 Constructor visual de árboles binarios")
st.caption("Crea nodos, conecta ramas, mueve subárboles y observa los recorridos.")

# Cada nodo tiene un identificador único y referencias a sus hijos.
def nuevo_nodo(arbol, etiqueta):
    nid = arbol["siguiente_id"]
    arbol["siguiente_id"] += 1
    arbol["nodos"][nid] = {"valor": str(etiqueta), "izq": None, "der": None}
    return nid

def inicializar():
    return {"nodos": {}, "raiz": None, "siguiente_id": 1}

if "arbol" not in st.session_state:
    st.session_state.arbol = inicializar()

arbol = st.session_state.arbol

def recorrer(nid, tipo, salida):
    if nid is None:
        return
    n = arbol["nodos"][nid]
    if tipo == "Preorden":
        salida.append(n["valor"])
    recorrer(n["izq"], tipo, salida)
    if tipo == "Inorden":
        salida.append(n["valor"])
    recorrer(n["der"], tipo, salida)
    if tipo == "Postorden":
        salida.append(n["valor"])

def obtener_recorrido(tipo):
    salida = []
    recorrer(arbol["raiz"], tipo, salida)
    return salida

def subarbol_ids(nid):
    if nid is None or nid not in arbol["nodos"]:
        return set()
    n = arbol["nodos"][nid]
    return {nid} | subarbol_ids(n["izq"]) | subarbol_ids(n["der"])

def padre_de(nid):
    for pid, n in arbol["nodos"].items():
        if n["izq"] == nid or n["der"] == nid:
            return pid
    return None

def eliminar_subarbol(nid):
    if nid == arbol["raiz"]:
        arbol["raiz"] = None
    else:
        pid = padre_de(nid)
        if pid is not None:
            if arbol["nodos"][pid]["izq"] == nid:
                arbol["nodos"][pid]["izq"] = None
            else:
                arbol["nodos"][pid]["der"] = None
    for x in subarbol_ids(nid):
        arbol["nodos"].pop(x, None)

def posiciones():
    """Asigna x mediante recorrido inorden; y depende del nivel."""
    coords = {}
    contador = [0]
    def ubicar(nid, nivel):
        if nid is None:
            return
        n = arbol["nodos"][nid]
        ubicar(n["izq"], nivel + 1)
        coords[nid] = (contador[0], -nivel)
        contador[0] += 1
        ubicar(n["der"], nivel + 1)
    ubicar(arbol["raiz"], 0)
    return coords

def dibujar():
    if arbol["raiz"] is None:
        st.info("El árbol está vacío. Crea una raíz para comenzar.")
        return
    coords = posiciones()
    fig, ax = plt.subplots(figsize=(max(8, len(coords) * 1.15), 5.5))
    # Primero las conexiones para que queden detrás de los nodos.
    for nid, n in arbol["nodos"].items():
        x, y = coords[nid]
        for lado in ("izq", "der"):
            hijo = n[lado]
            if hijo is not None:
                hx, hy = coords[hijo]
                ax.plot([x, hx], [y, hy], linewidth=2, color="#64748b", zorder=1)
                mx, my = (x + hx) / 2, (y + hy) / 2
                ax.text(mx, my + 0.12, "I" if lado == "izq" else "D",
                        ha="center", va="center", fontsize=9, color="#475569")
    for nid, n in arbol["nodos"].items():
        x, y = coords[nid]
        ax.scatter(x, y, s=1450, color="#dbeafe", edgecolors="#2563eb",
                   linewidths=2.2, zorder=2)
        ax.text(x, y, n["valor"], ha="center", va="center",
                fontsize=11, weight="bold", color="#0f172a", zorder=3)
    ax.set_title("Representación del árbol", fontsize=14, pad=18)
    ax.axis("off")
    ax.margins(x=0.12, y=0.35)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

def opciones_nodos():
    return {f'{n["valor"]}  (ID {nid})': nid for nid, n in arbol["nodos"].items()}

def crear_arbol_cantidad(cantidad, valores):
    nuevo = inicializar()
    ids = []
    for i in range(cantidad):
        valor = valores[i].strip() if i < len(valores) and valores[i].strip() else str(i + 1)
        ids.append(nuevo_nodo(nuevo, valor))
    nuevo["raiz"] = ids[0]
    # Construcción por niveles: árbol binario completo.
    for i, nid in enumerate(ids):
        izq, der = 2 * i + 1, 2 * i + 2
        if izq < cantidad:
            nuevo["nodos"][nid]["izq"] = ids[izq]
        if der < cantidad:
            nuevo["nodos"][nid]["der"] = ids[der]
    return nuevo

# Panel principal
col_arbol, col_panel = st.columns([2.2, 1], gap="large")
with col_arbol:
    st.subheader("Visualización")
    dibujar()
    st.subheader("Recorridos")
    c1, c2, c3 = st.columns(3)
    for col, tipo in zip((c1, c2, c3), ("Inorden", "Preorden", "Postorden")):
        with col:
            st.markdown(f"**{tipo}**")
            if arbol["raiz"] is None:
                st.write("—")
            else:
                st.code(" → ".join(obtener_recorrido(tipo)))

with col_panel:
    st.subheader("1. Crear árbol")
    cantidad = st.number_input("Cantidad de nodos", min_value=1, max_value=31, value=7, step=1)
    valores_txt = st.text_input("Valores (separados por comas)", placeholder="A, B, C, D, E, F, G")
    st.caption("Si dejas valores vacíos, se usarán 1, 2, 3…")
    if st.button("Generar árbol por niveles", use_container_width=True, type="primary"):
        valores = valores_txt.split(",") if valores_txt.strip() else []
        st.session_state.arbol = crear_arbol_cantidad(int(cantidad), valores)
        st.rerun()

    st.divider()
    st.subheader("2. Agregar nodo")
    if arbol["raiz"] is None:
        if st.button("Crear raíz", use_container_width=True):
            arbol["raiz"] = nuevo_nodo(arbol, "Raíz")
            st.rerun()
    else:
        opciones = opciones_nodos()
        padre_label = st.selectbox("Nodo padre", list(opciones), key="add_parent")
        lado = st.radio("Posición", ["Izquierda", "Derecha"], horizontal=True, key="add_side")
        valor = st.text_input("Valor del nuevo nodo", key="add_value")
        if st.button("Agregar nodo", use_container_width=True):
            pid = opciones[padre_label]
            campo = "izq" if lado == "Izquierda" else "der"
            if arbol["nodos"][pid][campo] is not None:
                st.error("Ese espacio ya está ocupado. Elimina o mueve primero el nodo existente.")
            elif not valor.strip():
                st.error("Escribe un valor para el nodo.")
            else:
                arbol["nodos"][pid][campo] = nuevo_nodo(arbol, valor.strip())
                st.rerun()

    st.divider()
    st.subheader("3. Mover nodo")
    if arbol["nodos"]:
        opciones = opciones_nodos()
        mover_label = st.selectbox("Subárbol que moverás", list(opciones), key="move_node")
        destinos = {k: v for k, v in opciones.items() if v != opciones[mover_label]}
        if destinos:
            destino_label = st.selectbox("Nuevo nodo padre", list(destinos), key="move_parent")
            nuevo_lado = st.radio("Nuevo lado", ["Izquierda", "Derecha"], horizontal=True, key="move_side")
            if st.button("Mover subárbol", use_container_width=True):
                nid, pid = opciones[mover_label], destinos[destino_label]
                campo = "izq" if nuevo_lado == "Izquierda" else "der"
                if pid in subarbol_ids(nid):
                    st.error("Movimiento inválido: no puedes colocar un nodo dentro de su propio subárbol.")
                elif arbol["nodos"][pid][campo] is not None and arbol["nodos"][pid][campo] != nid:
                    st.error("La posición de destino ya está ocupada.")
                elif nid == arbol["raiz"]:
                    st.error("No puedes mover la raíz como hijo. Elige otro nodo.")
                else:
                    viejo_padre = padre_de(nid)
                    if viejo_padre is not None:
                        if arbol["nodos"][viejo_padre]["izq"] == nid:
                            arbol["nodos"][viejo_padre]["izq"] = None
                        else:
                            arbol["nodos"][viejo_padre]["der"] = None
                    arbol["nodos"][pid][campo] = nid
                    st.rerun()
        else:
            st.caption("Se necesita otro nodo para mover un subárbol.")

    st.divider()
    st.subheader("4. Eliminar nodo")
    if arbol["nodos"]:
        opciones = opciones_nodos()
        borrar_label = st.selectbox("Nodo que deseas eliminar", list(opciones), key="delete_node")
        st.caption("Se eliminará también todo el subárbol que dependa de ese nodo.")
        if st.button("Eliminar nodo y descendientes", use_container_width=True):
            eliminar_subarbol(opciones[borrar_label])
            st.rerun()

    st.divider()
    if st.button("Vaciar árbol", use_container_width=True):
        st.session_state.arbol = inicializar()
        st.rerun()

st.caption("Nota: el árbol se construye por niveles al generar una cantidad inicial. Después puedes editar libremente sus conexiones.")