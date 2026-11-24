"""
Búsqueda binaria.

Ejercicio: una papelería tiene su catálogo con los códigos de producto
ordenados de menor a mayor. Se captura un código y el programa dice si el
producto existe y en qué posición del catálogo está.

El método necesita que la lista esté ORDENADA. Compara el valor buscado con el
elemento de en medio: si es igual, termina; si es menor, descarta la mitad
derecha; si es mayor, descarta la mitad izquierda. Repite con la mitad que queda.
"""

from interfaz import VentanaBusqueda


def busqueda_binaria(lista, objetivo):
    """Regresa (posicion, pasos). La lista debe estar ordenada. -1 si no existe."""
    pasos = []
    izquierda, derecha = 0, len(lista) - 1
    vuelta = 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        pasos.append(f"Vuelta {vuelta}: izquierda={izquierda}, derecha={derecha}, "
                     f"medio={medio} -> lista[{medio}] = {lista[medio]}")
        if lista[medio] == objetivo:
            pasos.append(f"   {lista[medio]} == {objetivo}  -> ¡encontrado!")
            return medio, pasos
        if lista[medio] < objetivo:
            pasos.append(f"   {lista[medio]} < {objetivo}  -> se descarta la mitad izquierda")
            izquierda = medio + 1
        else:
            pasos.append(f"   {lista[medio]} > {objetivo}  -> se descarta la mitad derecha")
            derecha = medio - 1
        vuelta += 1
    pasos.append("Ya no quedan elementos por revisar (izquierda > derecha).")
    return -1, pasos


def buscar_gui(texto_datos, texto_valor):
    """Valida lo que escribió el usuario y ejecuta la búsqueda."""
    try:
        lista = [int(d) for d in texto_datos.split(",") if d.strip()]
    except ValueError:
        raise ValueError("Los códigos deben ser números enteros separados por comas.")
    if not lista:
        raise ValueError("Escribe al menos un código en el catálogo.")
    try:
        objetivo = int(texto_valor.strip())
    except ValueError:
        raise ValueError("El código a buscar debe ser un número entero.")

    encabezado = []
    if lista != sorted(lista):
        lista = sorted(lista)
        encabezado = ["La búsqueda binaria necesita la lista ordenada, así que primero se ordenó:",
                      str(lista), ""]

    posicion, pasos = busqueda_binaria(lista, objetivo)
    vueltas = sum(1 for p in pasos if p.startswith("Vuelta"))
    if posicion == -1:
        resultado = f"El código {objetivo} NO está en el catálogo ({vueltas} vueltas)."
    else:
        resultado = f"El código {objetivo} se encontró en la posición {posicion} ({vueltas} vueltas)."
    return resultado, encabezado + pasos


METODO = {
    "descripcion": ("Catálogo de una papelería con códigos ordenados de menor a mayor. "
                    "La búsqueda binaria parte la lista a la mitad en cada vuelta."),
    "etiqueta_datos": "Códigos del catálogo (enteros separados por comas):",
    "etiqueta_buscar": "Código a buscar:",
    "ejemplo_datos": "101, 105, 112, 120, 134, 150, 167, 180, 195, 210",
    "ejemplo_buscar": "167",
    "buscar": buscar_gui,
}

if __name__ == "__main__":
    VentanaBusqueda({"Binaria": METODO}, "Búsqueda Binaria").iniciar()
