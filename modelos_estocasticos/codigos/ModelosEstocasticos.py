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
            print( 'X_' + str(t) + ': ' + self.S[X[t]] )

        # Retorna la secuencia de indices de estados
        return X

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

    def muestrea_secuencia( self, inicio, num_pasos) :
        """
        Muestrea aleatoriamente una secuencia de estados de acuerdo a la
        matriz de transicion de la cadena por un numero de pasos deseado

        @param inicio: Inicio de la secuencia. Puede ser un estado, el indice de
                       un estado, o una distribucion del estado inicial.
                       Si es un estado debe encontrarse en la lista de estados,
                       caso contrario se arrojara un error. Si es el indice de
                       un estado debe ser un entero entre cero y n-1.
                       Si es una distribucion debe ser un arreglo numpy de
                       tamano (n,) que sea un vector de probabilidad.
        @param num_pasos: Numero de pasos a muestrear.

        @return Una lista de longitud num_pasos conteniendo los indices de
                los estados muestreados.
        """

        # Verifica que se haya provisto un estado o distribucion inicial
        if inicio is None :
            raise ValueError( 'Provea un estado o distribucion inicial' )
        # Ejecuta si inicio es el indice del estado inicial
        if isinstance( inicio, int) and 0 <= inicio < self.n :
            indice_estado = inicio
        # Ejecuta si inicio es un vector de probabilidades iniciales
        elif isinstance( inicio, np.ndarray) :
            tamano_correcto = ( self.n,)
            if not np.shape(inicio) == tamano_correcto :
                raise ValueError( 'Parametro inicio debe ser un arreglo numpy ' +
                                  'de tamano ' + str(tamano_correcto) )
            if np.any( inicio < 0.0 ) or abs( np.sum(inicio) - 1.0 ) > 1e-8 :
                raise ValueError( 'Parametro inicio debe ser un vector de ' +
                                  'probabilidades' )
            indice_estado = np.random.choice( self.n, p = inicio)
        else :
            # Intenta buscar 'inicio' entre los estados y obtener su indice
            try :
                indice_estado = int( self.S.index(inicio) )
            except Exception :
                raise ValueError( 'Estado inicial \'' + str(inicio) + '\' no existe' )

        # Imprime mensaje de inicio
        print( 'Muestreando una secuencia de ' + str(num_pasos) + ' pasos' )

        # Inicializa la historia arbitrariamente para evitar alocaciones de
        # memoria durante el muestreo
        X = [ 0 for t in range(num_pasos) ]

        # Para cada iteracion...
        for t in range(num_pasos) :
            # Registra el estado actual y lo imprime
            X[t] = self.S[indice_estado]
            print( 'X_' + str(t) + ': ' + X[t] )
            # Obtiene el vector de probabilidades de transicion asociadas
            # con el estado actual
            prob_transicion = self.P[ indice_estado, :]
            # Muestrea el indice del siguiente estado
            indice_estado = np.random.choice( self.n, p = prob_transicion)

        # Retorna la secuencia de indices de estados visitados
        return X

    def propaga_distribucion( self, distribucion, num_pasos) :
        """
        Propaga una distribucion del estado inicial por un numero de pasos deseado

        @param distribucion: Distribucion del estado inicial. Debe ser un arreglo numpy
                             de tamano (n,) que sea un vector de probabilidad.
        @param num_pasos: Numero de pasos a muestrear.

        @return Una lista de longitud num_pasos conteniendo las distribuciones
                deseadas como vectores de probabilidad
        """

        # Verifica que la distribucion sea un arreglo numpy
        if not isinstance( distribucion, np.ndarray) :
            raise ValueError( 'Parametro distribucion debe ser un arreglo numpy ' )
        # Verifica que la distribucion sea un vector de tamano n
        tamano_correcto = ( self.n,)
        if not np.shape( distribucion) == tamano_correcto :
            raise ValueError( 'Parametro distribucion debe ser un arreglo numpy ' +
                              'de tamano ' + str(tamano_correcto) )
        if np.any( distribucion < 0.0 ) or abs( np.sum(distribucion) - 1.0 ) > 1e-8 :
            raise ValueError( 'Parametro distribucion debe ser un vector de ' +
                              'probabilidades' )

        # Imprime mensaje de inicio
        print( 'Propagando una distribucion por ' + str(num_pasos) + ' pasos' )

        # Inicializa la historia arbitrariamente para evitar alocaciones de
        # memoria durante el muestreo
        pi = [ 0 for t in range(num_pasos) ]

        # Para cada iteracion...
        for t in range(num_pasos) :
            # Registra la distribucion actual y la imprime
            pi[t] = distribucion
            print( 'pi_' + str(t) + ': ' + pi[t] )
            # Computa la distribucion del siguiente estado
            distribucion = np.dot( distribucion, self.P).flatten()

        # Retorna la secuencia de distribuciones computadas
        return pi
