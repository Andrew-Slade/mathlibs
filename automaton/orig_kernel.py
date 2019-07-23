#!/usr/bin/env python3

#Automaton test function

import Automaton as auto


def functionality_test():
  """
  creates a simple automaton
  >>> requirements: (a list of tuples) a list of states
                    (variable type) an initial state
                    (a list of variable type) accepted states
                    (a list of variable type) an alphabet
                    (function\lambda) a function to move the state
  """
  #(state,where a takes you, where b takes you)
  states = [(0,1,2),(1,2,1),(2,1,2)]#must be ordered by the first tuple val
  print(states) #print all states for user
  #the following correlate with the first tuple value
  init_state = states[0]#initial state
  accept_states = [0,1]#all accepted states
  print("Initial state: ",init_state)#print init state
  print("Accept state: ", accept_states)#print accept states
  alphabet = ["a","b"]#the automaton alphabet
  #lambda must accept a letter as a and a current state as b
  func = lambda a,b:  states[b[1]] if a=="a" else states[b[2]]  
  #create automaton
  usr_auto = auto.Automaton(states, init_state, accept_states, alphabet, func)
  
  #get user word
  print("Please enter in the word you want to process: ")
  usr_word = str(input())
  word_check = usr_auto.check_word(usr_word)#check user word

  #test automaton or break
  usr_auto.test_automaton(usr_word) if word_check else print("Ending")

