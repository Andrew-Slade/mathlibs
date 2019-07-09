#!/usr/bin/env python3

import Automaton as auto
import random as r

def functionality_test():
  """
  creates a simple automaton
  """
  #Test 1
  states = gen_test_data(5)
  print(states)
  init_state = r.randint(0,1)
  accept_state = r.randint(0,1)
  print("Initial state: ",init_state)
  print("Accept state: ", accept_state)
  alphabet = [0,1]
  func = lambda a: True or 0 
  usr_auto = auto.Automaton(states, init_state, accept_state, alphabet, func)

  test_automaton(usr_auto)#test automaton


  #Test 2
  states = gen_test_data(25)
  print(states)
  init_state = r.randint(0,1)
  accept_state = r.randint(0,1)
  print("Initial state: ",init_state)
  print("Accept state: ", accept_state)
  alphabet = [0,1]
  func = lambda a: True or 0 
  usr_auto = auto.Automaton(states, init_state, accept_state, alphabet, func)

  test_automaton(usr_auto)#test automaton

  #Test 3
  states = gen_test_data(125)
  print(states)
  init_state = r.randint(0,1)
  accept_state = r.randint(0,1)
  print("Initial state: ",init_state)
  print("Accept state: ", accept_state)
  alphabet = [0,1]
  func = lambda a: True or 0 
  usr_auto = auto.Automaton(states, init_state, accept_state, alphabet, func)
  
  test_automaton(usr_auto)#test automaton

  #Test 4
  #Generalized test
#  states = 
#  print(states)
#  init_state = r.randint(0,1)
#  accept_state = r.randint(0,1)
#  print("Initial state: ",init_state)
#  print("Accept state: ", accept_state)
#  alphabet = [0,1]
#  func = lambda a: True or 0 
#  usr_auto = auto.Automaton(states, init_state, accept_state, alphabet, func)
  
#  test_automaton(usr_auto)#test automaton



def test_automaton(automaton):
  """
  test the automaton
  >>>takes (Automaton) an automaton
  """
  automaton.process()#Process the data
    
  e_state = automaton.check_end_state()#check the end state
  automaton.print_results(e_state)#print results


def gen_test_data(test_range):
  states = [r.randint(0,1) for n in range(test_range)]
  return states
