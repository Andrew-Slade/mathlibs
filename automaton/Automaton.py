#!/usr/bin/env python3

# A Non-Deterministic Finite State Automaton
# Base code for a Deterministic Finite State Automaton from Andrew Slade at https://github.com/Andrew-Slade July 11, 2019
# Refactored to handle multiple states and non-determinism by Chris Cunningham 7/17/2019

class Automaton:

  #Constructor
  def __init__(self, states, init_states, accept_states, alphabet, transition_function, Construction_Counter=[0]):

    # Make sure the states are okay.
    if not isinstance(states, set):
      raise TypeError("The states for an automaton must be a Set.")

    # Make sure the initial states are okay.
    if not isinstance(init_states, set):
      raise TypeError("The Initial States must be a Set. If you only want one initial state, make a set with one element.")
    if not init_states.issubset(states): 
      raise ValueError("The Initial States must be a subset of the States. You have an initial state that is not in the states for this automaton.")

    # Make sure the accepting states are okay.
    if not isinstance(accept_states, set):
      raise TypeError("The Accepted States must be a subset of the States. If you only want one accepted state, make a set with one element.")
    if not accept_states.issubset(states):
      raise ValueError("The Accepted States must be a subset of the States. You have an accepted state that is not in the states for this automaton.")

    # Make sure the alphabet is okay.
    if not isinstance(alphabet, set):
      raise TypeError("The alphabet for an automaton must be a Set.")
    if any(x in alphabet for x in ["*","(",")","+"]):
      raise ValueError("Your alphabet choices really make me question your sanity. To make me feel better, your alphabet shouldn't contain any of these four characters: *()+")    

    # Make sure the transition function is okay.
    if isinstance(transition_function, set):
      for edge in transition_function:
        if not isinstance(edge, tuple):
          raise TypeError("Each element of the set that makes up the transition function should be a Tuple.")
        if edge[0] not in states:
          raise ValueError("Each list in the set that makes up the transition function must have a valid state as its first element in position 0: the starting point of the arrow.")
        if edge[2] not in states:
          raise ValueError("Each list in the set that makes up the transition function must have a valid state as its third element in position 2: the ending point of the arrow.")
        if edge[1] not in alphabet:
          raise ValueError("Each list in the set that makes up the transition function must have a letter of the alphabet as its second element in position 1.")
    elif isinstance(transition_function, str):
      for e in transition_function.split(","):
        # For this to work all states mentioned in edges have to be one character.
        if len(e) is not 3:
          raise ValueError("If you construct an Automaton using a string for its transition function, the string should be a comma-delimited list of length 3 pieces, like 'qxr,qyr,qxs'. Consider passing a Set instead.")
        if e[0] not in states:
          raise ValueError("Each length 3 piece of the string must start with the name of a state. Failed on"+e)
        if e[1] not in alphabet:
          raise ValueError("Each length 3 piece of the string must have a letter of the alphabet in the middle. Failed on"+e)
        if e[2] not in states:
          raise ValueError("Each length 3 piece of the string must end with the name of a state. Failed on"+e)      
    else:
      raise TypeError("The transition function must be either a set of tuples, one for each edge, or a comma-delimited string of 3-character edges.")

    self.Q = states        # A set of states.
    self.I = init_states   # A set of initial states., which is a subset of Q; 
                           #   usually this is a set containing a single element of Q.
    self.F = accept_states # A set of accepted states. A subset of Q.
    self.S = alphabet      # An alphabet (a set of letters) that allows moves between states.

    if isinstance(transition_function, set):
      # You can pass a set of tuples directly.
      self.D = transition_function # A set of edges which are each tuples (q1, x, q2) meaning q1 --x--> q2.
                                   # The edge starts at q1 in Q, ends at q2 in Q, and is labeled by x in S.
    elif isinstance(transition_function, str):
      # If you pass a string, you are promising that the states are individual letters and things are easy.
      self.D = self.parse_transition_string(transition_function)

    self.C = self.I        # At the beginning, the automaton will be in these initial states.

    Construction_Counter[0] += 1
    self.ID = int(Construction_Counter[0])  # A quick unique identifier for the automaton.
    


  #Accessors
  def states(self):
    return self.Q
  def initial_states(self):
    return self.I
  def accepting_states(self):
    return self.F
  def alphabet(self):
    return self.S
  def transition_function(self):
    return self.D
  def current_states(self):
    return self.C
  def id(self):
    return self.ID

  # The string representation of the automaton
  def __repr__(self):
    return self.showatdepth(0)

  #  
  def showatdepth(self, depth):
    """
    Returns a string representation of the Automaton with padding based on the recursion depth.
    The recursion depth "depth" should be an integer, and usually 0.
    """
    return ("Automaton #"+str(self.ID)+
                  ": Alphabet "+", ".join([str(x) for x in sorted(self.S)])+
                  "; States: "+", ".join([str(q) for q in sorted(self.Q)])+
                  "; Initial "+", ".join([str(q) for q in sorted(self.I)])+
                  "; Accepting "+", ".join([str(q) for q in sorted(self.F)])+"\n"+
            pad(depth)+"Transition#"+str(self.ID)+": "+", ".join([str(e[0])+str(e[1])+str(e[2]) for e in self.D]))

  def successors(self, R, x):
    """
    Take a set of states R, a subset of Q, and a letter in S. Find all states that follow from elements of R along an edge labeled x.
    >>> takes: a Set of states R that is a subset of Q, and a letter x of the alphabet S.
    >>> returns: (Set) The set of states you can get to from q, following x. Maybe empty.
    """    
    if not all(self.isState(q) for q in R):
      raise ValueError("You can only find the successors of a set of states.")
    if not self.isLetter(x):
      raise ValueError("You have to follow a single letter of the alphabet if you want to go anywhere.")

    # We will eventually return set_of_successors. In case we don't find anywhere to go, though, we should probably start with the empty set.
    set_of_successors = set()

    # Now go through each edge in the diagram of the automaton:
    for e in self.D:
      # If we are following this type of edge right now:
      if e[1] == x:
        # And we are starting at the beginning of this edge:
        if e[0] in R:
          # Then we can end up at the end of this edge.
          set_of_successors.add(e[2])

    # Once you've covered all the edges, you have found all the possible places you can end.
    return set_of_successors

  def isState(self, q):
    """
    Check an object to see if it is a state in this automaton.
    >>> takes: (anything) a purported state.
    >>> returns: (boolean) whether that is really one of our states.
    """
    return q in self.Q

  def isLetter(self, x):
    """
    Check an object to see if it is a letter in the alphabet.
    >>> takes: (String) a purported letter.
    >>> returns: (boolean) whether that is really in our alphabet.
    """
    return x in self.S

  def isWord(self, word):
    """
    Check a users word to make sure it is made of letters in this automaton's alphabet.
    >>> takes: (string) a word
    >>> returns: (boolean) whether that word is over the proper alphabet.
    """
    return all(self.isLetter(letter) for letter in word)

  def process(self, x):
    """
    Move the current states C of this automaton following the letter x in S.
    >>> takes: (string) A letter in the alphabet S
    """
    if not self.isLetter(x):
      raise ValueError("You have to follow a single letter of the alphabet if you want to go anywhere.")
    self.C = self.successors(self.C, x)
    if len(self.C) is 0:
      print("Following letter", x, "leads nowhere.")
    else:
      print("Following letter", x, "leads to", ",".join(self.C))

  def isHappy(self):
    """
    Check end states vs current states
    >>> takes: nothing; instead checks its internal states "C".
    >>> returns: (boolean) whether the current set of states includes an accepting state.
    """    
    return any(q in self.F for q in self.C)
      
  def read_word(self, word):
    """
    test the automaton
    >>> takes: (string) a word made of letters in the alphabet S
    """
    if not self.isWord(word):
      raise ValueError("An automaton can only read a word made up of elements of its alphabet.")

    self.C = self.I
    print("                Starting at", ",".join(self.C))
    
    # For each letter in the word,
    for letter in word:
      self.process(letter) # Process this letter. This will change the internal state C of this automaton.

    print("The word is over. Let's see if we recognize it.")
    
    if self.isHappy():
      print("Yes! We have reached an accepting state; hooray!")
    else:
      print("No! We are not in an accepting state; sorry.")

    # Make sure the transition function is okay.
  def parse_transition_string(self, s):
    """
    Convert a string like "1x2,2x3,3y3" to a set of tuples {("1","x","2"),("2","x","3"),("3","y","3")}
    """
    set_of_edges = set()
    for e in s.split(","):
      set_of_edges.add( (e[0],e[1],e[2]) )

    return set_of_edges


def pad(depth):
  """
  Takes a recursion depth and returns an appropriate amount of indentation to try to be able to read what is going on.
  >>> takes: An integer, 0 or more
  >>> returns: Some spaces or whatever padding we want for something at this depth
  """
  return "> "*depth
