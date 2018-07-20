"""
Problema de Programacion de Personal del Supermercado (Leccion 03, Problema 1)
@author: Luis I. Reyes Castro
"""

import pandas as pd
import pulp

archivo = 'Datos/Datos_Problema-07.xlsx'
datos   = { 'Empleados_Requeridos' : None,
            'Tiempo_Completo'      : None,
            'Tiempo_Medio'         : None,
             'Otros-parametros'    : None }

for hoja in datos :
    manija = open( archivo, 'rb')
    datos[hoja] = pd.read_excel( manija, hoja, index_col = 0)
    manija.close()

df_req     = datos['Empleados_Requeridos']
intervalos = list(df_req.index)
m          = len(intervalos)
vector_req = df_req.values.flatten()

df_tc     = datos['Tiempo_Completo']
turnos_tc = list(df_tc.columns)
n_tc      = len(turnos_tc)
matriz_tc = df_tc.values
horas_tc  = matriz_tc.sum(axis=0)

df_tm     = datos['Tiempo_Medio']
turnos_tm = list(df_tm.columns)
n_tm      = len(turnos_tm)
matriz_tm = df_tm.values
horas_tm  = matriz_tm.sum(axis=0)

df_otros = datos['Otros-parametros']
costo_tc = df_otros.loc['Costo por Empleado a Tiempo Completo']['Valor']
costo_tm = df_otros.loc['Costo por Empleado a Tiempo Medio']['Valor']
min_tc   = df_otros.loc['Numero Minimo de Empleados a Tiempo Completo']['Valor']

prob = pulp.LpProblem( 'Problema_del_Supermercado', pulp.LpMinimize)

x = []
for ( i, turno) in enumerate(turnos_tc) :
    x_i = pulp.LpVariable( 'x_' + str(turno), 0, None, pulp.LpInteger)
    x.append(x_i)

y = []
for ( j, turno) in enumerate(turnos_tm) :
    y_j = pulp.LpVariable( 'y_' + str(turno), 0, None, pulp.LpInteger)
    y.append(y_j)

for ( k, intervalo) in enumerate(intervalos) :
    prob += pulp.lpSum( matriz_tc[k][i] * x[i] for i in range(n_tc) ) + \
            pulp.lpSum( matriz_tm[k][j] * y[j] for j in range(n_tm) ) >= \
            vector_req[k], 'Intervalo_' + str(intervalo)

prob += pulp.lpSum( x[i] for i in range(n_tc) ) >= min_tc, \
        'Imagen_Corporativa'

prob += costo_tc * pulp.lpSum( horas_tc[i] * x[i] for i in range(n_tc) ) + \
        costo_tm * pulp.lpSum( horas_tm[j] * y[j] for j in range(n_tm) ), \
        'Costos_de_salarios'

print(prob)
prob.solve()

print( 'Estado (en ingles):', pulp.LpStatus[prob.status])
print( 'Costo_Optimo =', pulp.value(prob.objective) )
print( 'Valores optimos de las variables de decision:')
for var in prob.variables() :
    print( var.name, '=', var.varValue)
