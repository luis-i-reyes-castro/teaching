"""
Implementacion de la Cadena de Markov del Ejemplo del Taller Mecanico
encontrado en la Seccion 16.8 del texto de Hillier & Lieberman (9ED).

@author: Luis I. Reyes Castro

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkovEnTiempoContinuo

# Lista de estados
S = [ 0, 1, 2]
# Matriz de transicion
P = np.array( [ [ 0., 2., 0. ],
                [ 2., 0., 1. ],
                [ 0., 2., 0. ] ] )

# Construye una nuevo objeto que representa una Cadena de Markov
cadena = CadenaDeMarkovEnTiempoContinuo( S, P)
# Computa la distribucion estacionaria
pi_estrella = cadena.distribucion_estacionaria()
