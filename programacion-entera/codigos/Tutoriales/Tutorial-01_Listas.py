"""
Tutorial sobre Uso de Listas
@author: Luis I. Reyes Castro
"""

# Creamos una lista explicitamente
lista_A = [ 2, -54, 56, 1, -8, -3, 21]
# Imprimimos la lista anterior al terminal
print( 'lista_A:', lista_A)
# Solicitamos la longitud de la lista
longitud_lista_A = len(lista_A)
# Imprimimos la longitud de la lista
print( 'Longitud de lista_A:', longitud_lista_A)

# Solicitamos el primer elemento de la lista
print( 'Primer elemento de la lista:', lista_A[0])
# Solicitamos el segundo elemento de la lista
print( 'Segundo elemento de la lista:', lista_A[1])
# Solicitamos el tercer elemento de la lista
print( 'Tercer elemento de la lista:', lista_A[2])
# Solicitamos el ultimo elemento de la lista
print( 'Ultimo elemento de la lista:', lista_A[-1])
# Solicitamos el penultimo elemento de la lista
print( 'Penultimo elemento de la lista:', lista_A[-2])

# Solicitamos la sublista conformada por todos los elementos 
# desde el segundo hasta el ultimo
print( 'lista_A desde el segundo hasta el ultimo:', lista_A[1:])
# Solicitamos la sublista conformada por todos los elementos 
# desde el primero hasta el penultimo
print( 'lista_A desde el primero hasta el penultimo:', lista_A[:-1])
# Solicitamos la sublista conformada por todos los elementos 
# desde el segundo hasta el penultimo
print( 'lista_A desde el segundo hasta el penultimo:', lista_A[1:-1])
# Solicitamos la lista original saltandonos un elemento
print( 'lista_A saltando un elemento:', lista_A[::2] )
# Solicitamos la lista original saltandonos dos elementos
print( 'lista_A saltando un elemento:', lista_A[::3] )
# Solicitamos la lista original en orden reverso
print( 'lista_A en orden reverso:', lista_A[::-1] )

# Iteramos sobre la lista_A e imprimimos sus elementos
print( 'Elementos_de_la_lista_A:')
for elem in lista_A:
    print( 'Elemento:', elem)

# Iteramos sobre la lista_A e imprimimos sus ( posiciones, elementos)
print( 'Elementos_de_la_lista_A:')
for ( pos, elem) in enumerate(lista_A):
    print( 'Elemento en posicion', pos, 'es', elem)

# Iteramos sobre la lista_A en orden reverso e imprimimos sus elementos
print( 'Elementos_de_la_lista_A_en_orden_reverso:')
for elem in lista_A[::-1]:
    print( 'Elemento:', elem)

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

