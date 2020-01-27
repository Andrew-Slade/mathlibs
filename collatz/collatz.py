#!/usr/bin/env python3
#Copyright 2020, Andrew Slade, All rights reserved.
import sys

#collatz library

def collatz():
  '''Run an instance of collatz'''
  userVal = userinput() 
  newfile()
  #run a user specified number of times
  for value in range(1,userVal):
    array = []
    array.append(value)
    collatz_gen(value,str(value),array)
  print("Output done. Check collatz_output")
    
def newfile():
  '''creates a new file'''
  
  filein = open("collatz_output", "w")
  filein.write("")
  filein.close()
    

def userinput():
  '''get user input'''

  #user input block
  print("Please enter in a top boundary value: ")
  uInput =input()
  try:
    uIn = int(uInput)
    return uIn
  except ValueError:
    print("Not an integer")
    
    
def collatz_gen(i,initial,arr):
  """collatz test and output
  >> parameters:
         (int)  initial value
         (int)  unmodified initial value
         (list) collatz values  
  """
  def inner_collatz_troubleValues(ar):
    """inner function to find values for
        which the function grows

    >>>takes: (list)  an array of collatz values
    >>>returns: (list) values for which the collatz increases
    """
    values = []
    if(len(ar)) != 1:
      for i in range(len(ar)-1):
        if ar[i + 1] > 2*ar[i]:
          values.append(ar[i])
      return values
    else:
      return values

  def inner_collatz_output(arr,initial):
    """output function protected from any outside modification
    >>>takes: (list) collatz values
              (int) initial, unmodified value
    """
    tdivider = "****************************\n"
    divider = "****************************\n\n"
    infile = open("collatz_output", "a")
    infile.write(tdivider)
    infile.write(initial + " is done\n")
    for el in arr:
      if(len(arr)) > 1:
        infile.write(str(el)+" ")
      else:
        infile.write(str(el))
    infile.write("\nnumber of iterations: " + str(len(arr)))
    trouble = inner_collatz_troubleValues(arr)
    infile.write("\ngrowth values are: ")
    for ele in trouble:
      infile.write(str(ele) + " ")
    infile.write("\n")
    infile.write(divider)
    infile.close()

  #collatz block
  if i != 1:
    #collatz recursion
    if i % 2 == 0:
      i = i // 2
      arr.append(i)
      collatz_gen(i,initial,arr)  
    elif i % 2 == 1:
      i = 3 * i + 1
      arr.append(i)
      collatz_gen(i,initial,arr)
  else:
    #recursion catch
    inner_collatz_output(arr, initial)
