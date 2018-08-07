# Deberia imprimir resultados de manera mas amigable

from pulp import LpVariable, LpBinary
from pulp import LpProblem, LpMinimize
from pulp import lpSum
from Rutinas_ProgEntera import importar_excel
import pulp
archivo = 'Datos/Datos_Problema-09-A.xlsx'

df_filas    = importar_excel( archivo, 'Filas')
df_columnas = importar_excel( archivo, 'Columnas')
df_cm       = importar_excel( archivo, 'Centro-de-Masa')
df_ld       = importar_excel( archivo, 'Locaciones-Deshabilitadas')
df_cont     = importar_excel( archivo, 'Contenedores')

filas    = list( df_filas.index )
columnas = list( df_columnas.index )
dist_x   = df_filas.values
dist_y   = df_columnas.values

x_tilde = df_cm.loc['x']['Distancia (m)']
y_tilde = df_cm.loc['y']['Distancia (m)']

ld = df_ld.values

contenedores = list( df_cont.index )
pesos        = df_cont.values.flatten()
peso_total   = pesos.sum()

x      = {}
dict_x = {}
for i in filas :
    for j in columnas :
        for k in contenedores :
            nom = 'x_' + str(i) + '_' + str(j) + '_' + str(k).zfill(2)
            var = LpVariable( nom, 0, 1, LpBinary)
            x[(i,j,k)] = var
            dict_x[var.name] = (i,j,k)

x_barra = LpVariable( 'x_barra', 0, None)
y_barra = LpVariable( 'y_barra', 0, None)
x_mas   = LpVariable( 'x_mas', 0, None)
x_menos = LpVariable( 'x_menos', 0, None)
y_mas   = LpVariable( 'y_mas', 0, None)
y_menos = LpVariable( 'y_menos', 0, None)

prob = LpProblem( 'Problema_del_Loadmaster', LpMinimize)

prob += 0

for f in ld:
    i= f[0]
    j = f[1]
    prob += lpSum( x[(i,j,k)] for k in contenedores ) <= 0, 'Locacion Deshabilitada' +str (i) + '' + str(j)

for i in filas :
    for j in columnas :
        prob += lpSum( x[(i,j,k)] for k in contenedores ) <= 1, \
                'Maximo un contenedor en la locacion (' + str(i) + \
                ',' + str(j) + ')'

for k in contenedores :
    x_ij_k = []
    for i in filas :
        for j in columnas :
            x_ij_k.append( x[(i,j,k)] )
    prob += lpSum( x_ij for x_ij in x_ij_k ) == 1, \
            'Asignacion del contenedor ' + str(k)



terminos_x = []
terminos_y = []
for ( i, fila) in enumerate(filas) :
    for ( j, col) in enumerate(columnas) :
        for ( k, cont) in enumerate(contenedores) :
            terminos_x.append( dist_x[i] * pesos[k] * x[(fila,col,cont)] )
            terminos_y.append( dist_y[j] * pesos[k] * x[(fila,col,cont)] )


prob += x_barra == ( 1.0 / peso_total ) *  \
                   lpSum( termino for termino in terminos_x ), \
                   'Centro_de_masa_en_x'
prob += y_barra == ( 1.0 / peso_total ) *  \
                   lpSum( termino for termino in terminos_y ), \
                   'Centro_de_masa_en_y'

z_x = LpVariable ('x')
prob += x_barra-x_tilde <= z_x, 'x mas'
prob += x_tilde-x_barra <= z_x, 'x menos'

z_y = LpVariable ('y')
prob += y_barra-y_tilde <= z_y, 'y mas'
prob += y_tilde-y_barra <= z_y, 'y menos'

prob += z_x + z_y
print(prob)
prob.solve()

print (pulp.LpStatus[ prob.status])
print ('resultados')
# COMENTADO POR EL PROFESOR -------------------------
#for var in prob.variables():
#     print(var.name, '=', var.varValue)
# ---------------------------------------------------
print ('optimo', pulp.value (prob.objective))

for var in prob.variables():
    if var.varValue>0.0:
        print (var.name,'=', var.varValue)
