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
  @sum
  M=0

  //mask=1
  D=0
  @mask
  M=D+1
  
  //base=R0
  @0
  D=M
  //D=R0
  @base
  M=D

(LOOP) 
  //if i>=16 jump to END
  @i
  D=M
  @16
  D=D-A
  @END
  D;JLT

  //if ith-bit of R1>0, sum=sum+base
  @1
  D=M
  //D=R1
  @mask
  D=D&M
  @LABEL1
  D;JEQ
  @base
  D=M
  @sum
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
  @sum
  D=M
  @2
  M=D
  

(ENDLOOP)
  @ENDLOOP
  0;JMP
