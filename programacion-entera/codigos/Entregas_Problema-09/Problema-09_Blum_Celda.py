# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 16:14:58 2018

@author: FIMCP
"""
# Esto es adorable! Y tambien vale cero jajaja

from pulp import LpProblem,LpMinimize
from pulp import lpSum
from pulp import LpVariable,LpBinary

from Rutinas_ProgEntera import importar_excel
archivo="Datos/Datos_Problema-09-A.xlsx"
df_filas=importar_excel(archivo, "Filas")
df_columnas=importar_excel(archivo, "Columnas")
df_cm=importar_excel(archivo, "Centro-de-Masa")
df_id=importar_excel(archivo, "Locaciones-Deshabilitadas")
df_cont=importar_excel(archivo, "Contenedores")

filas=list(df_filas.index)
columnas=list(df_columnas.index)
dist_x=df_filas.values
dist_y=df_columnas.values

x_tilde=df_cm.loc["x"]["Distancia (m)"]
y_tilde=df_cm.loc["y"]["Distancia (m)"]
id=df_id.values
contenedores=list(df_cont.index)
pesos=df_cont.values.flatten()
peso_total=pesos.sum()
x={}
dict_x={}
for i in filas:
    for j in columnas:
        for k in contenedores:
            nom="x" + str(i) + "_" + str(j)  + "_" + str(k).zfill(2)
            var=LpVariable(nom,0,1,LpBinary)
            x[(i,j,k)]=var
            dict_x[var.name]=(i,j,k)
prob=LpProblem("Problema_del_Loadmaster",LpMinimize)

for i in filas:
    for j in columnas:
        prob += lpSum( x[(i,j,k)]for k in contenedores) <=1, \
        'Maximo un contenedor en la locacion (' + str(i) + \
        ',' + str(j) + ')'

for k in contenedores:
    x_ij_k=[]
    for i in filas:
        for j in columnas:
            x_ij_k.append(x[(i,j,k)])
    prob +=lpSum(x_ij for x_ij in x_ij_k)==1,\
           "Asignacion del contenedor "+str(k)

x_barra=LpVariable('x_barra',0,None)
y_barra=LpVariable('y_barra',0,None)
x_mas=LpVariable('x_mas',0,None)
x_menos=LpVariable('x_menos',0,None)
y_mas=LpVariable('y_mas',0,None)
y_menos=LpVariable('y_menos',0,None)

terminos_x=[]
terminos_y=[]
for (i,fila)in enumerate(filas):
    for (j,col)in enumerate(columnas):
        for (k,cont) in enumerate(contenedores):
            terminos_x.append(dist_x[i]*pesos[k]*x[(fila,col,cont)])
            terminos_y.append(dist_y[j]*pesos[k]*x[(fila,col,cont)])

prob +=x_barra==(1.0 / peso_total)*\
                lpSum(termino for termino in terminos_x),\
                "centro_de_masa_en_x"

prob +=y_barra==(1.0 / peso_total)*\
                lpSum(termino for termino in terminos_y),\
                "centro_de_masa_en_y"

prob+=0.0,"Costo"
print(prob)



for angie in prob.variables():
    if angie.name=='x_barra':
        companera_x=angie.name,'=',angie.varValue
    if angie.name=='y_barra':
        companera_y=angie.name,'=',angie.varValue


print('cm x',companera_x)
print('cm y',companera_y)

resultado_x=companera_x[2]-x_tilde
resultado_y=companera_y[2]-y_tilde

print('eje x',resultado_x)
print('eje y',resultado_y)



