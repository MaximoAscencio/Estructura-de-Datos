import random
import time

# ==========================================
# CONFIGURACIÓN (Puedes modificar estas variables)
# ==========================================
num_alumnos = 10000
num_materias = 6

# 1. Crear listas de nombres automáticamente
alumnos = [f"Alumno {i}" for i in range(1, num_alumnos + 1)]
materias = [f"Materia {i}" for i in range(1, num_materias + 1)]

# 2. Crear la matriz de calificaciones (Filas = Alumnos, Columnas = Materias)
matriz_calificaciones = [
    [random.randint(1, 10) for _ in range(num_materias)] 
    for _ in range(num_alumnos)
]

# --- VERIFICACIÓN Y MUESTRA DE DATOS CON MEDICIÓN DE TIEMPO ---

print("Estructura de la matriz creada con éxito.")
print(f"Filas (Alumnos): {len(matriz_calificaciones)}")
print(f"Columnas (Materias): {len(matriz_calificaciones[0])}\n")

# Formato del encabezado con las materias como columnas
encabezado = f"{'Alumno':<12} | " + " | ".join(f"{m:<12}" for m in materias)

# ⏱️ INICIO DE MEDICIÓN DE TIEMPO DE LA TABLA
inicio_tiempo = time.perf_counter()

print(f"--- Tabla de calificaciones ({num_alumnos} Alumnos) ---")
print(encabezado)
print("-" * len(encabezado))

# Imprimir las calificaciones de los alumnos
for i in range(num_alumnos):
    nombre_alumno = alumnos[i]
    calificaciones = matriz_calificaciones[i]
    
    # Formatear la fila con las calificaciones del alumno
    cal_str = " | ".join(f"{cal:^12}" for cal in calificaciones)
    print(f"{nombre_alumno:<12} | {cal_str}")

# ⏱️ FIN DE MEDICIÓN DE TIEMPO DE LA TABLA
fin_tiempo = time.perf_counter()
tiempo_ejecucion = fin_tiempo - inicio_tiempo

print("\nMatriz de calificaciones generada e impresa correctamente.")
print(f"⏱️ Tiempo de ejecución de la tabla: {tiempo_ejecucion:.4f} segundos\n")

# --- SECCIÓN INTERACTIVA DE CONSULTA ---

while True:
    print("\n" + "=" * 45)
    print("      CONSULTA DE CALIFICACIONES DE ALUMNOS")
    print("=" * 45)
    
    # Solicitar el número de alumno
    entrada_alumno = input(f"Ingresa el número de alumno (1 al {num_alumnos}) o escribe 'salir' para terminar: ")
    
    # Opción para finalizar el programa
    if entrada_alumno.lower() == 'salir':
        print("\n¡Gracias por usar el sistema! Hasta luego.")
        break

    # Validar que sea un número entero
    if not entrada_alumno.isdigit():
        print("❌ Error: Debes ingresar un número entero válido.")
        continue

    num_alumno = int(entrada_alumno)

    # Validar rango del número de alumno
    if num_alumno < 1 or num_alumno > num_alumnos:
        print(f"❌ Error: El número de alumno debe estar entre 1 y {num_alumnos}.")
        continue

    # Convertir a índice de matriz
    idx_alumno = num_alumno - 1

    # Menú de opciones de consulta
    print(f"\n¿Qué deseas consultar de {alumnos[idx_alumno]}?")
    print("1. Ver todas las materias")
    print("2. Ver una materia en específico")
    
    opcion = input("Selecciona una opción (1 o 2): ")

    if opcion == "1":
        # Mostrar todas las materias del alumno
        print(f"\n📋 Calificaciones de {alumnos[idx_alumno]}:")
        for idx_materia, nombre_materia in enumerate(materias):
            calificacion = matriz_calificaciones[idx_alumno][idx_materia]
            print(f"  • {nombre_materia:<12}: {calificacion}")

    elif opcion == "2":
        # Desplegar menú de materias para elegir una
        print("\nMaterias disponibles:")
        for i, nombre_materia in enumerate(materias, 1):
            print(f"  {i}. {nombre_materia}")
        
        entrada_materia = input(f"Selecciona el número de la materia (1 al {num_materias}): ")

        if entrada_materia.isdigit():
            num_materia = int(entrada_materia)
            if 1 <= num_materia <= len(materias):
                idx_materia = num_materia - 1
                nombre_materia = materias[idx_materia]
                
                calificacion = matriz_calificaciones[idx_alumno][idx_materia]
                print(f"\n📌 En {nombre_materia}, {alumnos[idx_alumno]} tiene una calificación de: {calificacion}")
            else:
                print("❌ Opción de materia no válida.")
        else:
            print("❌ Entrada inválida. Debes ingresar un número de la lista.")
            
    else:
        print("❌ Opción no válida. Intenta de nuevo.")