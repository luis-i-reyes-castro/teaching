"""
Problema de Inversion sobre Multiples Periodos
@author: Luis I. Reyes Castro
"""

# Importamos el modulo para programacion lineal
import pulp

# Construirmos un objeto que representa un programa lineal
prob = pulp.LpProblem( 'Problema_de_Inversion_Multiperiodo', pulp.LpMaximize)

# Construimos dos variables de decision utilizando la funcion LpVariable
# Argumento 1 (obligatorio): Cadena de caracteres conteniendo nombre de la variable
# Argumento 2 (opcional): Acota inferior de la variable (se ingresa None si no la hay)
# - Si no se ingresa nada, el sistema asume que la variable es mayor o igual a -infinito
# Argumento 3 (opcional): Acota superior de la variable (se ingresa None si no la hay)
# - Si no se ingresa nada, el sistema asume que la variable es menor o igual a +infinito
# Argumento 4 (opcional): Tipo de variable. Se ingresa: 
# - pulp.LpContinuous si es continua (i.e. si puede tomar valores decimales)
# - pulp.LpInteger si es entera (i.e. solo puede tomar valores enteros)
# - Si no se ingresa nada, el sistema asume que la variable es continua
x_15 = pulp.LpVariable( 'x_15', 0, None, pulp.LpInteger)
x_16 = pulp.LpVariable( 'x_16', 0, None, pulp.LpInteger)
x_17 = pulp.LpVariable( 'x_17', 0, None, pulp.LpInteger)
y_15 = pulp.LpVariable( 'y_15', 0, None, pulp.LpInteger)
y_16 = pulp.LpVariable( 'y_16', 0, None, pulp.LpInteger)
z_16_17 = pulp.LpVariable( 'z^(16)_17', 0)
z_16_18 = pulp.LpVariable( 'z^(16)_18', 0)
z_16_19 = pulp.LpVariable( 'z^(16)_19', 0)
w_15 = pulp.LpVariable( 'w_15', 0)
w_16 = pulp.LpVariable( 'w_16', 0)
w_17 = pulp.LpVariable( 'w_17', 0)
w_18 = pulp.LpVariable( 'w_18', 0)
r = pulp.LpVariable( 'r', 0)

# Ingresamos las restricciones
# - Si queremos darle un nombre a una restriccion, escribimos una coma despues de 
# la restriccion e ingresamos el nombre como una cadena de caracteres
# - Caso contrario, no escribimos ni la coma ni la cadena de caracteres
prob += 320000 == 89.28 * x_15 + 84.74 * y_15 + w_15, 'Anyo_2015'
prob += 30 * y_15 + z_16_17 + z_16_18 + z_16_19 + w_15 == \
89.28 * x_16 + 84.74 * y_16 + w_16, 'Anyo_2016'
prob += 100 * x_15 + 30 * y_15 + 30 * y_16 + w_16 == \
89.28 * x_17 + 1.0400 * z_16_17 + w_17, 'Anyo_2017'
prob += 100 * x_16 + 40 * y_15 + 30 * y_16 + w_17 == \
1.0816 * z_16_18 + w_18, 'Anyo_2018'
prob += 100 * x_17 + 40 * y_16 + w_18 == \
1.1248 * z_16_19 + r, 'Anyo_2019'
prob += z_16_17 + z_16_18 + z_16_19 <= 80000, \
'Monto_maximo_que_puede_ser_tomado_en_prestamo'

# Declaramos la funcion de utilidad
prob += r

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
    # Imprimimos al terminal el nombre de la variable de decision, seguido del simbolo igual, 
    # y del valor optimo de la variable
    print( var.name, '=', var.varValue)

# Imprimimos al terminal la utilidad optima
print( 'Utilidad_Optima =', pulp.value(prob.objective) )
