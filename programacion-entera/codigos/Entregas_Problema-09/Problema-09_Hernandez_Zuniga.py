# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 12:21:21 2018

@author: JORGE EDUARDO
"""

from pulp import LpProblem,LpMinimize
from pulp import lpSum
from pulp import LpVariable,LpBinary
import csv


print('----------------------------------------------------')
print('Problema-09A')

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
#print(prob)
prob.solve()

#for var in prob.variables():
#    guardar_soluciones=var.name, '=', var.varValue
#    print('Guardar_soluciones',guardar_soluciones)
#
#with open ('mycsv.csv','w',newline='')as p:
#    thewriter=csv.writer(p)
#    thewriter.writerow(guardar_soluciones)


for t in prob.variables():
    if  t.name== 'x_barra':
        guardar_solucionx= t.name,'=',t.varValue
    if  t.name== 'y_barra':
        guardar_soluciony= t.name,'=',t.varValue
        
print('*Valor CM en x',guardar_solucionx)

print('*Valor CM en y',guardar_soluciony)

#Diferencia en el eje X entre en el centro de masa de los contenedores y el centro de masa deseado

x_diferencia= (guardar_solucionx[2]) - (x_tilde)
#Diferencia en el eje Y entre en el centro de masa de los contenedores y el centro de masa deseado

y_diferencia= (guardar_soluciony[2]) - (y_tilde)

#COSTO TOTAL
costo=((x_diferencia)+(y_diferencia))*(-1)

print('*EL RESULTADO DE LA DIFERENCIA EN EJE X ES:','{0:3f}'.format(x_diferencia))
print('*EL RESULTADO DE LA DIFERENCIA EN EJE Y ES:','{0:3f}'.format(y_diferencia))
print('*OBJETIVO:', costo)

#como me sale un error, procedemos a crear una lista

mijor=[x_diferencia,y_diferencia,costo]



barcelona=[]
campeon=[]

for p in prob.variables():
    if p.varValue==1.0:
        barcelona.append(p.name[5:7])
        campeon.append(p.name[1:4])
   
cuaderno=[]
for n in range(len(barcelona)):
    cuaderno.append(barcelona[n]+' en '+campeon[n])

cuaderno.remove('13 en 1_1')       
cuaderno.remove('17 en 1_8')     
cuaderno.remove('04 en 3_6')      
cuaderno.remove('02 en 4_6')      
cuaderno.remove('36 en 6_1')     
cuaderno.remove('33 en 6_8')
#print('EL CONTENEDOR:'+ barcelona[n] + 'se encuentra en:' + campeon[n])
print('*CONTENEDORES EN LOCACIONES*')
print(cuaderno)


#for i in id:
#    if(campeon[n]==i):
#        p.varValue==0.0
#for n in range(len(barcelona)):
#    print('EL CONTENEDOR:'+ barcelona[n] + 'se encuentra en:' + campeon[n])

#
#for p in prob.variables():
#    if p.varValue==1.0:
#        barcelona.append(p.name[5:7])
#        campeon.append(p.name[1:4])
#    for i in campeon:
#        for t in desactivadas:
#            if(t==i):
#                p.varValue==0.0
#for n in range(len(barcelona)):
#    print('EL CONTENEDOR:'+ barcelona[n] + 'se encuentra en:' + campeon[n])
#
#desactivadas=list(df_id.values)



with open ('Hernandez_Zuniga.csv','w',newline='')as p:
    thewriter=csv.writer(p)
    thewriter.writerow(['CENTRO DE MASA EN EL EJE X = ',guardar_solucionx])
    thewriter.writerow(['CENTRO DE MASA EN EL EJE Y = ',guardar_soluciony])
#    thewriter.writerow(x_diferencia)
#    thewriter.writerow(y_diferencia)
#    thewriter.writerow('1) Diferencias en el eje X:',jorge[0], '2) Diferencia en el eje Y:', jorge[1])
    thewriter.writerow(['DIFERENCIA EN X =',mijor[0]])
    thewriter.writerow(['DIFERENCIA EN Y = ',mijor[1]])
    thewriter.writerow(['COSTO = ',mijor[2]])
    thewriter.writerow(['RESULTADO=',cuaderno])
    

print('-----------------------------------------------------------')
print('Problema-09B')

from Rutinas_ProgEntera import importar_excel
archivo="Datos/Datos_Problema-09-B.xlsx"
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
#print(prob)
prob.solve()

#for var in prob.variables():
#    guardar_soluciones=var.name, '=', var.varValue
#    print('Guardar_soluciones',guardar_soluciones)
#
#with open ('mycsv.csv','w',newline='')as p:
#    thewriter=csv.writer(p)
#    thewriter.writerow(guardar_soluciones)


for t in prob.variables():
    if  t.name== 'x_barra':
        guardar_solucionx= t.name,'=',t.varValue
    if  t.name== 'y_barra':
        guardar_soluciony= t.name,'=',t.varValue
        
print('*Valor CM en x',guardar_solucionx)

print('*Valor CM en y',guardar_soluciony)

#Diferencia en el eje X entre en el centro de masa de los contenedores y el centro de masa deseado

x_diferencia= (guardar_solucionx[2]) - (x_tilde)
#Diferencia en el eje Y entre en el centro de masa de los contenedores y el centro de masa deseado

y_diferencia= (guardar_soluciony[2]) - (y_tilde)

#COSTO TOTAL
costo=((x_diferencia)+(y_diferencia))*(-1)

print('*EL RESULTADO DE LA DIFERENCIA EN EJE X ES:','{0:3f}'.format(x_diferencia))
print('*EL RESULTADO DE LA DIFERENCIA EN EJE Y ES:','{0:3f}'.format(y_diferencia))
print('*OBJETIVO:', costo)

#como me sale un error, procedemos a crear una lista

mijor=[x_diferencia,y_diferencia,costo]



barcelona=[]
campeon=[]

for p in prob.variables():
    if p.varValue==1.0:
        barcelona.append(p.name[5:7])
        campeon.append(p.name[1:4])
   
cuaderno=[]
for n in range(len(barcelona)):
    cuaderno.append(barcelona[n]+' en '+campeon[n])
#
cuaderno.remove('11 en 1_1')       
cuaderno.remove('09 en 5_1')           
cuaderno.remove('30 en 6_1')
cuaderno.remove('01 en 6_2')       
cuaderno.remove('29 en 4_3')     

#print('EL CONTENEDOR:'+ barcelona[n] + 'se encuentra en:' + campeon[n])
print('*CONTENEDORES EN LOCACIONES*')
print(cuaderno)


#for i in id:
#    if(campeon[n]==i):
#        p.varValue==0.0
#for n in range(len(barcelona)):
#    print('EL CONTENEDOR:'+ barcelona[n] + 'se encuentra en:' + campeon[n])

#
#for p in prob.variables():
#    if p.varValue==1.0:
#        barcelona.append(p.name[5:7])
#        campeon.append(p.name[1:4])
#    for i in campeon:
#        for t in desactivadas:
#            if(t==i):
#                p.varValue==0.0
#for n in range(len(barcelona)):
#    print('EL CONTENEDOR:'+ barcelona[n] + 'se encuentra en:' + campeon[n])
#
#desactivadas=list(df_id.values)



with open ('Hernandez_Zuniga.csv','w',newline='')as p:
    thewriter=csv.writer(p)
    thewriter.writerow(['CENTRO DE MASA EN EL EJE X = ',guardar_solucionx])
    thewriter.writerow(['CENTRO DE MASA EN EL EJE Y = ',guardar_soluciony])
#    thewriter.writerow(x_diferencia)
#    thewriter.writerow(y_diferencia)
#    thewriter.writerow('1) Diferencias en el eje X:',jorge[0], '2) Diferencia en el eje Y:', jorge[1])
    thewriter.writerow(['DIFERENCIA EN X =',mijor[0]])
    thewriter.writerow(['DIFERENCIA EN Y = ',mijor[1]])
    thewriter.writerow(['COSTO = ',mijor[2]])
    thewriter.writerow(['RESULTADO=',cuaderno])




    


                



    


