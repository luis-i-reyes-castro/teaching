"""
@author Luis I. Reyes Castro, M.Sc.
        Facultad de Ingenieria en Mecanica y Ciencias de la Produccion (FIMCP)
        Escuela Superior Politecnica del Litoral

Implementaciones de los modelos vistos en mi curso de Modelos Estocasticos
para Manufactura y Servicios (INDG-1008).

"""

import numpy as np

class ProcesoBernoulli :
    """
    Implementa las principales funciones de un proceso Bernoulli.
    """

    # Miembros:
    S = []
    p = 0.5 # parametro

    def __init__( self, estados, parametro) :
        """
        Constructor

        @param estados: Lista conteniendo los dos posibles estados
        @param parametro: Parametro del proceso Bernoulli
        """

        # Verifica y copia la lista de los dos estados posibles
        if not isinstance( estados, list) or len(estados) != 2 :
            raise ValueError( 'Parametro estados debe ser una lista de ' +
                              'longitud exactamente igual a dos' )
        else :
            self.S = estados

        # Verifica y copia el valor del parametro del proceso
        if not ( 0 < parametro < 1 ) :
            raise ValueError( 'Parametro del proceso debe estar entre cero y uno' )
        else :
            self.p = parametro

        return

    def muestrea( self, num_pasos) :
        """
        Muestrea aleatoriamente del proceso por un numero de pasos deseado

        @param num_pasos: Numero de pasos a muestrear.

        @return Una lista de longitud num_pasos conteniendo los indices de
                los estados muestreados.
        """

        # Imprime mensaje de inicio
        print( 'Muestreando una secuencia de ' + str(num_pasos) + ' pasos' )

        # Muestrea num_pasos variables aleatorias Uniforme(0,1)
        U = np.random.random_sample(num_pasos)
        # Genera variables Bernoulli usando las variables uniformes
        X = np.where( U < self.p, 0, 1)

        # Imprime la secuencia de estados
        for t in range(num_pasos) :
            print( 'X_' + str(t) + ': ' + str( self.S[X[t]] ) )

        # Computa el vector de frecuencias
        frequencia = np.zeros( shape = (2,) )
        frequencia[1] = 1.0 * sum(X) / num_pasos
        frequencia[0] = 1 - frequencia[1]

        # Retorna la secuencia de indices de estados y las frecuencias de visita
        return ( X, frequencia)

    def divide_proceso( self, probabilidades) :
        """
        Divide al proceso de acuerdo al vector de probabilidades ingresado

        @param probabilidades: Vector de probabilidades

        @return Lista de los n procesos Bernoulli resultantes, donde n es la
        longitud del vector de probabilidades ingresado
        """

        # Verifica que el vector de probabilidades sea valido
        if not isinstance( probabilidades, ( list, tuple, np.ndarray) ) :
            raise ValueError( 'Parametro inicio debe ser una lista, tupla ' +
                              'o vector numpy' )

        # Verifica que la distribucion sea un vector de tamano n
        probabilidades = np.array( probabilidades).flatten()
        if np.any( probabilidades < 0.0 ) \
        or abs( np.sum(probabilidades) - 1.0 ) > 1e-8 :
            raise ValueError( 'Parametro inicio debe ser un vector de ' +
                              'probabilidades' )

        # Crea cada uno de los procesos
        procesos = []
        for ( i, _) in enumerate(probabilidades) :
            nuevo_proceso = ProcesoBernoulli( self.S, probabilidades[i] * self.p)
            procesos.append( nuevo_proceso )

        # Crea los dos procesos
        return procesos

class CadenaDeMarkov :
    """
    Implementa las principales funciones de una Cadena de Markov.
    """

    # Miembros
    S = [] # lista de estados
    n = 0  # numero de estados
    P = np.array([]) # matriz de transicion

    def __init__( self, estados, matriz_transicion) :
        """
        Constructor

        @param estados: Lista de estados. Los elementos de la lista pueden ser
                        literalmente cualquier objeto de python, pero recomiendo
                        usar cadenas de caracteres (i.e. strings).
        @param matriz_P: Matriz de transicion. Debe ser un arreglo numpy
                         de tamano (n,n), donde n es el numero de estados.
        """

        # Verifica que el parametro estados sea una lista no-vacia
        if not isinstance( estados, list) :
            raise ValueError( 'Parametro estados debe ser una lista' )
        if len(estados) < 2 :
            raise ValueError( 'Numero de estados debe ser al menos dos' )

        # Copia los estados ingresados y los cuenta
        self.S = estados
        self.n = len(estados)

        # Verifica que el parametro matriz de transicion sea un arreglo numpy
        if not isinstance( matriz_transicion, np.ndarray) :
            raise ValueError( 'Matriz de transicion debe ser un arreglo numpy' )

        # Verifica que la matriz de transicion tenga tamano n-por-n
        tamano_correcto = ( self.n, self.n)
        if not np.shape( matriz_transicion) == tamano_correcto :
            raise ValueError( 'Matriz de transicion debe ser un arreglo numpy ' +
                              'de tamano ' + str(tamano_correcto) )
        # Verifica cada fila de la matriz de transicion
        for fila in range(self.n) :
            # avisa si alguna entrada es negativa
            cols_malas = matriz_transicion[fila,:] < 0.0
            if np.any( cols_malas) :
                todas_cols = np.arange(self.n)
                cols_malas = todas_cols[cols_malas]
                raise ValueError( 'Matriz de transicion tiene entradas negativas ' +
                                  'en la fila ' + str(fila) + ' columnas ' +
                                  tuple(cols_malas) )
            # avisa si la suma de las  entradas es diferente de uno
            suma_entradas = np.sum( matriz_transicion[fila,:] )
            if abs( suma_entradas - 1.0 ) > 1E-8 :
                raise Warning( 'Matriz de transicion tiene fuga o exceso de ' +
                               'probabilidad en la fila ' + str(fila) )

        # Copia la matriz de transicion ingresada
        self.P = matriz_transicion

        return

    def contenidos( self) :
        """
        Retorna todos los contenidos del objeto como un diccionario

        @return Diccionario del objeto
        """
        return self.__dict__

    def muestrea( self, inicio, num_pasos) :
        """
        Muestrea aleatoriamente una secuencia de estados de acuerdo a la
        matriz de transicion de la cadena por un numero de pasos deseado

        @param inicio: Inicio de la secuencia. Puede ser un estado, el indice de
                       un estado, o una distribucion del estado inicial.
                       Si es un estado debe encontrarse en la lista de estados,
                       caso contrario se arrojara un error. Si es el indice de
                       un estado debe ser un entero entre cero y n-1.
                       Si es una distribucion debe ser un arreglo de
                       tamano (n,) que sea un vector de probabilidad.
        @param num_pasos: Numero de pasos a muestrear.

        @return Una 2-tupla que contiene en su primera entrada una lista de
        longitud num_pasos conteniendo los indices de los estados muestreados y
        en su segunda entrada el vector de frecuencias de visitas a estados.
        """

        # Verifica que se haya provisto un estado o distribucion inicial
        if inicio is None :
            raise ValueError( 'Provea un estado o distribucion inicial' )

        # Si inicio es el indice del estado inicial solo lo copiamos
        if isinstance( inicio, int) and 0 <= inicio < self.n :
            indice_estado = inicio

        # Si inicio no es una lista, tupla o vector busca su indice
        elif not isinstance( inicio, ( list, tuple, np.ndarray) ) :
            try :
                indice_estado = int( self.S.index(inicio) )
            except Exception :
                raise ValueError( 'Estado \'' + str(inicio) + '\' no existe' )

        # Si inicio es un vector de probabilidades iniciales entonces
        # usalo para muestrear el estado inicial
        else :
            inicio = np.array(inicio)
            tamano_correcto = ( self.n,)
            if not np.shape(inicio) == tamano_correcto :
                raise ValueError( 'Parametro inicio debe ser un arreglo ' +
                                  'de tamano ' + str(tamano_correcto) )
            if np.any( inicio < 0.0 ) or abs( np.sum(inicio) - 1.0 ) > 1e-8 :
                raise ValueError( 'Parametro inicio debe ser un vector de ' +
                                  'probabilidades' )
            indice_estado = np.random.choice( self.n, p = inicio)

        # Imprime mensaje de inicio
        print( 'Muestreando una secuencia de ' + str(num_pasos) + ' pasos' )

        # Inicializa la historia arbitrariamente para evitar alocaciones de
        # memoria durante el muestreo
        X = [ 0 for t in range(num_pasos) ]

        # Para cada iteracion...
        for t in range(num_pasos) :
            # Registra el estado actual y lo imprime
            X[t] = indice_estado
            print( 'X_' + str(t) + ': ' + self.S[X[t]] )
            # Obtiene el vector de probabilidades de transicion asociadas
            # con el estado actual
            prob_transicion = self.P[ indice_estado, :]
            # Muestrea el indice del siguiente estado
            indice_estado = np.random.choice( self.n, p = prob_transicion)

        # Computa el vector de frecuencias de visitas a estados
        frequencia = np.zeros( shape = ( self.n,) )
        for estado in range(self.n) :
            visitas = [ 1.0 if X[t] == estado else 0.0 for t in range(num_pasos) ]
            frequencia[estado] = sum(visitas) / num_pasos

        # Retorna la secuencia de indices de estados visitados y el vector
        # de frecuencias de visitas a estados
        return ( X, frequencia)

    def propaga_distribucion( self, inicio, num_pasos) :
        """
        Propaga una distribucion del estado inicial por un numero de pasos deseado

        @param inicio: Distribucion del estado inicial. Debe ser un arreglo
                       de tamano (n,) que sea un vector de probabilidad.
        @param num_pasos: Numero de pasos a propagar.

        @return Una matriz numpy de tamano num_pasos-por-n donde la entrada (t,i)
        es la probabilidad en el periodo t de estar en el estado i.
        """

        # Verifica que la distribucion sea un arreglo numpy
        if not isinstance( inicio, ( list, tuple, np.ndarray) ) :
            raise ValueError( 'Parametro inicio debe ser una lista, tupla ' +
                              'o vector numpy' )

        # Verifica que la distribucion sea un vector de tamano n
        inicio = np.array(inicio)
        tamano_correcto = ( self.n,)
        if not np.shape( inicio) == tamano_correcto :
            raise ValueError( 'Parametro inicio debe ser un arreglo ' +
                              'de tamano ' + str(tamano_correcto) )
        if np.any( inicio < 0.0 ) or abs( np.sum(inicio) - 1.0 ) > 1e-8 :
            raise ValueError( 'Parametro inicio debe ser un vector de ' +
                              'probabilidades' )

        # Inicializa la historia arbitrariamente para evitar alocaciones de
        # memoria durante el muestreo
        pi = np.zeros( shape = ( num_pasos, self.n) )
        pi[-1,:] = inicio

        # Para cada iteracion...
        for t in range(num_pasos) :
            # Computa la distribucion actual de acuerdo a la recursion:
            # pi_t+1' = pi_t' * P
            pi[t,:] = np.dot( pi[t-1,:], self.P).flatten()

        # Retorna la secuencia de distribuciones computadas
        return pi
