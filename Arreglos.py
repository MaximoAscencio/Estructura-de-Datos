DEPARTAMENTOS = ["Ropa", "Deportes", "Juguetería"]
MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

class ControlVentas:
    def __init__(self):
    
        self.ventas = [[0.0 for _ in range(len(DEPARTAMENTOS))] for _ in range(len(MESES))]

    def insertar_venta(self, mes, departamento, monto):
        """1. Método para insertar o actualizar elementos en el arreglo."""
        i_mes = self._obtener_indice_mes(mes)
        i_dept = self._obtener_indice_dept(departamento)

        if i_mes is not None and i_dept is not None:
            self.ventas[i_mes][i_dept] = float(monto)
            print(f"\n[✓] Venta de ${monto:.2f} registrada en {DEPARTAMENTOS[i_dept]} ({MESES[i_mes]}).")
        else:
            print("\n[X] Error: Mes o departamento no válido.")

    def buscar_venta(self, monto):
        """2. Método para buscar un elemento por su monto."""
        coincidencias = []
        for i, fila in enumerate(self.ventas):
            for j, valor in enumerate(fila):
                if valor == monto:
                    coincidencias.append((MESES[i], DEPARTAMENTOS[j]))

        if coincidencias:
            print(f"\n[✓] Se encontró el monto de ${monto:.2f} en:")
            for mes, dept in coincidencias:
                print(f"   - {mes}, Departamento de {dept}")
        else:
            print(f"\n[X] No se encontró ninguna venta registrada con el monto ${monto:.2f}.")

    def eliminar_venta(self, mes, departamento):
        """3. Método para eliminar una venta en particular de un departamento."""
        i_mes = self._obtener_indice_mes(mes)
        i_dept = self._obtener_indice_dept(departamento)

        if i_mes is not None and i_dept is not None:
            monto_previo = self.ventas[i_mes][i_dept]
            self.ventas[i_mes][i_dept] = 0.0
            print(f"\n[✓] Se eliminó la venta de ${monto_previo:.2f} en {DEPARTAMENTOS[i_dept]} ({MESES[i_mes]}).")
        else:
            print("\n[X] Error: Mes o departamento no válido.")

    def mostrar_matriz(self):
        """Muestra el arreglo bidimensional formateado en pantalla."""
        print(f"\n{'Mes':<12} | {'Ropa':<10} | {'Deportes':<10} | {'Juguetería':<10}")
        print("-" * 50)
        for i, mes in enumerate(MESES):
            r, d, j = self.ventas[i]
            print(f"{mes:<12} | ${r:<9.2f} | ${d:<9.2f} | ${j:<9.2f}")

    def _obtener_indice_mes(self, mes):
        if isinstance(mes, str) and mes.isdigit():
            mes = int(mes)
        if isinstance(mes, int) and 1 <= mes <= 12:
            return mes - 1
        if isinstance(mes, str) and mes.capitalize() in MESES:
            return MESES.index(mes.capitalize())
        return None

    def _obtener_indice_dept(self, dept):
        if isinstance(dept, str) and dept.capitalize() in DEPARTAMENTOS:
            return DEPARTAMENTOS.index(dept.capitalize())
        return None


# Bucle interactivo para mantener el menú y el método de inserción siempre disponibles
def ejecutar_sistema():
    tienda = ControlVentas()

    while True:
        print("\n" + "="*40)
        print("  SISTEMA DE CONTROL DE VENTAS")
        print("="*40)
        print("1. Insertar venta")
        print("2. Buscar venta por monto")
        print("3. Eliminar venta")
        print("4. Mostrar matriz de ventas")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()

        if opcion == "1":
            mes = input("Mes (1-12 o Nombre): ")
            dept = input("Departamento (Ropa, Deportes, Juguetería): ")
            try:
                monto = float(input("Monto de la venta: $"))
                tienda.insertar_venta(mes, dept, monto)
            except ValueError:
                print("\n[X] Error: Debes ingresar un número válido para el monto.")

        elif opcion == "2":
            try:
                monto = float(input("Monto a buscar: $"))
                tienda.buscar_venta(monto)
            except ValueError:
                print("\n[X] Error: Ingresa un valor numérico válido.")

        elif opcion == "3":
            mes = input("Mes (1-12 o Nombre): ")
            dept = input("Departamento (Ropa, Deportes, Juguetería): ")
            tienda.eliminar_venta(mes, dept)

        elif opcion == "4":
            tienda.mostrar_matriz()

        elif opcion == "5":
            print("\n¡Programa finalizado!")
            break
        else:
            print("\n[X] Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    ejecutar_sistema()