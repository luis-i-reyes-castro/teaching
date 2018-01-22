"""
Ejemplo del Robot Vigilante

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

@author: Luis I. Reyes Castro

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

# Genera muestras de 100 pasos empezando desde Loc-1
( X_t, freq) = cadena.muestrea( inicio = 'Loc-1', num_pasos = 100)
# Propaga la distribucion de la locacion del robot para el caso cuando
# el robot inicia desde Loc-1
pi_0 = { 'Loc-1' : 1.0 }
pi_t = cadena.propaga_distribucion( inicio = pi_0, num_pasos = 10)
# Computa la distribucion estacionaria (i.e. en estado estable) de la cadena
pi_estrella = cadena.distribucion_estacionaria()
