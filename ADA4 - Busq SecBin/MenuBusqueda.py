"""
Menú general de búsqueda: una sola ventana desde la que se elige entre los
tres métodos (Secuencial, Binaria y Hash).

Para ejecutarlo:   python MenuBusqueda.py
"""

from interfaz import VentanaBusqueda
import Secuencial
import Binaria
import Hash

METODOS = {
    "1. Secuencial": Secuencial.METODO,
    "2. Binaria": Binaria.METODO,
    "3. Hash": Hash.METODO,
}

if __name__ == "__main__":
    VentanaBusqueda(METODOS, "Menú de métodos de búsqueda").iniciar()
