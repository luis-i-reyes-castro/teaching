"""
Problema de Programacion de Profesores
@author: Luis I. Reyes Castro
"""

import os
import numpy as np
import pandas as pd
import pulp
from Rutinas_ProgEntera import importar_excel

archivo_requerimientos = 'Datos/Datos_Problema-08.xlsx'
hoja_requerimientos    = 'Requerimientos'
columna_requerimientos = 'Profesores Requeridos'
directorio_propuestas  = 'Datos/Datos_Problema-08_Propuestas/'
hoja_propuestas        = 'Propuestas'
columnas_propuestas    = [ 'Tiempo Medio', 'Tiempo Parcial', 'Tiempo Completo' ]
archivo_solucion       = 'Soluciones/Solucion_Problema-08.xlsx'

imprimir_prog_entero   = False
imprimir_plan_optimo   = True

print( '\n' + 'SOFTWARE PARA PROGRAMACION DE PROFESORES' )
print( '\n' + 'EJECUCION INICIADA'  )
print( 'LEYENDO ARCHIVO DE REQUERIMIENTOS...' )

df_req         = importar_excel( archivo_requerimientos, hoja_requerimientos)
materias       = list( df_req['Materia'] )
requerimientos = df_req[columna_requerimientos].values.flatten()

print( 'LEYENDO ARCHIVOS DE POSTULACIONES...' )
nom_archivos   = os.listdir( directorio_propuestas)
dict_dfs       = {}
for nom_archivo in nom_archivos :
    archivo  = directorio_propuestas + nom_archivo
    profesor = nom_archivo[11:-5]
    print( 'Leyendo archivo:' + archivo )
    dict_dfs[profesor] = importar_excel( archivo, hoja_propuestas)

profesores = list( dict_dfs.keys() )
profesores.sort()

matrices_D  = []
vectores_c  = []
vectores_p  = []
materias_tm = {}
materias_tp = {}
materias_tc = {}

for profe in profesores :

    df      = dict_dfs[profe]
    valores = df[columnas_propuestas].values

    matriz_D_prof = valores[:-1,:]
    vector_c_prof = valores[-1,:]
    vector_c_prof[0] = 2.0 * vector_c_prof[0]
    vector_c_prof[1] = 3.0 * vector_c_prof[1]
    vector_c_prof[2] = 4.0 * vector_c_prof[2]
    vector_p_prof = matriz_D_prof.sum( axis = 1) > 0.0
    matrices_D.append( matriz_D_prof)
    vectores_c.append( vector_c_prof)
    vectores_p.append( vector_p_prof)

    indices_tm = list( matriz_D_prof[:,0].nonzero()[0] )
    indices_tp = list( matriz_D_prof[:,1].nonzero()[0] )
    indices_tc = list( matriz_D_prof[:,2].nonzero()[0] )
    materias_tm[profe] = [ materias[ indices_tm[0] ], \
                           materias[ indices_tm[1] ] ]
    materias_tp[profe] = [ materias[ indices_tp[0] ], \
                           materias[ indices_tp[1] ],
                           materias[ indices_tp[2] ] ]
    materias_tc[profe] = [ materias[ indices_tc[0] ], \
                           materias[ indices_tc[1] ],
                           materias[ indices_tc[2] ],
                           materias[ indices_tc[3] ] ]

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

x             = []
dict_profe    = {}
dict_tiempo   = {}
dict_materias = {}

for profe in profesores :

    x_prof_tm = pulp.LpVariable( 'x_' + profe + '_TM', 0, 1, pulp.LpBinary)
    x_prof_tp = pulp.LpVariable( 'x_' + profe + '_TP', 0, 1, pulp.LpBinary)
    x_prof_tc = pulp.LpVariable( 'x_' + profe + '_TC', 0, 1, pulp.LpBinary)

    # RESTRICCION: Cada candidato puede ser contratado a un solo tiempo
    prob += x_prof_tm + x_prof_tp + x_prof_tc <= 1, \
         'Restriccion para el candidato ' + profe

    dict_profe[x_prof_tm.name]    = profe
    dict_profe[x_prof_tp.name]    = profe
    dict_profe[x_prof_tc.name]    = profe
    dict_tiempo[x_prof_tm.name]   = 'TM'
    dict_tiempo[x_prof_tp.name]   = 'TP'
    dict_tiempo[x_prof_tc.name]   = 'TC'
    dict_materias[x_prof_tm.name] = materias_tm[profe]
    dict_materias[x_prof_tp.name] = materias_tp[profe]
    dict_materias[x_prof_tc.name] = materias_tc[profe]

    x += [ x_prof_tm, x_prof_tp, x_prof_tc ]

# RESTRICCION: Satisfacer los requerimientos de las materias
for ( k, materia) in enumerate(materias) :
    # Sumatoria con lpDot
    prob += pulp.lpDot( matriz_D[k,:], x) >= requerimientos[k], \
            'Requerimiento de la materia ' + materia
    # Sumatoria equivalente con lpSum
    # prob += pulp.lpSum( matriz_D[k,i] * x[i] for (i,_) in enumerate(x) ) \
    #         >= requerimientos[k], 'Requerimiento de la materia ' + materia

# FUNCION DE COSTO: Costo por Salarios
# Sumatoria con lpDot
prob += pulp.lpDot( vector_c, x), 'Costo_por_Salarios'
# Sumatoria equivalente con lpSum
# prob += pulp.lpSum( vector_c[i] * x[i] for (i,_) in enumerate(x) ), 'Costo_por_Salarios'

if imprimir_prog_entero :
    print(prob)

print( '\n' + 'RESOLVIENDO PROGRAMA ENTERO...' )
prob.solve()

if pulp.LpStatus[prob.status] == 'Optimal' :

    print( 'Resultado: Solucion Optima Encontrada' )

    if imprimir_prog_entero :
        print( 'Estado (en ingles):', pulp.LpStatus[prob.status])
        print( 'Costo_Optimo =', pulp.value(prob.objective) )
        for var in prob.variables() :
            if var.varValue > 0.0 :
                print( var.name, '=', var.varValue)

    if imprimir_plan_optimo :

        profesores_tm = []
        profesores_tp = []
        profesores_tc = []
        asignacion_materias = { materia : [] for materia in materias }

        for ( i, x_i) in enumerate(x) :
            if x_i.varValue > 0.0 :
                profesor_x_i = dict_profe[x_i.name]
                tiempo_x_i   = dict_tiempo[x_i.name]
                materias_x_i = dict_materias[x_i.name]
                if tiempo_x_i == 'TM' :
                    profesores_tm.append( profesor_x_i)
                if tiempo_x_i == 'TP' :
                    profesores_tp.append( profesor_x_i)
                if tiempo_x_i == 'TC' :
                    profesores_tc.append( profesor_x_i)
                for materia_x_i in materias_x_i :
                    asignacion_materias[materia_x_i].append( profesor_x_i)

        print( '\n' + 'PLAN DE CONTRATACION OPTIMO:' )
        print( '[+] Costo:' + str(pulp.value(prob.objective)) )
        print( '[+] Profesores a Tiempo Medio:' )
        for profe in profesores_tm :
            print( '\t' + profe )
        print( '[+] Profesores a Tiempo Parcial:' )
        for profe in profesores_tp :
            print( '\t' + profe )
        print( '[+] Profesores a Tiempo Completo:' )
        for profe in profesores_tc :
            print( '\t' + profe )

        print( '\n' + 'ASIGNACION DE MATERIAS:' )
        lista_asignados = []

        for materia in materias :

            profesores_materia = asignacion_materias[materia]
            print( '[+] ' + materia + ' :' )
            for profe in profesores_materia :
                print( '\t - ' + profe )

            if len(profesores_materia) == 0 :
                lista_asignados.append( 'N/A' )
            elif len(profesores_materia) == 1 :
                lista_asignados.append( profesores_materia[0] )
            else :
                nombres = ''
                for profe in profesores_materia[:-1] :
                    nombres += profe + ', '
                nombres += profesores_materia[-1]
                lista_asignados.append( nombres )

        index_df_tm = [ i+1 for (i,_) in enumerate(profesores_tm) ]
        index_df_tp = [ i+1 for (i,_) in enumerate(profesores_tp) ]
        index_df_tc = [ i+1 for (i,_) in enumerate(profesores_tc) ]
        index_df_as = [ i+1 for (i,_) in enumerate(materias) ]

        df_tm = pd.DataFrame( index = index_df_tm, columns = [ 'Profesores' ])
        df_tp = pd.DataFrame( index = index_df_tp, columns = [ 'Profesores' ])
        df_tc = pd.DataFrame( index = index_df_tc, columns = [ 'Profesores' ])
        df_as = pd.DataFrame( index = index_df_as,
                              columns = [ 'Materias', 'Profesores' ] )

        df_tm['Profesores'] = profesores_tm
        df_tp['Profesores'] = profesores_tp
        df_tc['Profesores'] = profesores_tc
        df_as['Materias']   = materias
        df_as['Profesores'] = lista_asignados

        print( '\n' + 'GUARDANDO PLAN OPTIMO EN ARCHIVO: ' + archivo_solucion )
        writer = pd.ExcelWriter(archivo_solucion)
        df_tm.to_excel( writer, sheet_name = 'Tiempo Medio')
        df_tp.to_excel( writer, sheet_name = 'Tiempo Parcial')
        df_tc.to_excel( writer, sheet_name = 'Tiempo Completo')
        df_as.to_excel( writer, sheet_name = 'Asignacion de Materias')
        writer.close()

else :

    print( 'Resultado: Problema infactible!' )

print( '\n' + 'EJECUCION COMPLETADA' + '\n' )
