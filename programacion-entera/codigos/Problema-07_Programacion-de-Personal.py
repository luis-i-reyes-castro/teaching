"""
Problema de Programacion de Personal del Supermercado (Leccion 03, Problema 1)
@author: Luis I. Reyes Castro
"""

# Importamos los modulos requeridos
import openpyxl # Para importar y exportar datos desde y hacia archivos de MS Excel
import pulp # Para modelar y solucionar PLs

# Creamos una manija al archivo de MS Excel
manija = openpyxl.load_workbook( 'Ejercicio_09_Datos_(LLENO).xlsx')
# Extraemos los datos de la hoja 'Tiempo_Completo'
hoja = manija.get_sheet_by_name( 'Tiempo_Completo')
celdas_de_interes = hoja['B2':'E13']
horarios_tc = [ [ cell.value for cell in row ] for row in celdas_de_interes ]
# Extraemos los datos de la hoja 'Tiempo_Medio'
hoja = manija.get_sheet_by_name( 'Tiempo_Medio')
celdas_de_interes = hoja['B2':'J13']
horarios_tm = [ [ cell.value for cell in row ] for row in celdas_de_interes ]
# Extraemos los datos de la hoja 'Empleados_Requeridos'
hoja = manija.get_sheet_by_name( 'Empleados_Requeridos')
celdas_de_interes = hoja['B2':'B13']
empleados_req = [ [ cell.value for cell in row ] for row in celdas_de_interes ]

# Extraemos los numeros de intervalos, de turnos de empleados a tiempo completo, 
# y de turnos de empleados a tiempo medio
num_intervalos = len( horarios_tc )
num_turnos_tc = len( horarios_tc[0] )
num_turnos_tm = len( horarios_tm[0] )

# Construirmos un objeto que representa un programa lineal
prob = pulp.LpProblem( 'Problema_del_Supermercado', pulp.LpMinimize)

# Construimos una lista de variables de decision de empleados a tiempo completo
x = [ \
pulp.LpVariable( 'x_' + str(k).zfill(2), 0, None, pulp.LpInteger) for k in range(8,12) ]
# Construimos una lista de variables de decision de empleados a tiempo medio
y = [ \
pulp.LpVariable( 'y_' + str(k).zfill(2), 0, None, pulp.LpInteger) for k in range(8,17) ]

# Ingresamos las restricciones por los numeros de empleados requeridos
for k in range( 0, num_intervalos): 
    prob += pulp.lpSum( horarios_tc[k][m] * x[m] for m in range( 0, num_turnos_tc) ) \
    + pulp.lpSum( horarios_tm[k][n] * y[n] for n in range( 0, num_turnos_tm) ) \
    >= empleados_req[k][0], \
    'Intervalo_' + str(k+8).zfill(2) + 'h-' + str(k+9).zfill(2) + 'h'

# Ingresamos la restriccion por numero minimo de empleados a tiempo completo requeridos
prob += pulp.lpSum( x[m] for m in range( 0, num_turnos_tc) ) >= 6, 'Imagen_Corporativa'

# Ingresamos la funcion de costo
prob += 14.50 * 8 * pulp.lpSum( x[m] for m in range( 0, num_turnos_tc) ) \
+ 9.50 * 4 * pulp.lpSum( y[n] for n in range( 0, num_turnos_tm) )

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
