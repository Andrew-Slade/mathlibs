#!/usr/bin/env python3

class Automaton:

  #Constructor
  
  def __init__(self, states, init_state, accept_state, alpha, fx):
     self.Q = states #set of states with their next states
     self.I = init_state #set of initial states
     self.T = accept_states #set of terminal states
     self.S = alpha #an alphabet
     self.L = fx #a function
     self.C = self.I #start at the current state
    
#Accessors

  def getQ(self):
    return self.Q
  
  def getI(self):
    return self.I

  def getT(self):
    return self.T

  def getS(self):
    return self.S

  def getL(self):
    return self.L
 
  def getC(self):
    return self.C

#Methods

  def alpha_check(self):
    """
    Check whether or not the word is build using the
    alphabet provided
    """
    for alpha in self.Q:
      if alpha in self.S:
        isalpha = True
        break
      else:
        isalpha = False
    return isalpha

  #Generalize me and the states
  def process(self):
    """
    Move states
    >>> takes: (variable type)data
    >>> returns: (variable type) a new state
    """
    return self.T 
  

  def check_end_state(self, currentState):
    """
    Check end states vs current states
    >>> takes: (variable type) state
    >>> returns: (boolean) whether current state is accepted
    """    
    return False or currentState in self.T
      

  def print_results(self, result):
    """
    Print the result of the automaton
    >>>takes (boolean) result of check end state
    """
    if result == True :
      print("The data passed the conditions")
    else:
      print("The data did not pass the conditions")
