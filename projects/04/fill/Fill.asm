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

// Put your code here.

  //Constant
  @black
  M=0
  M=!M
  @white
  M=0

(LOOP)
  //initiazlize pointer by address value of screen (MEM[POINTER]=SCREEN)
  @SCREEN
  D=A
  @POINTER
  M=D
  
  //if MEM[KBD]==0, whiten the screen ; else blacken the screen
  @KBD
  D=M
  @WHITEN
  D;JEQ

(BLACKEN)  
  // if MEM[POINTER] < KBD, blacken MEM[MEM[POINTER]]=1111111111111111
  // else jump to next loop
  @POINTER
  D=M
  @KBD
  D=A-D
  @LOOP
  D;JEQ
  @black
  D=M
  @POINTER
  A=M
  M=D

  // MEM[POINTER]+=1
  @POINTER
  M=M+1

  @BLACKEN
  0;JMP

(WHITEN)
  // if MEM[POINTER] < KBD, whiten MEM[MEM[POINTER]]=0000000000000000
  // else jump to next loop
  @POINTER
  D=M
  @KBD
  D=A-D
  @LOOP
  D;JEQ
  @white
  D=M
  @POINTER
  A=M
  M=D

  //MEM[POINTER]+=1
  @POINTER
  M=M+1

  @WHITEN
  0;JMP
