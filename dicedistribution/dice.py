#!/usr/bin/env python3
#Copyright 2020, Andrew Slade, All rights reserved.

#dice rolling simulation library
#standard roll given by roll()
import random as rand
import functools as red
import pandas as pd
import collections as cl


def roll():
  """
  calls a standard roll simulation then outputs it 

  """
  print("Please enter in the sample size: ")
  sample = int(input())
  print("Please enter in the dice type: ")
  dice = int(input())
  rolls = d_roll(sample, dice)
  diceavg = average(rolls)
  dicecount = count(rolls)
  dicemode = mode(dicecount)
  output(diceavg, dicemode, dicecount)


def d_roll(samplesize, dicetype):
  """
  produces an array of rolls for a dice type

  >>>takes: (int) sample size
            (int) dice type (4,6,8,10,12,20)
  >>>returns: (list) dice rolls
  """
  darray = []
  for i in range(samplesize):
    darray.append(rand.randint(1,dicetype))#dice rolls
  return darray


def average(drolls):
  """
  produces an average of rolls for a dice type

  >>>takes: (list) dice rolls
  >>>returns: (int) average of rolls
  """
  sum = red.reduce(lambda a, b: a + b, drolls)#list sum
  avg = sum / len(drolls)#average that sum
  return avg


def mode(drolls):
  """
  produces a mode of rolls for a dice type

  >>>takes: (list) dice rolls
  >>>returns: (list) mode of rolls
  """
  dmode = []#element that is the mode
  dmodeindex = red.reduce(lambda a,b: a if a > b else b,
               drolls.values()) #find mode index
  for element in drolls:#iterate over Counter structure
    if drolls[element] == dmodeindex: #check value
      dmode.append(element) #add key
  return dmode


def count(drolls):
  """
  produces a count of rolls for a dice type

  >>>takes: (list) dice rolls
  >>>returns: (Counter) dice roll count
  """
  counter = cl.Counter(drolls)#return a counter with each roll
  return counter


def output(daverage, dmode, dcount):
  """
  produces output

  >>>takes: (int) average of the rolls
            (list) mode of the rolls
            (Counter) a collection of rolls
  >>>returns: nothing
  """
  print("Average: " + str(daverage))
  print("Mode: ", dmode)
  print("Dice pool:\n " , sorted(dcount.items()))

