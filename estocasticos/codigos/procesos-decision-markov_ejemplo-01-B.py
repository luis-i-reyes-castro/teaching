"""
Implementacion del Proceso de Decision Markoviano (PDM) del
Problema prototipo de la Seccion 19.1 del texto de Hillier & Lieberman (9ED)

@author: Luis I. Reyes Castro

"""

from ModelosEstocasticos import ProcesoDeDecisionMarkoviano

# Declaramos los estados
S = [ 0, 1, 2, 3]
# Declaramos las acciones disponibles en cada estado
A = { 0 : [ 'Nada' ],
      1 : [ 'Nada', 'Remplazo' ],
      2 : [ 'Nada', 'Reparacion-general', 'Remplazo' ],
      3 : [ 'Remplazo' ] }
# Declaramos las transiciones
T = { ( 0, 'Nada') : { 1 : 7/8, 2 : 1/16, 3 : 1/16 },
      ( 1, 'Nada') : { 1 : 3/4, 2 : 1/8, 3 : 1/8  },
      ( 1, 'Remplazo') : { 0 : 1 },
      ( 2, 'Nada') : { 2 : 1/2, 3 : 1/2 },
      ( 2, 'Reparacion-general') : { 1 : 1 },
      ( 2, 'Remplazo') : { 0 : 1 },
      ( 3, 'Remplazo') : { 0 : 1 } }
# Declaramos los costos
C = { ( 0, 'Nada') : 0,
      ( 1, 'Nada') : 1000,
      ( 1, 'Remplazo') : 6000,
      ( 2, 'Nada') : 3000,
      ( 2, 'Reparacion-general') : 4000,
      ( 2, 'Remplazo') : 6000,
      ( 3, 'Remplazo') : 6000 }

pdm = ProcesoDeDecisionMarkoviano( S, A, T, C)
