#!/usr/bin/env python3

import Automaton as auto
import random as r

def functionality_test():
  """
  creates a simple automaton
  """
  #Test 1
  states = [(0,1,2),(1,2,1),(2,1,2)]#state, a transfer, b transfer
  print(states)
  init_state = states[0]
  accept_states = [0,1]
  print("Initial state: ",init_state)
  print("Accept state: ", accept_states)
  alphabet = [0,1,2]
  func = lambda a: a=="a" and states[1] or states[2]  
  usr_auto = auto.Automaton(states, init_state, accept_states, alphabet, func)

  check = usr_auto.alpha_check()#alphabet check
  print(check)
  #test_automaton(usr_auto)#test automaton




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
