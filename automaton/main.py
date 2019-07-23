#!/usr/bin/env python3
from Automaton import Automaton
from regular import reg_ex, pad

# you_play() runs an automaton on words of your choosing.
# function_test() runs some assertions to make sure basic things are behaving well.
# do_homework() does the homework assignment that was assigned July 17.

# The documentation of automaton.py (the Automaton class) is decent.

# The documentation of regular.py (the functions that compute a regular expression
# for a given automaton) is an ambitious project - the comments ARE an induction proof
# that the regular expression can be found.

# Hit "run" in the top bar if you want to run whatever is set up to run here right now.



# Run the tests to make sure the code isn't broken. Sorry, I don't remember how to
# do proper unit tests.


# I don't remember how to do unit tests properly, but asserts are a fine bandaid.


# 1. Make an automaton with no states and nothing happening.
A = Automaton(set(),set(),set(),set(),set())
assert(reg_ex(A) == "")


# 2. Make an automaton that only has one state and can loop by "a" but not "b".
A = Automaton({"q"},{"q"},{"q"},{"a","b"},"qaq")
assert(reg_ex(A) == "a*")


# 3. Make an automaton that just goes by move "d" to an end state but has extra useless alphabet letters.
A = Automaton({"0","F"},{"0"},{"F"},{"a","b","c","d","e","f"},"0dF")
assert(reg_ex(A) == "d")


# 4. Make an automaton that can recognize ab*a.
A = Automaton({"0","1","2"},{"0"},{"2"},{"a","b"},"0a1,1b1,1a2")
assert(reg_ex(A) == "ab*a")


# 5. Make an automaton that can recognize (aaa)*.
A = Automaton({"0","1","2"},{"0"},{"0"},{"a","b"},"0a1,1a2,2a0")
assert(reg_ex(A) == "(aaa)*")


# 6. Make an automaton that can recognize (aa+bb)*
A = Automaton({"0","1","2"},{"0"},{"0"},{"a","b"},"0a1,1a0,0b2,2b0")
assert(reg_ex(A) == "(aa+bb)*")


# 7. Make a non-deterministic automaton that matches a+aa.
A = Automaton({"0","1","2"},{"0"},{"2"},{"a"},"0a2,0a1,1a2")
assert(reg_ex(A) == "a+aa")


# 8. Make an automaton that matches a+aa using two accepting states.
A = Automaton({"0","1","2","3"},{"0"},{"2","3"},{"a"},"0a3,0a1,1a2")
assert(reg_ex(A) == "a+aa")


# 9. Make an automaton that matches a+aa using two initial states.
A = Automaton({"0","1","2","3"},{"0","2"},{"3"},{"a"},"2a3,0a1,1a3")
assert(reg_ex(A) in ["a+aa","aa+a"])


# 10. Make an automaton that matches bab*a+bbb*a. Credit to Allison Abels for finding this.
A = Automaton({"0","2","3","4"},{"0"},{"4"},{"a","b"},"0b2,2a3,2b3,3b3,3a4")
assert(reg_ex(A) == "bab*a+bbb*a")


def play_with_sample():
  read_words(sample_automaton())


def sample_automaton():
  """
  Creates a sample automaton and returns it.
  """
  # The states are a python Set. Name them whatever you want.
  states = {"0","1","2"} 

  # Choose one of the states to be the initial state. You need to give this a Set, but that Set usually only contains one state.
  init_state = {"0"}
  
  # The set of accepted states should also be a subset of the states.
  accept_states = {"0","1"}

  # The automaton works based on a set alphabet.
  alphabet = {"a","b"}

  #The transition diagram for the automaton is a set of edges. Each edge q1 --x--> q2 is represented by a tuple (not a list!) (q1, x, q2).
  # The constructor will accept the actual set, like below, or you can pass it a
  # simplified string that shows the edges. So either of the two lines below works.
  d = { ("0","a","1"), ("0","b","2"), ("1","a","2"), ("2","b","0") }
  d = "0a1,0b2,2b0"
  #create automaton
  usr_auto = Automaton(states, init_state, accept_states, alphabet, d)
  return usr_auto


def read_words(A):
  """
  Lets you actually type words and see the automaton read the word.
  >>> takes: an Automaton.
  """
  print("\n---")
  print("Working with this automaton:")
  print(A)
  print("Its regular expression is:", reg_ex(A))

  while True:
    #get user word
    print("---")
    print("Please enter the word you want to process, or press enter to quit this: ")
    usr_word = str(input())
    if usr_word is "":
      break
    elif any([letter not in A.alphabet() for letter in usr_word]):
      print("Your word needs to be in the alphabet ",A.alphabet())
    else:
      A.read_word(usr_word) #Read the user's word and see what happens.


def do_homework():
  print("--\nExercise 1")
  A = Automaton({"0","1","2","3"},{"0"},{"1","2"},{"a","b"},"0a1,0b2,1a3,2a1,2b3,3a2,3b1")
  print("Answer is: "+reg_ex(A))

  print("--\nExercise 2")
  A = Automaton({"0","1","2","3","4"},{"0"},{"1"},{"a","b"},"0a1,0a2,0a3,0b4,1b3,2a1,2b1,3a0,3b2,4a3,4b4")
  print("Answer is: "+reg_ex(A))

  print("--\nExercise ▲")
  A = Automaton({"0","1","2"},{"0"},{"0"},{"a","b"},"0a1,0b2,1b0,1b2,2a0,2a1")
  print("Answer is: "+reg_ex(A))

  print("--\nExercise 3")
  A = Automaton({"0","1","2","3","q","r","s"},{"0"},{"1","q"},{"a","b"},"0a1,0bq,1a2,1b3,2b1,2b3,3a1,3a2,qar,qbs,rbq,rbs,saq,sar")
  print("Answer is: "+reg_ex(A))

  print("--\nExercise 4")
  A = Automaton({"0","1","2","q","r","s"},{"0"},{"r"},{"a","b"},"0a1,0b2,1b0,1b2,2a0,2a1,1bq,qaq,qbr,qas,raq,ras,sbq,sbr")
  print("Answer is: "+reg_ex(A))  


def build_auto():
  print("")
  print("Building an automaton!")
  print("       An Automaton is made of:")
  print("       1/5: Q, the states.")
  print("       2/5: I, the initial state(s).")
  print("       3/5: F, the accepting state(s).")
  print("       4/5: S, the alphabet.")
  print("       5/5: d, a transition function.")
  print("Let's go.")

  while True:
    print("1/5: The states Q.")
    print("     Enter the names of your states with no separation.")
    print("     For example if you want four states, you might enter 0123 or ABCD.")
    string_of_states = str(input("     "))
    if len(string_of_states) is 0:
      print("Maybe you wanted an automaton with no states, but I doubt it, so...")
      return True
    elif any([s in "() +" for s in string_of_states]):
      print("     Um, can you not use parentheses, spaces, or pluses as names of states? That seems really confusing.")
    else:
      # If you use set() on a string, it makes a set out of the characters.
      Q = set(string_of_states)
      print("     OK, got your states: ",",".join(sorted(Q)))
      break

  while True:
    print("\n2/5: The initial state(s) I.")
    print("     Enter the names of your initial states with no separation.")
    print("     For example if you want two initial states 1 and 2, type 12.")
    string_of_initial_states = str(input("     "))
    if len(string_of_initial_states) is 0:
      print("Maybe you wanted an automaton with no initial states, but I doubt it, so...")
      return True
    if not all([q in Q for q in string_of_initial_states]):
      print("     You need to use the names of the states you chose before. Or press enter to quit.")
    else:
      # If you use set() on a string, it makes a set out of the characters.
      I = set(string_of_initial_states)
      print("     OK, got your initial state(s): ",",".join(sorted(I)))
      break

  while True:
    print("\n3/5: The accepting state(s) F.")
    print("     Enter the names of your accepting states with no separation.")
    print("     For example if you want two accepting states 1 and 2, type 12.")
    string_of_accepting_states = str(input("     "))
    if len(string_of_accepting_states) is 0:
      print("Maybe you wanted an automaton with no accepting states, but I doubt it, so...")
      return True
    if not all([q in Q for q in string_of_accepting_states]):
      print("     You need to use the names of the states you chose before. Or press enter to quit.")
    else:
      # If you use set() on a string, it makes a set out of the characters.
      F = set(string_of_accepting_states)
      print("     OK, got your accepting state(s): ",",".join(sorted(F)))
      break

  while True:
    print("\n4/5: The alphabet S.")
    print("     Enter your alphabet with no separation.")
    print("     For example if you want two letters, type ab.")    
    string_of_alphabet = str(input("     "))
    if len(string_of_alphabet) is 0:
      print("Maybe you wanted an automaton with no alphabet, but I doubt it, so...")
      return True
    if any([x in Q for x in string_of_alphabet]):
      print("     Warning: Your alphabet reuses some of the same letters as the states. OK I guess...")
    S = set(string_of_alphabet)
    print("     OK, got your alphabet: ",",".join(sorted(S)))
    break    
   
  while True:
    print("\n5/5: The transition function d.")
    print("     Enter your edges with commas between each edge but no spaces.") 
    print("     For example if you have an edge labeled 'a' taking you from state 0 to 1")
    print("                 and an edge labeled 'b' taking you from state 1 to 2,")
    print("                 then you should enter 0a1,1b2.")
    print("     Nondeterminism is fine, so enter 0a0,0a1,0a2,0a3 if you feel like it.")
    string_of_transition_function = str(input("     "))
    if len(string_of_transition_function) is 0:
      print("Maybe you wanted an automaton with no moves, but I doubt it, so...")
      return True
    all_edges_are_fine = True
    for edge in string_of_transition_function.split(","):
      if len(edge) is not 3:
        print("     The edge "+edge+" is not three characters. It should be of the form qxr for states q,r and letter x.")
        all_edges_are_fine = False
      else:
        if edge[0] not in Q:
          print("     The edge "+edge+" should start with a character that is in the set of states.")
          all_edges_are_fine = False
        if edge[1] not in S:
          print("     The edge "+edge+" should have a letter of the alphabet in the middle.")
          all_edges_are_fine = False
        if edge[2] not in Q:
          print("     The edge "+edge+" should end with a character that is in the set of states.")
    if all_edges_are_fine:
      d = string_of_transition_function
      break

  A = Automaton(Q, I, F, S, d)
  print("\nOkay, the automaton is complete. Now you can see it at work!")
  read_words(A)     



while True:
  print("---")
  print("It's Automata Time! ☺")
  print("What would you like to do?")
  print("  1: See an example automaton and watch it read words.")
  print("  2: Do the homework assignment that was assigned 7/17/2019.")
  print("  3: Build your own automaton and play with it.")

  do_the_thing = { "1": play_with_sample,
                   "2": do_homework,
                   "3": build_auto }

  your_choice = str(input())

  if your_choice in do_the_thing:
    do_the_thing[your_choice]()
