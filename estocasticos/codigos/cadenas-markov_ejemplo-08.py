"""
Implementacion de la Cadena de Markov del Problema 17.5-5 del texto de
Hillier & Lieberman (9ED).

@author: Luis I. Reyes Castro

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkovEnTiempoContinuo

# Lista de estados
S = [ 0, 1, 2, 3]
# Matriz de transicion
P = np.array( [ [  0., 15.,  0.,  0. ],
                [ 15.,  0., 10.,  0. ],
                [  0., 15.,  0.,  5. ],
                [  0.,  0., 15.,  0. ] ] )

# Construye una nuevo objeto que representa una Cadena de Markov
cadena = CadenaDeMarkovEnTiempoContinuo( S, P)
# Computa la distribucion estacionaria
pi_estrella = cadena.distribucion_estacionaria()
