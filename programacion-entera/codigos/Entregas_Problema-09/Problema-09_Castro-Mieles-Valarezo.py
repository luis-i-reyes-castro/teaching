"""
Problema del Loadmaster
@author: Castro-Mieles-Valarezo
"""
import pulp
from pulp import LpVariable, LpBinary
from pulp import LpProblem, LpMinimize
from pulp import lpSum
from Rutinas_ProgEntera import importar_excel

archivo = './Datos/Datos_Problema-09-B.xlsx'

df_filas    = importar_excel( archivo, 'Filas')
df_columnas = importar_excel( archivo, 'Columnas')
df_cm       = importar_excel( archivo, 'Centro-de-Masa')
df_ld       = importar_excel( archivo, 'Locaciones-Deshabilitadas')
df_cont     = importar_excel( archivo, 'Contenedores')

filas    = list( df_filas.index )
columnas = list( df_columnas.index )
dist_x   = df_filas.values
dist_y   = df_columnas.values

x_tilde = df_cm.loc['x']['Distancia (m)']
y_tilde = df_cm.loc['y']['Distancia (m)']

ld = df_ld.values
contenedores = list( df_cont.index )
pesos        = df_cont.values.flatten()
peso_total   = pesos.sum()

x      = {}
dict_x = {}
for i in filas :
    for j in columnas :
        for k in contenedores :
            nom = 'x_' + str(i) + '_' + str(j) + '_' + str(k).zfill(2)
            var = LpVariable( nom, 0, 1, LpBinary)
            x[(i,j,k)] = var
            dict_x[var.name] = (i,j,k)

prob = LpProblem( 'Problema_del_Loadmaster', LpMinimize)

for nulo in ld:
    i = nulo[0]
    j = nulo[1]
    prob += lpSum( x[(i,j,k)] for k in contenedores ) <= 0, "locacion sin asignacion " + str(i) + " " + str (j) 

for i in filas :
    for j in columnas :
        prob += lpSum( x[(i,j,k)] for k in contenedores ) <= 1, \
                'Maximo un contenedor en la locacion (' + str(i) + \
                ',' + str(j) + ')'

for k in contenedores :
    x_ij_k = []
    for i in filas :
        for j in columnas :
            x_ij_k.append( x[(i,j,k)] )
    prob += lpSum( x_ij for x_ij in x_ij_k ) == 1, \
            'Asignacion del contenedor ' + str(k)

x_barra = LpVariable("x_barra", 0, None)
y_barra = LpVariable("y_barra", 0, None)
x_mas   = LpVariable("x_mas", 0, None)
x_menos = LpVariable("x_menos", 0, None)
y_mas   = LpVariable("y_mas", 0, None)
y_menos = LpVariable("y_menos", 0, None)

terminos_x = []
terminos_y = []
for ( i, fila) in enumerate(filas) :
    for ( j, col) in enumerate(columnas) :
        for ( k, cont) in enumerate(contenedores) :
            terminos_x.append( dist_x[i] * pesos[k] * x[(fila,col,cont)] )
            terminos_y.append( dist_y[j] * pesos[k] * x[(fila,col,cont)] )

prob += x_barra == ( 1.0 / peso_total ) *  \
                   lpSum( termino for termino in terminos_x ), \
                   'Centro_de_masa_en_x'
prob += y_barra == ( 1.0 / peso_total ) *  \
                   lpSum( termino for termino in terminos_y ), \
                   'Centro_de_masa_en_y'

         
z_x= LpVariable("x",0,None,pulp.LpContinuous) 
prob+= x_barra-x_tilde <= z_x
prob+= x_tilde-x_barra <= z_x

z_y= LpVariable ("y",0,None,pulp.LpContinuous)
prob+= y_barra-y_tilde <= z_y
prob+= y_tilde-y_barra <= z_y

prob += z_x + z_y
  
print(prob)
prob.solve()

print (pulp.LpStatus[prob.status])
print ("Locaciones asignadas")

for var in prob.variables():
    if var.varValue>0.0:
     print (var.name, "=", var.varValue)

nombre=[]
locacion=[]
for var in prob.variables():
    if var.varValue==1.0:
        locacion.append(var.name)
        nombre.append(var.name.split('_'))


dimx = []
dimy = []
datos = []
for (i,_) in enumerate(nombre):
    datos=nombre[i]   
    dimx.append(int(datos[1]))
    dimy.append(int(datos[2]))

for (j,_) in enumerate(locacion):
    a=dimx[j]
    b=dimy[j]
    print(locacion[j],  x_tilde-dist_x[a-1], y_tilde-dist_y[b-1])
   

















