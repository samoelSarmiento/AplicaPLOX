#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import stopwords
import csv
import string
from collections import Counter
import re
import unicodedata
#DATOS A ELIMINAR
punt=["'",'!','#','$','%','&','\' ,','(',')','*','+','–','.','/',':',';','.','<','=','>','?','@','[','^','_','`','{','|','}','~',',','•','●','§',
      '1','2','3','4','5','6','7','8','9','0','¿','¡','"','°','´','»', '\n']
cachedStopWords = stopwords.words("spanish")+stopwords.words("english")+ [u'ingeniero']
cachedStopWords.remove("ti")
cachedStopWords.remove("it")
for word in cachedStopWords:
	unicodedata.normalize('NFKD', word).encode('ascii','ignore')


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
print listaPalabras

palRep = []
row = listaPalabras
vecPalabras = []

print listaPalabras[0]

for i in range(0,len(listaPalabras)):
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
#procesada = [w for w in vec if not w in cachedStopWords]
print vectorPalComparacion

