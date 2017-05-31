"""
@author: Luis I. Reyes Castro
"""

import numpy as np
from MarkovChain import MarkovChain

# Define the Markov Chain
states = [ 'Celda-1', 'Celda-2', 'Celda-3', 'Celda-4', 'Celda-5', 'Celda-6']
transition_matrix = np.zeros( (6,6) )
transition_matrix[0,:] = np.array( [ 0.5,   0 ,    0,     0.5,   0,     0    ] )
transition_matrix[1,:] = np.array( [ 0,     0.333, 0.333, 0,     0.333, 0    ] )
transition_matrix[2,:] = np.array( [ 0,     0.333, 0.333, 0,     0,     0.333] )
transition_matrix[3,:] = np.array( [ 0.333, 0,     0,     0.333, 0.333, 0    ] )
transition_matrix[4,:] = np.array( [ 0,     0.25,  0,     0.25,  0.25,  0.25 ] )
transition_matrix[5,:] = np.array( [ 0,     0,     0.333, 0,     0.333, 0.333] )
chain = MarkovChain( states, transition_matrix)
# Propagate an initial distribution
pi_0 = np.array( [ 0.5, 0.0, 0.0, 0.0, 0.5, 0.0] )
list_of_states_02 = \
chain.propagate_distribution( num_steps = 100, initial_distribution = pi_0)
