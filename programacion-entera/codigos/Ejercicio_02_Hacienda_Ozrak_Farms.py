"""
Ejemplo de la Hacienda Ozrac Farms (Taha, Ejemplo 2.2-2)
@author: Luis I. Reyes Castro
"""

# Importamos el modulo para programacion lineal
import pulp

prob = pulp.LpProblem( 'Problema_de_la_Hacienda_Ozrac_Farms', pulp.LpMinimize)

x_1 = pulp.LpVariable( 'x_1', 0)
x_2 = pulp.LpVariable( 'x_2', 0)

prob += x_1 + x_2 >= 800, 'Peso_minimo_de_la_mezcla'
prob += 0.09 * x_1 + 0.60 * x_2 >= 0.30 * ( x_1 + x_2 ), 'Contenido_de_Proteina'
prob += 0.02 * x_1 + 0.06 * x_2 <= 0.05 * ( x_1 + x_2 ), 'Contenido_de_Fibra'

prob += 0.30 * x_1 + 0.90 * x_2

print(prob)
prob.solve()

print( 'Estado (en ingles):', pulp.LpStatus[prob.status])

print( 'Valores optimos de las variables de decision:')
for var in prob.variables() :
    print( var.name, '=', var.varValue)

print( 'Costo_Optimo =', pulp.value(prob.objective) )
