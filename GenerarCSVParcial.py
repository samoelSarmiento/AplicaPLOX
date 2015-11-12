#Pasar a archivo de texto los 3 ultimos campos
import csv

#Lectura de archivos
salida = open("TA_Registros_etiquetadosParcial.csv","wt")
entrada = open("TA_Registros_etiquetados.csv","rt")
csv_entrada = csv.reader(entrada)
csv_salida = csv.writer(salida,lineterminator='\n')

data = []
for row in csv_entrada:
    fila = []
    for i in  range(3, 6):
        fila.append(row[i])
	csv_salida.writerow(fila)
salida.close
entrada.close
