"""
Menú general de ordenamiento externo: una sola ventana desde la que se elige
entre los tres métodos (Intercalación, Mezcla Directa y Mezcla Equilibrada).

Para ejecutarlo:   python MenuOrdenamientoExt.py
"""

from interfaz import VentanaOrdenamiento
import Intercalacion
import MezclaDirecta
import MezclaEquilibrada

METODOS = {
    "1. Intercalación": Intercalacion.METODO,
    "2. Mezcla Directa": MezclaDirecta.METODO,
    "3. Mezcla Equilibrada": MezclaEquilibrada.METODO,
}

if __name__ == "__main__":
    VentanaOrdenamiento(METODOS, "Menú de ordenamiento externo").iniciar()
