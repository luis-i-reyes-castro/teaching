"""
Implementaciones de los modelos vistos en mi curso de Modelos Estocasticos
para Manufactura y Servicios (INDG-1008).

@author Luis I. Reyes Castro, M.Sc.
        Facultad de Ingenieria en Mecanica y Ciencias de la Produccion (FIMCP)
        Escuela Superior Politecnica del Litoral

"""

import numpy as np

class CadenaDeMarkov :
    """
    Implementa las principales funciones de una Cadena de Markov.
    """

    def __init__( self, estados, matriz_transicion) :
        """
        Constructor

        @param estados: Lista de estados, donde cada estado es representado por
                        una cadena de caracteres (i.e. un tipo string).
        @param matriz_P: Matriz de transicion. Debe ser un arreglo numpy
                         de tamano (n,n), donde n es el numero de estados.
        """

        # Copia los datos ingresados
        self.S = estados
        self.n = len(estados)
        self.P = matriz_transicion

        # Verifica que el parametro estados sea una lista no-vacia
        if not isinstance( estados, list) :
            raise ValueError( 'Parametro estados debe ser una lista' )
        if len(estados) < 2 :
            raise ValueError( 'Numero de estados debe ser al menos dos' )

        # Verifica que el parametro matriz de transicion sea un arreglo numpy
        if not isinstance( matriz_transicion, np.ndarray) :
            raise ValueError( 'Matriz de transicion debe ser un arreglo numpy' )

        # Verifica que la matriz de transicion tenga tamano n-por-n
        tamano_correcto = ( self.n, self.n)
        if not np.shape( matriz_transicion) == tamano_correcto :
            raise ValueError( 'Matriz de transicion debe ser un arreglo numpy ' +
                              'de tamano ' + str(tamano_correcto) )

        # Verifica que cada fila de la matriz de transicion corresponda a
        # una distribucion valida
        for fila in range( self.n) :
            # Avisa si alguna entrada es negativa
            cols_malas = matriz_transicion[fila,:] < 0.0
            if np.any( cols_malas) :
                todas_cols = np.arange( self.n)
                cols_malas = todas_cols[cols_malas]
                raise ValueError( 'Matriz de transicion tiene entradas negativas ' +
                                  'en la fila ' + str(fila) + ' columnas ' +
                                  tuple(cols_malas) )
            # Avisa si la suma de las  entradas es diferente de uno
            suma_entradas = np.sum( matriz_transicion[fila,:] )
            if abs( suma_entradas - 1.0 ) > 1E-8 :
                raise Warning( 'Matriz de transicion tiene fuga o exceso de ' +
                               'probabilidad en la fila ' + str(fila) )

        return

    def contenidos( self) :
        """
        Retorna los contenidos como un diccionario.

        @return Diccionario que contiene dos entradas: 'estados' contiene una
        lista de los estados, 'matriz_transicion' contiene la matriz de transicion
        como arreglo numpy.
        """

        return { 'estados' : self.S, 'matriz_transicion' : self.P }

    def muestrea( self, inicio, num_pasos) :
        """
        Muestrea aleatoriamente una secuencia de estados

        @param inicio: Inicio de la secuencia. Puede ser un estado, el indice de
                       un estado, o una distribucion del estado inicial.
                       Si es un estado debe encontrarse en la lista de estados.
                       Si es el indice de un estado debe ser un entero entre
                       cero y n-1. Si es una distribucion debe ser un
                       diccionario de estados a probabilidades, aunque puede
                       ser disperso, i.e. solo se requiere especificar
                       los estados con probabilidades estrictamente positivas.
        @param num_pasos: Numero de pasos a muestrear.

        @return Una 2-tupla que contiene en su primera entrada la secuencia de
                estados muestreada y en su segunda entrada el diccionario de
                frecuencias de visitas a estados de la muestra.
        """

        # Inicializa la historia de estados arbitrariamente para evitar
        # alocaciones de memoria durante el muestreo
        X = [ 0 for t in range(num_pasos) ]

        # Si inicio es un estado entonces obtenemos su indice
        if inicio in self.S :
            X[-1] = int( self.S.index(inicio) )

        # Si inicio es el indice del estado inicial solo lo copiamos
        elif isinstance( inicio, int) and 0 <= inicio < self.n :
            X[-1] = inicio

        # Si inicio es un diccionario de probabilidades entonces muestreamos
        # el estado inicial
        elif isinstance( inicio, dict) :
            pi_0 = np.zeros( shape = ( self.n,) )
            for ( i, estado) in self.S :
                if estado in inicio :
                    pi_0[i] += inicio[estado]
            if np.any( pi_0 < 0.0 ) or abs( np.sum(pi_0) - 1.0 ) > 1E-6 :
                raise ValueError( 'Parametro inicio no representa una ' +
                                  'distribucion valida!' )
            X[-1] = np.random.choice( self.n, p = pi_0)
        else :
            raise ValueError( 'Parametro inicio no se entiende!' )

        # Para cada paso...
        for t in range(num_pasos) :
            # Extrae la fila de la matriz de transicion asociada con el
            # estado anterior
            prob_transicion = self.P[ X[t-1], :]
            # Muestrea el indice del estado actual
            X[t] = np.random.choice( self.n, p = prob_transicion)

        # Construye la secuencia de estados visitados
        estados_visitados = [ self.S[ X[t] ] for t in range(num_pasos) ]

        # Construye el diccionario de frecuencias de visitas a estados
        frequencias = { estado : 0.0 for estado in self.S }
        for estado in estados_visitados :
            frequencias[estado] += 1.0 / num_pasos

        return ( estados_visitados, frequencias)

    def propaga_distribucion( self, inicio, num_pasos) :
        """
        Propaga la distribucion del estado inicial

        @param inicio: Distribucion del estado inicial como un diccionario de
                       estados a probabilidades. Puede ser un diccionario
                       disperso, i.e. solo se requiere especificar
                       los estados con probabilidades estrictamente positivas.
        @param num_pasos: Numero de pasos a propagar.

        @return Una matriz numpy de tamano ( num_pasos, n) cuya entrada (t,i)
                es la probabilidad en el periodo t de estar en el estado i.
        """

        # Costruye el vector de distribucion inicial a partir del diccionario
        if isinstance( inicio, dict ) :
            pi_t = np.zeros( shape = ( self.n,) )
            for ( i, estado) in enumerate(self.S) :
                if estado in inicio :
                    pi_t[i] += inicio[estado]
            if np.any( pi_t < 0.0 ) or abs( np.sum(pi_t) - 1.0 ) > 1E-6 :
                raise ValueError( 'Parametro inicio no representa una ' +
                                  'distribucion valida!' )
        else :
            raise ValueError( 'Parametro inicio debe ser un diccionario!' )

        # Para cada iteracion...
        for t in range(num_pasos) :
            # Computa la distribucion actual de acuerdo a la recursion:
            # pi_t+1' = pi_t' * P
            pi_t = np.dot( pi_t, self.P).flatten()

        # Formatea la distribucion final como un diccionario y la retorna
        pi_t_diccionario = { estado : 0.0 for estado in self.S }
        for ( i, estado) in enumerate(self.S) :
            pi_t_diccionario[estado] = pi_t[i]

        return pi_t_diccionario

    def distribucion_estacionaria( self) :
        """
        Si la cadena es ergodica, computa la distribucion estacionaria.

        @return Si la cadena es ergodica, la distribucion estacionaria
                como un diccionario; caso contrario, se imprime un mensaje
                indicando que la cadena no es ergodica y se retorna None.
        """

        # Declara la matriz del lado izquierdo A = P' - I
        matriz_A = self.P.transpose() - np.identity( self.n)
        # Declara el vector del lado derecho b = 0
        vector_b = np.zeros( shape = ( self.n,) )

        # Reemplaza la ultima fila de matriz_A con unos
        matriz_A[ -1, :] = 1.0
        # Reemplaza la ultima entrada de vector_b con uno
        vector_b[ -1]    = 1.0

        # Computa la distribucion estacionaria
        try :
            vector_pi = np.linalg.solve( matriz_A, vector_b)
        except np.linalg.LinAlgError :
            print( 'Esta cadena no es ergodica!' )
            return None

        # Construye el diccionario de la distribucion estacionaria
        pi_estrella = {}
        for ( i, estado) in enumerate(self.S) :
            pi_estrella[estado] = vector_pi[i]

        return pi_estrella

    def tiempo_esperado_de_retorno( self) :
        """
        Si la cadena es ergodica, computa la el tiempo esperado de retorno
        a cada estado.

        @return Si la cadena es ergodica, el tiempo esperado de retorno a
                cada estado como un diccionario; caso contrario, se imprime
                un mensaje indicando que la cadena no es ergodica y
                se retorna None.
        """

        tiempo_retorno = {}
        pi_estrella     = self.distribucion_estacionaria()

        for estado in self.S :
            if pi_estrella[estado] > 1E-6 :
                tiempo_retorno[estado] = 1.0 / pi_estrella[estado]
            else :
                tiempo_retorno[estado] = np.Inf

        return tiempo_retorno

    def tiempo_esperado_de_primera_visita( self, estado) :
        """
        Si la cadena es ergodica, computa el tiempo esperado de primera visita
        desde cada estado hasta el estado espeficicado.

        @param estado Estado hacia el cual nos interesa calcular el tiempo
                      esperado de primera visita. Puede ser ingresado
                      como un estado o como un indice de estado.

        @return Si la cadena es ergodica, el tiempo esperado de primera visita
                desde cada estado hacia el estado especificado,
                como un diccionario; caso contrario, se imprime un mensaje
                indicando que la cadena no es ergodica y se retorna None.
        """

        # Leemos el estado ingresado
        if estado in self.S :
            estado = int( self.S.index(estado) )
        elif not ( isinstance( estado, int) and 0 <= estado < self.n ) :
            raise ValueError( 'Parametro estado no se entiende!' )

        # Construye la matriz P_menos_estado
        P_menos_estado = self.P.copy()
        P_menos_estado[ :, estado] = 0.0
        # Declara la matriz del lado izquierdo A = I - P
        matriz_A = np.identity( self.n) - P_menos_estado
        # Declara el vector del lado derecho b = 1
        vector_b = np.ones( shape = ( self.n) )

        # Computa los tiempos esperados de primer paso para cada estado
        # resolviendo el sistema A * vector_T = b
        try :
            vector_T = np.linalg.solve( matriz_A, vector_b)
        except np.linalg.LinAlgError :
            print( 'Esta cadena no es ergodica!' )
            return None

        # Construye el diccionario de tiempos esperados de primera visita
        tiempo_primera_visita = {}
        for ( i, estado) in enumerate(self.S) :
            tiempo_primera_visita[estado] = vector_T[i]

        return tiempo_primera_visita

    def valor_acumulado_hasta_primera_visita( self, valor_por_estado, estado) :
        """
        Si la cadena es ergodica, computa el valor esperado del
        valor acumulado desde cada estado hasta el estado espeficicado.

        @param valor_por_estado Diccionario de estados a valores reales.
        @param estado Estado hacia el cual nos interesa calcular el valor
                      acumulado hasta la primera visita. Puede ser ingresado
                      como un estado o como un indice de estado.

        @return Si la cadena es ergodica, el valor esperado del valor acumulado
                desde cada estado hacia el estado especificado,
                como un diccionario; caso contrario, se imprime un mensaje
                indicando que la cadena no es ergodica y se retorna None.
        """

        # Leemos el estado ingresado
        if estado in self.S :
            estado = int( self.S.index(estado) )
        elif not ( isinstance( estado, int) and 0 <= estado < self.n ) :
            raise ValueError( 'Parametro estado no se entiende!' )

        # Construye la matriz P_menos_estado
        P_menos_estado = self.P.copy()
        P_menos_estado[ :, estado] = 0.0
        # Declara la matriz del lado izquierdo A = I - P
        matriz_A = np.identity( self.n) - P_menos_estado

        # Declara el vector del lado derecho b = valor_por_estado
        vector_b = np.zeros( shape = ( self.n) )
        for ( i, estado) in enumerate(self.S) :
            vector_b[i] += valor_por_estado[estado]

        # Computa el vector de valores esperados resolviendo el sistema
        # A * vector_VAPV = b
        try :
            vector_VAPV = np.linalg.solve( matriz_A, vector_b)
        except np.linalg.LinAlgError :
            print( 'Esta cadena no es ergodica!' )
            return None

        # Construye el diccionario de valores acumulados
        valor_acumulado = {}
        for ( i, estado) in enumerate(self.S) :
            valor_acumulado[estado] = vector_VAPV[i]

        return valor_acumulado

    def valor_actual_neto( self, valor_por_estado, factor_descuento) :
        """
        Si la cadena es ergodica, computa el valor esperado del
        valor actual neto (VAN) a ser recolectad desde cada estado.

        @param valor_por_estado Diccionario de estados a valores reales.
        @param factor_descuento Factor de descuento.

        @return Si la cadena es ergodica, el valor esperado del valor
        actual neto (VAN) a ser recolectado desde cada estado,
        como un diccionario.
        """

        # Declara la matriz del lado izquierdo A = I - factor_descuento * P
        matriz_A = np.identity( self.n) - factor_descuento * self.P

        # Declara el vector del lado derecho b = valor_por_estado
        vector_b = np.zeros( shape = ( self.n) )
        for ( i, estado) in enumerate(self.S) :
            vector_b[i] += valor_por_estado[estado]

        # Computa el vector de valores esperados resolviendo el sistema
        # A * vector_VAN = b
        try :
            vector_VAN = np.linalg.solve( matriz_A, vector_b)
        except np.linalg.LinAlgError :
            print( 'Esta cadena no es ergodica!' )
            return None

        # Construye el diccionario de valores esperados
        valor_actual_neto = {}
        for ( i, estado) in enumerate(self.S) :
            valor_actual_neto[estado] = vector_VAN[i]

        return valor_actual_neto

class CadenaDeMarkovEnTiempoContinuo :
    """
    Implementa las principales funciones de una Cadena de Markov en
    Tiempo Continuo.
    """

    def __init__( self, estados, matriz_transicion) :
        """
        Constructor

        @param estados: Lista de estados, donde cada estado es representado por
                        una cadena de caracteres (i.e. un tipo string).
        @param matriz_P: Matriz de transicion. Debe ser un arreglo numpy
                         de tamano (n,n), donde n es el numero de estados.
        """

        # Copia los datos ingresados
        self.S = estados
        self.n = len(estados)
        self.Q = matriz_transicion

        # Verifica que el parametro estados sea una lista no-vacia
        if not isinstance( estados, list) :
            raise ValueError( 'Parametro estados debe ser una lista' )
        if len(estados) < 2 :
            raise ValueError( 'Numero de estados debe ser al menos dos' )

        # Verifica que el parametro matriz de transicion sea un arreglo numpy
        if not isinstance( self.Q, np.ndarray) :
            raise ValueError( 'Matriz de transicion debe ser un arreglo numpy' )

        # Verifica que la matriz de transicion tenga tamano n-por-n
        tamano_correcto = ( self.n, self.n)
        if not np.shape( self.Q) == tamano_correcto :
            raise ValueError( 'Matriz de transicion debe ser un arreglo numpy ' +
                              'de tamano ' + str(tamano_correcto) )

        # Valida cada fila (estado) de la matriz de transicion
        for fila in range( self.n) :
            # Avisa si alguna entrada es negativa
            cols_malas = self.Q[fila,:] < 0.0
            if np.any( cols_malas) :
                todas_cols = np.arange( self.n)
                cols_malas = todas_cols[cols_malas]
                raise ValueError( 'Matriz de transicion tiene entradas negativas ' +
                                  'en la fila ' + str(fila) + ' columnas ' +
                                  tuple(cols_malas) )
            # Avisa si el estado tiene una transicion a si mismo
            if np.abs( self.Q[fila,fila] ) > 1E-6 :
                raise ValueError( 'Matriz de transicion tiene un valor ' +
                                  'diferente de cero en su entrada diagonal ' +
                                  str( tuple(fila,fila) ) )

        return

    def contenidos( self) :
        """
        Retorna los contenidos como un diccionario.

        @return Diccionario que contiene dos entradas: 'estados' contiene una
        lista de los estados, 'matriz_transicion' contiene la matriz de transicion
        como arreglo numpy.
        """

        return { 'estados' : self.S, 'matriz_transicion' : self.Q }

    def distribucion_estacionaria( self) :
        """
        Si la cadena es ergodica, computa la distribucion estacionaria.

        @return Si la cadena es ergodica, la distribucion estacionaria
                como un diccionario; caso contrario, se imprime un mensaje
                indicando que la cadena no es ergodica y se retorna None.
        """

        # Declara la matriz Q diagonal
        matriz_Q_diagonal = np.diag( np.sum( self.Q, axis = 1) )
        # Declara la matriz del lado izquierdo A = Q' - Q_diagonal
        matriz_A = self.Q.transpose() - matriz_Q_diagonal
        # Declara el vector del lado derecho b = 0
        vector_b = np.zeros( shape = ( self.n,) )

        # Reemplaza la ultima fila de matriz_A con unos
        matriz_A[ -1, :] = 1.0
        # Reemplaza la ultima entrada de vector_b con uno
        vector_b[ -1]    = 1.0

        # Computa la distribucion estacionaria
        try :
            vector_pi = np.linalg.solve( matriz_A, vector_b)
        except np.linalg.LinAlgError :
            print( 'Esta cadena no es ergodica!' )
            return None

        # Construye el diccionario de la distribucion estacionaria
        pi_estrella = {}
        for ( i, estado) in enumerate(self.S) :
            pi_estrella[estado] = vector_pi[i]

        return pi_estrella

class ProcesoDeDecisionMarkoviano :
    """
    Implementa las principales funciones de un Proceso de Decision Markoviano.
    """

    def __init__( self, estados, acciones, transiciones, valores) :
        """
        Constructor

        @param estados: Lista de estados, donde cada estado es ingresado como
                        una cadena de caracteres (i.e. un tipo string).
        @param acciones: Diccionario de estados a listas de acciones
                         disponibles en los respectivos estados, donde cada
                         accion es representada por una cadena de caracteres
                         (i.e. un tipo string). Cada estado debe tener al menos
                         una accion disponible.
        @param transiciones: Diccionario de pares (2-tuplas) estado-accion a
                             distribuciones de probabilidad sobre los
                             estados sucesores, donde las distribuciones
                             son ingresadas como listas de numeros.
        @param valores: Diccionario de pares (2-tuplas) estado-accion a
                        valores reales (costos o recompensas).
        """

        # Copia los datos ingresados
        self.S = estados
        self.n = len(estados)
        self.A = acciones
        self.T = transiciones
        self.V = valores

        # Para cada estado...
        for estado in self.S :

            # Verifica que haya al menos una accion disponible
            if estado not in self.A :
                raise ValueError( 'No se ha provisto una lista de acciones validas ' +
                                  'para el estado ' + str(estado) )
            elif not isinstance( self.A[estado], ( list, tuple)) :
                raise ValueError( 'Provea una lista o tupla de acciones validas ' +
                                  'para el estado ' + str(estado) )
            elif len( self.A[estado] ) == 0 :
                raise ValueError( 'Provea al menos una accion valida ' +
                                  'para el estado ' + str(estado) )

            # Verifica las transiciones
            for accion in self.A[estado] :
                if ( estado, accion) not in self.T :
                    raise ValueError( 'Para el estado ' + str(estado) +
                                      ' se ha provisto la accion ' + str(accion) +
                                      ' pero no se ha provisto su transicion' )
                elif not isinstance( self.T[ ( estado, accion) ], dict) :
                    raise ValueError( 'Para el estado ' + str(estado) +
                                      ' se ha provisto la accion ' + str(accion) +
                                      ' pero no se ha provisto un diccionario ' +
                                      ' que represente la distribucion sobre los ' +
                                      ' estados sucesores' )
                else :
                    prob = 0.0
                    for estado_sucesor in self.T[ ( estado, accion) ] :
                        if estado_sucesor not in self.S :
                            raise ValueError( 'Para el par estado-accion ' +
                                              str(estado) + '-' + str(accion) +
                                              ' la transicion al estado ' +
                                              str(estado_sucesor) + ' es invalida' )
                        elif self.T[ ( estado, accion) ][ estado_sucesor] < 0.0 :
                            raise ValueError( 'Para el par estado-accion ' +
                                              str(estado) + '-' + str(accion) +
                                              ' la transicion al estado ' +
                                              str(estado_sucesor) + ' tiene' +
                                              ' probabilidad negativa' )
                        else :
                            prob += self.T[ ( estado, accion) ][ estado_sucesor]

                    if abs( prob - 1.0 ) > 1E-6 :
                        raise ValueError( 'Para el par estado-accion ' +
                                          str(estado) + '-' + str(accion) +
                                          ' el diccionario de probabilidades de' +
                                          ' transicion no suma a uno' )
            # Verifica los valores (recompensas o costos) de las transiciones
            for accion in self.A[estado] :
                if ( estado, accion) not in self.V :
                    raise ValueError( 'Para el estado ' + str(estado) +
                                      ' se ha provisto la accion ' + str(accion) +
                                      ' pero no se ha provisto su valor' +
                                      ' (i.e., recompensa o costo)' )

            # Convierte las transiciones de diccionarios a arreglos numpy
            for accion in self.A[estado] :
                vector = np.zeros( shape = ( self.n) )
                for estado_sucesor in self.T[ ( estado, accion) ].keys() :
                    i = self.S.index(estado_sucesor)
                    vector[i] = self.T[ ( estado, accion) ][ estado_sucesor]
                self.T[ ( estado, accion) ] = vector

        return

    def verifica_politica( self, politica) :

        if not isinstance( politica, dict) :
            raise ValueError( 'Politica debe ser ingresada como un diccionario' )
        else :
            for estado in self.S :
                if estado not in politica :
                    raise ValueError( 'Politica ingresada no asigna ninguna accion ' +
                                      'al estado ' + str(estado) )
                elif politica[estado] not in self.A[estado] :
                    raise ValueError( 'Politica ingresada no asigna una accion ' +
                                      'valida al estado ' + str(estado) )

        return

    def imprime_politica( self, politica) :

        print( 'POLITICA:' )
        for estado in self.S :
            accion = politica[estado]
            msg = 'Estado: ' + str(estado) + ' --> '
            msg += 'Accion: ' + str(accion)

        return

    def evalua_politica( self, politica) :

        self.verifica_politica( politica)

        P = np.zeros( shape = ( self.n, self.n) )
        V = {}
        for ( i, estado) in self.S :
            accion = politica[estado]
            P[i,:] = self.T[ ( estado, accion) ]
            V[estado] = self.V[ ( estado, accion) ]

        cadena      = CadenaDeMarkov( self.S, P)
        pi_estrella = cadena.distribucion_estacionaria()
        valor       =  0.0
        for estado in self.S :
            valor += pi_estrella[estado] * V[estado]

        return valor
