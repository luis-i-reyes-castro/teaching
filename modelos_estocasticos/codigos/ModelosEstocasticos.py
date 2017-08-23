"""
@author Luis I. Reyes Castro, M.Sc.
        Facultad de Ingenieria en Mecanica y Ciencias de la Produccion (FIMCP)
        Escuela Superior Politecnica del Litoral

Implementaciones de los modelos vistos en mi curso de Modelos Estocasticos
para Manufactura y Servicios (INDG-1008).

"""

import numpy as np

# -------------------------------------------------------------------------------------
class ProcesoBernoulli :
    """
    Implementa las principales funciones de un proceso Bernoulli.
    """

    # Miembros:
    p = None # parametro

    def __init__( self, p, modo = 'AND') :
        """
        Constructor

        @param p: Parametro del proceso o lista o tupla de proceso a combinar.
                  - Si p es un decimal en (0,1) entonces se instancia un
                    proceso Bernoulli independiente con ese parametro.
                  - Si p es una lista o tupla de procesos Bernoulli entonces se
                    instancia la combinacion de esos procesos de acuerdo al
                    parametro modo.
        @param modo: Modo de combinacion (de ser aplicable): 'AND', 'OR'
        """

        if not isinstance( p, ( float, list, tuple) ) :
            raise ValueError( 'Parametro p debe ser una probabilidad o una ' +
                              'lista o tupla de procesos Bernoulli' )

        elif isinstance( p, float) :
            if not ( 0 < p < 1 ) :
                raise ValueError( 'Instanciar un proceso independiente requiere ' +
                                  'que el parametro p sea un decimal ' +
                                  'en el intervalo abierto (0,1)' )
            else :
                self.p = p

        else :
            self.combina( p, modo)

        return

    def combina( self, procesos, modo) :

        # Verifica que cada objeto en procesos sea un proceso Bernoulli
        for proceso in procesos :
            if not isinstance( proceso, ProcesoBernoulli) :
                raise ValueError( 'Lista o tupla de procesos tiene al menos una ' +
                                  'entrada que no es de la clase ProcesoBernoulli' )

        # Extrae los parametros de los procesos en la lista
        parametros = np.array( [ proceso.p for proceso in procesos ] )

        # Calcula el parametro del nuevo proceso
        if modo == 'AND' :
            self.p = np.prod( parametros )
        elif modo == 'OR' :
            self.p = 1.0 - np.prod( 1.0 - parametros )
        else :
            raise ValueError( 'Modo invalido, opciones validas son: AND, XOR' )

        return

    def divide( self, probabilidades) :
        """
        Divide al proceso de acuerdo al vector de probabilidades ingresado

        @param probabilidades: Vector de probabilidades de los n procesos

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
            raise ValueError( 'Parametro inicio debe ser una lista, tupla o ' +
                              'vector de probabilidades, i.e. sus entradas ' +
                              'deben ser no-negativas y sumar a uno')

        # Instancia cada nuevo proceso con su parametro correcto
        procesos = []
        for ( i, _) in enumerate(probabilidades) :
            nuevo_proceso = ProcesoBernoulli( probabilidades[i] * self.p )
            procesos.append( nuevo_proceso )

        return procesos

    def muestrea( self, num_pasos) :
        """
        Muestrea aleatoriamente del proceso por un numero de pasos deseado

        @param num_pasos: Numero de pasos a muestrear

        @return Una 2-tupla conteniendo en su primera entrada los indices de
                los estados muestreados y en su segunda entrada las frecuencias
                de los estados ocurridos
        """

        # Muestrea num_pasos variables aleatorias Uniforme(0,1)
        U = np.random.random_sample(num_pasos)
        # Genera variables Bernoulli usando las variables uniformes
        X = np.where( U < self.p, 0, 1)

        # Computa el vector de frecuencias
        frequencia = np.zeros( shape = (2,) )
        frequencia[1] = 1.0 * sum(X) / num_pasos
        frequencia[0] = 1 - frequencia[1]

        return ( X, frequencia)

# -------------------------------------------------------------------------------------
class CadenaDeMarkov :
    """
    Implementa las principales funciones de una Cadena de Markov.
    """

    # Miembros
    estados  = [] # lista de estados
    n        = 0  # numero de estados
    matriz_P = np.array([]) # matriz de transicion

    def __init__( self, estados, matriz_transicion) :
        """
        Constructor

        @param estados: Lista de estados, donde cada estado es representado por
                        una cadena de caracteres (i.e. un tipo string).
        @param matriz_P: Matriz de transicion. Debe ser un arreglo numpy
                         de tamano (n,n), donde n es el numero de estados.
        """

        # Copia los datos ingresados
        self.estados  = estados
        self.n        = len(estados)
        self.matrix_P = matriz_transicion

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

        return

    def contenidos( self) :
        """
        Retorna los contenidos como un diccionario.

        @return Diccionario que contiene dos entradas: 'estados' contiene una
        lista de los estados, 'matriz_transicion' contiene la matriz de transicion
        como arreglo numpy.
        """

        return { 'estados' : self.estados, 'matriz_transicion' : self.matrix_P }

    def muestrea( self, inicio, num_pasos) :
        """
        Muestrea aleatoriamente una secuencia de estados

        @param inicio: Inicio de la secuencia. Puede ser un estado, el indice de
                       un estado, o una distribucion del estado inicial.
                       Si es un estado debe encontrarse en la lista de estados,
                       caso contrario se arrojara un error. Si es el indice de
                       un estado debe ser un entero entre cero y n-1.
                       Si es una distribucion debe ser un arreglo de
                       tamano (n,) que sea un vector de probabilidad.
        @param num_pasos: Numero de pasos a muestrear.

        @return Una 3-tupla que contiene en su primera entrada la secuencia de
                estados muestreada, en su segunda entrada la lista de indices
                de los mismos estados, y en su tercera entrada el diccionario de
                frecuencias de visitas a estados de la muestra.
        """

        # Inicializa la historia de estados arbitrariamente para evitar
        # alocaciones de memoria durante el muestreo
        X = [ 0 for t in range(num_pasos) ]

        # Verifica que se haya provisto un estado o distribucion inicial
        if inicio is None :
            raise ValueError( 'Provea un estado o distribucion inicial' )

        # Si inicio es el indice del estado inicial solo lo copiamos
        if isinstance( inicio, int) and 0 <= inicio < self.n :
            X[-1] = inicio

        # Si inicio no es una lista, tupla o vector entonces busca el indice
        # del estado inicio, si existe; caso contrario avisa
        elif not isinstance( inicio, ( list, tuple, np.ndarray) ) :
            try :
                X[-1] = int( self.estados.index(inicio) )
            except Exception :
                raise ValueError( 'Estado \'' + str(inicio) + '\' no existe' )

        # Si inicio es un vector de probabilidades iniciales entonces
        # lo utilizamos para muestrear el estado inicial
        else :
            inicio = np.array(inicio)
            tamano_correcto = ( self.n,)
            if not np.shape(inicio) == tamano_correcto :
                raise ValueError( 'Parametro inicio debe ser un arreglo ' +
                                  'de tamano ' + str(tamano_correcto) )
            if np.any( inicio < 0.0 ) or abs( np.sum(inicio) - 1.0 ) > 1e-8 :
                raise ValueError( 'Parametro inicio debe ser un vector de ' +
                                  'probabilidades' )
            X[-1] = np.random.choice( self.n, p = inicio)

        # Para cada paso...
        for t in range(num_pasos) :
            # Extrae la fila de la matriz de transicion asociada con el
            # estado anterior
            prob_transicion = self.matrix_P[ X[t-1], :]
            # Muestrea el indice del estado actual
            X[t] = np.random.choice( self.n, p = prob_transicion)

        # Construye la secuencia de estados visitados
        estados_visitados = [ self.estados[ X[t] ] for t in range(num_pasos) ]

        # Construye el diccionario de frecuencias de visitas a estados
        frequencias = { estado : 0.0 for estado in self.estados }

        for estado_visitado in estados_visitados :
            frequencias[estado_visitado] += 1.0

        for estado in frequencias :
            frequencias[estado] /= num_pasos

        return ( estados_visitados, frequencias)

    def propaga_distribucion( self, distribucion_inicial, num_pasos) :
        """
        Propaga la distribucion del estado inicial

        @param distribucion_inicial: Distribucion del estado inicial como un
                       diccionario disperso, i.e. solo se requiere especificar
                       los estados con probabilidades estrictamente positivas.
        @param num_pasos: Numero de pasos a propagar.

        @return Una matriz numpy de tamano ( num_pasos, n) cuya entrada (t,i)
                es la probabilidad en el periodo t de estar en el estado i.
        """

        # Verifica que la distribucion sea un diccionario
        if not isinstance( distribucion_inicial, dict ) :
            raise ValueError( 'Parametro distribucion_inicial debe ser ' +
                              'un diccionario.' )

        # Costruye el vector de distribucion inicial a partir del diccionario
        pi_t = np.zeros( shape = ( self.n) )
        for estado in distribucion_inicial :
            if not estado in self.estados :
                raise ValueError ( 'Entrada \'' + str(estado) + '\' del parametro ' +
                                   'distribucion_inicial no es un estado' )
            else :
                indice_estado = self.estados.index( estado)
                pi_t[indice_estado] = distribucion_inicial[estado]

        # Verifica el vector de distribucion inicial
        if np.any( pi_t < 0.0 ) or abs( np.sum(pi_t) - 1.0 ) > 1e-8 :
            raise ValueError( 'Parametro distribucion_inicial no representa una ' +
                              'distribucion valida porque alguna entrada ' +
                              'es negativa o porque sus entradas no suman a uno.' )

        # Para cada iteracion...
        for t in range(num_pasos) :
            # Computa la distribucion actual de acuerdo a la recursion:
            # pi_t+1' = pi_t' * P
            pi_t = np.dot( pi_t, self.matrix_P).flatten()

        # Formatea la distribucion final como un diccionario y la retorna
        distribucion_final = { estado : 0.0 for estado in self.estados }
        for i in range(self.n) :
            distribucion_final[ self.estados[i] ] = pi_t[i]

        return distribucion_final

    def distribucion_estacionaria( self) :
        """
        Computa la distribucion estacionaria de la cadena (si la cadena es ergodica)

        @return La distribucion estacionaria de la cadena como un diccionario,
                si la cadena es ergodica; caso contrario, se imprime un mensaje
                indicando que la cadena no es ergodica y se retorna None.
        """

        # Declara la matriz del lado izquierdo A = P' - I
        matriz_A = self.matrix_P.transpose() - np.identity( self.n)
        # Declara el vector del lado derecho b = 0
        vector_b = np.zeros( shape = ( self.n) )

        # Reemplaza la ultima fila de matriz_A con unos
        matriz_A[ -1, :] = 1.0
        # Reemplaza la ultima entrada de vector_b con uno
        vector_b[-1] = 1.0

        # Computa la distribucion estacionaria
        try :
            vector_pi = np.linalg.solve( matriz_A, vector_b)
        except np.linalg.LinAlgError :
            print( 'Esta cadena no es ergodica!' )
            return None

        # Construye el diccionario de la distribucion
        pi_estrella = {}
        for i in range(self.n) :
            pi_estrella[ self.estados[i] ] = vector_pi[i]

        return pi_estrella

    def tiempo_esperado_de_retorno( self) :
        """
        Computa el tiempo esperado de retorno para cada estado

        @return El tiempo esperado de retorno a cada estado como un diccionario,
                si la cadena es ergodica; caso contrario, se imprime un mensaje
                indicando que la cadena no es ergodica y se retorna None.
        """

        tiempo_esperado = {}
        pi_estrella     = self.distribucion_estacionaria()

        for estado in pi_estrella :
            tiempo_esperado[estado] = 1.0 / pi_estrella[estado]

        return tiempo_esperado

    def tiempo_esperado_de_primer_paso( self, estado) :
        """
        Computa el tiempo esperado de primer paso desde cada estado hasta
        el estado espeficicado

        @param estado Estado hacia el cual nos interesa calcular el tiempo esperado
                      de primer paso. Puede ser un estado o un indice de estado.

        @return El tiempo esperado de primer paso desde cada estado hacia el
                estado especificado como un diccionario, si la cadena es ergodica;
                caso contrario, se imprime un mensaje indicando que la cadena
                no es ergodica y se retorna None.
        """

        # Verifica que se haya provisto un estado final
        if estado is None :
            raise ValueError( 'Provea un estado hacia el cual desea calcular ' +
                              'el tiempo esperado de primer paso.' )

        # Si el estado final se espefica como un indice no hacemos nada;
        # caso contrario buscamos el indice del estado
        if not isinstance( estado, int) or not ( 0 <= estado < self.n ) :
            try :
                estado = int( self.estados.index(estado) )
            except Exception :
                raise ValueError( 'Estado \'' + str(estado) + '\' no existe' )

        # Declara la matriz del lado izquierdo A = I - P
        matriz_A = np.identity( self.n) - self.matrix_P
        # Declara el vector del lado derecho b = 1
        vector_b = np.ones( shape = ( self.n) )

        # Reemplaza la fila de la matriz A y la entrada del vector b asociada con
        # el estado final de tal manera que la ecuacion asociada con esa fila es
        # 1.0 * T_{estado_final} = 0
        matriz_A[ estado, :]      = 0.0
        matriz_A[ estado, estado] = 1.0
        vector_b[ estado]         = 0.0

        # Computa los tiempos esperados de primer paso para cada estado
        # resolviendo el sistema A * vector_T = b
        try :
            vector_T = np.linalg.solve( matriz_A, vector_b)
        except np.linalg.LinAlgError :
            print( 'Esta cadena no es ergodica!' )
            return None

        # Construye el diccionario de tiempos esperados de primer paso
        tiempo_esperado = {}
        for ( i, estado) in enumerate(self.estados) :
            tiempo_esperado[estado] = vector_T[i]

        return tiempo_esperado

    def funcion_de_valor( self, funcion_recompensa, factor_descuento) :
        """
        Computa la funcion de valor por estado de acuerdo a la funcion de recompensa
        ingresada y el factor de descuento.

        @param funcion_recompensa Funcion de recompensa por estado como
               un diccionario de estados a valores.
        @param factor_descuento Factor de descuento.

        @return La funcion de valor como un diccionario de estados a valores.
        """

        # Declara la matriz del lado izquierdo A = I - factor_descuento * P
        matriz_A = np.identity( self.n) - factor_descuento * self.matrix_P
        # Declara el vector del lado derecho b = funcion_recompensa
        vector_b = np.ones( shape = ( self.n) )
        for ( i, estado) in enumerate(self.estados) :
            vector_b[i] = funcion_recompensa[estado]

        # Computa la funcion de valor resolviendo el sistema A * vector_V = b
        try :
            vector_V = np.linalg.solve( matriz_A, vector_b)
        except np.linalg.LinAlgError :
            print( 'Esta cadena no es ergodica!' )
            return None

        # Construye el diccionario asociado con la funcion de valor
        funcion_de_valor = {}
        for ( i, estado) in enumerate(self.estados) :
            funcion_de_valor[estado] = vector_V[i]

        return funcion_de_valor
