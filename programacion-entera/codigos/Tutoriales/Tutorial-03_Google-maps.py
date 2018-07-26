"""
Tutorial sobre Uso del Modulo Google Maps para Obtener Distancias
@author: Luis I. Reyes Castro
"""

import googlemaps as gmaps
import numpy as np

origenes = [ 'Riocentro Ceibos, Calle 14 NO, Guayaquil',
             'Mall del Sol, Joaquin J Orrantia Gonzalez, Guayaquil',
             'CityMall, Av Benjamin Carrion Mora, Guayaquil' ]

destinos = [ 'Escuela Superior Politecnica del Litoral (ESPOL), ' +
             'Via Perimetral 5, Guayaquil',
             'Universidad de Guayaquil (UG), 1er Callejon 5 NO, Guayaquil',
             'Universidad Catolica de Santiago de Guayaquil, ' +
             'Av Pdte Carlos Julio Arosemena Tola, Guayaquil' ]

print( 'PROGRAMA PARA OBTENER DISTANCIAS Y TIEMPOS ENTRE DIRECCIONES' )
print( 'IMPORTACION DE DATOS DE DISTANCIAS Y TIEMPO EMPEZADA' )
print( 'Direcciones de Origen:' )
for origen in origenes :
    print( '\t -' + origen )
print( 'Direcciones de Destinacion:' )
for destino in destinos :
    print( '\t -' + destino )

print( 'Solicitando matriz de distancias al servidor de Google Maps...' )
cliente_gm = gmaps.Client( key = 'AIzaSyBIoDs5XQOEcAi9RxwBO5KL_rM_wSvAtF8')
dict_gm    = cliente_gm.distance_matrix( origenes, destinos, mode = 'driving')

print( 'Solicitud de matriz de distancia completada.' )
print( 'Estado de la solicitud: ' + dict_gm['status'] )

print( 'Compilando matrices de distancia y tiempo.' )
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

print( 'EJECUCION TERMINADA' )
