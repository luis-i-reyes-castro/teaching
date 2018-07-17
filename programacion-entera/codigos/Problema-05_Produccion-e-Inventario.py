"""
Problema de Manejo de Inventario de la Compania ACME (Taha, Ejemplo 2.4-3)
@author: Luis I. Reyes Castro
"""

import pulp

demandas  = [ 100, 250, 190, 140, 220, 110]
costo_fab = [ 50, 45, 55, 52, 50, 50]
costo_inv = 8

prob = pulp.LpProblem( 'Problema_de_la_Compania_ACME', pulp.LpMinimize)

x = []
for ( i, dem) in enumerate(demandas) :
    variable = pulp.LpVariable( 'x_' + str(i+1), 0)
    x.append(variable)

y = []
for ( i, dem) in enumerate(demandas[:-1]) :
    variable = pulp.LpVariable( 'y_' + str(i+1), 0)
    y.append(variable)

for ( t, d_t) in enumerate(demandas) :
    x_t   = x[t]
    y_tm1 = y[t-1] if t - 1 >= 0 else 0.0
    y_t   = y[t] if t < len(demandas) - 1 else 0.0
    prob += x_t + y_tm1 == d_t + y_t, 'Mes_' + str(t+1).zfill(2)

prob += pulp.lpSum( costo_fab[k] * x[k] for k in range(6) ) \
     +  costo_inv * pulp.lpSum( y[k] for k in range(5) )

print(prob)
prob.solve()

print( 'Estado (en ingles):', pulp.LpStatus[prob.status])
print( 'Costo_Optimo =', pulp.value(prob.objective) )
print( 'Valores optimos de las variables de decision:')
for var in prob.variables() :
    print( var.name, '=', var.varValue)
