"""
Estatica: Este archivo contiene una clase para modelar y analizar armaduras
estaticamente determinables.

@author: Luis I. Reyes-Castro.

COPYRIGHT

All contributions by Luis I. Reyes-Castro:
Copyright (c) 2018, Luis Ignacio Reyes Castro.
All rights reserved.

LICENSE

The MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import numpy as np
import matplotlib.pyplot as plt

class Armadura2D :
    """
    Modela, resuelve y grafica Armaduras en 2D

    Esta clase permite modelar armaduras estaticamente determinables en 2D
    que esten fijadas al suelo por un soporte empernado y un patin.
    """

    def __init__( self, nodos,
                        miembros,
                        soporte_empernado,
                        patin,
                        tipo_patin,
                        cargas,
                        peso_especifico_miembros = 0.0,
                        verboso = False ) :

        self.nodos      = list( nodos.keys() )
        self.nodos.sort()
        self.n          = len( self.nodos)
        self.pos_nodos  = nodos
        self.miembros   = miembros
        self.m          = len( self.miembros)

        # Verifica el tipo de patin ingresado
        if not tipo_patin in [ 'Horizontal', 'Pared'] :
            raise ValueError( 'No se entiende el tipo de patin! ' +
            'Opciones validas son \'Horizontal\' y \'Pared\'.' )
            return

        # Verifica que la armadura sea estaticamente determinable
        if 2 * self.n == self.m + 3 :
            print( 'CONSTRUYENDO ARMADURA...' )
        elif 2 * self.n < self.m + 3 :
            raise ValueError( 'Armadura no es estaticamente determinable ' +
                              'porque tiene demasiados miembros o muy pocos nodos!' )
        else :
            raise ValueError( 'Armadura no es estaticamente determinable ' +
                              'porque tiene muy pocos miembros o demasiados nodos!' )

        # Elimina miembros repetidos
        miembros_sin_repeticion = []
        for miembro in self.miembros :
            if ( miembro[0], miembro[1]) not in miembros_sin_repeticion and \
               ( miembro[1], miembro[0]) not in miembros_sin_repeticion :
                   miembros_sin_repeticion.append(miembro)
            else :
                print( 'Advertencia: Obviando miembro ' + str(miembro) +
                       ' porque esta repetido' )
        self.miembros = miembros_sin_repeticion

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

            if verboso :
                print( 'Nodo actual:', nodo)

            fila = self.ecuaciones[nodo]

            if nodo == soporte_empernado :
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

                if verboso :
                    print( '\t' + 'Procesando miembro ' +
                           nodo + '-' + nodo_vecino + ':' )
                col  = self.incognitas[ ( nodo, nodo_vecino) ]
                vec  = self.vector_unitario( nodo_vecino, nodo)

                if verboso :
                    print( '\t\t' + 'Direccion de la fuerza:', vec)
                self.mat_A[ fila + 0, col] = vec[0]
                self.mat_A[ fila + 1, col] = vec[1]

                peso_miembros += \
                0.5 * peso_especifico_miembros \
                    * self.longitud_miembro( nodo, nodo_vecino)

            if nodo in cargas :
                if verboso :
                    print( '\t' + 'Procesando carga: ' +
                           str( np.array(cargas[nodo]) ) )
                self.vec_b[ fila + 0 ] = -cargas[nodo][0]
                self.vec_b[ fila + 1 ] = -cargas[nodo][1] + peso_miembros

        print( 'Listo!' )
        return

    def resuelve( self) :

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

        max_com = 0.0
        max_ten = 0.0
        for miembro in self.miembros :
            if self.fuerzas[miembro] > max_com :
                max_com = self.fuerzas[miembro]
            if self.fuerzas[miembro] < max_ten :
                max_ten = self.fuerzas[miembro]

        miembros_max_com = []
        miembros_max_ten = []
        for miembro in self.miembros :
            if abs( self.fuerzas[miembro] - max_com ) < 1E-5 :
                miembros_max_com.append( miembro )
            if abs( self.fuerzas[miembro] - max_ten ) < 1E-5 :
                miembros_max_ten.append( miembro )

        print( 'MIEMBROS CRITICOS:' )

        mensaje = '\t' + 'Maxima compresion esta en '
        if len(miembros_max_com) == 1 :
            mensaje += 'el Miembro ' \
            + miembros_max_com[0][0] + '-' + miembros_max_com[0][1]
        elif len(miembros_max_com) > 1 :
            mensaje += 'los Miembros '
            for miembro in miembros_max_com :
                mensaje += miembro[0] + '-' + miembro[1] + ', '
            mensaje = mensaje[:-2]

        print(mensaje)
        print( '\t\t' + 'Magnitud:', abs(max_com) )

        mensaje = '\t' + 'Maxima tension esta en '
        if len(miembros_max_ten) == 1 :
            mensaje += 'el Miembro ' \
            + miembros_max_ten[0][0] + '-' + miembros_max_ten[0][1]
        elif len(miembros_max_ten) > 1 :
            mensaje += 'los Miembros '
            for miembro in miembros_max_ten :
                mensaje += miembro[0] + '-' + miembro[1] + ', '
            mensaje = mensaje[:-2]

        print(mensaje)
        print( '\t\t' + 'Magnitud:', abs(max_ten) )

        return

    def grafica_solucion( self, tamano_figura_en_pulgadas = 8,
                                tamano_nodos = 8,
                                ancho_miembros = 3.0 ) :

        fuerza_max = np.max( np.abs( self.x) )

        nodos_x = [ self.pos_nodos[nodo][0] for nodo in self.nodos ]
        nodos_y = [ self.pos_nodos[nodo][1] for nodo in self.nodos ]
        delta_x = max(nodos_x) - min(nodos_x)
        delta_y = max(nodos_y) - min(nodos_y)

        x_min = min(nodos_x) - 0.1 * delta_x
        x_max = max(nodos_x) + 0.1 * delta_x
        y_min = min(nodos_y) - 0.1 * delta_y
        y_max = max(nodos_y) + 0.1 * delta_y

        tamano_figura = ( tamano_figura_en_pulgadas,
                          tamano_figura_en_pulgadas )
        plt.figure( figsize = tamano_figura, dpi = 90)
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
