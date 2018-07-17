"""
Problema de Alquiler de Estacionamientos de CarroCosta
@author: Luis I. Reyes Castro
"""

# Importamos el modulo para programacion lineal
import pulp

demandas = [ 6, 28, 46, 52, 46, 24, 28, 44, 44, 46, 14]

prob = pulp.LpProblem( 'Problema_de_CarroCosta', pulp.LpMinimize)

y, y_AR, y_AB = [], [], []
for ( t, dem) in enumerate(demandas) :
    variable_y = pulp.LpVariable( 'y_' + str(t+1).zfill(2), 0)
    variable_y_AR = pulp.LpVariable( 'y_' + str(t+1).zfill(2) + '_AR', 0)
    variable_y_AB = pulp.LpVariable( 'y_' + str(t+1).zfill(2) + '_AB', 0)
    y.append(variable_y)
    y_AR.append(variable_y_AR)
    y_AB.append(variable_y_AB)

# Ingresamos las restricciones de aumento o disminucion de estacionamientos
# Mes 01:
prob += y[0] == y_AR[0]
prob += y[0] >= demandas[0]
# Meses 02-11:
for t in range(1,11):
    prob += y[t] == y[t-1] + y_AR[t] - y_AB[t], \
    'Mes_' + str(t+1).zfill(2)
    prob += y[t] >= demandas[t]

# Declaramos la funcion de costo
prob += 25 * pulp.lpSum( y[t] for t in range(0,11) ) \
      + 50 * pulp.lpSum( y_AR[t] for t in range(0,11) ) \
      + 35 * pulp.lpSum( y_AB[t] for t in range(0,11) )

# Imprimimos al terminal el PL
print(prob)

# Ordenamos al objeto que representa el PL que lo solucione
prob.solve()

# Imprimimos al terminal el estado de la solucion
print( 'Estado (en ingles):', pulp.LpStatus[prob.status])

# Iteramos sobre las variables de decision del problema, imprimiendo al terminal
# el valor optimo de cada variable
print( 'Valores optimos de las variables de decision:')
for var in prob.variables() :
    print( var.name, '=', var.varValue)

# Imprimimos al terminal la utilidad optima
print( 'Costo_Optimo =', pulp.value(prob.objective) )
