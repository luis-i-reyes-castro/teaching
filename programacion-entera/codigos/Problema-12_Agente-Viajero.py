"""
Agente Viajero Ecuatoriano

@author: Luis I. Reyes Castro
"""

import numpy as np
import pulp
import Rutinas_ProgEntera as rutinas

archivo_datos = 'Datos/Datos_Problema-12.xlsx'
hoja_ciudades = 'Origenes'
hoja_distancias = 'Distancias (km)'

df_ciudades = rutinas.importar_excel( archivo_datos, hoja_ciudades)
df_distancias = rutinas.importar_excel( archivo_datos, hoja_distancias)

ciudades = list( df_ciudades['Origen'] )
n        = len(ciudades)
distancias = df_distancias.values
distancias = ( distancias + distancias.transpose() ) / 2.0

# Declaramos un programa lineal entero
prob = pulp.LpProblem( 'Agente-Viajero', pulp.LpMinimize)

# Declaramos las variables de decision
x = {}
lista_x = []
lista_c = []
for i in range(0, n-1) :
    ind_i = str(i+1).zfill(2)
    for j in range( i+1, n) :
        ind_j = str(j+1).zfill(2)
        if not np.isnan( distancias[i,j] ) :
            x_nom = 'x_' + ind_i + '_' + ind_j
            x[( ind_i, ind_j)] = pulp.LpVariable( x_nom, 0, 1, pulp.LpContinuous)
            x[( ind_j, ind_i)] = x[( ind_i, ind_j)]
            lista_c.append( distancias[i,j] )
            lista_x.append( x[( ind_i, ind_j)] )

# Declaramos la funcion de costo
prob += pulp.lpDot( lista_c, lista_x), 'Distancia total del recorrido'

# Creamos diccinario de ciudades vecinas
vecinas = {}
for i in range(n) :
    ind_i = str(i+1).zfill(2)
    vecinas[ind_i] = []
    for j in range(n) :
        ind_j = str(j+1).zfill(2)
        if not np.isnan( distancias[i,j] ) :
            vecinas[ind_i].append(ind_j)

# Iteramos por las ciudades creando las restricciones iniciales
for i in range(n) :
    ind_i = str(i+1).zfill(2)
    prob += pulp.lpSum( x[( ind_i, ind_j)] for ind_j in vecinas[ind_i] ) == 2, \
    'Restriccion para la ciudad ' + ciudades[i]

print(prob)
prob.solve()

print( 'Estado (en ingles):', pulp.LpStatus[prob.status])
print( 'Costo_Optimo =', pulp.value(prob.objective) )
print( 'Valores optimos de las variables de decision:')
for var in prob.variables() :
    if var.varValue > 0.0 :
        print( var.name, '=', var.varValue)

# Definimos una funcion que retorna los arcos fronterizos de un subconjunto
# de ciudades ingresadas como indices
def arcos_fronterizos( indices_ciudades) :
    arcos = set()
    for ind_i in indices_ciudades :
        for ind_j in vecinas[ind_i] :
            if ind_j not in indices_ciudades :
                arcos.add( x[ ind_i, ind_j ] )

    return list(arcos)
