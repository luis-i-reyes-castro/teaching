"""
Programa para Resolver Armaduras para Puentes
@author: Luis I. Reyes Castro

"""

# Importamos numpy
import numpy as np

# Declaramos la lista de nodos
nodos = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ]
N     = len(nodos)
filas = { nodo : 2*i for (i,nodo) in enumerate(nodos) }
# Declaramos el diccionario de posiciones de los nodos
posicion = { 'A' : ( 0.0, 0.0), 'B' : ( 1.0, 1.0),
             'C' : ( 1.0, 0.0), 'D' : ( 2.0, 1.0),
             'E' : ( 2.0, 0.0), 'F' : ( 3.0, 1.0),
             'G' : ( 3.0, 0.0), 'H' : ( 4.0, 0.0) }
# Declaramos la lista de miembros
miembros = [ ('A','B'), ('A','C'), ('B','C'), ('B','D'),
             ('B','E'), ('C','E'), ('D','E'), ('D','F'),
             ('E','F'), ('E','G'), ('F','G'), ('F','H'),
             ('G','H') ]
M        = len(miembros)

columnas = { miembro : i for (i,miembro) in enumerate(miembros) }
columnas['Ax'] = len(miembros)
columnas['Ay'] = len(miembros) + 1
columnas['Hy'] = len(miembros) + 2

# Alocamos la matriz del lado izquierdo y el vector del lado derecho
A_izq = np.zeros( shape = ( 2*N, 2*N) )
b_der = np.zeros( shape = ( 2*N,) )

# Construimos un diccionario de vecinos de cada nodo
vecinos = {}
for nodo in nodos :
    vecinos[nodo] = []
    for miembro in miembros :
        if miembro[0] == nodo :
            vecinos[nodo].append( miembro[1] )
        elif miembro[1] == nodo :
            vecinos[nodo].append( miembro[0] )

# Iteramos sobre todos los nodos
for ( i, nodo) in enumerate(nodos) :
    print( 'Nodo actual:', nodo)
    vecinos = vecinos[nodo]
    fila    = filas[nodo]
    for vecino in vecinos :
        r = posicion[vecino] - posicion[nodo]
        u = r / np.linalg.norm(r)
