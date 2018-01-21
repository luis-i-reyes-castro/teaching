"""
@author: Luis I. Reyes Castro

Hillier & Lieberman (H&L) - Problema 19.2-2

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkov

def CadenaDeMarkovInducida( accion_e0 = 'L',
                            accion_e1 = 'L',
                            accion_e2 = 'L' ) :

    estados = [ 0, 1, 2]
    matriz_transicion = np.zeros( shape = (3,3) )
    recompensa = { 0 : 0.0, 1 : 0.0, 2 : 0.0 }

    # Estado 0
    matriz_transicion[0,:] = [ 0.5, 0.5, 0]
    if accion_e0 == 'L' :
        recompensa[0] = -3.0
    elif accion_e0 == 'R' :
        recompensa[0] = -9.0

    # Estado 1
    if accion_e1 == 'L' :
        matriz_transicion[1,:] = [ 0.3, 0.5, 0.2]
        recompensa[1] = 27.0
    elif accion_e1 == 'R' :
        matriz_transicion[1,:] = [ 0.4, 0.5, 0.1]
        recompensa[1] = 31.0

    # Estado 2
    if accion_e2 == 'L' :
        matriz_transicion[2,:] = [ 0, 0.6, 0.4]
        recompensa[2] = 27.0
    elif accion_e2 == 'R' :
        matriz_transicion[2,:] = [ 0, 0.8, 0.2]
        recompensa[2] = 31.0

    return ( estados, matriz_transicion, recompensa)

# Evaluamos una politica en particular
( S, P, recompensa) = CadenaDeMarkovInducida( 'R', 'R', 'L')
cadena = CadenaDeMarkov( S, P)
pi_estrella = cadena.distribucion_estacionaria()

recompensa_politica = 0.0
for estado in S :
    recompensa_politica += pi_estrella[estado] * recompensa[estado]

print( 'Recompensa de la politica:', str(recompensa_politica))
