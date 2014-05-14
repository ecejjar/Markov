'''
Created on 11/10/2013

@author: ecejjar
'''
import unittest
from model import State, Chain
from calc import steadyState

class MarkovTest ( unittest.TestCase ):

    def testModel ( self ):
        A = State("A")
        B = State("B")
        A.add(A, .3) or A.add(B, .7)
        B.add(A, .5) or B.add(B, .5)
        self.assertEqual(A.prob("A"), .3, "P(A->A) not 0.3")
        self.assertEqual(A.prob(B), .7, "P(A->B) not 0.7")
        self.assertEqual(B.prob("A"), .5, "P(B->A) not 0.5")
        self.assertEqual(B.prob(B), .5, "P(B->B) not 0.5")
        
        chain = Chain((A, B))
        self.assertDictEqual(
            chain.transitionMatrix(),
            {"A": {"A": .3, "B": .7}, "B": {"A": .5, "B": .5}},
            "Transition matrix incorrect")
    
    def testSteadyState ( self ):
        A = {"A": {"A": .3, "B": .7}, "B": {"A": .5, "B": .5}}
        R = steadyState(A)
        Rr = dict(map(lambda i: (i[0], round(i[1],2)), R.items()))
        self.assertDictEqual({"A": 0.42, "B": 0.58}, Rr, "A not correct")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
