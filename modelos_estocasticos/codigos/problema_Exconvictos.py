"""
@author: Luis I. Reyes Castro

Problema de Donald Trump

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkov

# Lista de estados
S = [ 'Libertad', 'Juicio', 'Libertad-Condicional', 'Carcel' ]
# Matriz de transicion
P = np.array( [ [ 0.5, 0.5, 0,   0   ],
                [ 0,   0,   0.4, 0.6 ],
                [ 0.1, 0.1, 0.3, 0.5 ],
                [ 0.1, 0,   0,   0.9 ] ] )

# Crea una nuevo objeto que representa una Cadena de Markov
cadena = CadenaDeMarkov( S, P)
# Computa la distribucion estacionaria (i.e. en estado estable) de la cadena
pi_estrella = cadena.distribucion_estacionaria()
# Computa el tiempo esperado de retorno para cada estado
tiempo_retorno = cadena.tiempo_esperado_de_retorno()
