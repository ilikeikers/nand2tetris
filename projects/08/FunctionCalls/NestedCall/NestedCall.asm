//function Sys.init 0
(Sys.init)
@0
D=A
@code_Sys.init
D;JEQ
(LCL_Sys.init)
@LCL
A=A+D
M=0
D=D-1
@LCL_assign_Sys.init
D;JEQ
@0
D=A
(Sys.init)
@LCL
D=A+D
@SP
M=D
//push constant 4000
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop pointer 0
@THIS
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//push constant 5000
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop pointer 1
@THAT
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//call Sys.main 0
@SP
D=M
@retAddr_Sys.main
M=D
@LCL
D=M
@retAddr_Sys.main
A=M+1
M=D
@ARG
D=M
@retAddr_Sys.main
A=M+1
A=A+1
M=D
@THIS
D=M
@retAddr_Sys.main
A=M+1
A=A+1
A=A+1
M=D
@THAT
D=M
@retAddr_Sys.main
A=M+1
A=A+1
A=A+1
A=A+1
M=D
A=A+1
D=A
@LCL
M=D
@SP
M=D
@retAddr_Sys.main
D=A
@0
D=D-A
@ARG
M=D
//pop temp 1
@1
D=A
@R5
D=A+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//label LOOP
(LOOP)
//goto LOOP
@LOOP
0;JMP
//function Sys.main 5
(Sys.main)
@5
D=A
@code_Sys.main
D;JEQ
(LCL_Sys.main)
@LCL
A=A+D
M=0
D=D-1
@LCL_assign_Sys.main
D;JEQ
@5
D=A
(Sys.main)
@LCL
D=A+D
@SP
M=D
//push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop pointer 0
@THIS
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//push constant 5001
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop pointer 1
@THAT
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop local 1
@1
D=A
@LCL
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop local 2
@2
D=A
@LCL
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop local 3
@3
D=A
@LCL
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
//call Sys.add12 1
@SP
D=M
@retAddr_Sys.add12
M=D
@LCL
D=M
@retAddr_Sys.add12
A=M+1
M=D
@ARG
D=M
@retAddr_Sys.add12
A=M+1
A=A+1
M=D
@THIS
D=M
@retAddr_Sys.add12
A=M+1
A=A+1
A=A+1
M=D
@THAT
D=M
@retAddr_Sys.add12
A=M+1
A=A+1
A=A+1
A=A+1
M=D
A=A+1
D=A
@LCL
M=D
@SP
M=D
@retAddr_Sys.add12
D=A
@1
D=D-A
@ARG
M=D
//pop temp 0
@0
D=A
@R5
D=A+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//push local 0
@0
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//push local 1
@1
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//push local 2
@2
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//push local 3
@3
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//push local 4
@4
D=A
@LCL
A=M+D
D=M
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
//return
@SP
A=M-1
D=M
@ARG
A=M
M=D
D=A+1
@SP
M=D
@LCL
A=M-1
D=M
@THAT
M=D
@LCL
A=M-1
A=A-1
D=M
@THIS
M=D
@LCL
A=M-1
A=A-1
A=A-1
D=M
@ARG
M=D
@LCL
A=M-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D
//function Sys.add12 0
(Sys.add12)
@0
D=A
@code_Sys.add12
D;JEQ
(LCL_Sys.add12)
@LCL
A=A+D
M=0
D=D-1
@LCL_assign_Sys.add12
D;JEQ
@0
D=A
(Sys.add12)
@LCL
D=A+D
@SP
M=D
//push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop pointer 0
@THIS
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//push constant 5002
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop pointer 1
@THAT
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//push constant 12
@12
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
//return
@SP
A=M-1
D=M
@ARG
A=M
M=D
D=A+1
@SP
M=D
@LCL
A=M-1
D=M
@THAT
M=D
@LCL
A=M-1
A=A-1
D=M
@THIS
M=D
@LCL
A=M-1
A=A-1
A=A-1
D=M
@ARG
M=D
@LCL
A=M-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D