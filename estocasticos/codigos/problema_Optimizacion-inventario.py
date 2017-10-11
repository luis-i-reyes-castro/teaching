"""
@author: Luis I. Reyes Castro

Problema de Optimizacion de Inventario
"""

import numpy as np
from scipy.stats import poisson
from ModelosEstocasticos import CadenaDeMarkov

# Estados
I_max       = 5
estados     = [ unidades for unidades in range( I_max + 1 ) ]
num_estados = len(estados)

# Acciones disponibles en cada estado
reposiciones = [ 0, 1, 2, 3]
acciones = {}
for nivel_inventario in estados :
    acciones[nivel_inventario] = []
    for reposicion in reposiciones :
        if nivel_inventario + reposicion <= I_max :
            acciones[nivel_inventario].append( reposicion)

# Parametro de la demanda
mu = 2.1
# Funcion de probabilidad de una Poisson truncada
def poisson_pmf_truncada( k, maximo) :
    if 0 <= k < maximo :
        return poisson.pmf( k, mu)
    elif k == maximo :
        return 1.0 - sum( [ poisson.pmf( l, mu) for l in range(maximo) ] )
    return 0.0

# Funcion de transicion
funcion_P = {}
for ( i, nivel_inventario) in enumerate(estados) :

    num_acciones                = len( acciones[nivel_inventario] )
    funcion_P[nivel_inventario] = np.zeros( ( num_acciones, num_estados) )

    for ( j, reposicion) in enumerate( acciones[nivel_inventario] ) :
        for ( i_prima, nivel_inventario_prima) in enumerate(estados) :

            demanda = ( nivel_inventario + reposicion ) - nivel_inventario_prima

            funcion_P[nivel_inventario][ j, i_prima] = \
            poisson_pmf_truncada( demanda, nivel_inventario)
