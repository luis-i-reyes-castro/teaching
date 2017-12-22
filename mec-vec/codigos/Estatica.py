#!/usr/bin/env python3
"""
Estatica: Este archivo contiene algunas clases para modelar y analizar
estructuras estaticamente determinables.

@author: Luis I. Reyes-Castro.
"""

import numpy as np
import matplotlib.pyplot as plt

class Armadura2D :
    """
    Modela y resuelve Armaduras en 2D
    """

    def __init__( self, nodos, miembros, perno, patin, tipo_patin,
                  cargas, peso_miembros_por_unidad_longitud = 0.0 ) :

        self.nodos      = list( nodos.keys() )
        self.nodos.sort()
        self.n          = len( self.nodos)
        self.pos_nodos  = nodos
        self.miembros   = miembros
        self.m          = len( self.miembros)

        # Verifica que el tipo de patin
        if not tipo_patin in [ 'Horizontal', 'Pared'] :
            print( 'Error: No se entiende el tipo de patin!' )
            return

        # Verifica que la armadura sea estaticamente determinable
        if 2 * self.n == self.m + 3 :
            print( 'CONSTRUYENDO ARMADURA...' )
        else :
            raise ValueError( 'Armadura no es estaticamente determinable!' )

        # Declaramos un diccionario de ecuaciones
        self.ecuaciones = {}
        for ( indice, nodo) in enumerate( self.nodos) :
            self.ecuaciones[nodo] = 2 * indice

        # Declaramos un diccionario de incognitas
        self.incognitas = { 'Perno_x' : 0, 'Perno_y' : 1, 'Patin' : 2 }
        for ( indice, miembro) in enumerate( self.miembros) :
            self.incognitas[ ( miembro[0], miembro[1] ) ] = 3 + indice
            self.incognitas[ ( miembro[1], miembro[0] ) ] = 3 + indice

        # Declaramos la matriz A y el vector b para el sistema A * x = b
        self.mat_A = np.zeros( shape = ( 2 * self.n, 2 * self.n) )
        self.vec_b = np.zeros( shape = ( 2 * self.n, ) )

        # Poblamos la matriz A y el vector b
        for ( i, nodo) in enumerate( self.nodos) :

            print( 'Nodo actual:', nodo)

            fila = self.ecuaciones[nodo]

            if nodo == perno :
                col = self.incognitas['Perno_x']
                self.mat_A[ fila + 0, col] = 1.0
                col = self.incognitas['Perno_y']
                self.mat_A[ fila + 1, col] = 1.0

            elif nodo == patin :
                col = self.incognitas['Patin']
                if tipo_patin == 'Horizontal' :
                    self.mat_A[ fila + 1, col] = 1.0
                else :
                    self.mat_A[ fila + 0, col] = 1.0

            vecinos       = self.nodos_vecinos( nodo)
            peso_miembros = 0.0
            for ( j, nodo_vecino) in enumerate( vecinos) :
                print( '\t' + 'Procesando miembro ' + nodo + '-' + nodo_vecino + ':' )
                col  = self.incognitas[ ( nodo, nodo_vecino) ]
                vec  = self.vector_unitario( nodo_vecino, nodo)
                print( '\t\t' + 'Direccion de la fuerza:', vec)
                self.mat_A[ fila + 0, col] = vec[0]
                self.mat_A[ fila + 1, col] = vec[1]
                peso_miembros += 0.5 * self.longitud_miembro( nodo, nodo_vecino) \
                              * peso_miembros_por_unidad_longitud

            if nodo in cargas :
                print( '\t' + 'Procesando carga: ' + str(np.array(cargas[nodo])) )
                self.vec_b[ fila + 0 ] = -cargas[nodo][0]
                self.vec_b[ fila + 1 ] = -cargas[nodo][1] + peso_miembros

        print( 'Listo!' )
        return

    def nodos_vecinos( self, nodo) :

        vecinos = []
        for miembro in self.miembros :
            if miembro[0] == nodo :
                vecinos.append( miembro[1] )
            elif miembro[1] == nodo :
                vecinos.append( miembro[0] )

        return vecinos

    def vector_unitario( self, nodo_i, nodo_f) :

        pos_i     = np.array( self.pos_nodos[nodo_i] )
        pos_f     = np.array( self.pos_nodos[nodo_f] )
        delta_pos = pos_f - pos_i

        return ( 1.0 / np.linalg.norm(delta_pos) ) * delta_pos

    def longitud_miembro( self, nodo_i, nodo_f) :

        pos_i = np.array( self.pos_nodos[nodo_i] )
        pos_f = np.array( self.pos_nodos[nodo_f] )

        return np.linalg.norm( pos_f - pos_i )


    def resuelve( self, grafica = False) :

        print( 'RESOLVIENDO ARMADURA...' )
        self.x = np.linalg.solve( self.mat_A, self.vec_b)

        self.fuerzas = {}
        for miembro in self.miembros :
            fuerza = self.x[ self.incognitas[miembro] ]
            self.fuerzas[miembro] = fuerza if abs(fuerza) > 1E-6 else 0.0

        print( 'Listo!' )
        return

    def imprime_solucion( self) :

        print( 'ANALISIS DE LA ARMADURA:' )

        print( 'REACCIONES:' )
        print( '\t' + 'Perno_x:', self.x[ self.incognitas['Perno_x'] ] )
        print( '\t' + 'Perno_y:', self.x[ self.incognitas['Perno_y'] ] )
        print( '\t' + 'Patin:',   self.x[ self.incognitas['Patin'] ] )

        print( 'FUERZAS INTERNAS:' )
        for miembro in self.miembros :
            nom_miembro = \
            '\t' + 'Miembro ' + miembro[0] + '-' + miembro[1] + ':'
            magnitud = abs( self.fuerzas[miembro] )
            signo    = ''
            if self.fuerzas[miembro] > 0 :
                signo += 'compresion'
            elif self.fuerzas[miembro] < 0 :
                signo = 'tension'
            print( nom_miembro, magnitud, signo)

        return

    def grafica_solucion( self, tamano_nodos = 8, ancho_miembros = 3.0) :

        fuerza_max = np.max( np.abs( self.x) )

        nodos_x = [ self.pos_nodos[nodo][0] for nodo in self.nodos ]
        nodos_y = [ self.pos_nodos[nodo][1] for nodo in self.nodos ]
        delta_x = max(nodos_x) - min(nodos_x)
        delta_y = max(nodos_y) - min(nodos_y)

        x_min = min(nodos_x) - 0.1 * delta_x
        x_max = max(nodos_x) + 0.1 * delta_x
        y_min = min(nodos_y) - 0.1 * delta_y
        y_max = max(nodos_y) + 0.1 * delta_y


        plt.figure( figsize = ( 10, 5), dpi = 90)
        plt.axis( 'square' )
        plt.xlim( ( x_min, x_max) )
        plt.ylim( ( y_min, y_max) )

        for miembro in self.miembros :

            pos_i     = list( self.pos_nodos[ miembro[0] ] )
            pos_f     = list( self.pos_nodos[ miembro[1] ] )
            arreglo_x = ( pos_i[0], pos_f[0])
            arreglo_y = ( pos_i[1], pos_f[1])

            fuerza_rel = self.fuerzas[miembro] / fuerza_max
            color      = [ 0.35, 0.35, 0.35]

            color[1] += ( 1.0 - color[1]) / ( 1.0 + 10 * abs(fuerza_rel) )

            if fuerza_rel > 0 :
                color[0] += ( 1.0 - color[0] ) * abs(fuerza_rel)
                color[2] /= 1.0 + 10 * abs(fuerza_rel)
            elif fuerza_rel < 0 :
                color[2] += ( 1.0 - color[2] ) * abs(fuerza_rel)
                color[0] /= 1.0 + 10 * abs(fuerza_rel)

            plt.plot( arreglo_x, arreglo_y, linestyle = '-',
                      linewidth = ancho_miembros, color = color,
                      marker = 'o', markerfacecolor = 'black',
                      markeredgecolor = 'None', markersize = tamano_nodos)

        plt.show()

        return
