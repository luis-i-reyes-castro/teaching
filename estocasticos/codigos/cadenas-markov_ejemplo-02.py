"""
@author: Luis I. Reyes Castro

Problema de Manejo de Inventario de Dave

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkov

# Lista de estados
S = [ 0, 1, 2, 3 ]
# Matriz de transicion
P = np.array( [ [ 0.08, 0.18, 0.37, 0.37 ],
                [ 0.63, 0.37, 0.,   0.   ],
                [ 0.26, 0.37, 0.37, 0.   ],
                [ 0.08, 0.18, 0.37, 0.37 ] ] )

# Crea una nuevo objeto que representa una Cadena de Markov
cadena = CadenaDeMarkov( S, P)

# Computa la distribucion estacionaria
pi_estrella = cadena.distribucion_estacionaria()
