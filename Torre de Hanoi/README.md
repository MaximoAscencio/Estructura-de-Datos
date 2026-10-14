# Codigo Torre de Hanoi 

## Métodos 

Dentro del codigo, la función que utilizamos con la recursividad es la función llamada 
torre hanoi.
Tambien contamos con otras funciones como:

- print(): Muestra los movimientos

- input(): Solicita el número de discos

- int(): Convierte la entrada a entero

- time.perf_counter(): Mide el tiempo de ejecución

## Tiempos de solución

5 Discos: Para los 5 discos se realizan un total de 31 movimientos que se realizan en 0.002 segundos o 2.144 ms 

10 Discos: Para la cantidad de 10 discos se realizan en total de 1,023 movimientos que se realizan en 0.059 segundos o 59.341 ms

30 Discos: Para 30 discos la cantidad de movimientos se eleva exponencialmente dando un total de 1,073,741,823 movimientos, aquí realicé
calculos estimando el tiempo de cada movimiento (6.451612903x10^-5) y multiplicando por los movimientos dando un total de 69273.666 segundos o 19.2427 horas 

60 Discos: Para 60 discos la cantidad de movimientos se eleva exponencialmente dando un total de 18,446,744,073,709,551,615 movimientos, aquí realicé calculos estimando el tiempo de cada movimiento (6.451612903x10^-5) y multiplicando por los movimientos dando un total de 
1.190112521x10^15 segundos o aproximadamente 370,280.9267 siglos

## Conclusión

Cuando aumentamos la cantidad de discos, el tiempo de ejecución igual aumenta de manera exponencial, llegando a un punto 
en el que ligeros cambios como agregar un solo disco más, puede provocar agregar miles de movimientos extra.