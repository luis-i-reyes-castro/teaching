"""
Programa para Resolver Armaduras para Puentes
@author: Luis I. Reyes Castro

"""

# Importamos numpy
import numpy as np

# -------------------------------------------------------------------------------------
# Declaramos la lista de nodos
nodos = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ]
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

# Declaramos las locaciones del perno, del patin, y de las cargas
perno  = 'A'
patin  = 'H'
cargas = { 'C' : ( 0.0, -10.0),
           'E' : ( 0.0, -10.0),
           'G' : ( 0.0, -10.0) }

# -------------------------------------------------------------------------------------
# Verificamos que la armadura sea estaticamente determinable
N = len(nodos)
M = len(miembros)
if 2 * N != M + 3 :
    print( 'ERROR: Armadura no es estaticamente determinable!' )

# Alocamos la matriz del lado izquierdo y el vector del lado derecho
A_izq = np.zeros( shape = ( 2*N, 2*N) )
b_der = np.zeros( shape = ( 2*N,) )

# Declaramos un diccionario de ecuaciones
ecuaciones = { nodo : 2 * indice for ( indice, nodo) in enumerate(nodos) }

# Declaramos un diccionario de incognitas
incognitas = { 'Perno_x' : 0, 'Perno_y' : 1, 'Patin_y' : 2 }
for ( indice, miembro) in enumerate(miembros) :
    incognitas[ ( miembro[0], miembro[1] ) ] = 3 + indice
    incognitas[ ( miembro[1], miembro[0] ) ] = 3 + indice

# Declaramos una funcion que retorna los vecinos de un nodo
def nodos_vecinos( nodo) :
    vecinos = []
    for miembro in miembros :
        if miembro[0] == nodo :
            vecinos.append( miembro[1] )
        elif miembro[1] == nodo :
            vecinos.append( miembro[0] )
    return vecinos

# Declaramos una funcion que retorna el vector unitario en la direccion del
# miembro (eslabon) indicado
def vector_unitario( nodo_i, nodo_f) :
    pos_i = np.array( posicion[nodo_i] )
    pos_f = np.array( posicion[nodo_f] )
    vector = pos_f - pos_i
    return ( 1.0 / np.linalg.norm(vector) ) * vector

# -------------------------------------------------------------------------------------
# Iteramos sobre todos los nodos...
print( 'CONSTRUYENDO ARMADURA...' )
for ( i, nodo) in enumerate(nodos) :

    print( 'Nodo actual:', nodo)

    fila = ecuaciones[nodo]
    if nodo == perno :
        col = incognitas['Perno_x']
        A_izq[ fila + 0, col] = 1.0
        col = incognitas['Perno_y']
        A_izq[ fila + 1, col] = 1.0
    elif nodo == patin :
        col = incognitas['Patin_y']
        A_izq[ fila + 1, col] = 1.0

    vecinos = nodos_vecinos(nodo)
    for ( j, nodo_vecino) in enumerate(vecinos) :
        print( '\t' + 'Procesando vecino:', nodo_vecino)
        col  = incognitas[ ( nodo, nodo_vecino) ]
        vec  = vector_unitario( nodo_vecino, nodo)
        print( '\t\t' + 'direccion de la fuerza:', vec)
        A_izq[ fila + 0, col] = vec[0]
        A_izq[ fila + 1, col] = vec[1]

    if nodo in cargas :
        print( '\t' + 'Procesando carga:', cargas[nodo])
        b_der[ fila + 0 ] = -cargas[nodo][0]
        b_der[ fila + 1 ] = -cargas[nodo][1]

# -------------------------------------------------------------------------------------
# Resolvemos el sistema de ecuaciones lineales
print( ' ' )
print( 'RESOLVIENDO ARMADURA...' )
x = np.linalg.solve( A_izq, b_der)

# Imprimimos la solucion
print( ' ' )
print( 'ANALISIS DE FUERZAS INTERNAS:' )
print( '\t' + 'Perno_x:', x[ incognitas['Perno_x'] ] )
print( '\t' + 'Perno_y:', x[ incognitas['Perno_y'] ] )
print( '\t' + 'Patin_y:', x[ incognitas['Patin_y'] ] )
for miembro in miembros :
    nom_miembro = '\t' + 'Miembro ' + miembro[0] + '-' + miembro[1] + ':'
    fuerza      = x[ incognitas[miembro] ]
    fuerza      = fuerza if abs(fuerza) > 1E-6 else 0.0
    signo       = ''
    if fuerza > 0 :
        signo = 'compresion'
    elif fuerza < 0 :
        signo = 'tension'
    print( nom_miembro, abs(fuerza), signo)
