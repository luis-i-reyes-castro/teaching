"""
@author: Luis I. Reyes Castro
"""

import numpy as np

def construye_matriz_actividad_uno( n, p) :

    # Inicializa matriz de transicion
    matriz = np.zeros( shape = ( n+1, n+1) )

    # Inserta transiciones desde el estado cero hacia...
    matriz[ 0, 0] = 1 - p # Si mismo
    matriz[ 0, 1] = p     # El estado uno

    # Inserta transiciones desde el ultimo estado hacia...
    matriz[ -1, -2] = 1 - p # El penultimo estado
    matriz[ -1, -1] = p     # Si mismo

    # Inserta transiciones desde cada estado i entre uno y n-1 hacia...
    for i in range( 1, n) :
        matriz[ i, i-1] = 1 - p # El estado i-1
        matriz[ i, i+1] = p     # El estado i+1

    return matriz

def construye_matriz_actividad_dos( num_filas, num_cols) :

    # Define sub-funcion para calcular el indice de un estado a partir
    # de su posicion
    def encuentra_indice_estado( i, j) :
        return i * num_cols + j

    # Calcula numero de estados e inicializa la matriz de transicion
    num_estados = num_filas * num_cols
    matriz_P = np.zeros( shape = ( num_estados, num_estados) )

    # Itera sobre cada fila...
    for i in range(num_filas) :
        # Itera sobre cada columna...
        for j in range(num_cols) :

            # Computa el indice del estado actual
            indice_estado = encuentra_indice_estado(i,j)

            # Inserta transicion al mismo estado
            matriz_P[ indice_estado, indice_estado] = 1.0

            # Inserta transicion al vecino de arriba (si aplica)
            if i > 0 :
                indice_vecino = encuentra_indice_estado( i-1, j)
                matriz_P[ indice_estado, indice_vecino] = 1.0

            # Inserta transicion al vecino de abajo (si aplica)
            if i < num_filas - 1 :
                indice_vecino = encuentra_indice_estado( i+1, j)
                matriz_P[ indice_estado, indice_vecino] = 1.0

            # Inserta transicion al vecino de la izquierda (si aplica)
            if j > 0 :
                indice_vecino = encuentra_indice_estado( i, j-1)
                matriz_P[ indice_estado, indice_vecino] = 1.0

            # Inserta transicion al vecino de la derecha (si aplica)
            if j < num_cols - 1 :
                indice_vecino = encuentra_indice_estado( i, j+1)
                matriz_P[ indice_estado, indice_vecino] = 1.0

    # Dividimos cada fila para el numero de vecinos factibles para que
    # cada fila corresponda a una distribucion uniforme
    for k in range(num_estados) :
        suma_de_fila = np.sum( matriz_P[k,:] )
        matriz_P[k,:] /= suma_de_fila

    return matriz_P

# Ejemplo de utilizacion de la funcion de la actividad uno
matriz_P_actividad_uno = construye_matriz_actividad_uno( 5, 0.5)

# Ejemplo de utilizacion de la funcion de la actividad dos
matriz_P_actividad_dos = construye_matriz_actividad_dos( 3, 4)
