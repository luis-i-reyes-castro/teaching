"""
Ejemplo del uso del modula Estatica, clase Armadura2D.
@author: Luis I. Reyes Castro

"""

from Estatica import Armadura2D

# -----------------------------------------------------------------------------
# Ejemplo: Beer & Johnson (9ED) - Problema 6.12

# Declaramos el diccionario de nodos y posiciones
nodos = { 'A' : (  0., 0.00),
          'B' : (  8., 6.00),
          'C' : (  8., 0.00),
          'D' : ( 16., 8.33),
          'E' : ( 16., 0.00),
          'F' : ( 24., 6.00),
          'G' : ( 24., 0.00),
          'H' : ( 32., 0.00) }

# Declaramos la lista de miembros
miembros = [ ('A','B'), ('A','C'),
             ('B','C'), ('B','D'), ('B','E'),
             ('C','E'),
             ('D','E'), ('D','F'),
             ('E','F'), ('E','G'),
             ('F','G'), ('F','H'),
             ('G','H') ]

# Declaramos las locaciones del perno, del patin, y de las cargas
perno      = 'A'
patin      = 'H'
tipo_patin = 'Horizontal'
cargas     = { 'A' : ( 0., -300.),
               'B' : ( 0., -600.),
               'D' : ( 0., -600.),
               'F' : ( 0., -600.),
               'H' : ( 0., -300.) }

# Construimos un objeto de la la clase armadura
armadura = Armadura2D( nodos, miembros, perno, patin, tipo_patin, cargas)
# Ordenamos al objeto resolver el modelo y mostrar la solucion
armadura.resuelve()
armadura.imprime_solucion()
armadura.grafica_solucion()

# -----------------------------------------------------------------------------
# Ejemplo: Beer & Johnson (9ED) - Problema 6.13

# Declaramos el diccionario de nodos y posiciones
nodos = { 'A' : ( 0., 0.0),
          'B' : ( 2., 0.0),
          'C' : ( 4., 0.0),
          'D' : ( 6., 0.0),
          'E' : ( 0., -2.500),
          'F' : ( 2., -1.667),
          'G' : ( 4., -0.833) }

# Declaramos la lista de miembros
miembros = [ ('A','B'), ('A','E'),
             ('B','C'), ('B','E'), ('B','F'),
             ('C','D'), ('C','F'), ('C','G'),
             ('D','G'),
             ('E','F'),
             ('F','G') ]

# Declaramos las locaciones del perno, del patin, y de las cargas
perno      = 'A'
patin      = 'E'
tipo_patin = 'Pared'
cargas     = { 'A' : ( 0., -12.5),
               'B' : ( 0., -12.5),
               'C' : ( 0., -12.5),
               'D' : ( 0., -12.5) }

# Construimos un objeto de la la clase armadura
armadura = Armadura2D( nodos, miembros, perno, patin, tipo_patin, cargas)
# Ordenamos al objeto resolver el modelo y mostrar la solucion
armadura.resuelve()
armadura.imprime_solucion()
armadura.grafica_solucion()
