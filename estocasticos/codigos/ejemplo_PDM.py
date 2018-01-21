"""
@author: Luis I. Reyes Castro

Ejemplo Prototipo de H&L - 19.1

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkov

def CadenaDeMarkovInducida( accion_e1 = 1, accion_e2 = 1 ) :

    estados = [ 0, 1, 2, 3]

    # Alocamos una matriz vacia para las transiciones
    P = np.zeros( shape = (4,4) )
    # Alocamos un diccionario de costos
    costo = { 0 : 0.0, 1 : 0.0, 2 : 0.0, 3 : 0.0 }

    # Estado 0
    P[0,:] = [ 0, 7.0/8, 1.0/16, 1.0/16]

    # Estado 1
    if accion_e1 == 1 : # No hacer nada
        P[1,:] = [ 0, 3.0/4, 1.0/8, 1.0/8]
        costo[1] = 1000.0
    elif accion_e1 == 3 : # Reemplazo
        P[1,:] = [ 1, 0, 0, 0]
        costo[1] = 6000.0

    # Estado 2
    if accion_e2 == 1 : # No hacer nada
        P[2,:] = [ 0, 0, 1.0/2, 1.0/2]
        costo[2] = 3000.0
    elif accion_e2 == 2 : # Reparacion general
        P[2,:] = [ 0, 1, 0, 0]
        costo[2] = 4000.0
    elif accion_e2 == 3 : # Reemplazo
        P[2,:] = [ 1, 0, 0, 0]
        costo[2] = 6000.0

    # Estado 3
    P[3,:] = [ 1, 0, 0, 0]
    costo[3] = 6000.0

    return ( estados, P, costo)

# Evaluamos una politica en particular
accion_e1 = 3
accion_e2 = 3
( S, P, costo) = CadenaDeMarkovInducida( accion_e1, accion_e2)
cadena = CadenaDeMarkov( S, P)
pi_estrella = cadena.distribucion_estacionaria()

costo_politica = 0.0
for estado in S :
    costo_politica += pi_estrella[estado] * costo[estado]
