class Nodo:
    def __init__(self, dato):
        """
        Inicializa un nodo con un dato y referencias nulas a sus hijos.
        Equivalente a la clase Nodo de la presentación.
        """
        self.dato = dato
        self.izquierdo = None
        self.derecho = None

class Arbol:
    def __init__(self):
        """
        Inicializa el árbol con una raíz vacía (None).
        """
        self.raiz = None

    def es_vacio(self):
        return self.raiz is None

    def insertar(self, valor):
        """
        Inserta un nuevo valor en el Árbol Binario de Búsqueda.
        """
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(valor, self.raiz)

    def _insertar_recursivo(self, valor, nodo_actual):
        if valor < nodo_actual.dato:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = Nodo(valor)
            else:
                self._insertar_recursivo(valor, nodo_actual.izquierdo)
        elif valor > nodo_actual.dato:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = Nodo(valor)
            else:
                self._insertar_recursivo(valor, nodo_actual.derecho)

    def busqueda(self, x, nodo_actual=None):
        """
        Busca un valor x de manera recursiva en el árbol.
        """
        if nodo_actual is None:
            # Si es la primera llamada y no se pasó nodo, empezamos en la raíz
            nodo_actual = self.raiz 
            
            # Si el árbol está completamente vacío
            if nodo_actual is None:
                return False

        if x == nodo_actual.dato:
            return True
        elif x < nodo_actual.dato and nodo_actual.izquierdo is not None:
            return self.busqueda(x, nodo_actual.izquierdo)
        elif x > nodo_actual.dato and nodo_actual.derecho is not None:
            return self.busqueda(x, nodo_actual.derecho)
        
        return False

    def in_orden(self, nodo_actual):
        """
        Recorrido InOrden: Izquierdo, Raíz, Derecho.
        Imprime los valores en orden ascendente.
        """
        if nodo_actual is not None:
            self.in_orden(nodo_actual.izquierdo)
            print(nodo_actual.dato, end=" - ")
            self.in_orden(nodo_actual.derecho)

    def pre_orden(self, nodo_actual):
        """
        Recorrido PreOrden: Raíz, Izquierdo, Derecho.
        """
        if nodo_actual is not None:
            print(nodo_actual.dato, end=" - ")
            self.pre_orden(nodo_actual.izquierdo)
            self.pre_orden(nodo_actual.derecho)

    def post_orden(self, nodo_actual):
        """
        Recorrido PostOrden: Izquierdo, Derecho, Raíz.
        """
        if nodo_actual is not None:
            self.post_orden(nodo_actual.izquierdo)
            self.post_orden(nodo_actual.derecho)
            print(nodo_actual.dato, end=" - ")

# --- Ejemplo de uso ---
if __name__ == "__main__":
    arbol = Arbol()
    
    # Insertar datos basados en un ejemplo de la presentación (8, 3, 20, 1, 5, 10, 7, 4)
    valores = [8, 3, 20, 1, 5, 10, 7, 4]
    for v in valores:
        arbol.insertar(v)
        
    print("Recorrido InOrden:")
    arbol.in_orden(arbol.raiz)
    print("\n")
    
    print("Recorrido PreOrden:")
    arbol.pre_orden(arbol.raiz)
    print("\n")
    
    print("Recorrido PostOrden:")
    arbol.post_orden(arbol.raiz)
    print("\n")
    
    # Búsqueda
    valor_a_buscar = 7
    if arbol.busqueda(valor_a_buscar):
        print(f"El elemento {valor_a_buscar} ha sido encontrado en el árbol.")
    else:
        print("Elemento no encontrado.")