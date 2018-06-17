"""
Ejemplo de lectura de hojas de calculo.
@author: Luis I. Reyes Castro
"""

import pandas as pd

# Declaramos una manija
manija = open( 'Propuestas_Reyes-Luis.xlsx', 'rb')
df = pd.read_excel( manija, 'Propuestas')
manija.close()

# Extraemos las preferencias del profesor
df2 = df.iloc[0:25][ [ 'Tiempo Medio', 'Tiempo Parcial', 'Tiempo Completo'] ]
salario_medio = df.iloc[-1]['Tiempo Medio']
salario_parcial = df.iloc[-1]['Tiempo Parcial']
salario_completo = df.iloc[-1]['Tiempo Completo']

# Extraemos un arreglo numpy de df2
matriz = df2.as_matrix()
