"""
Tutorial sobre Importacion y Exportacion de Datos desde Hojas de Calculo
@author: Luis I. Reyes Castro
"""

import numpy as np
import pandas as pd

# Importacion de datos

manija = open( '../Datos/Datos_Tutorial-02.xlsx', 'rb')
df = pd.read_excel( manija, 'Propuestas', index_col = 0)
manija.close()

columnas = [ 'Tiempo Medio', 'Tiempo Parcial', 'Tiempo Completo']
matriz_D = df.iloc[0:-1][columnas].values.astype( np.float)
vector_c = df.iloc[-1][columnas].values.astype( np.float)

# Exportacion de datos

datos_A_cols   = [ 'Nombre' ]
datos_A        = [ 'Jorge', 'Diana', 'Pedro', 'Maria' ]
index_A        = [ i+1 for (i,_) in enumerate(datos_A) ]
df_A           = pd.DataFrame( index = index_A, columns = datos_A_cols)
df_A['Nombre'] = datos_A

datos_B_cols     = [ 'Nombre', 'Edad', 'Bitcoins' ]
datos_B          = [ ( 'Jorge', 18, 20.8),
                     ( 'Diana', 46, 82.1),
                     ( 'Pedro', 23, 45.0),
                     ( 'Maria', 34, 56.7) ]
index_B          = [ i+1 for (i,_) in enumerate(datos_B) ]
df_B             = pd.DataFrame( index = index_A, columns = datos_B_cols)
df_B['Nombre']   = [ elem[0] for elem in datos_B ]
df_B['Edad']     = [ elem[1] for elem in datos_B ]
df_B['Bitcoins'] = [ elem[2] for elem in datos_B ]

datos_C_cols   = [ 'Nombre',  'Cualidad-1', 'Cualidad-2', 'Cualidad-3' ]
datos_C        = datos_A
datos_C_extra  = np.array( [ [ 0.5, 0.7, 7.5 ],
                             [ 1.2, 8.4, 0.2 ],
                             [ 4.8, 0.7, 0.4 ],
                             [ 4.5, 0.2, 1.5 ] ] )
index_C        = [ i+1 for (i,_) in enumerate(datos_C) ]
df_C           = pd.DataFrame( index = index_C, columns = datos_C_cols)
df_C['Nombre'] = datos_C
df_C[ datos_C_cols[1:] ] = datos_C_extra

writer = pd.ExcelWriter( 'Hoja-de-calculo_Tutorial-02.xlsx')
df_A.to_excel( writer, sheet_name = 'Juego de Datos A')
df_B.to_excel( writer, sheet_name = 'Juego de Datos B')
df_C.to_excel( writer, sheet_name = 'Juego de Datos C')
writer.close()
