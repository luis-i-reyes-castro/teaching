#!/usr/bin/env python3
"""
Estudiante: Reyes Castro Luis Ignacio
Paralelo: 09-08

Problema 00

"""

from Estatica import Armadura2D

# Declaramos el diccionario de nodos y posiciones
nodos = { 'A' : ( 0.0, 0.0),
          'B' : ( 3.0, 0.0),
          'C' : ( 0.5, 2.5),
          'D' : ( 2.5, 2.5),
          'E' : ( 1.5, 2.5),
          'F' : ( 0.5, 4.5),
          'G' : ( 2.5, 4.5),
          'H' : ( 0.0, 7.0),
          'I' : ( 3.0, 7.0),
          'J' : ( 1.5, 7.0) }

# Declaramos la lista de miembros
miembros = [ ('A','C'), ('A','E'),
             ('B','D'), ('B','E'),
             ('C','E'), ('C','F'),
             ('D','E'), ('D','G'),
             ('E','F'), ('E','G'),
             ('F','G'), ('F','H'), ('F','J'),
             ('G','J'), ('G','I'),
             ('H','J'),
             ('I','J') ]

# Declaramos las locaciones del soporte empernado y del patin
soporte_empernado = 'A'
patin             = 'B'
tipo_patin        = 'Horizontal'

# Declaramos el diccionario de cargas externas
cargas = { 'F' : ( 0., -250.),
           'G' : ( 0., -250.),
           'H' : ( 0., -250.),
           'I' : ( 0., -250.) }

# Declaramos el peso por metro de los miembros
peso_por_metro_de_miembro = 9.0

# Construimos un objeto de la la clase armadura
armadura = Armadura2D( nodos,
                       miembros,
                       soporte_empernado,
                       patin,
                       tipo_patin,
                       cargas,
                       peso_por_metro_de_miembro )

# Ordenamos al objeto resolver el modelo y mostrar la solucion
armadura.resuelve()
armadura.imprime_solucion()
armadura.grafica_solucion()
