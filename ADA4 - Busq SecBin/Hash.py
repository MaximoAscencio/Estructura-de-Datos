"""
Búsqueda por Hash (tabla hash).

Ejercicio: una agenda de contactos. Cada contacto tiene un nombre y un
teléfono. Al escribir un nombre, el programa calcula directamente en qué
posición de la tabla está guardado, sin revisar uno por uno.

Función hash: suma de los códigos ASCII de las letras del nombre, módulo el
tamaño de la tabla. Si dos nombres caen en la misma posición (colisión), se
guardan en una lista dentro de esa posición (encadenamiento).
"""

from interfaz import VentanaBusqueda

TAMANIO = 7


def funcion_hash(clave, tamanio=TAMANIO):
    """Suma de los valores ASCII de la clave (en minúsculas) módulo el tamaño."""
    return sum(ord(c) for c in clave.lower()) % tamanio


class TablaHash:
    def __init__(self, tamanio=TAMANIO):
        self.tamanio = tamanio
        self.tabla = [[] for _ in range(tamanio)]

    def insertar(self, clave, valor):
        posicion = funcion_hash(clave, self.tamanio)
        for par in self.tabla[posicion]:
            if par[0].lower() == clave.lower():
                par[1] = valor          # si la clave ya existe, se actualiza
                return posicion
        self.tabla[posicion].append([clave, valor])
        return posicion

    def buscar(self, clave):
        """Regresa (valor o None, posicion, pasos)."""
        posicion = funcion_hash(clave, self.tamanio)
        pasos = [f"Hash('{clave}') = {self._suma(clave)} % {self.tamanio} = {posicion}",
                 f"Se revisa solo la posición {posicion} de la tabla:"]
        cubeta = self.tabla[posicion]
        if not cubeta:
            pasos.append("   La posición está vacía -> el contacto no existe.")
            return None, posicion, pasos
        for par in cubeta:
            if par[0].lower() == clave.lower():
                pasos.append(f"   '{par[0]}' == '{clave}'  -> ¡encontrado!")
                return par[1], posicion, pasos
            pasos.append(f"   '{par[0]}' != '{clave}'  -> colisión, se sigue en la cadena")
        pasos.append("   Se acabó la cadena -> el contacto no existe.")
        return None, posicion, pasos

    @staticmethod
    def _suma(clave):
        return sum(ord(c) for c in clave.lower())

    def mostrar(self):
        lineas = ["Contenido de la tabla hash:"]
        for i, cubeta in enumerate(self.tabla):
            contenido = ", ".join(f"{k}:{v}" for k, v in cubeta) if cubeta else "(vacía)"
            lineas.append(f"   [{i}] -> {contenido}")
        return lineas


def buscar_gui(texto_datos, texto_valor):
    """Valida lo que escribió el usuario, arma la tabla y busca."""
    tabla = TablaHash()
    for elemento in texto_datos.split(","):
        elemento = elemento.strip()
        if not elemento:
            continue
        if ":" not in elemento:
            raise ValueError(f"'{elemento}' no tiene el formato nombre:teléfono.")
        nombre, telefono = [x.strip() for x in elemento.split(":", 1)]
        if not nombre or not telefono:
            raise ValueError(f"'{elemento}' no tiene el formato nombre:teléfono.")
        tabla.insertar(nombre, telefono)
    if all(not cubeta for cubeta in tabla.tabla):
        raise ValueError("Escribe al menos un contacto con el formato nombre:teléfono.")
    nombre_buscado = texto_valor.strip()
    if not nombre_buscado:
        raise ValueError("Escribe el nombre que quieres buscar.")

    telefono, posicion, pasos = tabla.buscar(nombre_buscado)
    if telefono is None:
        resultado = f"'{nombre_buscado}' NO está en la agenda."
    else:
        resultado = f"Teléfono de {nombre_buscado}: {telefono} (posición {posicion} de la tabla)."
    return resultado, tabla.mostrar() + [""] + pasos


METODO = {
    "descripcion": ("Agenda de contactos (nombre:teléfono). La tabla hash calcula la posición "
                    "del nombre con una función y va directo a ella, sin recorrer toda la lista."),
    "etiqueta_datos": "Contactos (nombre:teléfono, separados por comas):",
    "etiqueta_buscar": "Nombre a buscar:",
    "ejemplo_datos": "Ana:9991234567, Luis:9997654321, Pedro:9991112233, María:9994445566, "
                     "Sofía:9998889900, Carlos:9992223344",
    "ejemplo_buscar": "María",
    "buscar": buscar_gui,
}

if __name__ == "__main__":
    VentanaBusqueda({"Hash": METODO}, "Búsqueda Hash").iniciar()
