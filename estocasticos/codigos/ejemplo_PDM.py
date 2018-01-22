"""
Implementacion del Proceso de Decision Markoviano (PDM) del
Problema prototipo de la Seccion 19.1 del texto de Hillier & Lieberman (9ED)

@author: Luis I. Reyes Castro

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkov

# Declaramos una funcion que toma como argumento una politica factible y
# retorna la Cadena de Markov inducida por la politica junto con la funcion
# de costo promedio por estado
def CadenaDeMarkovInducida( accion_e1 = 'Nada',
                            accion_e2 = 'Nada' ) :

    # Declaramos los estados y matriz de transicion
    S = [ 0, 1, 2, 3]
    P = np.zeros( shape = (4,4) )
    # Declaramos el diccionario de costo promedio por estado
    costo = { estado : 0.0 for estado in S }

    # Estado 0
    P[0,:] = [ 0.0, 7.0/8, 1.0/16, 1.0/16]

    # Estado 1
    if accion_e1 == 'Nada' :
        P[1,:] = [ 0.0, 3.0/4, 1.0/8, 1.0/8]
        costo[1] = 1000.0
    elif accion_e1 == 'Remplazo':
        P[1,:] = [ 1.0, 0.0, 0.0, 0.0]
        costo[1] = 6000.0

    # Estado 2
    if accion_e2 == 'Nada' :
        P[2,:] = [ 0.0, 0.0, 1.0/2, 1.0/2]
        costo[2] = 3000.0
    elif accion_e2 == 'Reparacion-general' :
        P[2,:] = [ 0.0, 1.0, 0.0, 0.0]
        costo[2] = 4000.0
    elif accion_e2 == 'Remplazo' :
        P[2,:] = [ 1.0, 0.0, 0.0, 0.0]
        costo[2] = 6000.0

    # Estado 3
    P[3,:] = [ 1.0, 0.0, 0.0, 0.0]
    costo[3] = 6000.0

    return ( S, P, costo)

# Escogemos una politica
accion_e1 = 'Nada'
accion_e2 = 'Reparacion-general'
# Construimos la Cadena de Markov inducida por la politica
( S, P, costo) = CadenaDeMarkovInducida( accion_e1, accion_e2)
cadena         = CadenaDeMarkov( S, P)

# Calculamos el costo promedio que incurre la politica escogida
pi_estrella    = cadena.distribucion_estacionaria()
costo_politica = 0.0
for estado in S :
    costo_politica += pi_estrella[estado] * costo[estado]

# Imprimimos la politica y su costo promedio
print( 'POLITICA' )
print( 'Estado: 0 -> Accion: Nada' )
print( 'Estado: 1 -> Accion: ' + accion_e1 )
print( 'Estado: 2 -> Accion: ' + accion_e2 )
print( 'Estado: 3 -> Accion: Remplazo' )
print( 'Costo promedio por periodo: ' + str(costo_politica) )
