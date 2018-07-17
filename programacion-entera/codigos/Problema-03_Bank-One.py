"""
Problema de Bank One (Taha, Ejemplo Ejemplo 2.4-1)
@author: Luis I. Reyes Castro
"""

import pulp

prob = pulp.LpProblem( 'Problema_de_Bank_One', pulp.LpMaximize)

x_1 = pulp.LpVariable( 'x_1', 0)
x_2 = pulp.LpVariable( 'x_2', 0)
x_3 = pulp.LpVariable( 'x_3', 0)
x_4 = pulp.LpVariable( 'x_4', 0)
x_5 = pulp.LpVariable( 'x_5', 0)

prob += x_1 + x_2 + x_3 + x_4 + x_5 <= 12, 'Monto_total'
prob += x_4 + x_5 >= 0.40 * ( x_1 + x_2 + x_3 + x_4 + x_5 ), 'Preferencia-1'
prob += x_3 >= 0.50 * ( x_1 + x_2 + x_3 ), 'Preferencia-2'
prob += 0.10 * x_1 + 0.07 * x_2 + \
        0.03 * x_3 + 0.05 * x_4 + 0.02 * x_5 <= \
        0.04 * ( x_1 + x_2 + x_3 + x_4 + x_5 ), 'Preferencia-3'

prob += 0.0260 * x_1 + 0.0509 * x_2 + \
0.0864 * x_3 + 0.0688 * x_4 + 0.0780 * x_5, 'Redito_total'

print(prob)
prob.solve()

print( 'Estado (en ingles):', pulp.LpStatus[prob.status])
print( 'Utilidad_Optima =', pulp.value(prob.objective) )
print( 'Valores optimos de las variables de decision:')
for var in prob.variables() :
    print( var.name, '=', var.varValue)
