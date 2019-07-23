from Automaton import Automaton

#
# Chris Cunningham July 18, 2019
# 
# This is a strange function. The function reg_ex takes a non-deterministic finite state
# automaton and tries to create a regular expression that recognizes its language.
#
# The strange part is that the function is recursively defined in a way that allows
# the comments of the code to literally be a proof by induction that the function terminates,
# actually finding the regular expression.
#
# The end result is that the comments are a proof of the tricky part of Kleene's Theorem,
# and the code is the algorithm for generating the desired regular expression.

def reg_ex(A, depth=0, known_strings={}, known_identifiers=[0]):
  """
  Takes a (non-deterministic) finite state automaton and returns a string 
  (a regular expression) that recognizes the same language. Follows the outline
  of a proof by induction that you can read along with in the comments.
  >>> takes: A, an Automaton. Supports non-determinism, multiple initial, and multiple ending states.
             depth, an integer used to track how deep we are in the recursion. 
                    Should be 0 if called naturally, or depth+1 if called inside this function. 
             known_strings, a dictionary containing entries like "ababa*+ab(ab)*a":"L1"
                    If you expect certain strings in the answer and you already
                    have a name for them, you can pass a dict in here. But either way,
                    the function will build up a dictionary of strings that are "too long" as it goes.
             known_identifiers, a list containing all the numbers that are reserved and should not be
                    used to name new strings. So for example if L1, L2, L3 are taken, known_identifiers
                    would be [0,1,2,3]. Starts at [0] so the first new string is L1.
  >>> returns: (string or None) a regular expression recognizing the same language, 
               proving its language is regular. In the rare case that the automaton accepts nothing, 
               not even the empty word, then this function will instead return None. 
               This doesn't break the proof -- we aren't interested in the empty language.
  """

  if not isinstance(A, Automaton): 
    raise TypeError("You can only find the regular expression of an Automaton.")
  show_work(A.showatdepth(depth), depth)

  # Kleene's Theorem part 3: All non-empty Recognizable Languages are Regular.
  # Proof:
  # (I) By induction on the number of states N of an automaton A that recognizes the language.
  N = len(A.states())
  # (I.a) Base Case: The language is recognizable by an automaton A with 0 states.
  if N == 0: 
        # In this case we have the empty language, so its regular expression is the empty string.
        return returnable_result("", depth, A)
  # (I.b) Base Case: The language is recognizable by an automaton A with 1 state. 
  if N == 1:
        # Call the one state q. In this case, the transition edges all go from q to q.
        # Each edge allows another possible letter in the language; you can have
        # as many of these letters as you like in whatever order you like.
        # For example, if you have edges a, f, f, b, and f, then the acceptable letters are [a, b, f],
        acceptable_letters = sorted(set([str(edge[1]) for edge in A.transition_function()]))
        # and the language is (a+b+f)*.
        resulting_string = reg_star(reg_add(acceptable_letters, known_strings, known_identifiers, A), known_strings)
        return returnable_result(resulting_string, depth, A)

  # (I.c) Induction Step: Suppose all automata with N-1 states recognize regular languages. Then 
  #       we want to show that any automaton with N states also recognizes a regular language. 
  #       Let A be an automaton with N states.
  #           
  # (I.c.1) We need only consider automata with one accepting state.
  if len(A.accepting_states()) > 1:
          # If our automaton has multiple accepting states, 
          show_work("This has "+str(len(A.accepting_states()))+" accepting states; split it into bits with one accepting state each.",depth)
          # then we can find a regular expression for the corresponding automata that
          # have one accepting state each,
          regexes = []
          for q in A.accepting_states():
              AA = Automaton(A.states(), A.initial_states(), {q}, A.alphabet(), A.transition_function())
              show_work("Descend "+str(A.id())+": Use only accepting state "+q+".", depth)
              regexes.append(reg_ex(AA, depth+1, known_strings, known_identifiers))
          # then use "+" to combine them together.
          resulting_string = reg_add(regexes, known_strings, known_identifiers, A)
          return returnable_result(resulting_string, depth, A)
  # So without loss of generality we can assume we have one accepting state.
  # Name the one accepting state "q."
  q,=A.accepting_states()
  # (I.c.2) We need only consider automata with one initial state. 
  if len(A.initial_states()) > 1:
          # If our automaton has multiple initial states, 
          show_work("This has "+str(len(A.initial_states()))+" initial states; split it into bits with one initial state each.",depth)
          # then we can find a regular expression for the corresponding automata that
          # have one accepting state each,
          regexes = []
          for q0 in A.initial_states():
              AA = Automaton(A.states(), {q0}, {q}, A.alphabet(), A.transition_function())
              show_work("Descend "+str(A.id())+": Use only initial state "+q0+".", depth)
              regexes.append(reg_ex(AA,depth+1,known_strings))
          # then use "+" to combine them together.
          resulting_string = reg_add(regexes, known_strings, known_identifiers, A)
          return returnable_result(resulting_string, depth, A)
  # So without loss of generality we can assume we have one initial state.
  # Name the one initial state "q0.""
  q0,=A.initial_states()

  # (I.c.3) We need only consider loop automata (same initial and accepting state). 
  if q is not q0:
          show_work("Automaton "+str(A.id())+" isn't a loop automaton.",depth)
          # If our automaton A has a different initial and accepting state,
          # then we will use the strategy from Jack Gallagher, reordered by Allison Smith,
          # as follows: Split accepted words into two parts. The first part will
          # contain all the loops starting and ending at q0. An automaton that accepts
          # these loops, call it A1, is a loop automaton. It is the same as A except that
          # it accepts q0 instead of q.
          A1 = Automaton(A.states(), A.initial_states(), {q0}, A.alphabet(), A.transition_function())
          # The second part, A2, has multiple cases:
          A2_regexes = []
          # It is all the ways to leave q0, reach q, and never revisit q0. To exhaust these,
          # look at each edge of the form q0 --x--> q2, 
          for edge in A.transition_function():        
            if edge[0] is q0 and edge[2] is not q0: 
              # (where q2 != q0,)  
              flag_no_edges_of_this_form = False
              x,q2 = edge[1],edge[2]
              # we make an automaton A2 that removes q0 completely: q0 isn't a state
              new_states = A.states().copy()
              new_states.remove(q0)
              # and you can't go to or from q0 anymore.
              new_transition_function = set([edge for edge in A.transition_function() if (edge[0] is not q0 and edge[2] is not q0)])
              # This automaton A2 starts at q2, and ends at q, but has no q0.
              A2 = Automaton(new_states, {q2}, {q}, A.alphabet(), new_transition_function)
              show_work("Descend "+str(A.id())+": Leaving "+q0+" using "+x+", heading for "+q2+", planning to never come back.",depth)
              A2_regex = reg_ex(A2,depth+1,known_strings)
              if A2_regex is not None:
                # Note that it is possible that the new automaton accepts *no* words,
                # not even the empty word. In this case, we discard this path out of q0.
                # Assuming the new automaton A2 accepts at least one word, this covers one of
                # the ways to get from q0 to q: take x, then whatever A2 does.
                A2_regexes.append(reg_concat(x,A2_regex))

          # If there are no edges of this form at all, so we can't even get out of q0,
          # then this is already the case of the automaton that accepts no words, not even 
          # the empty word. We aren't interested in this case; the theorem is about nonempty
          # languages. 
          if len(A2_regexes) is 0: 
            return returnable_result(None, depth, A)

          # To reach the accepting state in A, you can loop around as much as you want at q0,
          # which is represented by the automaton A1*, but eventually you have to be done 
          # with the starting state. Then you follow all the cases of A2. 
          # So the regular expression is A1* followed by the sum of all the A2 options.
          show_work("Descend "+str(A.id())+": Leaving "+q0+", but coming back.",depth)
          regex1 = reg_ex(A1,depth+1, known_strings, known_identifiers)
          resulting_string = reg_concat(reg_star(regex1, known_strings), reg_add(A2_regexes, known_strings, known_identifiers,A))
          return returnable_result(resulting_string, depth, A)
          # We know both regular expressions can be found because A1 is a loop automaton
          # and A2 has N-1 states, which means we can use the induction hypothesis.

  # So without loss of generality we can assume we are a loop automaton.

  # In total we have reduced to the case of a loop automaton A with initial state q0
  # and final state q. We need to construct a regular expression for this automaton.
  #
  show_work("Automaton "+str(A.id())+" is a loop automaton.", depth)
  # (I.c.4) The loop automaton A accepts a regular language.
          # The key plan:
          # If we can write a regular expression L that accepts exactly the words that loop 
          # exactly once from q back to q, then the overall regular expression will be L*.
          # So we need to find this regular expression L.
  regexes = []
  # We will find L by constructing an automaton *without the state q* that accepts the same language.
  # To do so, consider each pair (an edge leaving q, an edge entering q)
  startedges = [edge for edge in A.transition_function() if edge[0] is q and edge[2] is not q]
  endedges   = [edge for edge in A.transition_function() if edge[0] is not q and edge[2] is q]
  # (We will handle the case of a loop from q directly to q after this.)
  loopedges  = [edge for edge in A.transition_function() if edge[0] is q and edge[2] is q] 
  for startedge in startedges:
      # Say the edge starting at q is q --x1--> q1 
      x1,q1 = startedge[1],startedge[2]
      for endedge in endedges:
          # and the edge ending at q is q2 --x2--> q.    
          q2,x2 = endedge[0],endedge[1] 
          # Make a new automaton for this pair that is just A again, but with no q, 
          new_states = A.states().copy()
          new_states.remove(q)
          new_transition_function = set([edge for edge in A.transition_function() if (edge[0] is not q and edge[2] is not q)])
          # initial state q1, and accepted state q2.
          # Then this automaton AA has N-1 states, 
          AA = Automaton(new_states, {q1}, {q2}, A.alphabet(), new_transition_function)
          # so it has a regular expression M by the induction hypothesis.
          show_work("Descend "+str(A.id())+": Start by following "+x1+" toward "+q1+" and end by following "+x2+" from "+q2+" to "+q+".",depth)
          M = reg_ex(AA,depth+1, known_strings, known_identifiers)
          # There is one way M could fail to exist -- if its language is empty and does not even contain the empty word.
          # That means we are in the case that you can't leave by q1 and come back by q2.
          if M is not None:           
            # As long as we skip that, the regular expression xMy covers this way of looping once at q.
            regexes.append(reg_concat(reg_concat(x1,M),x2))
  # The last possibility is that there are one-edge loops from q to itself. Include those.
  for loopedge in loopedges:
      regexes.append(loopedge[1])
      
  # Once we cover all these cases, add them together to get L.
  L = reg_add(regexes, known_strings, known_identifiers, A)
  # Then we are done; the regular expression for A is L*.
  Lstar = reg_star(L, known_strings)
  return returnable_result(Lstar, depth, A)
  # QED

def reg_add(regexes, known_strings, known_identifiers, A):
  """
  Takes a list of things and puts plus between string representations of them and parentheses around them if there was more than one. So [3,4] should return "(3+4)" but [3] should return "3".
  This is the point in the regular expression construction where you sometimes get a really unwieldy object.
  So there is some effort here to make the answer human-readable. If the result is longer than some threshhold,
  instead name this string and add the name to the dictionary, then return the new name.
  >>> takes: regexes, a list of strings
             known_strings, a dictionary of things like "ababaa*+ab*":"L1"
             known_identifiers, a list of numbers we have already used to name strings.
  >>> returns: a string

  """
  # First remove all the empty strings and such from the list of regexes.
  regexes = sorted(set([s for s in regexes if len(s) > 0]))

  if len(regexes) == 1:
    return regexes[0]
  elif len(regexes) == 0:
    return ""
  else:
    # Okay there is a lot going on here.
    # First, [str x for x in regexes] makes a list of all the regular expressions we are adding, as strings.
    # Then, set( that ) removes duplicates. This is a mathematical fact: for regexes, a+a = a.
    # Then, sorted( that ) turns it back into a list and sorts it in order.
    # Then finally "+".join(that) puts all the pieces together with "+"s inbetween. 
    resulting_string = "+".join(sorted(set([str(x) for x in regexes])))

    # If the resulting string is really long, let's see if it is in the known_strings.
    if len(resulting_string) > 12:
      if resulting_string in known_strings:
        return known_strings[resulting_string]
      else:
        # In this case we need to invent a new name for this ridiculous string.

        # Find the next number we haven't used yet.
        new_identifier = known_identifiers[-1] + 1
        known_identifiers.append(new_identifier)

        # Name it Lthat. Like L1 or L2 etc.
        new_name = "L"+str(new_identifier)
        known_strings.update({resulting_string: new_name})

        # When this happens, we usually have one initial and accepting state.
        initial_state = ",".join(A.initial_states())
        accepting_state = ",".join(A.accepting_states())
        if initial_state is accepting_state:
          # If they are the same, we are in the midst of making *one* loop.
          prefix_words = "To get from "+initial_state+" to "+accepting_state+" using "+",".join(sorted(A.states()))+" only reaching "+initial_state+" once, let "
        else:
          # If they are not the same, we are trying to get from a to b without ever revisiting a.
          prefix_words = "To get from "+initial_state+" to "+accepting_state+" using "+",".join(sorted(A.states()))+" without revisiting "+initial_state+", let "

        print(prefix_words + new_name + " = " + resulting_string + ".")

        # Then just return the new name.
        return new_name
    else:
      # The string isn't that long, just ship it.
      return resulting_string

def grouped(s, mode):
  """
  Takes a string and a mode. The mode is either "concatenate" or "star." 
  Determines if the string needs parentheses around it before it gets concatenated or starred with something. 
  Returns either the original string or the string with parentheses around it.
  """
  if len(s) == 1:
    # If you are looking at a, you can concatenate or star that already.
    return s
  elif len(s) > 1 and s[0] == "(" and s[-1] == ")":
    # If you are looking at (a+b+c*), you can concatenate or star that already.
    return s
  elif len(s) == 0:
    # If you have the empty string, that's ready.
    return ""
  elif mode is "concatenate":
    if s[-1] is "*":
      # Whether you are looking at abc* or (a+b+c)*, you can concatenate  that already.
      return s
    for (index,char) in enumerate(s):
      # If you have abababab or a(a+b)b, that is concatenate ready, but not star ready. Check whether the +s are all inside parentheses.
      if char is "+":
        # Each + needs to be inside parentheses for this to be concatenate-ready.
        if s[:index].count("(") <= s[:index].count(")"):
          # We're not ready; this + has fewer (s before it than )s.
          return "("+s+")"
    return s
  elif mode is "star":
    # If you are looking at a+b+c*, you need parentheses first no matter what: (a+b+c*)
    return "("+s+")"
  
def reg_concat(r1, r2):
  """
  Takes two regular expressions and concatenates them.
  If either one is long, it gets parentheses.
  """

  if r1 is "" or r2 is "":
    # Don't go into all the parenthesis checking if one of the strings is empty.
    return r1 + r2
  elif r1.count("(") is 0 and r2.count("(") is 0:
    # If I concatenate "a" with "ab+aa+bb+ba", I would prefer if it "distributed" to cut down on parentheses.
    # Basically if neither one has parentheses, let's just tell it to distribute. Then we will only
    # use parentheses for the stars. Maybe this is good? Maybe this is too much distributing.
    regexes = []
    for term_1 in r1.split("+"):
      for term_2 in r2.split("+"):
        regexes.append(term_1 + term_2)  #This is + as string concatenation, sorry!!
    return "+".join(regexes)

  else:
    return grouped(r1, "concatenate") + grouped(r2, "concatenate")
  


def reg_star(s, known_strings):
  """
  Takes a string and stars it. If it's the blank string, starring it doesn't un-blank it. 
  If it's already a quantity star, don't re-star it.
  >>> takes: s, a String.
             known_strings, a dictionary of things like "ababaa*+ab*":"L1"
  >>> returns: A String.
  """
  if len(s) is 0:
    # If you star the empty string, it's still empty.
    return s  
  elif len(s) is 2 and s[1] is "*":
    # If you star a*, you get a*
    return s
  elif len(s) > 1 and s[0] == "(" and s[-2:] == ")*":
    # If you star (a+b+c)*, you get (a+b+c)*
    return s
  else:
    # If you star a+b+ccc, you get (a+b+ccc)*.
    resulting_string = grouped(s, "star") + "*"
    # If we already know this string, report it out. But leave the creation of new
    # known strings to the reg_add function.
    if resulting_string in known_strings:
      return known_strings[resulting_string]
    else:
      return resulting_string

def returnable_result(s, depth, A):
  """
  Get all the debug-printing and returning of results out of the main flow of the program.
  Basically just returns what you say to return.
  If s is None, say so.
  """
  if s is None:
      show_work("Answer "+str(A.id())+": None", depth)
  else:
      show_work("Answer "+str(A.id())+": "+s, depth)
  return s
  
def pad(depth):
  """
  Takes a recursion depth and returns an appropriate amount of indentation to try to be able to read what is going on.
  >>> takes: An integer, 0 or more
  >>> returns: Some spaces or whatever padding we want for something at this depth
  """
  return "> "*depth

def show_work(s, depth):
  """
  Takes a string s and reports it out to the screen, with some formatting.
  """
  # OH COME ON DO I HAVE TO
  you_have_to_show_your_work = False

  if you_have_to_show_your_work:
    # FINE
    print(pad(depth) + s)
  else:
    # HA I KNEW IT
    return


