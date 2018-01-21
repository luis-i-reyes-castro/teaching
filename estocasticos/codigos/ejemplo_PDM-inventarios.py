"""
@author: Luis I. Reyes Castro

Hillier & Lieberman (H&L) - Problema 19.2-8

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkov

def CadenaDeMarkovInducida( accion_e0 = 0,
                            accion_e1 = 0,
                            accion_e2 = 0 ) :

    estados = [ 0, 1, 2]
    matriz_transicion = np.zeros( shape = (3,3) )
    recompensa = { 0 : 0.0, 1 : 0.0, 2 : 0.0 }

    # Estado 0
    if accion_e0 == 0 :
        matriz_transicion[0,:] = [ 1.0, 0.0, 0.0]
        recompensa[0] = 0
    elif accion_e0 == 1 :
        matriz_transicion[0,:] = [ 2.0/3, 1.0/3, 0.0]
        recompensa[0] = 0
    elif accion_e0 == 2 :
        matriz_transicion[0,:] = [ 1.0/3, 1.0/3, 1.0/3]
        recompensa[0] = 0

    # Estado 1
    if accion_e1 == 0 :
        matriz_transicion[1,:] = [ 2.0/3, 1.0/3, 0.0]
        recompensa[1] = 0
    elif accion_e1 == 1 :
        matriz_transicion[1,:] = [ 1.0/3, 1.0/3, 1.0/3]
        recompensa[1] = 0

    # Estado 2
    matriz_transicion[2,:] = [ 1.0/3, 1.0/3, 1.0/3]
    recompensa[2] = 27.0

    return ( estados, matriz_transicion, recompensa)

# Evaluamos una politica en particular
( S, P, recompensa) = CadenaDeMarkovInducida( 'R', 'R', 'L')
cadena = CadenaDeMarkov( S, P)
pi_estrella = cadena.distribucion_estacionaria()

recompensa_politica = 0.0
for estado in S :
    recompensa_politica += pi_estrella[estado] * recompensa[estado]

print( 'Recompensa de la politica:', str(recompensa_politica))
