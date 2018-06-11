"""
Implementacion de una Cola M/M/1/C.

@author: Luis I. Reyes Castro

"""

import numpy as np
from ModelosEstocasticos import CadenaDeMarkovEnTiempoContinuo

# Declarmos una funcion que toma los parametros de una colar M/M/1/C y
# retorna la lista de estados y matriz de transicion de la Cadena de Markov
# en Tiempo Continuo asociada con la cola
def cola_M_M_1_C( tasa_arribo, tasa_servicio, capacidad) :

    # Calcula numero de estados y declara lista de estados
    n = capacidad + 1
    S = [ i for i in range(n) ]

    # Declara la matriz de transicion (vacia)
    Q = np.zeros( shape = ( n, n) )
    # Itera sobre cada fila (estado) de la matriz de transicion
    for estado in S :
        # Inserta transicion asociada con servicio
        if estado > 0 :
            Q[ estado, estado - 1] = tasa_servicio
        # Inserta transicion asociada con arribo
        if estado < n - 1 :
            Q[ estado, estado + 1] = tasa_arribo

    return CadenaDeMarkovEnTiempoContinuo( S, Q)

# Ingresamos los parametros de la cola
tasa_arribo   = 1.0
tasa_servicio = 2.0
capacidad     = 6

# Construyimos la Cadena de Markov asociada con la cola
cola = cola_M_M_1_C( tasa_arribo, tasa_servicio, capacidad)
# Computamos la distribucion estacionaria
pi_estrella = cola.distribucion_estacionaria()

# Calculamos el numero promedio de clientes en el sistema y en cola
L   = 0.0
L_q = 0.0
for estado in cola.S :
    L   += estado * pi_estrella[estado]
    L_q += max( [ 0.0, estado - 1] ) * pi_estrella[estado]
# Calculamos el tiempo promedio de espera en el sistema y en cola
W   = L   / tasa_arribo
W_q = L_q / tasa_arribo

# Imprimimos los resultados
print( 'MODELO DE COLA M/M/1/C' )
print( 'Tasa de arribo (lambda) = ' + str(tasa_arribo) )
print( 'Tasa de servicio (mu) = ' + str(tasa_servicio) )
print( 'Capacidad (C) = ' + str(capacidad) )
print( 'Numero promedio de clientes en el sistema (L) = ' + str(L) )
print( 'Numero promedio de clientes en cola (L_q) = ' + str(L_q) )
print( 'Tiempo promedio de espera en el sistema (W) = ' + str(W) )
print( 'Tiempo promedio de espera en cola (W_q) = ' + str(W_q) )
