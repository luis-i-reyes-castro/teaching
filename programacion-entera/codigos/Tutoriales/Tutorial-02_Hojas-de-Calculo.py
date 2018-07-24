"""
Tutorial sobre Importacion y Exportacion de Datos desde Hojas de Calculo
@author: Luis I. Reyes Castro
"""

import numpy as np
import pandas as pd

# Importacion de datos

manija = open( '../Datos/Datos_Tutorial-02.xlsx', 'rb')
df = pd.read_excel( manija, 'Propuestas')
manija.close()

columnas         = [ 'Tiempo Medio', 'Tiempo Parcial', 'Tiempo Completo']
matriz_valores   = df.iloc[0:25][columnas].values
salario_medio    = df.iloc[-1][columnas[0]]
salario_parcial  = df.iloc[-1][columnas[1]]
salario_completo = df.iloc[-1][columnas[2]]

# Exportacion de datos

datos_A = [ 'Jorge', 'Diana', 'Pedro', 'Maria' ]
datos_B = [ ( 'Jorge', 18, 20.8),
            ( 'Diana', 46, 82.1),
            ( 'Pedro', 23, 45.0),
            ( 'Maria', 34, 56.7) ]

datos_C_cols = [ 'Nombre',  'Cualidad-1', 'Cualidad-2', 'Cualidad-3' ]
datos_C      = np.array( [ [ 0.5, 0.7, 7.5 ],
                           [ 1.2, 8.4, 0.2 ],
                           [ 4.8, 0.7, 0.4 ],
                           [ 4.5, 0.2, 1.5 ] ] )

index_A = [ i+1 for (i,_) in enumerate(datos_A) ]
index_B = [ i+1 for (i,_) in enumerate(datos_B) ]
index_C = [ i+1 for (i,_) in enumerate(datos_A) ]

df_A = pd.DataFrame( index = index_A, columns = ['Nombre'] )
df_B = pd.DataFrame( index = index_A,
                     columns = [ 'Nombre', 'Edad', 'Bitcoins'] )
df_A['Nombre']   = datos_A
df_B['Nombre']   = [ elem[0] for elem in datos_B ]
df_B['Edad']     = [ elem[1] for elem in datos_B ]
df_B['Bitcoins'] = [ elem[2] for elem in datos_B ]

df_C = pd.DataFrame( index = index_C, columns = datos_C_cols)
df_C['Nombre'] = datos_A
df_C[ [ 'Cualidad-1', 'Cualidad-2', 'Cualidad-3' ] ] = datos_C

writer = pd.ExcelWriter( 'Hoja-de-calculo_Tutorial-02.xlsx')
df_A.to_excel( writer, sheet_name = 'Juego de Datos A')
df_B.to_excel( writer, sheet_name = 'Juego de Datos B')
df_C.to_excel( writer, sheet_name = 'Juego de Datos C')
writer.close()
