"""
Problema de Alquiler de Estacionamientos de CarroCosta
@author: Luis I. Reyes Castro
"""

import pulp

demandas = [ 6, 28, 46, 52, 46, 24, 28, 44, 44, 46, 14]

prob = pulp.LpProblem( 'Problema_de_CarroCosta', pulp.LpMinimize)

y, y_AR, y_AB = [], [], []
for ( t, d_t) in enumerate(demandas) :
    variable_y    = pulp.LpVariable( 'y_' + str(t+1).zfill(2), 0)
    variable_y_AR = pulp.LpVariable( 'y_' + str(t+1).zfill(2) + '_AR', 0)
    variable_y_AB = pulp.LpVariable( 'y_' + str(t+1).zfill(2) + '_AB', 0)
    y.append(variable_y)
    y_AR.append(variable_y_AR)
    y_AB.append(variable_y_AB)

for ( t, d_t) in enumerate(demandas) :
    y_t    = y[t]
    y_tm1  = y[t-1] if t -1 >= 0 else 0.0
    y_t_AR = y_AR[t]
    y_t_AB = y_AB[t]
    prob += y_t >= d_t, \
            'Demanda_en_el_mes_' + str(t+1).zfill(2)
    prob += y_t == y_tm1 + y_t_AR - y_t_AB, \
            'Alquiler-solicitud-y-entrega_en_el_mes_' + str(t+1).zfill(2)

prob += 25 * pulp.lpSum( y[t] for t in range(0,11) ) \
      + 50 * pulp.lpSum( y_AR[t] for t in range(0,11) ) \
      + 35 * pulp.lpSum( y_AB[t] for t in range(0,11) ), 'Costo_total'

print(prob)
prob.solve()

print( 'Estado (en ingles):', pulp.LpStatus[prob.status])
print( 'Costo_Optimo =', pulp.value(prob.objective) )
print( 'Valores optimos de las variables de decision:')
for var in prob.variables() :
    print( var.name, '=', var.varValue)
