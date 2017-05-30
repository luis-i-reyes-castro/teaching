# -*- coding: utf-8 -*-
"""
Programa para resolver ejercicio de estructuras de vigas ideales
@author: Luis I. Reyes Castro
"""

# Importamos el modulo numpy
import numpy as np
import taller_01_graficos

# Declaramos una lista (o arreglo) de ecuaciones
lista_ecu = [ 'N1x', 'N1y', 'N2x', 'N2y', 'N3x', 'N3y', \
              'N4x', 'N4y', 'N5x', 'N5y', 'N6x', 'N6y' ]
# Declaramos un diccionario que toma nombres de ecuaciones 
# y retorna sus indices
ind_ecu = { }
for i in range(len(lista_ecu)):
    ind_ecu[ lista_ecu[i] ] = i

# Declaramos una lista (o arreglo) de variables
lista_var = [ 'F_12', 'F_13', 'F_14', 'F_15', 'F_25', 'F_26', \
              'F_34', 'F_45', 'F_56', 'F_N3', 'F_T3', 'F_N6' ]
# Declaramos un diccionario que toma nombres de variables 
# y retorna sus indices
ind_var = { }
for j in range(len(lista_var)):
    ind_var[ lista_var[j] ] = j

# Declaramos una funcion que toma un angulo en grados 
# y retorna el angulo en radianes
def grados_a_radianes( angulo_en_grados):
    angulo_en_radianes = ( np.pi / 180.0 ) * angulo_en_grados
    return angulo_en_radianes

# Declaramos una matriz de ceros 12-por-12
A = np.zeros( (12,12) )
# Declaramos un vector de ceros en R-12 (i.e. el vector nulo de R-12)
b = np.zeros( (12,1) )

# Declaramos las fuerzas externas
F_A = -1000
F_B = 1000

# Ingresamos la ecuacion del Nodo 1-x: 
A[ ind_ecu['N1x'], ind_var['F_12'] ] = -1.0
A[ ind_ecu['N1x'], ind_var['F_15'] ] = -np.cos( grados_a_radianes(45) )
A[ ind_ecu['N1x'], ind_var['F_13'] ] = +np.cos( grados_a_radianes(45) )
b[ ind_ecu['N1x'], 0 ] = 0.0
# Ingresamos la ecuacion del Nodo 1-y: 
A[ ind_ecu['N1y'], ind_var['F_14'] ] = +1.0
A[ ind_ecu['N1y'], ind_var['F_13'] ] = +np.sin( grados_a_radianes(45) )
A[ ind_ecu['N1y'], ind_var['F_15'] ] = +np.sin( grados_a_radianes(45) )
b[ ind_ecu['N1y'], 0 ] = 0.0

# Ingresamos la ecuacion del Nodo 2-x: 
A[ ind_ecu['N2x'], ind_var['F_12'] ] = +1.0
A[ ind_ecu['N2x'], ind_var['F_26'] ] = -np.cos( grados_a_radianes(45) )
b[ ind_ecu['N2x'], 0 ] = 0.0
# Ingresamos la ecuacion del Nodo 2-y: 
A[ ind_ecu['N2y'], ind_var['F_25'] ] = +1.0
A[ ind_ecu['N2y'], ind_var['F_26'] ] = +np.sin( grados_a_radianes(45) )
b[ ind_ecu['N2y'], 0 ] = 0.0

# Ingresamos la ecuacion del Nodo 3-x: 
A[ ind_ecu['N3x'], ind_var['F_34'] ] = -1.0
A[ ind_ecu['N3x'], ind_var['F_13'] ] = -np.cos( grados_a_radianes(45) )
A[ ind_ecu['N3x'], ind_var['F_T3'] ] = +1.0
b[ ind_ecu['N3x'], 0 ] = 0.0
# Ingresamos la ecuacion del Nodo 3-y: 
A[ ind_ecu['N3y'], ind_var['F_13'] ] = -np.sin( grados_a_radianes(45) )
A[ ind_ecu['N3y'], ind_var['F_N3'] ] = +1.0
b[ ind_ecu['N3y'], 0 ] = 0.0

# Ingresamos la ecuacion del Nodo 4-x: 
A[ ind_ecu['N4x'], ind_var['F_34'] ] = +1.0
A[ ind_ecu['N4x'], ind_var['F_45'] ] = -1.0
b[ ind_ecu['N4x'], 0 ] = 0.0
# Ingresamos la ecuacion del Nodo 4-y: 
A[ ind_ecu['N4y'], ind_var['F_14'] ] = -1.0
b[ ind_ecu['N4y'], 0 ] = F_A

# Ingresamos la ecuacion del Nodo 5-x: 
A[ ind_ecu['N5x'], ind_var['F_15'] ] = +np.cos( grados_a_radianes(45) )
A[ ind_ecu['N5x'], ind_var['F_45'] ] = +1.0
A[ ind_ecu['N5x'], ind_var['F_56'] ] = -1.0
b[ ind_ecu['N5x'], 0 ] = 0.0
# Ingresamos la ecuacion del Nodo 5-y: 
A[ ind_ecu['N5y'], ind_var['F_25'] ] = -1.0
A[ ind_ecu['N5y'], ind_var['F_15'] ] = -np.sin( grados_a_radianes(45) )
b[ ind_ecu['N5y'], 0 ] = F_B

# Ingresamos la ecuacion del Nodo 6-x: 
A[ ind_ecu['N6x'], ind_var['F_56'] ] = +1.0
A[ ind_ecu['N6x'], ind_var['F_26'] ] = +np.cos( grados_a_radianes(45) )
b[ ind_ecu['N6x'], 0 ] = 0.0
# Ingresamos la ecuacion del Nodo 6-y: 
A[ ind_ecu['N6y'], ind_var['F_26'] ] = -np.sin( grados_a_radianes(45) )
A[ ind_ecu['N6y'], ind_var['F_N6'] ] = +1.0
b[ ind_ecu['N6y'], 0 ] = 0.0

# Resolvemos el sistema A x = b
vec_x = np.linalg.solve( A, b)
# Imprimimos la solucion
for var in lista_var:
    print( 'Fuerza', var, '=', vec_x[ ind_var[var], 0] )

# Graficamos la solucion
taller_01_graficos.graficar_solucion_01( ind_var, vec_x)














