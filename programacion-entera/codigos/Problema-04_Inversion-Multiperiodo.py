"""
Problema de Inversion sobre Multiples Periodos
@author: Luis I. Reyes Castro
"""

import pulp

prob = pulp.LpProblem( 'Problema_de_Inversion_Multiperiodo', pulp.LpMaximize)

x_15    = pulp.LpVariable( 'x_15', 0, None, pulp.LpInteger)
x_16    = pulp.LpVariable( 'x_16', 0, None, pulp.LpInteger)
x_17    = pulp.LpVariable( 'x_17', 0, None, pulp.LpInteger)
y_15    = pulp.LpVariable( 'y_15', 0, None, pulp.LpInteger)
y_16    = pulp.LpVariable( 'y_16', 0, None, pulp.LpInteger)
z_16_17 = pulp.LpVariable( 'z^(16)_17', 0)
z_16_18 = pulp.LpVariable( 'z^(16)_18', 0)
z_16_19 = pulp.LpVariable( 'z^(16)_19', 0)
w_15    = pulp.LpVariable( 'w_15', 0)
w_16    = pulp.LpVariable( 'w_16', 0)
w_17    = pulp.LpVariable( 'w_17', 0)
w_18    = pulp.LpVariable( 'w_18', 0)
r       = pulp.LpVariable( 'r', 0)

prob += 320000 == \
        89.28 * x_15 + 84.74 * y_15 + w_15, \
        'Anyo_2015'
prob += 30 * y_15 + z_16_17 + z_16_18 + z_16_19 + w_15 == \
        89.28 * x_16 + 84.74 * y_16 + w_16, \
        'Anyo_2016'
prob += 100 * x_15 + 30 * y_15 + 30 * y_16 + w_16 == \
        89.28 * x_17 + 1.0400 * z_16_17 + w_17, \
        'Anyo_2017'
prob += 100 * x_16 + 40 * y_15 + 30 * y_16 + w_17 == \
        1.0816 * z_16_18 + w_18, \
        'Anyo_2018'
prob += 100 * x_17 + 40 * y_16 + w_18 == \
        1.1248 * z_16_19 + r, \
        'Anyo_2019'

prob += z_16_17 + z_16_18 + z_16_19 <= 80000, \
        'Monto_maximo_que_puede_ser_tomado_en_prestamo'

prob += r, 'Retorno_final'

print(prob)
prob.solve()

print( 'Estado (en ingles):', pulp.LpStatus[prob.status])
print( 'Utilidad_Optima =', pulp.value(prob.objective) )
print( 'Valores optimos de las variables de decision:')
for var in prob.variables() :
    print( var.name, '=', var.varValue)
