"""
@author: Luis I. Reyes Castro

Problema de Donald Trump

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkov

# Lista de estados
S = [ 'Elecciones', 'Rusia', 'Pared', 'NAFTA', 'Twitter' ]
# Matriz de transicion
P = np.array( [ [ 0.5, 0,   0.25, 0.25, 0   ],
                [ 0,   0.6, 0,    0,    0.4 ],
                [ 0,   1,   0,    0,    0   ],
                [ 0.9, 0.1, 0,    0,    0   ],
                [ 0,   0.3, 0.3,  0,    0.4 ] ] )

# Crea una nuevo objeto que representa una Cadena de Markov
cadena = CadenaDeMarkov( S, P)
# Computa la distribucion estacionaria (i.e. en estado estable) de la cadena
pi_estrella = cadena.distribucion_estacionaria()
