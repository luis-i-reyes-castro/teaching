"""
@author: Luis I. Reyes Castro
"""

import numpy as np
from MarkovChain import MarkovChain

# Define the Markov Chain
states = [ 'Rain', 'No rain']
transition_matrix = np.array( [ [ 0.8, 0.2], [ 0.6, 0.4] ] )
chain = MarkovChain( states, transition_matrix)
# Sample from the chain with an initial state 'Rain'
list_of_states_01 = \
chain.sample_sequence_of_states( num_steps = 10, initial_state = 0)
# Sample from the chain with an initial distribution
pi_0 = np.array( [ 0.9, 0.1] )
list_of_states_02 = \
chain.sample_sequence_of_states( num_steps = 10, initial_distribution = pi_0)
