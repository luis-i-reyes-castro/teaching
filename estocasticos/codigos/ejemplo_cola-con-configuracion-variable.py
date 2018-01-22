"""
Implementacion del Proceso de Decision Markoviano (PDM) del
Problema 19.2-2 del texto de Hillier & Lieberman (9ED)

@author: Luis I. Reyes Castro

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkov

# Declaramos una funcion que toma como argumento una politica factible y
# retorna la Cadena de Markov inducida por la politica junto con la funcion
# de recompensa promedio por estado
def CadenaDeMarkovInducida( accion_e0 = 'Configuracion-Lenta',
                            accion_e1 = 'Configuracion-Lenta',
                            accion_e2 = 'Configuracion-Lenta' ) :

    # Declaramos los estados y matriz de transicion
    S = [ 0, 1, 2]
    P = np.zeros( shape = (3,3) )
    # Declaramos el diccionario de recompensa promedio por estado
    R = { estado : 0.0 for estado in S }

    # Estado 0
    P[0,:] = [ 0.5, 0.5, 0]
    if accion_e0 == 'Configuracion-Lenta' :
        R[0] = -3.0
    elif accion_e0 == 'Configuracion-Rapida' :
        R[0] = -9.0

    # Estado 1
    if accion_e1 == 'Configuracion-Lenta' :
        P[1,:] = [ 0.3, 0.5, 0.2]
        R[1]   = 27.0
    elif accion_e1 == 'Configuracion-Rapida' :
        P[1,:] = [ 0.4, 0.5, 0.1]
        R[1]   = 31.0

    # Estado 2
    if accion_e2 == 'Configuracion-Lenta' :
        P[2,:] = [ 0, 0.6, 0.4]
        R[2]   = 27.0
    elif accion_e2 == 'Configuracion-Rapida' :
        P[2,:] = [ 0, 0.8, 0.2]
        R[2]   = 31.0

    return ( S, P, R)

# Escogemos una politica
accion_e0 = 'Configuracion-Lenta'
accion_e1 = 'Configuracion-Lenta'
accion_e2 = 'Configuracion-Rapida'
# Construimos la Cadena de Markov inducida por la politica
( S, P, R) = CadenaDeMarkovInducida( accion_e0, accion_e1, accion_e2)
cadena     = CadenaDeMarkov( S, P)

# Calculamos la recompensa promedio que obtiene la politica escogida
pi_estrella         = cadena.distribucion_estacionaria()
recompensa_politica = 0.0
for estado in S :
    recompensa_politica += pi_estrella[estado] * R[estado]

# Imprimimos la politica y su recompensa promedio
print( 'POLITICA' )
print( 'Estado: 0 -> Accion: ' + accion_e0 )
print( 'Estado: 1 -> Accion: ' + accion_e1 )
print( 'Estado: 2 -> Accion: ' + accion_e2 )
print( 'Recompensa promedio por periodo: ' + str(recompensa_politica) )
