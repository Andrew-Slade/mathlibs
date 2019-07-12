#!/usr/bin/env python3

class Polynomial(object):
  def __init__(self, deg, *argv):
    self.degree = 0
    self.degree = deg
    self.coefficients = argv[0]
  
  def printcoeffs(self):
    print(self.coefficients)
 
  def polycoeffs(self):
    return self.coefficients
