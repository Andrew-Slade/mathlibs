#!/usr/bin/env python3

class Automaton:

  #Constructor
  
  def __init__(self, states, init_state, accept_state, alpha, fx):
     self.Q = states#set of states
     self.I = init_state#set of initial states
     self.T = accept_state #set of terminal states
     self.S = alpha #an alphabet
     self.L = fx #a function

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

#Methods

  #Generalize me and the states
  def process(self):
    """
    Process data using automaton
    >>>takes: (variable type)data
    >>>returns: (variable type) a new state
    """
    for dataval in self.Q:
      print("Processed: ", dataval, " Against: ", self.T) 
      if self.T != dataval:#check current state vs data
        self.T = dataval#if data val is different change state
        print("Terminal state changed to: ", self.T) 
    return self.T 
  

  def check_end_state(self):
    """
    Check end state vs initial state
    """
    return False or self.T == self.I
      

  def print_results(self, result):
    """
    Print the result of the automaton
    >>>takes (boolean) result of check end state
    """
    print("The initial state was: ", self.I, " and the terminal state was: ", self.T)
    if result == True :
      print("The data passed the conditions")
    else:
      print("The data did not pass the conditions")
