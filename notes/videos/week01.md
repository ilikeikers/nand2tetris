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
