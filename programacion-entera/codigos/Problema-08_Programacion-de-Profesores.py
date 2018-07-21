"""
Problema de Programacion de Profesores
@author: Luis I. Reyes Castro
"""

import os
import numpy as np
import pandas as pd
import pulp

print( '\n' + 'SOFTWARE PARA PROGRAMACION DE PROFESORES' )
print( '\n' + 'EJECUCION INICIADA'  )

print( 'LEYENDO ARCHIVO DE REQUERIMIENTOS...' )
archivo = 'Datos/Datos_Problema-08.xlsx'
manija = open( archivo, 'rb')
df_req = pd.read_excel( manija, 'Requerimientos', index_col = 0)
manija.close()

materias       = list( df_req['Materia'] )
requerimientos = df_req['Profesores Requeridos'].values.flatten()

print( 'LEYENDO ARCHIVOS DE POSTULACIONES...' )
nom_directorio = 'Datos/Datos_Problema-08_Propuestas/'
nom_archivos   = os.listdir( nom_directorio)
dict_dfs       = {}
for nom_archivo in nom_archivos :
    archivo  = nom_directorio + nom_archivo
    profesor = nom_archivo[11:-5]
    print( 'Leyendo archivo:' + archivo )
    manija = open( archivo, 'rb')
    dict_dfs[profesor] = pd.read_excel( manija, 'Propuestas', index_col = 0)
    manija.close()

profesores = list( dict_dfs.keys() )
profesores.sort()
columnas   = [ 'Tiempo Medio', 'Tiempo Parcial', 'Tiempo Completo' ]
matrices_D = []
vectores_c = []
vectores_p = []
for profe in profesores :
    df = dict_dfs[profe]
    valores = df[columnas].values
    matriz_D_prof = valores[:-1,:]
    vector_c_prof = valores[-1,:]
    vector_p_prof = matriz_D_prof.sum( axis = 1) > 0.0
    matrices_D.append( matriz_D_prof)
    vectores_c.append( vector_c_prof)
    vectores_p.append( vector_p_prof)

matriz_D = np.concatenate( matrices_D, axis = 1)
vector_c = np.concatenate( vectores_c, axis = 0)
matriz_P = np.stack( vectores_p, axis = -1)
vector_p = matriz_P.sum( axis = -1)

print( '\n' + 'RESUMEN DE POSTULACIONES:' )
for ( k, materia) in enumerate(materias) :
    postulantes = vector_p[k]
    print( 'La materia ' + materia +
           ' tiene ' + str(postulantes) + ' postulantes.' )
    if postulantes < requerimientos[k] :
        print( '\t' + 'ADVERTENCIA: La materia ' + materia +
                      ' tiene menos postulantes que vacantes. ' +
                      'Por lo tanto se relajara el requerimiento de ' +
                      'esta materia a ' + str(postulantes) + ' vacantes.' )

prob = pulp.LpProblem( 'Progamacion_de_Profesores', pulp.LpMinimize)
x    = []
for profe in profesores :
    x_prof_tm = pulp.LpVariable( 'x_' + profe + '_TM', 0, 1, pulp.LpBinary)
    x_prof_tp = pulp.LpVariable( 'x_' + profe + '_TP', 0, 1, pulp.LpBinary)
    x_prof_tc = pulp.LpVariable( 'x_' + profe + '_TC', 0, 1, pulp.LpBinary)
    x_prof_tm.profe = profe
    x_prof_tp.profe = profe
    x_prof_tc.profe = profe
    prob += x_prof_tm + x_prof_tp + x_prof_tc <= 1, \
         'Restriccion para el candidato ' + profe
    x    += [ x_prof_tm, x_prof_tp, x_prof_tc ]

for ( k, materia) in enumerate(materias) :
    prob += pulp.lpDot( matriz_D[k,:], x) >= requerimientos[k], \
            'Requerimiento de la materia ' + materia

prob += pulp.lpDot( vector_c, x), 'Costo_por_Salarios'

print(prob)
prob.solve()

for var in prob.variables() :
    if var.varValue > 0.0 :
        print( var.name, '=', var.varValue)

#profesores_tm = []
#profesores_tp = []
#profesores_tc = []
#for var in prob.variables() :
#    if var.varValue > 0.0 :
#        if var.name[-2:] == 'TM' :
#            profesores_tm.append( var.profe)
#        elif var.name[-2:] == 'TP' :
#            profesores_tp.append( var.profe)
#        elif var.name[-2:] == 'TC' :
#            profesores_tc.append( var.profe)
#
#print( '\n' + 'PLAN DE CONTRATACION OPTIMO:' )
#print( '[+] Costo:' + str(pulp.value(prob.objective)) )
#print( '[+] Profesores a Tiempo Medio:' )
#for profe in profesores_tm :
#    print( '\t' + profe )
#print( '[+] Profesores a Tiempo Parcial:' )
#for profe in profesores_tp :
#    print( '\t' + profe )
#print( '[+] Profesores a Tiempo Completo:' )
#for profe in profesores_tc :
#    print( '\t' + profe )
#
#print( '\n' + 'EJECUCION COMPLETADA' + '\n' )
