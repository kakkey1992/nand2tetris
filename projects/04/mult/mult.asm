// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
  
 //##INITIALIZAION
  //i=0,sum=0,mask=1
  @i
  M=0
  @R2
  M=0

  //mask=1
  D=0
  @mask
  M=D+1
  
  //base=R0
  @R0
  D=M
  @base
  M=D

(LOOP) 
  //if i>=16 jump to END
  @i
  D=M
  @16
  D=D-A
  @END
  D;JGE

  //if ith-bit of R1>0, sum=sum+base
  @R1
  D=M
  @mask
  D=D&M
  @LABEL1
  D;JEQ
  @base
  D=M
  @R2
  M=D+M

(LABEL1)
  // i=i+1,base=2*base, mask=1 (i+1)th-bit ;0 otherwise
  @i
  M=M+1
  @base
  D=M
  @base
  M=D+M
  @mask
  D=M
  @mask
  M=D+M
  @LOOP
  0;JMP

(END)
  @ENDLOOP
  0;JMP
