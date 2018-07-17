"""
Ejemplo de la Compania Reddy Micks (Taha, Ejemplo Ejemplo 2.1-1)
@author: Luis I. Reyes Castro
"""

# Importamos el modulo para programacion lineal
import pulp

# Construirmos un objeto que representa un programa lineal utilizando
# la funcion LpProblem.
# Argumento 1 (opcional): Nombre del problema
# Argumento 2 (obligatorio): Sentido de optimizacion. Opciones son:
# maximizar: LpMaximize, minimizar: LpMinimize
prob = pulp.LpProblem( 'Problema_de_la_Compania_Reddy_Micks', pulp.LpMaximize)

# Construimos dos variables de decision utilizando la funcion LpVariable
# Argumento 1 (obligatorio): Nombre de la variable
# Argumento 2 (opcional): Acota inferior de la variable (generalmente cero)
# Argumento 3 (opcional): Acota superior de la variable
# Argumento 4 (opcional): Tipo de variable. Se ingresa:
# - LpContinuous si es continua (el tipo de variable predeterminada)
# - LpInteger si es entera
# - LpBinary si es cero o uno
x_1 = pulp.LpVariable( 'x_1', 0, None, pulp.LpContinuous)
x_2 = pulp.LpVariable( 'x_2', 0, 2, pulp.LpContinuous)

# Ingresamos las restricciones
# - Si queremos darle un nombre a una restriccion, escribimos una coma despues de
# la restriccion e ingresamos el nombre como una cadena de caracteres
# - Caso contrario, no escribimos ni la coma ni la cadena de caracteres
prob += 6 * x_1 + 4 * x_2 <= 24, 'Disponibilidad_de_Materia_Prima_M1'
prob += x_1 + 2 * x_2 <= 6, 'Disponibilidad_de_Materia_Prima_M2'
prob += x_2 <= x_1 + 1, 'Encuesta_de_Mercado'

# Declaramos la funcion de utilidad
prob += 5 * x_1 + 4 * x_2

# Imprimimos y resolvemos el PL
print(prob)
prob.solve()

# Imprimimos al terminal el estado de la solucion
print( 'Estado (en ingles):', pulp.LpStatus[prob.status])

# Iteramos sobre las variables de decision del problema, imprimiendo al terminal
# el valor optimo de cada variable
print( 'Valores optimos de las variables de decision:')
for var in prob.variables() :
    # Imprimimos al terminal el nombre de la variable de decision, seguido del simbolo igual,
    # y del valor optimo de la variable
    print( var.name, '=', var.varValue)

# Imprimimos al terminal la utilidad optima
print( 'Utilidad_Optima =', pulp.value(prob.objective) )
