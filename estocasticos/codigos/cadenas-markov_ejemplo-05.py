"""
@author: Luis I. Reyes Castro

Problema 17.4A-8 del texto de Taha: Problema de la Agencia de Renta de Carros

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkov

# Lista de estados
S = [ 'Phoenix', 'Denver', 'Chicago', 'Atlanta' ]
# Matriz de transicion
P = np.array( [ [       0.7, 0.3 * 0.2, 0.3 * 0.6, 0.3 * 0.2 ],
                [       0.0,       0.7, 0.3 * 0.6, 0.3 * 0.4 ],
                [       0.0, 0.3 * 0.5,       0.7, 0.3 * 0.5 ],
                [ 0.3 * 0.1, 0.3 * 0.1, 0.3 * 0.8,       0.7 ] ] )

# Crea una nuevo objeto que representa una Cadena de Markov
cadena = CadenaDeMarkov( S, P)

# Propaga la distribucion inicial dos pasos
dist_inicial = { estado : 0.25 for estado in S }
pi_2         = cadena.propaga_distribucion( dist_inicial, 2)
# Calcula el numero esperado de carros en cada ciudad
num_carros = { estado : 400 * pi_2[estado] for estado in S }

# Computa la distribucion estacionaria
pi_estrella = cadena.distribucion_estacionaria()
num_carros  = { estado : 400 * pi_estrella[estado] for estado in S }

# Computa el tiempo esperado de retorno a cada estado
tiempo_retorno = cadena.tiempo_esperado_de_retorno()
# Computa el tiempo esperado de primer paso hacia Atlanta
tiempo_primera_visita = cadena.tiempo_esperado_de_primera_visita( 'Chicago')
