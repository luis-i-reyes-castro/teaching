"""
Ejercicio de Manejo de Listas (II)
@author: Luis I. Reyes Castro
"""

# Imprimimos los numeros enteros entre el uno y el diez
lista_B1 = [ num for num in range(1,11) ]
print( 'Lista_B1 =', lista_B1)

# Imprimimos los numeros impares entre el uno y el diez
lista_B2 = [ num for num in range(1,11,2) ]
print( 'Lista_B2 =', lista_B2)

# Imprimimos los numeros pares entre el dos y el diez
lista_B3 = [ num for num in range(2,11,2) ]
print( 'Lista_B3 =', lista_B3)

# Imprimimos los numeros enteros entre el diez y el uno en orden reverso
lista_B4 = [ num for num in range(10,0,-1) ]
print( 'Lista_B4 =', lista_B4)
