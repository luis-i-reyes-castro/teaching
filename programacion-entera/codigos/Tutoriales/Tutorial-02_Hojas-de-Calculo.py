"""
Tutorial sobre Importacion de Datos desde Hojas de Calculo
@author: Luis I. Reyes Castro
"""

import pandas as pd

manija = open( '../Datos/Datos_Tutorial-02.xlsx', 'rb')
df = pd.read_excel( manija, 'Propuestas')
manija.close()

columnas         = [ 'Tiempo Medio', 'Tiempo Parcial', 'Tiempo Completo']
matriz_valores   = df.iloc[0:25][columnas].values
salario_medio    = df.iloc[-1][columnas[0]]
salario_parcial  = df.iloc[-1][columnas[1]]
salario_completo = df.iloc[-1][columnas[2]]
