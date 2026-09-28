# Explicación del Código

El código funciona por medio de métodos que dividen las actividades que se pueden realizar. Contamos con un total de 7 métodos dentro de la clase:

* **`ejecutar_sistema`**: Realiza un menú interactivo en el cual podemos ir seleccionando las actividades que queremos realizar de forma continua.
* **`__init__`**: Inicializa la estructura del programa creando la matriz de 12 meses por 3 departamentos con valores iniciales en `0.0`.
* **`insertar_venta`**: Solicita el mes, el departamento y el monto; se encarga de ubicar la casilla correspondiente en la matriz y guardar o actualizar el valor introducido.
* **`buscar_venta`**: Recorre la matriz completa buscando un monto en específico y muestra en pantalla la coincidencia junto con el mes y departamento donde se encuentra.
* **`eliminar_venta`**: Localiza la casilla seleccionada mediante el mes y el departamento y restablece el monto de esa venta a `0.0`.
* **`mostrar_matriz`**: Imprime en consola la tabla completa formateada con todos los meses y departamentos para visualizar el estado actual de las ventas.
* **`_obtener_indice_mes`**: Método auxiliar que convierte el mes ingresado (ya sea el número del 1 al 12 o el nombre del mes) en la posición numérica exacta de la matriz (índice 0 a 11).
* **`_obtener_indice_dept`**: Método auxiliar que valida el nombre del departamento ("Ropa", "Deportes", "Juguetería") y lo transforma en su índice numérico dentro del arreglo (0 a 2).