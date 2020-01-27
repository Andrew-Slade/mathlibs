#!/usr/bin/env python3
#Copyright 2020, Andrew Slade, All rights reserved.

#A Determinate Finite Automaton

class Automaton:

  #Constructor
  def __init__(self, states, init_state, accept_states, alpha, fx):
     self.Q = states #set of states with their next states
     self.I = init_state #set of initial states
     self.T = accept_states #set of terminal states
     self.S = alpha #an alphabet
     self.L = fx #a function taking current state and a letter
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
  def check_word(self, word):
    """
    Check a users word to make sure it is in the alphabet
    >>> takes: (string) user word
    >>> returns: (boolean) whether or not the word is a word
    """
    for letter in word:
      if letter in self.S:
        isword = True
      else:
        isword = False
        break
    return isword


  def process(self, letter):
    """
    Move states
    >>> takes: (string) user letter
    """
    self.C = self.L(letter, self.C)
    print(self.C)
  

  def check_end_state(self):
    """
    Check end states vs current states
    >>> takes: (variable type) states
    >>> returns: (boolean) whether current state is accepted
    """    
    return False or self.C[0] in self.T
      

  def print_results(self):
    """
    Print the result of the automaton
    >>> takes (boolean) result of check end state
    """
    if self.result == True :
      print("The data passed the conditions")
    else:
      print("The data did not pass the conditions")


  def test_automaton(self, word):
    """
    test the automaton
    >>> takes: (Automaton) an automaton
               (string) a word
    """
    print("Starting Automaton...")
    print(self.getI())#print init state
    for letter in word:
      self.process(letter)#Process the data and move states
    print("Automaton finished moving states")
    
    self.result = self.check_end_state()#check the end state
    self.print_results()#print results
