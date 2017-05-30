# -*- coding: utf-8 -*-
"""
Taller de Estructuras de Vigas Ideales
@author: Luis I. Reyes Castro
"""

# Importamos el modulo numpy
import numpy as np

# Declaramos la lista de ecuaciones del sistema
lista_ecu = [ 'N1x', 'N1y', 'N2x', 'N2y', 'N3x', 'N3y', \
              'N4x', 'N4y', 'N5x', 'N5y', 'N6x', 'N6y' ]
# Declaramos un diccionario que toma una ecuacion y retorna su indice
ind_ecu = {}
for i in range(len(lista_ecu)) :
    ind_ecu[ lista_ecu[i] ] = i

# Declaramos la lista_de variables (o incognitas) del sistema
lista_var = [ 'F_12', 'F_13', 'F_14', 'F_15', 'F_25', 'F_26', \
              'F_34', 'F_45', 'F_56', 'F_N3', 'F_T3', 'F_N6' ]
# Declaramos un diccionario que toma una ecuacion y retorna su indice
ind_var = {}
for j in range(len(lista_var)) :
    ind_var[ lista_var[j] ] = j

# Declaramos una funcion para convertir de grados a radianes
def grados_a_rad(angulo) :
    return np.pi * angulo / 180.0

# Declaramos la matriz del lado izquierdo
A = np.zeros((12,12))
# Declaramos el vector del lado derecho
b = np.zeros((12,1))
# Declaramos las fuerzas en los nodos 4 y 5
F_A = -1000
F_B = 0

# Ingresamos la ecuacion del Nodo 1-X
A[ ind_ecu['N1x'], ind_var['F_12'] ] = -1.0
A[ ind_ecu['N1x'], ind_var['F_15'] ] = -np.cos(grados_a_rad(45))
A[ ind_ecu['N1x'], ind_var['F_13'] ] = +np.cos(grados_a_rad(45))
b[ ind_ecu['N1x'], 0 ] = 0.0
# Ingresamos la ecuacion del Nodo 1-Y
A[ ind_ecu['N1y'], ind_var['F_15'] ] = +np.sin(grados_a_rad(45))
A[ ind_ecu['N1y'], ind_var['F_14'] ] = +1.0
A[ ind_ecu['N1y'], ind_var['F_13'] ] = +np.sin(grados_a_rad(45))
b[ ind_ecu['N1y'], 0 ] = 0.0

# Ingresamos la ecuacion del Nodo 2-X
A[ ind_ecu['N2x'], ind_var['F_12'] ] = +1.0
A[ ind_ecu['N2x'], ind_var['F_26'] ] = -np.cos(grados_a_rad(45))
b[ ind_ecu['N2x'], 0 ] = 0.0
# Ingresamos la ecuacion del Nodo 2-Y
A[ ind_ecu['N2y'], ind_var['F_25'] ] = +1.0
A[ ind_ecu['N2y'], ind_var['F_26'] ] = +np.sin(grados_a_rad(45))
b[ ind_ecu['N2y'], 0 ] = 0.0

# Ingresamos la ecuacion del Nodo 3-X
A[ ind_ecu['N3x'], ind_var['F_T3'] ] = +1.0
A[ ind_ecu['N3x'], ind_var['F_13'] ] = -np.cos(grados_a_rad(45))
A[ ind_ecu['N3x'], ind_var['F_34'] ] = -1.0
b[ ind_ecu['N3x'], 0 ] = 0.0
# Ingresamos la ecuacion del Nodo 3-Y
A[ ind_ecu['N3y'], ind_var['F_N3'] ] = +1.0
A[ ind_ecu['N3y'], ind_var['F_13'] ] = -np.sin(grados_a_rad(45))
b[ ind_ecu['N3y'], 0 ] = 0.0

# Ingresamos la ecuacion del Nodo 4-X
A[ ind_ecu['N4x'], ind_var['F_34'] ] = +1.0
A[ ind_ecu['N4x'], ind_var['F_45'] ] = -1.0
b[ ind_ecu['N4x'], 0 ] = 0.0
# Ingresamos la ecuacion del Nodo 4-Y
A[ ind_ecu['N4y'], ind_var['F_14'] ] = -1.0
b[ ind_ecu['N4y'], 0 ] = F_A

# Ingresamos la ecuacion del Nodo 5-X
A[ ind_ecu['N5x'], ind_var['F_45'] ] = +1.0
A[ ind_ecu['N5x'], ind_var['F_15'] ] = +np.cos(grados_a_rad(45))
A[ ind_ecu['N5x'], ind_var['F_56'] ] = -1.0
b[ ind_ecu['N5x'], 0 ] = 0.0
# Ingresamos la ecuacion del Nodo 5-Y
A[ ind_ecu['N5y'], ind_var['F_15'] ] = -np.sin(grados_a_rad(45))
A[ ind_ecu['N5y'], ind_var['F_25'] ] = -1.0
b[ ind_ecu['N5y'], 0 ] = F_B

# Ingresamos la ecuacion del Nodo 6-X
A[ ind_ecu['N6x'], ind_var['F_56'] ] = +1.0
A[ ind_ecu['N6x'], ind_var['F_26'] ] = +np.cos(grados_a_rad(45))
b[ ind_ecu['N6x'], 0 ] = 0.0
# Ingresamos la ecuacion del Nodo 6-Y
A[ ind_ecu['N6y'], ind_var['F_26'] ] = -np.sin(grados_a_rad(45))
A[ ind_ecu['N6y'], ind_var['F_N6'] ] = +1.0
b[ ind_ecu['N6y'], 0 ] = 0.0

# Resolvemos el sistema de ecuaciones lineales A x = b
x = np.linalg.solve( A, b)
# Imprimimos la solucion
for var in lista_var :
    print( 'Fuerza ' + var + ' = ' + str( x[ ind_var[var], 0] ) )
