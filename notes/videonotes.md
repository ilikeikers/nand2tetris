# Boolean Logic

## Unit 1.1

* Commutative Laws
    * (x AND y) = (y AND x)
    * (x OR y) = (y OR x)

* Associative Laws
    * (x AND(y AND z)) = ((x AND y) AND z)
    * (x OR(y OR z)) = ((x OR y) OR z)

* Distributive Laws
    * (x AND(y OR z)) = (x AND y) OR (x AND z)
    * (x OR(y AND z)) = (x OR y) AND (x OR z)

* De Morgan's Laws
    * !(x AND y) = !x OR !y
    * !(x OR y) = !x AND !y

## Unit 1.2

* Function synthesis from a truth table
    * Write an expression that produces '1' for each row of the truth table containing a '1' answer
    * OR all the expressions together

* Proof for any function expressed containing AND and NOT
    * (x OR y) = !(!x AND !y)

* NAND
    * (x NAND y) = !(x AND y)
    * Only NAND Required 
        * !x = (x NAND x)
        * (x AND y) = !(x NAND y)

## Unit 1.3

* Logic Gates
    * Elementary (NAND, AND, OR...)
        * AND: if (a==1 and b==1) then out=1 else out=0
        * OR: if (a==1 or b==1) then out=1 else out=0
        * NOT: if (in=0) then out=1 else out=0
    * Composite (MUX, ADDR...)

## Unit 1.4

* Designing Chips
    * Need a full and complete description of the gate's behavior
        * Truth table for example

* HDL 
    * Contains the chips interface as the header and the implementation as the body
    * Begins with a description of the chip
        * In a comment /** ... */
        * Single line comment //
    * Name the chip
        * CHIP ... {
    * Name the inputs/outputs
        * IN a, b, c...;
        * OUT out;
     * Define the implementation
        * PARTS: ...... }
    * Unlimited "thin out"
        * Can copy a given signal as many times as needed

* HDL Comments
    * Make sure comment and documantation are there for readability
    * HDL is static code, we will implement procedural later

## Unit 1.5/1.6

* Tutorial on HDL

## Unit 1.7

* Multiplexor
    * Output 'a' if 'sel'==0 and 'b' if 'sel'==1
    * Other gates can be put before the mux gate to create logic that changes
      based on the desired behavior

* Demultiplexor
    * Takes one input and produces an output on certain channels based on the
      selector
    
* Selectors can be set as oscillators for communication networks

# Boolean Arithmetic and the ALU

## Unit 2.1

* Converting binary to decimal: 2^n + 2^n-1 ... 2^0 
* Converting decimal to binary: start with the largest power of 2 to fit in the
  number and work your way down

## Unit 2.2

* Adders will contain a carry bit and a sum bit to be implimented

## Unit 2.3

* With n bits, can represent the positive integers in the range:
    * 0...2^(n)-1
    * Represent Negative number '-x' using the positive number 2^(n)-x
        * Using this, positive numbers in range: 0...2^(n-1)-1
        * Negative numbers in range: -1...-2^(n-1)
        * Shortcut to find complement: flip all the bits and add one

# Unit 2.4

* Hack ALU:
    * Two 16-bit data inputs (x, y)
    * Single 16-bit output
    * Output determined by six control bits (zx, nx, zy, ny, f, no)
    * Two 1-bit control outputs (zr, ng)
        * if out == 0 then zr=1, else zr=0
        * if out < 0 then ng=1, else ng=0
* Simplicity is the ultimate sophistication

# Unit 2.5

* Half-Adder
    * Takes two bits, adds them up and outputs a carry and sum bit
    * Sum truth table == Xor truth table
    * Carry truth table == And truth table

* Full-Adder
    * Sums up three bits, same Carry and Sum output
    * Can be built from two Half-Adders

* 16-Bit Adder
    * Sequence of 16 Full-Adders

* 16-Bit Incrementer
    * Takes in one input and adds 1 to it
    * The single-bit 0 and 1 values are represented in HDL as false and true

* ALU
    * Add16 and various Project 1 chips to use
    * Can be built with less than 20 lines of HDL code
      




