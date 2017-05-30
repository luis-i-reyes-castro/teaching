# -*- coding: utf-8 -*-
"""
Taller de Analisis de Estructuras de Vigas Ideales
Funciones para graficar las soluciones
@author: Luis I. Reyes Castro
"""

# Importamos las funciones del modulo matplotlib.pyplot
import matplotlib.pyplot as plt

# Funcion para graficar las fuerzas dentro de la estructura (ejemplo)
def graficar_solucion_01( ind_var, vector_x) :
    # -----------------------------------------------------------------------------------------
    LINEWIDTH           = 3.0
    MARKERSIZE          = 8
    F_MAX = max( [ abs(vector_x.max()), abs(vector_x.min()) ] )
    # -----------------------------------------------------------------------------------------    
    x = { }; y = { }
    x['13'] = [ 0.0, 1.0]; y['13'] = [ 0.0, 1.0]
    x['34'] = [ 0.0, 1.0]; y['34'] = [ 0.0, 0.0]
    x['14'] = [ 1.0, 1.0]; y['14'] = [ 0.0, 1.0]
    x['12'] = [ 1.0, 2.0]; y['12'] = [ 1.0, 1.0]
    x['45'] = [ 1.0, 2.0]; y['45'] = [ 0.0, 0.0]
    x['15'] = [ 1.0, 2.0]; y['15'] = [ 1.0, 0.0]
    x['25'] = [ 2.0, 2.0]; y['25'] = [ 1.0, 0.0]
    x['56'] = [ 2.0, 3.0]; y['56'] = [ 0.0, 0.0]
    x['26'] = [ 2.0, 3.0]; y['26'] = [ 1.0, 0.0]
    # -----------------------------------------------------------------------------------------
    plt.figure()
    plt.axis('equal')
    plt.xlim( -0.5, +3.5); plt.ylim( -0.5, +1.5)    
    # -----------------------------------------------------------------------------------------
    for viga in x :
        col_viga = [ 0.50, 0.0, 0.50]
        fuerza = vector_x[ ind_var[ 'F_' + viga ] ]
        if fuerza > 0.0001 :
            col_viga[0] += 0.50 * ( +fuerza / F_MAX )
        elif vector_x[ ind_var[ 'F_' + viga ] ] < 0.0001 :
            col_viga[2] += 0.50 * ( -fuerza / F_MAX )
        plt.plot( x[viga], y[viga], linestyle = '-', linewidth = LINEWIDTH, color = col_viga, \
                  marker = 'o', markerfacecolor = 'black', \
                  markeredgecolor = 'None', markersize = MARKERSIZE )
    # -----------------------------------------------------------------------------------------
    plt.show()
