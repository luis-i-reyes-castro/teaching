"""
Implementacion de la Cadena de Markov del Ejemplo del Vendedor que Recorre
Guayaquil, Quito y Cuenca, Recolectando Recompensas a una Tasa Descontada.

@author: Luis I. Reyes Castro

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkov

# Lista de estados
S = [ 'GYE', 'UIO', 'CUE' ]
# Matriz de transicion
P = np.array( [ [ 0.4, 0.3, 0.3 ],
                [ 0.7, 0.0, 0.3 ],
                [ 0.0, 0.5, 0.5 ] ] )

# Construimos nuevo objeto que representa una Cadena de Markov
cadena = CadenaDeMarkov( S, P)

# Declaramos la funcion de recompensa y el factor de descuento
recompensa = { 'GYE' : 20.0, 'UIO' : 35.0, 'CUE' : 12.0 }
gamma      = 0.98
# Computamos el valor actual neto desde cada estado
recompensa_esperada = cadena.valor_actual_neto( recompensa, gamma)
