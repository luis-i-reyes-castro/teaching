"""
@author: Luis I. Reyes Castro

Problema del Robot Vigilante:
===================================
===================================
||         ||         ::         ||
||  Loc-1  ||  Loc-2  ::  Loc-3  ||
||         ||         ::         ||
||  :::::  ::  :::::  ::  :::::  ||
||         ::         ::         ||
||  Loc-4  ::  Loc-5  ::  Loc-6  ||
||         ::         ::         ||
===================================
===================================
"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkov

# Lista de estados
S = [ 'Loc-1', 'Loc-2', 'Loc-3', 'Loc-4', 'Loc-5', 'Loc-6']
# Matriz de transicion
P = np.array( [ [ 1/2,   0,   0, 1/2,   0,   0 ],
                [   0, 1/3, 1/3,   0, 1/3,   0 ],
                [   0, 1/3, 1/3,   0,   0, 1/3 ],
                [ 1/3,   0,   0, 1/3, 1/3,   0 ],
                [   0, 1/4,   0, 1/4, 1/4, 1/4 ],
                [   0,   0, 1/3,   0, 1/3, 1/3 ] ] )

# Crea una nuevo objeto que representa una Cadena de Markov
cadena = CadenaDeMarkov( S, P)
# Genera muestras de 60 pasos empezando desde Loc-1
cadena.muestrea_secuencia( inicio = 'Loc-1', num_pasos = 60)

# Define la distribucion inicial
pi_0 = ( 1/2, 0, 0, 1/2, 0, 0)
# Propagala por 60 pasos
dists = cadena.propaga_distribucion( distribucion = pi_0, num_pasos = 600)
