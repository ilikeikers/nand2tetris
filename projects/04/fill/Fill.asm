// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(WATCH)
  @24576
  D = M
  @FILL
  D;JNE
  @WHITEN
  D;JEQ

(FILL)
  @SCREEN
  D = A
  @pixelLocation
  M = D
  @24575
  D = A
  @endLocation
  M = D
  (FILLLOOP)
  @endLocation
  D = M
  @pixelLocation
  D = D - M
  @BLACKEN
  D; JGE
  @WATCH
  D; JLT

(BLACKEN)
  @pixelLocation
  A = M
  M = -1
  @pixelLocation
  M = M + 1
  @FILLLOOP
  0;JMP

(WHITEN)
  @SCREEN
  D = A
  @pixelLocation
  M = D
  @24575
  D = A
  @endLocation
  M = D
  (CLEARLOOP)
  @endLocation
  D = M
  @pixelLocation
  D = D - M
  @CLEAR
  D; JGE
  @WATCH
  D; JLT

(CLEAR)
  @pixelLocation
  A = M
  M = 0
  @pixelLocation
  M = M + 1
  @CLEARLOOP
  0;JMP
