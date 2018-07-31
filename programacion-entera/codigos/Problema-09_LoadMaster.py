"""
Problema del Loadmaster (Maestro de Carga) de un Buque Carguero
@author: Luis I. Reyes Castro
"""

from pulp import LpVariable, LpBinary
from pulp import LpProblem, LpMinimize
from pulp import lpSum
from Rutinas_ProgEntera import importar_excel

archivo = 'Datos/Datos_Problema-09-A.xlsx'

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

# Declaramos el Programa Entero
prob = LpProblem( 'Problema_del_Loadmaster', LpMinimize)

# Declaramos las variables primarias
x      = {}
dict_x = {}
for i in filas :
    for j in columnas :
        for k in contenedores :
            nom = 'x_' + str(i) + '_' + str(j) + '_' + str(k).zfill(2)
            var = LpVariable( nom, 0, 1, LpBinary)
            x[(i,j,k)] = var
            dict_x[var.name] = (i,j,k)

# Declaramos las variables secundarias
x_barra = LpVariable( nom, 0, None)
y_barra = LpVariable( nom, 0, None)
x_mas   = LpVariable( nom, 0, None)
x_menos = LpVariable( nom, 0, None)
y_mas   = LpVariable( nom, 0, None)
y_menos = LpVariable( nom, 0, None)

# Agregamos las restricciones que previenen que mas de un contenedor
# sea puesto en cualquier locacion
for i in filas :
    for j in columnas :
        prob += lpSum( x[(i,j,k)] for k in contenedores ) <= 1, \
                'Maximo un contenedor en la locacion (' + str(i) + \
                ',' + str(j) + ')'

# Agregamos las restricciones que exigen que cada contenedor sea asignado
# a exactamente una sola locacion
for k in contenedores :
    x_ij_k = []
    for i in filas :
        for j in columnas :
            x_ij_k.append( x[(i,j,k)] )
    prob += lpSum( x_ij for x_ij in x_ij_k ) == 1, \
            'Asignacion del contenedor ' + str(k)

# Agregamos restricciones para forzar a las variables x_barra y y_barra
# a ser iguales a las coordenadas del centro de masa de los contenedores

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
