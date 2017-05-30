# -*- coding: utf-8 -*-
"""
Taller de Estructuras de Vigas Ideales
@author: Luis I. Reyes Castro
"""

# Importamos el modulo numpy
import numpy as np

# Declaramos la lista de ecuaciones del sistema
lista_ecu = [ 'N1x', 'N1y', 'N2x', 'N2y', 'N3x', 'N3y', \
              'N4x', 'N4y', 'N5x', 'N5y', 'N6x', 'N6y', \
              'N7x', 'N7y', 'N8x', 'N8y', 'N9x', 'N9y' ]
# Declaramos un diccionario que toma una ecuacion y retorna su indice
ind_ecu = { }
for i in range(len(lista_ecu)) :
    ind_ecu[ lista_ecu[i] ] = i

# Declaramos la lista_de variables (o incognitas) del sistema
lista_var = [ 'F_12', 'F_14', 'F_23', 'F_24', 'F_25', 'F_35', \
              'F_45', 'F_46', 'F_47', 'F_57', 'F_58', 'F_59', \
              'F_67', 'F_78', 'F_89', 'F_N6', 'F_T9', 'F_N9' ]
# Declaramos un diccionario que toma una ecuacion y retorna su indice
ind_var = { }
for j in range(len(lista_var)) :
    ind_var[ lista_var[j] ] = j

# Declaramos una funcion para convertir de grados a radianes
def grados_a_radianes( angulo_en_grados) :
    angulo_en_radianes = ( np.pi / 180.0 ) * angulo_en_grados
    return angulo_en_radianes

# Declaramos la matriz del lado izquierdo
A = np.zeros((18,18))
# Declaramos el vector del lado derecho
b = np.zeros((18,1))
# Declaramos las fuerzas en los nodos 4 y 5
F_A = 1000
F_B = 1000
F_C = 1000

# Ingresamos la ecuacion del Nodo 1-X: 
# -F_12 - F_14 cos(45) = 0
A[ ind_ecu['N1x'], ind_var['F_12'] ] = -1.0
A[ ind_ecu['N1x'], ind_var['F_14'] ] = -np.cos( grados_a_radianes(45) )
# Ingresamos la ecuacion del Nodo 1-Y: 
# F_14 sen(45) = F_A
A[ ind_ecu['N1y'], ind_var['F_14'] ] = +np.sin( grados_a_radianes(45) )
b[ ind_ecu['N1y'], 0 ] = F_A

# Ingresamos la ecuacion del Nodo 2-X: 
# F_12 - F_23 - F_25 cos(60) = 0
A[ ind_ecu['N2x'], ind_var['F_12'] ] = +1.0
A[ ind_ecu['N2x'], ind_var['F_23'] ] = -1.0
A[ ind_ecu['N2x'], ind_var['F_25'] ] = -np.cos( grados_a_radianes(60) )
# Ingresamos la ecuacion del Nodo 2-Y: 
# F_24 + F_25 sen(60) = F_B
A[ ind_ecu['N2y'], ind_var['F_24'] ] = +1.0
A[ ind_ecu['N2y'], ind_var['F_25'] ] = +np.sin( grados_a_radianes(60) )
b[ ind_ecu['N2y'], 0 ] = F_B

# Ingresamos la ecuacion del Nodo 3-X: 
# F_23 + F_35 cos(60) = 0
A[ ind_ecu['N3x'], ind_var['F_23'] ] = +1.0
A[ ind_ecu['N3x'], ind_var['F_35'] ] = +np.cos( grados_a_radianes(60) )
# Ingresamos la ecuacion del Nodo 3-Y: 
# F_35 sen(60) = F_C
A[ ind_ecu['N3y'], ind_var['F_35'] ] = +np.sin( grados_a_radianes(60) )
b[ ind_ecu['N3y'], 0 ] = F_C

# Ingresamos la ecuacion del Nodo 4-X: 
# F_14 cos(45) + F_46 cos(45) - F_45 = 0
A[ ind_ecu['N4x'], ind_var['F_14'] ] = +np.cos( grados_a_radianes(45) )
A[ ind_ecu['N4x'], ind_var['F_46'] ] = +np.cos( grados_a_radianes(45) )
A[ ind_ecu['N4x'], ind_var['F_45'] ] = -1.0
# Ingresamos la ecuacion del Nodo 4-Y: 
# -F_14 sen(45) + F_46 sen(45) - F_24 + F_47 = 0
A[ ind_ecu['N4y'], ind_var['F_14'] ] = -np.sin( grados_a_radianes(45) )
A[ ind_ecu['N4y'], ind_var['F_46'] ] = +np.sin( grados_a_radianes(45) )
A[ ind_ecu['N4y'], ind_var['F_24'] ] = -1.0
A[ ind_ecu['N4y'], ind_var['F_47'] ] = +1.0

# Ingresamos la ecuacion del Nodo 5-X: 
# F_45 + F_25 cos(60) - F_35 cos(60) + F_57 cos(60) - F_59 cos(60) = 0
A[ ind_ecu['N5x'], ind_var['F_45'] ] = +1.0
A[ ind_ecu['N5x'], ind_var['F_25'] ] = +np.cos( grados_a_radianes(60) )
A[ ind_ecu['N5x'], ind_var['F_35'] ] = -np.cos( grados_a_radianes(60) )
A[ ind_ecu['N5x'], ind_var['F_57'] ] = +np.cos( grados_a_radianes(60) )
A[ ind_ecu['N5x'], ind_var['F_59'] ] = -np.cos( grados_a_radianes(60) )
# Ingresamos la ecuacion del Nodo 5-Y: 
# F_58 - F_25 sen(60) - F_35 sen(60) + F_57 sen(60) + F_59 sen(60) = 0
A[ ind_ecu['N5y'], ind_var['F_58'] ] = +1.0
A[ ind_ecu['N5y'], ind_var['F_25'] ] = -np.sin( grados_a_radianes(60) )
A[ ind_ecu['N5y'], ind_var['F_35'] ] = -np.sin( grados_a_radianes(60) )
A[ ind_ecu['N5y'], ind_var['F_57'] ] = +np.sin( grados_a_radianes(60) )
A[ ind_ecu['N5y'], ind_var['F_59'] ] = +np.sin( grados_a_radianes(60) )

# Ingresamos la ecuacion del Nodo 6-X: 
# -F_46 cos(45) - F_67 = 0
A[ ind_ecu['N6x'], ind_var['F_46'] ] = -np.cos( grados_a_radianes(45) )
A[ ind_ecu['N6x'], ind_var['F_67'] ] = -1.0
# Ingresamos la ecuacion del Nodo 6-Y: 
# N_6 - F_46 sen(45) = 0
A[ ind_ecu['N6y'], ind_var['F_N6'] ] = +1.0
A[ ind_ecu['N6y'], ind_var['F_46'] ] = -np.sin( grados_a_radianes(45) )

# Ingresamos la ecuacion del Nodo 7-X: 
# F_67 - F_78 - F_57 cos(60) = 0
A[ ind_ecu['N7x'], ind_var['F_67'] ] = +1.0
A[ ind_ecu['N7x'], ind_var['F_78'] ] = -1.0
A[ ind_ecu['N7x'], ind_var['F_57'] ] = -np.cos( grados_a_radianes(60) )
# Ingresamos la ecuacion del Nodo 7-Y: 
# -F_47 - F_57 sen(60) = 0
A[ ind_ecu['N7y'], ind_var['F_47'] ] = -1.0
A[ ind_ecu['N7y'], ind_var['F_57'] ] = -np.sin( grados_a_radianes(60) )

# Ingresamos la ecuacion del Nodo 8-X: 
# F_78 - F_89 = 0
A[ ind_ecu['N8x'], ind_var['F_78'] ] = +1.0
A[ ind_ecu['N8x'], ind_var['F_89'] ] = -1.0
# Ingresamos la ecuacion del Nodo 8-Y: 
# -F_58 = 0
A[ ind_ecu['N8y'], ind_var['F_58'] ] = -1.0

# Ingresamos la ecuacion del Nodo 9-X: 
# T_9 + F_89 + F_59 cos(60) = 0
A[ ind_ecu['N9x'], ind_var['F_T9'] ] = +1.0
A[ ind_ecu['N9x'], ind_var['F_89'] ] = +1.0
A[ ind_ecu['N9x'], ind_var['F_59'] ] = +np.cos( grados_a_radianes(60) )
# Ingresamos la ecuacion del Nodo 9-Y: 
# N_9 - F_59 sen(60) = 0
A[ ind_ecu['N9y'], ind_var['F_N9'] ] = +1.0
A[ ind_ecu['N9y'], ind_var['F_59'] ] = -np.sin( grados_a_radianes(60) )

# Resolvemos el sistema de ecuaciones lineales A x = b
x = np.linalg.solve( A, b)
# Imprimimos la solucion
for var in lista_var :
    print( 'Fuerza ' + var + ' = ' + str( x[ ind_var[var], 0] ) )
