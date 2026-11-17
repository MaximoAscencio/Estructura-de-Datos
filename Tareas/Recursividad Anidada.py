def sanitizar_ruta(ruta: str) -> str:
    # Caso base: si la ruta ya no contiene la secuencia peligrosa, es segura
    if "../" not in ruta:
        return ruta
    
    return sanitizar_ruta(sanitizar_ruta(ruta.replace("../", "", 1)))


# --- Ejemplo de uso en la vida real ---
# Un usuario maligno envía esta ruta intentando acceder a passwords.txt:
ruta_maliciosa = "sistema/archivos/....//config/passwords.txt"

# Proceso de limpieza
ruta_limpia = sanitizar_ruta(ruta_maliciosa)

print(f"Ruta original: {ruta_maliciosa}")
print(f"Ruta limpia:   {ruta_limpia}")