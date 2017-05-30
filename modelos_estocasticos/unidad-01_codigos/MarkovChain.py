"""
@author Luis I. Reyes Castro, M.Sc.
"""

import numpy as np

class MarkovChain :
    """
    Implements a Markov Chain
    """

    # States and transition matrix
    states            = []
    transition_matrix = np.array(0.0)
    num_states        = 0
    # Current state and distribution
    current_state = 0
    current_distribution = np.array(0.0)

    def __init__( self, states, transition_matrix) :
        """
        Class constructor
        @param states: List of states
        @param transition_matrix: Transition Matrix
        """

        self.states            = states
        self.transition_matrix = transition_matrix
        self.num_states        = len(states)

        # Initialize the current state to be the first one (arbitrarily)
        self.current_state = 0
        # Initialize the current distribution to the uniform distribution
        self.current_distribution = ( 1.0 / self.num_states ) \
                                  * np.ones( shape = ( self.num_states,) )

        return

    def get_dictionary_of_variables( self) :
        """
        Get dictionary of all member variables and functions
        """
        return self.__dict__

    def sample_next_state( self) :
        """
        Sample the next state
        """
        # Retrieve vector of probabilities of transitioning from the current state
        # to each of the other states, which is the row of the transition matrix
        # associated with the current state
        probs = self.transition_matrix[ self.current_state, :]
        # Sample the next state
        self.current_state = np.random.choice( self.num_states, p = probs)
        return self.current_state

    def propagate_distribution_one_step( self) :
        """
        Propagate the state distribution vector one step forward
        """
        # current_distribution(t+1) = current_distribution(t) * transition_matrix
        self.current_distribution = np.dot( self.current_distribution,
                                            self.transition_matrix)
        return self.current_distribution

    def sample_sequence_of_states( self, num_steps,
                                   initial_state = None,
                                   initial_distribution = None,
                                   verbose = True) :

        if initial_state is None and initial_distribution is None :
            raise ValueError( 'Must provide an initial state or distribution' )

        if initial_state is not None :
            self.current_state = initial_state
        else :
            self.current_state = np.random.choice( self.num_states,
                                                   p = initial_distribution)

        if verbose :
            print( 'Markov Chain: Sampling a ' + str(num_steps) +
                   '-step state sequence' )

        sequence = []
        for t in range(num_steps) :
            if verbose :
                print( 'X_' + str(t) + ': ' +
                       str( self.states[self.current_state] ) )
            sequence.append( self.sample_next_state() )

        return sequence

    def propagate_distribution( self, num_steps,
                                initial_distribution, verbose = True) :

        if verbose :
            print( 'Markov Chain: Propagating a ' + str(num_steps) +
                   '-step state distribution sequence' )

        self.current_distribution = initial_distribution
        sequence = []
        for t in range(num_steps) :
            if verbose :
                print( 'pi_' + str(t) + ': ' + str( self.current_distribution ) )
            sequence.append( self.propagate_distribution_one_step() )

        return sequence
