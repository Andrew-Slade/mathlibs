#!/usr/bin/env python3
import polynomial as p


def main():
  user_input_numeric_coeffs()


def user_input_numeric_coeffs():

  def inner_input_check(usrpoly):
    outputpolynomial = []
    print("Is this what you wanted: ")
    coeffs = usrpoly.polycoeffs()
    for i in len(coeffs):
      outputpoly.append(str() + "x^" +#TODO put in polynomial stuff

  coeffs = []
  print("Please input the number of coefficients: ")
  print("Example: 5x^2 + 1 = 5x^2 + 0x + 1 (3 coefficients)")
  coeffcount = int(input())
  print("Please input the coefficients from left to right: ")
  for i in range(coeffcount):
    print(i, ": ")
    coeffs.append(int(input()))
  poly = p.Polynomial(coeffcount,coeffs[:])  
  inner_input_check(poly)

  

main()
