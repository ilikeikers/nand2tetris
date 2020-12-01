# BOOK NOTES FOR nand2tetris PROGRAM

## Ike Patton

#### www.nand2tetris.org


# CHAPTER 1:

* Every Boolean operator can be expressed using And, Or and Not
* The number of Boolean functions that can be defined over 'n' binary variables is ((2)^2)^n
* Both Nand and Nor functions can construct each of the operations (And, Or, Not)
* "f" is an operation that operates on "n" variables and returns "m" binary results
* The gate that implements "f" will have "n input pins" and "m output pins"
* Logic gates are implemented as transistors etched in silicon
    * Chips are the result
* The hardware can be abstracted. Thanks electrical engineers. 
* Primitive gates lead to composite gates
* Hardware Description Languange (HDL) is used to model these chips

# Chapter 2:
* Most operations performed by digital computers can be reduced to elementary
  additions of binary numbers
* (10011)_two = 1*2^4 + 0*2^3 + 0*2^2 + 1*2^1 + 1*2^0 = 19
* (x_(n)x_(n-1)...x_0)_b = sum(n,i=0) x_i*b^i
* Can add bits from right to left just like decimal additions
* A binary system with n digits can generate a set of 2^n different bit
  patterns
* The 2's Complement Method (radix complement) is used to represent signed
  binary numbers
    * complement = 2^n - x (if x != 0) or 0 (otherwise)
    * 5 bit representation of -2:
        * minus(00010)_two = 2^5-(00010)_two = (32)_ten - (2)_ten = (30)_ten =
          (11110)_two
            * (00010)_two + (11110)_two = (00000)_two
    * Can code a total of 2^n signed numbers
        * Max: 2^(n-1)-1
        * Min: -2^(n-1)
    * All positive numbers begin with a 0
    * All negative numbers begin with a 1
    * Shortcut: flip all of the bits of x and add 1 to the result
