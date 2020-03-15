import os
import sys
import glob
import CodeWriter
import Parser

inputname = sys.argv[1]
c =  CodeWriter.CodeWriter(inputname)
c.writeInit()
vmfiles=[]

if '.vm' not in inputname:
    os.chdir(inputname)
    vmfiles=glob.glob(os.getcwd() + '/*.vm')  
else:
    vmfiles.append(os.getcwd()+'/'+inputname)

for vmfile in vmfiles:
    f=open(vmfile,'r')
    p = Parser.Parser(f)
    c.setFileName(vmfile.split('/')[-1].split('.')[0])

    while p.hasMoreCommands():
        p.advance()
        commandType=p.commandType()

        if commandType == 'C_ARITHMETIC':
            c.writeArithmetic(p.arg1())

        elif commandType == 'C_PUSH':
            c.writePushPop('push',p.arg1(),p.arg2())

        elif commandType == 'C_POP':
            c.writePushPop('pop',p.arg1(),p.arg2())

        elif commandType == 'C_LABEL':
            c.writeLabel(p.arg1())

        elif commandType == 'C_GOTO':
            c.writeGoto(p.arg1())

        elif commandType == 'C_IF':
            c.writeIf(p.arg1())

        elif commandType == 'C_FUNCTION':
            c.writeFunction(p.arg1(),p.arg2())
        
        elif commandType == 'C_CALL':
            c.writeCall(p.arg1(),p.arg2())

        elif commandType == 'C_RETURN':
            c.writeReturn()


c.close()

        

