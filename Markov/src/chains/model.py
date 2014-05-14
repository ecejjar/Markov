'''
Created on 24/09/2013

@author: ecejjar
'''
from collections import namedtuple

ProbabilisticTransition = namedtuple('Transition', 'frm, to, p')

class State:
    '''
    A representation of a state in a Markov state transition diagram.
    A state has a name and a number of transitions to other states,
    each with a given probability.
    A state can tell what is the probability of transitioning from
    itself to another state.
    '''

    def __init__( self, name, iterable=None, **kwargs ):
        '''
        Constructor
        '''
        self.__name = name
        self.__to = {}
        if iterable is not None:
            for t in iterable: self.add(t[0], t[1])
        for k, v in kwargs: self.add(k, v)
        
    @property
    def name (self): return self.__name
    
    @property
    def to (self): return self.__to

    def add (self, nxt, p):
        self.__to[nxt.name] = ProbabilisticTransition(self, nxt, p)
        
    def prob (self, nxt):
        try:
            try:
                return self.__to[nxt.name].p
            except AttributeError:
                return self.__to[nxt].p
        except IndexError:
            return 0

    
class Chain ( list ):
    '''
    A representation of a Markov state transition diagram.
    It is a vector of states that can produce a
    Markov transition matrix as a dictionary of dictionaries,
    so that the probability of transitioning from state a to
    state b can be obtained as self[state.name][state.name] 
    '''
    
    def __init ( self, iterable=None, **kwargs ):
        '''
        Constructor
        '''
        super(Chain, self).__init__(iterable, **kwargs)
        
    def transitionMatrix ( self ):
        result = {}
        for state in self:
            result[state.name] = {}
            for trans in state.to.values():
                result[trans.frm.name][trans.to.name] = trans.p 
        return result
    
