"""
@author: Luis I. Reyes Castro

Problema del Robot Vigilante

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
# Genera muestras de 1000 pasos empezando desde Loc-1
( X_t, freq) = cadena.muestrea( inicio = 'Loc-1', num_pasos = 1000)

# Define la distribucion inicial como Loc-1 de manera deterministica
# (i.e., el estado inicial es Loc-1) y la propaga por 100 pasos
pi_0 = { 'Loc-1' : 1.0 }
pi_t = cadena.propaga_distribucion( distribucion_inicial = pi_0, num_pasos = 100)

# Computa la distribucion estacionaria (i.e. en estado estable) de la cadena
pi_estrella = cadena.distribucion_estacionaria()
