"""
Búsqueda secuencial (lineal).

Ejercicio: la lista de asistencia de un grupo. Los nombres están en el orden en
que los alumnos fueron llegando (sin ordenar) y el profesor quiere saber si un
alumno está en la lista y en qué posición.

El método revisa los elementos uno por uno, de izquierda a derecha, hasta
encontrar el buscado o llegar al final de la lista.
"""

from interfaz import VentanaBusqueda


def busqueda_secuencial(lista, objetivo):
    """Regresa (posicion, pasos). La posición es -1 si no se encontró."""
    pasos = []
    for i, elemento in enumerate(lista):
        if elemento.lower() == objetivo.lower():
            pasos.append(f"Posición {i}: '{elemento}' == '{objetivo}'  -> ¡encontrado!")
            return i, pasos
        pasos.append(f"Posición {i}: '{elemento}' != '{objetivo}'  -> se sigue con el siguiente")
    pasos.append("Se llegó al final de la lista sin encontrar el elemento.")
    return -1, pasos


def buscar_gui(texto_datos, texto_valor):
    """Valida lo que escribió el usuario y ejecuta la búsqueda."""
    lista = [d.strip() for d in texto_datos.split(",") if d.strip()]
    objetivo = texto_valor.strip()
    if not lista:
        raise ValueError("Escribe al menos un nombre en la lista, separados por comas.")
    if not objetivo:
        raise ValueError("Escribe el nombre que quieres buscar.")

    posicion, pasos = busqueda_secuencial(lista, objetivo)
    if posicion == -1:
        resultado = f"'{objetivo}' NO está en la lista ({len(lista)} comparaciones)."
    else:
        resultado = (f"'{objetivo}' se encontró en la posición {posicion} "
                     f"(lugar {posicion + 1}) con {posicion + 1} comparaciones.")
    return resultado, pasos


METODO = {
    "descripcion": ("Lista de asistencia: los nombres están en el orden de llegada (sin ordenar). "
                    "La búsqueda secuencial revisa uno por uno hasta encontrar al alumno."),
    "etiqueta_datos": "Nombres de la lista (separados por comas):",
    "etiqueta_buscar": "Nombre a buscar:",
    "ejemplo_datos": "Luis, Ana, Pedro, María, Sofía, Carlos, Elena",
    "ejemplo_buscar": "Sofía",
    "buscar": buscar_gui,
}

if __name__ == "__main__":
    VentanaBusqueda({"Secuencial": METODO}, "Búsqueda Secuencial").iniciar()
