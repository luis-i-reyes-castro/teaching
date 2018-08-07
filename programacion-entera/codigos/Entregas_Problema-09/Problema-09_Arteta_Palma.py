# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 16:14:58 2018

@author: Steeven Palma
"""
#from pulp import LpStatus
#from pulp import value
from pulp import LpProblem,LpMinimize
from pulp import lpSum
from pulp import LpVariable,LpBinary
import csv
from Rutinas_ProgEntera import importar_excel
archivo="Datos/Datos_Problema-09-A.xlsx"
df_filas=importar_excel(archivo, "Filas")
df_columnas=importar_excel(archivo, "Columnas")
df_cm=importar_excel(archivo, "Centro-de-Masa")
df_id=importar_excel(archivo, "Locaciones-Deshabilitadas")
df_cont=importar_excel(archivo, "Contenedores")
#archivo_solucion= 'Soluciones/Solucion_Problema-08.xlsx'
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
           
x_barra=LpVariable("x_barra",0,None)
y_barra=LpVariable("y_barra",0,None)
x_mas=LpVariable("x_mas",0,None)
x_menos=LpVariable("x_menos",0,None)
y_mas=LpVariable("y_mas",0,None)
y_menos=LpVariable("y_menos",0,None)

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
#print(prob)
prob.solve()

for var in prob.variables() :
    if var.name=="x_barra":
        guardar_x= var.name, '=', var.varValue
    if var.name=="y_barra":
        guardar_y= var.name, '=', var.varValue
print("Centro masa x",guardar_x)
print("Centro masa y",guardar_y)
error_x=guardar_x[2]-x_tilde
error_y=(guardar_y[2]-y_tilde)
Costo_Total= (error_x + error_y)*-1
print("X El error entre Locacion centro de masa contenedores y Locacion centro de masa deseado:",error_x)
print("Y El error entre Locacion centro de masa contenedores y Locacion centro de masa deseado:",error_y)
print("El costo total de la funcion objetivo es:",Costo_Total)
lista=[error_x,error_y,Costo_Total]
print(lista)

num_contene=[]
ubicacion=[]
contenedor_ubicacion=[]
for v in prob.variables() :
    if v.varValue==1.0:
        ubic_cont=("El contenedor" + " " + v.name[5:7] + " " + 'se encuentra en la locacion (fila_columna)=' + v.name[1:4])
        num_contene.append(v.name[5:7])
        ubicacion.append(v.name[1:4])

for n in range (len(num_contene)):
    contenedor_ubicacion.append(num_contene[n] + ":" + ubicacion[n] )
#print("El contenedor : se encuentra en locacion (x_y) ----> ",contenedor_ubicacion)

for i in contenedor_ubicacion:
   if i[3:6]==("1_1"):
       contenedor_ubicacion.remove(i)
   elif i[3:6]==("1_8"):
       contenedor_ubicacion.remove(i)
   elif i[3:6]==("3_6"):
       contenedor_ubicacion.remove(i)
   elif i[3:6]==("4_6"):
       contenedor_ubicacion.remove(i)
   elif i[3:6]==("6_1"):
       contenedor_ubicacion.remove(i)
   elif i[3:6]==("6_8"):
        contenedor_ubicacion.remove(i)
print("El contenedor : se encuentra en locacion (x_y) ----> ",contenedor_ubicacion)

"""contenedor_ubicacion.remove("13:1_1")
contenedor_ubicacion.remove("1_8")
contenedor_ubicacion.remove("3_6")
contenedor_ubicacion.remove("4_6")
contenedor_ubicacion.remove("6_1")
contenedor_ubicacion.remove("6_8")"""
        
with open ("solucionA.csv","w",newline="") as write:
    thewriter=csv.writer(write)
    thewriter.writerow(["Centro de masa calculado eje x " ,(guardar_x)])
    thewriter.writerow(["Centro de masa calculado eje y ",guardar_y])
    thewriter.writerow(["1) Error locacion x  "  ,lista[0]])
    thewriter.writerow(["2) Error locacion y  " , lista[1]])
    thewriter.writerow(["3) Costo total   " , lista[2]])
    #thewriter.writerow(["El contenedor Num " , num_contene])
    #thewriter.writerow(["se encuentra en la locacion " , ubicacion])
    thewriter.writerow(["El contenedor : se encuentra en locacion (x_y) ----> ", contenedor_ubicacion])
    #thewriter.writerow(error_y)

"""print( '\n' + 'GUARDANDO PLAN OPTIMO EN ARCHIVO: ' + archivo_solucion)
writer = pd.ExcelWriter(archivo_solucion)
        terminos_x.to_excel( writer, sheet_name = '')
        terminos_y.to_excel( writer, sheet_name = '')
        writer.close()"""
        
        
print("")      
print("")       
print("SOLUCION B ")
print("")

        



from Rutinas_ProgEntera import importar_excel
archivo="Datos/Datos_Problema-09-B.xlsx"
df_filas=importar_excel(archivo, "Filas")
df_columnas=importar_excel(archivo, "Columnas")
df_cm=importar_excel(archivo, "Centro-de-Masa")
df_id=importar_excel(archivo, "Locaciones-Deshabilitadas")
df_cont=importar_excel(archivo, "Contenedores")
#archivo_solucion= 'Soluciones/Solucion_Problema-08.xlsx'
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
           
x_barra=LpVariable("x_barra",0,None)
y_barra=LpVariable("y_barra",0,None)
x_mas=LpVariable("x_mas",0,None)
x_menos=LpVariable("x_menos",0,None)
y_mas=LpVariable("y_mas",0,None)
y_menos=LpVariable("y_menos",0,None)

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
#print(prob)
prob.solve()

for var in prob.variables() :
    if var.name=="x_barra":
        guardar_x= var.name, '=', var.varValue
    if var.name=="y_barra":
        guardar_y= var.name, '=', var.varValue
print("Centro masa x",guardar_x)
print("Centro masa y",guardar_y)
error_x=guardar_x[2]-x_tilde
error_y=(guardar_y[2]-y_tilde)
Costo_Total= (error_x + error_y)*-1
print("X El error entre Locacion centro de masa contenedores y Locacion centro de masa deseado:",error_x)
print("Y El error entre Locacion centro de masa contenedores y Locacion centro de masa deseado:",error_y)
print("El costo total de la funcion objetivo es:",Costo_Total)
lista=[error_x,error_y,Costo_Total]
print(lista)

num_contene=[]
ubicacion=[]
contenedor_ubicacion=[]
for v in prob.variables() :
    if v.varValue==1.0:
        ubic_cont=("El contenedor" + " " + v.name[5:7] + " " + 'se encuentra en la locacion (fila_columna)=' + v.name[1:4])
        num_contene.append(v.name[5:7])
        ubicacion.append(v.name[1:4])

for n in range (len(num_contene)):
    contenedor_ubicacion.append(num_contene[n] + ":" + ubicacion[n])
#print("El contenedor : se encuentra en locacion (x_y) ----> ",contenedor_ubicacion)

contenedor_ubicacion.remove("11:1_1")
contenedor_ubicacion.remove("09:5_1")
contenedor_ubicacion.remove("30:6_1")
contenedor_ubicacion.remove("01:6_2")
contenedor_ubicacion.remove("29:4_3")
print("El contenedor : se encuentra en locacion (x_y) ----> ",contenedor_ubicacion)

        
with open ("solucionB.csv","w",newline="") as write:
    thewriter=csv.writer(write)
    thewriter.writerow(["Centro de masa calculado eje x " ,(guardar_x)])
    thewriter.writerow(["Centro de masa calculado eje y ",guardar_y])
    thewriter.writerow(["1) Error locacion x  "  ,lista[0]])
    thewriter.writerow(["2) Error locacion y  " , lista[1]])
    thewriter.writerow(["3) Costo total   " , lista[2]])
    #thewriter.writerow(["El contenedor Num " , num_contene])
    #thewriter.writerow(["se encuentra en la locacion " , ubicacion])
    thewriter.writerow(["El contenedor : se encuentra en locacion (x_y) ----> ", contenedor_ubicacion])
    #thewriter.writerow(error_y)

"""print( '\n' + 'GUARDANDO PLAN OPTIMO EN ARCHIVO: ' + archivo_solucion)
writer = pd.ExcelWriter(archivo_solucion)
        terminos_x.to_excel( writer, sheet_name = '')
        terminos_y.to_excel( writer, sheet_name = '')
        writer.close()"""