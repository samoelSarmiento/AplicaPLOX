#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import nltk
from nltk.corpus import stopwords
import csv
import string
from collections import Counter
import re
import unicodedata
#DATOS A ELIMINAR
punt=["'",'!','#','$','%','&','\' ,','(',')','*','+','–','.','/',':',';','<','=','>','?','@','[','^','_','`','{','|','}','~',',','•','●','§',
      '1','2','3','4','5','6','7','8','9','0','¿','¡','"','°','´','»', '\n','★']
cachedStopWords = stopwords.words("spanish")+stopwords.words("english")+ [u'ingeniero']+[u'av']+[u'etc']
cachedStopWords.remove("ti")
cachedStopWords.remove("it")
for word in cachedStopWords:
	unicodedata.normalize('NFKD', word).encode('ascii','ignore')

def ppunto(v1,v2):
	suma = 0
	for i in range(0,len(v1)):
		suma += v1[i]*v2[i]
	return suma

def modulo(v1):
	suma = 0
	for i in range(0,len(v1)):
		suma += v1[i]**2
	return math.sqrt(suma)


#LECTURA DE DATOS

salida = open("TA_Registros_etiquetadosLimpio.csv","wt")
entrada = open("TA_Registros_etiquetados.csv","rt")
csv_entrada = csv.reader(entrada)
csv_salida = csv.writer(salida,lineterminator='\n')
listInvPalabras = []
diccPalabra = []
repeticionesPalabra = []
numPalListaInvertida = 0

# ["palabra",presencia,repTotal,[[0,2], [1,3]]]
def LlenaListaInvertida(filaPalabra, numDoc):
	#sin repeticiones
	sinRepeticiones = list(set(filaPalabra))
	for palabra in sinRepeticiones:
		#calculo las repeticione
		repeticiones = filaPalabra.count(palabra)
		#busco en lista invertida
		if diccPalabra.count(palabra) == 0:
			#no existe
			diccPalabra.append(palabra)
			nodoPalabra = [palabra,1,[[numDoc,repeticiones]]]
			listInvPalabras.append(nodoPalabra)
			repeticionesPalabra.append(repeticiones)
		else:
			#existe ya
			indice = diccPalabra.index(palabra)
			nodoPalabra = listInvPalabras[indice]
			nodoPalabra[1] += 1
			nodoDoc = [numDoc,repeticiones]
			nodoPalabra[2].append(nodoDoc)	
			repActual = repeticionesPalabra[indice]
			repeticionesPalabra[indice] = repActual+repeticiones		
#PREPROCESAMIENTO
cantDisciplinasOfertadas = 0
reg = re.compile('\S{1,}')#Controla las palabras que contará
palRep = []
documentoFiltrado = []
for row in csv_entrada:
	rep = []
	for i in range(3,6):		 				
		for car in punt:
			row[i] = row[i].replace(car,"")
			row[i] = row[i].replace('á','a')
			row[i] = row[i].replace('é', 'e')
			row[i] = row[i].replace('í', 'i')
			row[i] = row[i].replace('ó', 'o')
			row[i] = row[i].replace('ú', 'u')
			row[i] = row[i].replace('ü', 'u')
			row[i] = row[i].replace('-',' ')
		row[i] = row[i].lower()
		#Aquí removemos los stopwords
		procesada = []
 		vec = row[i].split()
		procesada = [w for w in vec if not w in cachedStopWords]
		removido = ' '.join(str(e) for e in procesada)
		row[i] = removido
		#Aquí voy juntando las palabras para contarlas
		texto = row[i].split()
		palRep.append(texto)
	#Aqui procesamos la lista invertida
	LlenaListaInvertida(row[3].split()+row[4].split()+row[5].split(),cantDisciplinasOfertadas+1)
	cantDisciplinasOfertadas = cantDisciplinasOfertadas + 1
	documentoFiltrado.append((row[3]+row[4]+row[5]).split())
	csv_salida.writerow(row)

listaInvertidaArchivo = open("Lista_Invertida.csv","wt")
csv_lista = csv.writer(listaInvertidaArchivo,lineterminator='\n')
csv_lista.writerow(listInvPalabras)

#Llevo las palabras extraidas a una "lista de palabras"
pals = [item for sublist in palRep for item in sublist]
newp = []
#Aquí vuelvo esta lista un string
newp = ' '.join(pals)
#Con esta instrucción agrupo y cuento las palabras en la cadena antes mencionada
c = Counter(ma.group() for ma in reg.finditer(newp))

#csv_entrada.close();

with open('Contador_de_palabras.csv', 'wb') as f:
    w = csv.writer(f)
    w.writerows(c.items())
    
lol = ["Cantidad de Disciplinas Ofertadas:",str(cantDisciplinasOfertadas)]
csv_salida.writerow(lol)


##======================
##PARA EL LABORATORIO 2
##======================

#ARCHIVO DE TEXTO CON TODAS LAS OFERTAS LABORALES
entrada = open("TA_Registros_etiquetados.csv","rt")
csv_entrada = csv.reader(entrada)
salidaDocVectores = open("DocVectoresOfertas.csv","wt")
csv_salida = csv.writer(salidaDocVectores,lineterminator='\n')
cabecera = ["Nro Registro","Area de Etiqueta","ID","Job Tittle","Description","Qualifications"]
csv_salida.writerow(cabecera)
for vectOfertas in csv_entrada:
	for i in range(1,6):
		csv_salida.writerow(vectOfertas)


###Un archivo de texto que muestre los índices invertidos de las ofertas laborales 
salidaDocVectores = open("DocVectorListaInvertida.csv","wt")
csv_salida = csv.writer(salidaDocVectores,lineterminator='\n')
for i in range(0,len(listInvPalabras)):
	csv_salida.writerow(listInvPalabras[i])

#Al momento de cargar el CV de consulta, imprimir (en consola o GUI) el vector que se usará
vectorPalComparacion = [];
"""Para el filtrado de las palabras apra formar el nuevo vector que se usará"""
arch = open('cv_test.txt', 'r')
estaLeyendo = True
#lista = arch.readlines()
lista = arch.readlines()

listaPalabras = []
##cantidad de palabras
for i in range(0,len(lista)):
	listaPalabraPorLinea = lista[i].split()
	cantPalabras = len(lista[i].split())
	for j in range(0,cantPalabras):
		listaPalabras.append(listaPalabraPorLinea[j])

palRep = []
row = listaPalabras
vecPalabras = []

for i in range(0,len(listaPalabras)):
	for car in punt:
		listaPalabras[i] = listaPalabras[i].replace(car,"")
		listaPalabras[i] = listaPalabras[i].replace('á','a')
		listaPalabras[i] = listaPalabras[i].replace('é', 'e')
		listaPalabras[i] = listaPalabras[i].replace('í', 'i')
		listaPalabras[i] = listaPalabras[i].replace('ó', 'o')
		listaPalabras[i] = listaPalabras[i].replace('ú', 'u')
		listaPalabras[i] = listaPalabras[i].replace('ü', 'u')
		listaPalabras[i] = listaPalabras[i].replace('-',' ')
	listaPalabras[i] = listaPalabras[i].lower()
	procesada = [w for w in listaPalabras[i] if not w in punt]
	#Aquí vuelvo esta lista un string
	removido = ''.join(str(e) for e in procesada)
	vectorPalComparacion.append(removido)
compresionLista = [w for w in vectorPalComparacion if not w in cachedStopWords]
compresionLista = [w for w in compresionLista if not w == ""]
#formamos el query del (0,0,0,0,0,0,1,0,0)
#diccPalabra
query = [0]*len(diccPalabra)
for i in range(0,len(compresionLista)):
	if diccPalabra.count(compresionLista[i]) != 0:
		indice = diccPalabra.index(compresionLista[i]
		query[indice] = 1
print query


"""
print listInvPalabras[0][0]
print listInvPalabras[0][1]
print listInvPalabras[0][2]

vectorCantPalComparacion = []
pos = 0
for i in range(0,len(vectorPalComparacion)):
	pos = diccPalabra.index(vectorPalComparacion[i]) #La posicion donde lo encuentra
	if (diccPalabra.count(vectorPalComparacion[i]) != 0): #Si existe en el diccPalabra
		listInvPalabras[pos]
		vectorCantPalComparacion[i] = listInvPalabras[pos]

print vectorCantPalComparacion[0]
"""
