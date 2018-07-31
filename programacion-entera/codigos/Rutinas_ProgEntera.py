"""
Rutinas Utiles para Programacion Entera
@author: Luis I. Reyes Castro
"""

import googlemaps as gmaps
import numpy as np
import pandas as pd

def importar_excel( archivo, hoja_de_calculo) :

    manija = open( archivo, 'rb')
    df = pd.read_excel( manija, hoja_de_calculo, index_col = 0)
    manija.close()

    return df

def descargar_matrices( archivo_datos, archivo_matriz) :

    print( 'EJECUTANDO IMPORTADOR DE MATRICES DE DISTANCIAS Y TIEMPOS' )
    print( 'Archivo de datos: ' + str(archivo_datos) )

    df_origenes = importar_excel( archivo_datos, 'Origenes')
    df_destinos = importar_excel( archivo_datos, 'Destinos')

    localidades = list( df_origenes['Localidad'] )
    direcciones = list( df_origenes['Direccion'] )
    ciudades    = list( df_origenes['Ciudad'] )

    origenes = []
    for (i,_) in enumerate(localidades) :
        origen = localidades[i] + ', ' + direcciones[i] + ', ' + ciudades[i]
        origenes.append( origen)

    localidades = list( df_destinos['Localidad'] )
    direcciones = list( df_destinos['Direccion'] )
    ciudades    = list( df_destinos['Ciudad'] )

    destinos = []
    for (i,_) in enumerate(localidades) :
        destino = localidades[i] + ', ' + direcciones[i] + ', ' + ciudades[i]
        destinos.append( destino)

    print( 'Direcciones de Origen:' )
    for origen in origenes :
        print( '\t -' + origen )
    print( 'Direcciones de Destinacion:' )
    for destino in destinos :
        print( '\t -' + destino )

    print( 'Solicitando matriz de distancias al servidor de Google Maps...' )
    cliente_gm = gmaps.Client( key = 'AIzaSyBIoDs5XQOEcAi9RxwBO5KL_rM_wSvAtF8')
    dict_gm    = cliente_gm.distance_matrix( origenes, destinos,
                                             mode = 'driving' )

    print( 'Solicitud de matriz de distancia completada.' )
    print( 'Estado de la solicitud: ' + dict_gm['status'] )

    print( 'Compilando matrices de distancia y tiempo...' )
    m = len(origenes)
    n = len(destinos)
    matriz_D = np.zeros( shape = (m,n) )
    matriz_T = np.zeros( shape = (m,n) )
    for i in range(m) :
        for j in range(n) :
            matriz_D[i,j] = dict_gm['rows'][i]['elements'][j]['distance']['value']
            matriz_T[i,j] = dict_gm['rows'][i]['elements'][j]['duration']['value']

    matriz_D /= 1000.0
    matriz_T /= 60.0

    indice_1 = [ i+1 for (i,_) in enumerate(origenes) ]
    indice_2 = [ j+1 for (j,_) in enumerate(destinos) ]

    df_1 = pd.DataFrame( index = indice_1, columns = ['Origen'] )
    df_2 = pd.DataFrame( index = indice_2, columns = ['Destino'] )
    df_D = pd.DataFrame( index = indice_1, columns = indice_2)
    df_T = pd.DataFrame( index = indice_1, columns = indice_2)

    df_1['Origen']  = origenes
    df_2['Destino'] = destinos
    df_D[indice_2]  = matriz_D
    df_T[indice_2]  = matriz_T

    print( 'Guardando matrices en archivo: ' + str(archivo_matriz) )
    writer = pd.ExcelWriter( archivo_matriz)
    df_1.to_excel( writer, sheet_name = 'Origenes')
    df_2.to_excel( writer, sheet_name = 'Destinos')
    df_D.to_excel( writer, sheet_name = 'Distancias (km)')
    df_T.to_excel( writer, sheet_name = 'Tiempos (min)')
    writer.close()

    print( 'EJECUCION TERMINADA' )

    return

def importar_matrices( archivo) :

    df_origenes = importar_excel( archivo, 'Origenes')
    df_destinos = importar_excel( archivo, 'Destinos')
    df_D        = importar_excel( archivo, 'Distancias (km)')
    df_T        = importar_excel( archivo, 'Tiempos (min)')

    datos = {}
    datos['origenes']   = list( df_origenes['Origen'] )
    datos['destinos']   = list( df_destinos['Destino'] )
    datos['distancias'] = df_D.values.astype( np.float)
    datos['tiempos']    = df_T.values.astype( np.float)

    return datos
