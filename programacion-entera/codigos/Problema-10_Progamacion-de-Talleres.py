"""
Problema de Programacion de Talleres
@author: Luis I. Reyes Castro
"""

import numpy as np
import pandas as pd
import pulp
from Rutinas_ProgEntera import importar_excel

# Declaramos las fuentes de datos y los importamos

archivo_datos = 'Datos/Datos_Problema-10.xlsx'
hoja_maquinas = 'Maquinas'
hoja_trabajos = 'Trabajos'

df_maquinas = importar_excel( archivo_datos, hoja_maquinas)
df_trabajos = importar_excel( archivo_datos, hoja_trabajos)

maquinas = list( df_maquinas.index )
trabajos = list( df_trabajos['Hoja'] )
m        = len( maquinas )
n        = len( trabajos )

dict_df = {}
for trabajo in trabajos :
    dict_df[trabajo] = importar_excel( archivo_datos, trabajo)

sigma    = np.zeros( shape = (m,n) )
duracion = np.zeros( shape = (m,n) )
for i in range(n) :
    trabajo = trabajos[i]
    df      = dict_df[trabajo]
    sigma[i,:]    = df['Maquina'].values
    duracion[i,:] = df['Tiempo (min)'].values

# Declaramos un problema
prob = pulp.LpProblem( 'Programacion-de-Talleres', pulp.LpMinimize)

# Declaramos las variables de decision
x = {}
z = {}
for i in range(m) :
    for j in range(n) :
        x_nom = 'x_M' + str(i) + '_' + 'T' + str(j+1).zfill(2)
        x[(i,j)] = pulp.LpVariable( x_nom, 0, None, pulp.LpContinuous)
        for k in range(n) :
            z_nom = 'z_M' + str(i) + '_T' + str(j+1).zfill(2) \
                  + '_T' + str(k+1).zfill(2)
            z[(i,j,k)] = pulp.LpVariable( z_nom, 0, 1, pulp.LpBinary)

# Declaramos las restricciones iniciales
for i in range(m) :
    for j in range(n) :
        prob += z[(i,j,j)] <= 0, 'Trivialidad de z_M' + str(i) \
                                 + '_T' + str(j).zfill(2) + '_T' + str(j).zfill(2)
        for k in range( j+1, n) :
            prob += z[(i,j,k)] + z[(i,k,j)] == 1, \
            'En la maquina ' + str(i) + ' el trabajo ' + str(j+1).zfill(2) \
            + ' y el trabajo ' + str(k+1).zfill(2) + ' no se translapan'

# Declaramos las restricciones
print(prob)


