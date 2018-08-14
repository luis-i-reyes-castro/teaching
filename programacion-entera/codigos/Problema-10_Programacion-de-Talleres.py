"""
Problema de Programacion de Talleres
@author: Luis I. Reyes Castro
"""

import numpy as np
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

sigma    = np.zeros( shape = (m,n), dtype = np.int)
duracion = np.zeros( shape = (m,n) )
for j in range(n) :
    trabajo = trabajos[j]
    df      = dict_df[trabajo]
    sigma[j,:]    = df['Maquina'].values
    duracion[j,:] = df['Tiempo (min)'].values

# Declaramos un problema
prob = pulp.LpProblem( 'Programacion-de-Talleres', pulp.LpMinimize)

# Declaramos las variables de decision
x = {}
z = {}
C_max = pulp.LpVariable( 'C_max', 0, None, pulp.LpContinuous)
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
                                 + '_T' + str(j+1).zfill(2) \
                                 + '_T' + str(j+1).zfill(2)
        for k in range( j+1, n) :
            prob += z[(i,j,k)] + z[(i,k,j)] == 1, \
            'En la maquina ' + str(i) + ' el trabajo ' \
            + str(j+1).zfill(2) + ' y el trabajo ' \
            + str(k+1).zfill(2) + ' no se translapan'

# Declaramos las restricciones que hacen que para cada trabajo el tiempo
# de arranque de la (h+1)-ava operacion sea siempre mayor or igual al
# tiempo de completacion de la h-ava operacion
for (j, trabajo) in enumerate(trabajos) :
    operaciones = sigma[j,:]
    duraciones  = duracion[j,:]
    for ( h, _) in enumerate(operaciones[:-1]) :
        ind_op_hm1 = operaciones[h+1]
        ind_op_h   = operaciones[h]
        dur_op_h   = duraciones[h]
        prob += x[( ind_op_hm1, j)] >= x[( ind_op_h, j)] + dur_op_h, \
        'En el trabajo ' + str(j+1).zfill(2) \
        + ' la operacion en la maquina M' + str(ind_op_hm1) \
        + ' arranca despues de la completacion de la operacion en la' \
        + ' maquina M' + str(ind_op_h)

# Declaramos las restricciones que hacen que para cada maquina y cada par
# de trabajos el tiempo de arranque de uno de los dos trabajos sea mayor
# o igual al tiempo de completacion del otro trabajo
V = duracion.sum()
for i in range(m) :
    for j in range(n) :
        for k in range( j+1, n) :
            
            operaciones_j = sigma[j,:]
            operaciones_k = sigma[k,:]
            duraciones_j  = duracion[j,:]
            duraciones_k  = duracion[k,:]
            p_i_j = duraciones_j[ np.nonzero( operaciones_j == i )[0][0] ]
            p_i_k = duraciones_k[ np.nonzero( operaciones_k == i )[0][0] ]
            
            prob += x[(i,j)] >= x[(i,k)] + p_i_k - V * z[(i,j,k)], \
            'Restriccion disjuntiva para la maquina M'  + str(i) \
            + ', el trabajo T' + str(j+1).zfill(2) + ', y el trabajo T' \
            + str(k+1).zfill(2) + ', Altertiva-A'
            prob += x[(i,k)] >= x[(i,j)] + p_i_j - V * ( 1 - z[(i,j,k)] ), \
            'Restriccion disjuntiva para la maquina M'  + str(i) \
            + ', el trabajo T' + str(j+1).zfill(2) + ', y el trabajo T' \
            + str(k+1).zfill(2) + ', Altertiva-B'

# Declaramos las restricciones asociadas con C_max
for (j, trabajo) in enumerate(trabajos) :
    ultima_op = sigma[j,-1]
    duracion_ultima_op = duracion[j,-1]
    prob += C_max >= x[ ultima_op, j] + duracion_ultima_op, \
    'La variable C_max es mayor o igual al tiempo de completacion de la' \
    + ' ultima operacion del trabajo T' + str(j+1).zfill(2)

# Declaramos la funcion que queremos minimizar
prob += C_max, 'Tiempo de finalizacion de todos los trabajos'

# Imprimimos y resolvesmos el problema
print(prob)
prob.solve()

# Imprimimos resultados
print( 'Estado (en ingles):', pulp.LpStatus[prob.status])
print( 'Costo_Optimo =', pulp.value(prob.objective) )
print( 'Valores optimos de las variables de decision no-triviales:')
for var in prob.variables() :
    if var.varValue > 0.0 :
        print( var.name, '=', var.varValue)
