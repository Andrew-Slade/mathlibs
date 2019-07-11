#!/usr/bin/env python3


import Automaton as auto


def functionality_test():
  """
  creates a simple automaton
  """
  states = [(0,1,2),(1,2,1),(2,1,2)]#state, a transfer, b transfer
  print(states) #print all states for user
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
  test_automaton(usr_auto,usr_word) if word_check else print("Ending")


def test_automaton(automaton, word):
  """
  test the automaton
  >>> takes (Automaton) an automaton
  """
  print("Starting Automaton...")
  print(automaton.getI())#print init state
  for letter in word:
    automaton.process(letter)#Process the data and move states
  print("Automaton finished moving states")
    
  e_state = automaton.check_end_state()#check the end state
  automaton.print_results(e_state)#print results
