def mostrar_vector(datos):
    for x in datos:
        print(x)

def media(datos):
    suma = sum(datos)
    return (print ("Media=", suma / len(datos)))

pares = [2, 4, 6, 8, 10]
impares = [1, 3, 5, 7, 9]

mostrar_vector(pares)
media(pares)

mostrar_vector(impares)
media(impares)