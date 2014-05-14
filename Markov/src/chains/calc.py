'''
Created on 24/09/2013

@author: ecejjar
'''
from operator import mul, add, sub
try:
    from functools import reduce
except:
    pass

def gaussianEliminationWithPartialPivoting ( A, C ):
    '''
    Solves the system of linear equations A*X=C using Gaussian elimination with
    partial pivoting.
    A must be a square NxN matrix of numbers; C must be a vector of size N.
    The function returns a vector of size N, or raises an exception if it cannot
    find a solution.
    '''
    def forwardElimination ( A, C, offset=0 ):
        '''
        Given a NxN matrix A and a vector C of size N, calculate coefficients a11/ai1
        for every 1 < i < n and multiply each row times the corresponding coefficient,
        then subtract from each row the first row.
        '''
        Aout, Cout = [],[]
        a11, firstrow = None, None
        for i, row in enumerate(map(lambda a,c: a+[c], A, C)):
            if a11 is None:
                Aout.append(list(row))  # Important: do NOT append row, since firstrow==row and when doing Aout[].pop() below we're changing firstrow!!
                if i == offset: a11, firstrow = row[i], row
            else:
                k = [0]*offset + [a11/row[offset]]*(len(row)-offset)
                Aout.append(list(map(sub, map(mul, k, row), firstrow)))
            Cout.append(Aout[-1].pop())

        return Aout, Cout
    
    def partialPivoting ( A, C ):
        '''
        Given a NxN matrix A and a vector C of size N, sort the rows of A in descending
        order by the absolute value of the coefficients.
        When exchanging two rows in A, exchange the corresponding rows in C as well.
        When A is the output of a forward elimination step, this has the effect that
        rows are sorted hi-to-low by the absolute values of the leftmost column
        having at least one non-zero coefficient, i.e. exactly what the partial pivoting
        requires.
        '''
        for i, row in enumerate(A): row.append(C[i])
        A.sort(key=lambda r: list(map(abs, r)), reverse=True)
        for i, row in enumerate(A): C[i] = row.pop()
        
    def backwardSubstitution ( A, C ):
        '''
        Given a NxN matrix A where coefficients aij=0 for every i>1 and j<i, and a
        vector C of size N, obtain a vector X of size N that satisfies A*X=C
        '''
        Xout = []
        A1, C1 = forwardElimination(reversed(A), reversed(C))
        return Xout
    
    # Triangularize
    for i in range(len(A)):
        A, C = forwardElimination(A, C, i)
        partialPivoting(A, C)
    
    # Reverse vertically and A also horizontally to leave the 0's at the top-right corner
    A, C = list(map(list, map(reversed, reversed(A)))), list(reversed(C))
    
    # Triangularize again (thus ending in diagonalized matrix)
    for i in range(len(A)):
        A, C = forwardElimination(A, C, i)
        partialPivoting(A, C)

    # Now we've got a diagonal matrix, but coefficient order is inverted WRT the original
    # input matrix so we've got to reverse vertically then horizontally once more to recover
    # the original order. Instead of repeating the reverse(reverse()) as above, we build
    # the resulting vector in reverse order and achieve the same effect.    
    result = []
    for a,c in zip(A,C):
        s = 0
        for x in a: s += x
        result.insert(0, c/s)
    return result
    #return map(lambda a,c: c/reduce(sum, a), A, C) Why it doesn't work??!!

def steadyState ( chain ):
    '''
    Returns a dictionary of pairs (name, p), being 'name' a state name and 'p' the probability
    the chain passed as argument is at the state with that name in the long run
    '''
    # Solve for the balance equations {steady-state-probs}*[transitionMatrix] = {steady-state-probs}
    # (comprehension below actually builds {steady-state-probs}*[transitionMatrix] - {steady-state-probs} = 0)
    # , extended with equation sum(steady-state-probs) = 1
    A = [[chain[rstate][cstate] - ((rstate==cstate and 1) or 0) for rstate in chain] for cstate in chain]
    C = [0]*len(A)
    A.append([1]*len(A.pop()))
    C.pop() or C.append(1)
    result = dict(zip(chain.keys(), gaussianEliminationWithPartialPivoting(A, C)))

    return result

