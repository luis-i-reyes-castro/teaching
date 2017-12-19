"""
Ejemplo del uso del modula Estatica, clase Armadura2D.
@author: Luis I. Reyes Castro

"""

from Estatica import Armadura2D

# -----------------------------------------------------------------------------
# EJEMPLO: Puente

# Declaramos el diccionario de nodos y posiciones
nodos = { 'A' : ( 0.0, 0.0), 'B' : ( 1.0, 1.0),
          'C' : ( 1.0, 0.0), 'D' : ( 2.0, 1.0),
          'E' : ( 2.0, 0.0), 'F' : ( 3.0, 1.0),
          'G' : ( 3.0, 0.0), 'H' : ( 4.0, 0.0) }

# Declaramos la lista de miembros
miembros = [ ('A','B'), ('A','C'), ('B','C'), ('B','D'),
             ('B','E'), ('C','E'), ('D','E'), ('D','F'),
             ('E','F'), ('E','G'), ('F','G'), ('F','H'),
             ('G','H') ]

# Declaramos las locaciones del perno, del patin, y de las cargas
perno      = 'A'
patin      = 'H'
tipo_patin = 'Horizontal'
cargas     = { 'C' : ( 0.0, -10.0),
               'E' : ( 0.0, -10.0),
               'G' : ( 0.0, -10.0) }

# Construimos un objeto de la la clase armadura
armadura = Armadura2D( nodos, miembros, perno, patin, tipo_patin, cargas)
# Ordenamos al objeto resolver el modelo y mostrar la solucion
armadura.resuelve()
armadura.imprime_solucion()
armadura.grafica_solucion()

# -----------------------------------------------------------------------------
# Ejemplo: Armadura colgada de una pared

# Declaramos el diccionario de nodos y posiciones
nodos = { 'A' : ( 0.0, 0.0), 'B' : ( 0.0, -2.0),
          'C' : ( 2.0, 1.0), 'D' : ( 3.0,  1.0),
          'E' : ( 4.0, 1.0), 'F' : ( 3.0,  0.0) }

# Declaramos la lista de miembros
miembros = [ ('A','B'), ('A','C'), ('A','F'), ('B','F'),
             ('C','D'), ('C','F'), ('D','E'), ('D','F'),
             ('E','F') ]

# Declaramos las locaciones del perno, del patin, y de las cargas
perno      = 'A'
patin      = 'B'
tipo_patin = 'Pared'
cargas     = { 'C' : ( 0.0, -10.0),
               'D' : ( 0.0, -10.0),
               'E' : ( 0.0, -10.0) }

# Construimos un objeto de la la clase armadura
armadura = Armadura2D( nodos, miembros, perno, patin, tipo_patin, cargas)
# Ordenamos al objeto resolver el modelo y mostrar la solucion
armadura.resuelve()
armadura.imprime_solucion()
armadura.grafica_solucion()
