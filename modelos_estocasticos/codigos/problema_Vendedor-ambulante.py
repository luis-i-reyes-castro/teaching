"""
@author: Luis I. Reyes Castro

Problema del Vendedor que Viaja entre GYE-UIO-CUE

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkov

# Lista de estados
S = [ 'GYE', 'UIO', 'CUE' ]
# Matriz de transicion
P = np.array( [ [ 0.4, 0.3, 0.3 ],
                [ 0.7, 0.0, 0.3 ],
                [ 0.0, 0.5, 0.5 ] ] )

# Crea una nuevo objeto que representa una Cadena de Markov
cadena = CadenaDeMarkov( S, P)
# Declaramos funcion de recompensa
recompensa = { 'GYE' : 20.0, 'UIO' : 35.0, 'CUE' : 12.0 }
factor_descuento = 0.98
# Computa la distribucion estacionaria (i.e. en estado estable) de la cadena
utilidad = cadena.funcion_de_valor( recompensa, factor_descuento)
# Computa la distribucion en estado estable
pi_estrella = cadena.distribucion_estacionaria()

# Calculamos la utilidad total descontada
U = 0
for ( i, estado) in enumerate(S) :
    U += pi_estrella[estado] * utilidad[estado]
