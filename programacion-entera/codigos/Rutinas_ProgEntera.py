"""
Rutinas Utiles para Programacion Entera
@author: Luis I. Reyes Castro
"""

import pandas as pd

def importar_excel( nombre_archivo, hoja_de_calculo) :

    manija = open( nombre_archivo, 'rb')
    df = pd.read_excel( manija, hoja_de_calculo, index_col = 0)
    manija.close()

    return df
