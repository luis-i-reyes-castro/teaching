"""
@author: Luis I. Reyes Castro

Problema de las Lineas de Produccion

"""

from ModelosEstocasticos import ProcesoBernoulli

# Lista de estados
S = [ 'Vacio', 'Lleno' ]
# Crea una nuevo objeto que representa una linea de produccion
linea = ProcesoBernoulli( estados = S, parametro = 0.8)
# Genera muestras de 1000 pasos
( X, freq) = linea.muestrea( num_pasos = 1000)

# Divide al proceso anterior en tres y genera muestras de 1000 pasos
# de cada uno de los procesos resultantes
( linea1, linea2, linea3) = linea.divide_proceso( [ 0.5, 0.4, 0.1] )
( X1, freq1) = linea1.muestrea( num_pasos = 1000)
( X2, freq2) = linea2.muestrea( num_pasos = 1000)
( X3, freq3) = linea3.muestrea( num_pasos = 1000)
