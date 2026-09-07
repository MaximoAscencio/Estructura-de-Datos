import random
import statistics

numeros = [random.randint(150,250)for _ in range(50)]

media = statistics.mean(numeros)
mediana = statistics.median(numeros)
moda = statistics.mode(numeros)
varianza = statistics.variance(numeros)
desviación = statistics.stdev(numeros)

print ("lista de numeros:", numeros)
print("Media \n", moda)
print("Mediana \n", mediana)
print("Moda\n", moda)
print("Varianza\n", varianza)
print("Desviación\n",desviación)