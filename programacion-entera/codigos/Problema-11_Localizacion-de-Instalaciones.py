"""
Problema de Localizacion de Instalaciones
@author: Luis I. Reyes Castro
"""

import pulp
from Rutinas_ProgEntera import importar_excel, importar_matrices

# Declaramos las fuentes de datos y los importamos
archivo_datos      = 'Datos/Datos_Problema-11.xlsx'
archivo_distancias = 'Datos/Datos_Problema-11_Distancias.xlsx'
hoja_origenes = 'Origenes'
hoja_destinos = 'Destinos'
hoja_costos   = 'Costos'
hoja_demandas = 'Demandas'
hoja_otros    = 'Otros-parametros'
presupuesto   = 'Presupuesto 01'

df_origenes = importar_excel( archivo_datos, hoja_origenes)
df_destinos = importar_excel( archivo_datos, hoja_destinos)
df_costos   = importar_excel( archivo_datos, hoja_costos)
df_demandas = importar_excel( archivo_datos, hoja_demandas)
df_otros    = importar_excel( archivo_datos, hoja_otros)

origenes = list( df_origenes['Ciudad'] )
destinos = list( df_destinos['Ciudad'] )
costos   = list( df_costos['Costo (USD/m2)'] )
demandas = list( df_demandas['Demanda'] )

area_f  = df_otros.loc['Area Fija']['Valor']
area_re = df_otros.loc['Area por Estacionamiento']['Valor']
monto_B = df_otros.loc[presupuesto]['Valor']

dict_dt           = importar_matrices( archivo_distancias)
matriz_distancias = dict_dt['distancias']

# Declaramos el problema
prob = pulp.LpProblem( 'Localizacion-de-Instalaciones', pulp.LpMinimize)

# Declaramos las variables de decision
x = {}
for ( i, origen) in enumerate(origenes) :
    for ( j, destino) in enumerate(destinos) :
        nom      = 'x_' + str(i+1).zfill(2) + '_' + str(j+1).zfill(2)
        x[(i,j)] = pulp.LpVariable( nom, 0, None, pulp.LpInteger)

y = {}
for ( i, origen) in enumerate(origenes) :
    nom  = 'y_' + str(i+1).zfill(2)
    y[i] = pulp.LpVariable( nom, 0, 1, pulp.LpBinary)

# Declaramos las restricciones que exigen que solo se puede servir clientes
# desde instalaciones que han sido construidas (implementacion 2)
for ( i, origen) in enumerate(origenes) :
    for ( j, destino) in enumerate(destinos) :
        prob += x[(i,j)] <= demandas[j] * y[i], \
        'Capacidad para servir desde la instalacion ' + str(i+1).zfill(2) + \
        ' al cliente ' + str(j+1).zfill(2)

# Declaramos las restricciones que exigen que todo cliente sea servido
for ( j, destino) in enumerate(destinos) :
    sumatoria = pulp.lpSum( x[(i,j)] for (i,_) in enumerate(origenes) )
    prob += sumatoria == demandas[j], \
    'El cliente ' + str(j+1).zfill(2) + ' debe ser servido'

# Declaramos la restriccion de presupuesto
c_area_f  = []
c_area_re = []
for ( i, origen) in enumerate(origenes) :
    c_area_f.append( costos[i] * area_f * y[i] )
    for ( j, destino) in enumerate(destinos) :
        c_area_re.append( costos[i] * area_re * x[(i,j)] )

prob += pulp.lpSum(c_area_f) + pulp.lpSum(c_area_re) <= monto_B, \
        'Restriccion de presupuesto'

# Declaramos la funcion de costo
distancias_recorridas = []
for ( i, origen) in enumerate(origenes) :
    for ( j, destino) in enumerate(destinos) :
        distancias_recorridas.append( matriz_distancias[i,j] * x[(i,j)] )

prob += pulp.lpSum(distancias_recorridas), \
        'Distancia recorrida por las retroexcavadoras'

# Imprimimos y resolvemos el problema
print(prob)
prob.solve()

print( 'Estado (en ingles):', pulp.LpStatus[prob.status])
print( 'Costo_Optimo =', pulp.value(prob.objective) )
print( 'Valores optimos de las variables de decision no-triviales:')
for var in prob.variables() :
    if var.varValue > 0.0 :
        print( var.name, '=', var.varValue)

# Imprimimos las solucion de una manera amigable
print( 'DESGLOSE DE LA SOLUCION OPTIMA:' )
for ( i, origen) in enumerate(origenes) :
    if y[i].varValue > 0.0 :
        msg = '[+] Abrir locacion ' + str(i+1).zfill(2) + ' - ' + origenes[i]
        print(msg)
        for ( j, destino) in enumerate(destinos) :
            if x[(i,j)].varValue > 0.0 :
                msg = '\t[-] Servir al destino ' + str(j+1).zfill(2) + ' - ' \
                    + destinos[j] + ': ' + str( x[(i,j)].varValue ) + ' unidades'
                print(msg)
