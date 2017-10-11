"""
@author: Luis I. Reyes Castro

Ejemplos del uso de la clase ProcesoBernoulli
"""

from ModelosEstocasticos import ProcesoBernoulli

# Declara un proceso Bernoulli con parametro p = 0.80
proceso_A = ProcesoBernoulli(0.80)
# Genera muestras de 1000 pasos del proceso anterior
( X, freq) = proceso_A.muestrea( num_pasos = 1000)

# Divide al proceso anterior en tres procesos, donde cada arribo al proceso
# es enviado al proceso_B con probabilidad de 0.50, al proceso_C con
# probabilidad de 0.15 y al proceso_D con probabilidad de 0.35
( proceso_B, proceso_C, proceso_D) = proceso_A.divide( [ 0.50, 0.15, 0.35] )

# Declara un proceso Bernoulli con parametro p = 0.60
proceso_U = ProcesoBernoulli(0.60)

# Combina el proceso_D y proceso_U en modo 'OR' para formar el proceso_V
proceso_V = ProcesoBernoulli( [ proceso_D, proceso_U], modo = 'OR' )
