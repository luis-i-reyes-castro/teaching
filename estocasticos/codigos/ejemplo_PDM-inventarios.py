"""
Implementacion del Proceso de Decision Markoviano (PDM) del
Problema 19.2-8 del texto de Hillier & Lieberman (9ED)

@author: Luis I. Reyes Castro

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkov

# Declaramos una funcion que toma como argumento una politica factible y
# retorna la Cadena de Markov inducida por la politica junto con la funcion
# de costo promedio por estado
def CadenaDeMarkovInducida( accion_e0 = 0,
                            accion_e1 = 0 ) :

    # Declaramos los estados y matriz de transicion
    S = [ 0, 1, 2]
    P = np.zeros( shape = (3,3) )
    # Declaramos el diccionario de costo promedio por estado
    C = { estado : 0.0 for estado in S }

    # Estado 0
    if accion_e0 == 0 :
        P[0,:] = [ 1.0, 0.0, 0.0]
        C[0]   = 13.33
    elif accion_e0 == 1 :
        P[0,:] = [ 2.0/3, 1.0/3, 0.0]
        C[0]   = 19.0
    elif accion_e0 == 2 :
        P[0,:] = [ 1.0/3, 1.0/3, 1.0/3]
        C[0]   = 24.0

    # Estado 1
    if accion_e1 == 0 :
        P[1,:] = [ 2.0/3, 1.0/3, 0.0]
        C[1]   = 4.0
    elif accion_e1 == 1 :
        P[1,:] = [ 1.0/3, 1.0/3, 1.0/3]
        C[1]   = 19.0

    # Estado 2
    P[2,:] = [ 1.0/3, 1.0/3, 1.0/3]
    C[2]   = 4.0

    return ( S, P, C)

# Escogemos una politica
accion_e0 = 2
accion_e1 = 0
# Construimos la Cadena de Markov inducida por la politica
( S, P, C) = CadenaDeMarkovInducida( accion_e0, accion_e1)
cadena     = CadenaDeMarkov( S, P)

# Calculamos el costo promedio que incurre la politica escogida
pi_estrella    = cadena.distribucion_estacionaria()
costo_politica = 0.0
for estado in S :
    costo_politica += pi_estrella[estado] * C[estado]

# Imprimimos la politica y su costo promedio
print( 'POLITICA' )
print( 'Estado: 0 -> Accion: ' + str(accion_e0) )
print( 'Estado: 1 -> Accion: ' + str(accion_e1) )
print( 'Estado: 2 -> Accion: 0' )
print( 'Costo promedio por periodo: ' + str(costo_politica) )
