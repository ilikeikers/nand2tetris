//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//eq
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@TRUE_EQ0
D;JEQ
@FALSE_EQ0
D;JNE
(TRUE_EQ0)
@SP
A=M
M=-1
@PUSH_EQ0
0;JMP
(FALSE_EQ0)
@SP
A=M
M=0
(PUSH_EQ0)
@SP
M=M+1
//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
//eq
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@TRUE_EQ1
D;JEQ
@FALSE_EQ1
D;JNE
(TRUE_EQ1)
@SP
A=M
M=-1
@PUSH_EQ1
0;JMP
(FALSE_EQ1)
@SP
A=M
M=0
(PUSH_EQ1)
@SP
M=M+1
//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//eq
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@TRUE_EQ2
D;JEQ
@FALSE_EQ2
D;JNE
(TRUE_EQ2)
@SP
A=M
M=-1
@PUSH_EQ2
0;JMP
(FALSE_EQ2)
@SP
A=M
M=0
(PUSH_EQ2)
@SP
M=M+1
//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//lt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@TRUE_LT3
D;JLT
@FALSE_LT3
D;JGE
(TRUE_LT3)
@SP
A=M
M=-1
@END_LT3
0;JMP
(FALSE_LT3)
@SP
A=M
M=0
(END_LT3)
@SP
M=M+1
//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
//lt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@TRUE_LT4
D;JLT
@FALSE_LT4
D;JGE
(TRUE_LT4)
@SP
A=M
M=-1
@END_LT4
0;JMP
(FALSE_LT4)
@SP
A=M
M=0
(END_LT4)
@SP
M=M+1
//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//lt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@TRUE_LT5
D;JLT
@FALSE_LT5
D;JGE
(TRUE_LT5)
@SP
A=M
M=-1
@END_LT5
0;JMP
(FALSE_LT5)
@SP
A=M
M=0
(END_LT5)
@SP
M=M+1
//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//gt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@TRUE_GT6
D;JGT
@FALSE_GT6
D;JLE
(TRUE_GT6)
@SP
A=M
M=-1
@END_GT6
0;JMP
(FALSE_GT6)
@SP
A=M
M=0
(END_GT6)
@SP
M=M+1
//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
//gt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@TRUE_GT7
D;JGT
@FALSE_GT7
D;JLE
(TRUE_GT7)
@SP
A=M
M=-1
@END_GT7
0;JMP
(FALSE_GT7)
@SP
A=M
M=0
(END_GT7)
@SP
M=M+1
//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//gt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@TRUE_GT8
D;JGT
@FALSE_GT8
D;JLE
(TRUE_GT8)
@SP
A=M
M=-1
@END_GT8
0;JMP
(FALSE_GT8)
@SP
A=M
M=0
(END_GT8)
@SP
M=M+1
//push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
//add
@SP
AM=M-1
D=M
@SP
AM=M-1
D=D+M
@SP
A=M
M=D
@SP
M=M+1
//push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@SP
A=M
M=D
@SP
M=M+1
//neg
@SP
AM=M-1
M=-M
@SP
M=M+1
//and
@SP
AM=M-1
D=M
@SP
AM=M-1
D=D&M
@SP
A=M
M=D
@SP
M=M+1
//push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
//or
@SP
AM=M-1
D=M
@SP
AM=M-1
D=D|M
@SP
A=M
M=D
@SP
M=M+1
//not
@SP
AM=M-1
M=!M
@SP
M=M+1