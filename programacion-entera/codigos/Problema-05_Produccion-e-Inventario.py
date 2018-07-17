"""
Problema de Manejo de Inventario de la Compania ACME (Taha, Ejemplo 2.4-3)
@author: Luis I. Reyes Castro
"""

# Importamos el modulo para programacion lineal
import pulp

# Declaramos la lista de unidades demandas
demandas = [ 100, 250, 190, 140, 220, 110]
# Declaramos los costos de fabricacion y de almacenamiento
costo_fab = [ 50, 45, 55, 52, 50, 50]
costo_inv = 8

# Construirmos un objeto que representa un programa lineal
prob = pulp.LpProblem( 'Problema_de_la_Compania_ACME', pulp.LpMinimize)

# Declaramos las variables de decision de produccion
x = []
for ( i, dem) in enumerate(demandas) :
    variable = pulp.LpVariable( 'x_' + str(i+1), 0)
    x.append(variable)
# Declaramos las variables de decision de almacenamiento
y = []
for ( i, dem) in enumerate(demandas[:-1]) :
    variable = pulp.LpVariable( 'y_' + str(i+1), 0)
    y.append(variable)

# Ingresamos la restriccion asociada con el Mes 01
prob += x[0] == demandas[0] + y[0], 'Mes_01'
# Ingresamos las restricciones asociadas con los Meses 02 al 05
for k in range(1,5):
    prob += x[k] + y[k-1] == demandas[k] + y[k], 'Mes_' + str(k+1).zfill(2)
# Ingresamos la restriccion asociada con el Mes 06
prob += x[-1] + y[-1] == demandas[-1], 'Mes_06'

# Declaramos la funcion de costo
prob += pulp.lpSum( costo_fab[k] * x[k] for k in range(6) ) \
     +  costo_inv * pulp.lpSum( y[k] for k in range(5) )

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
