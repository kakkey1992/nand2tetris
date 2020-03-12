import os
import sys
import glob
import CodeWriter
import Parser

inputname = sys.argv[1]
c =  CodeWriter.CodeWriter(inputname)

vmfiles=[]

if '.vm' not in inputname:
    vmfiles=glob.glob(os.getcwd() + '/*.vm')  
else:
    vmfiles.append(os.getcwd()+'/'+inputname)

for vmfile in vmfiles:
    f=open(vmfile,'r')
    p = Parser.Parser(f)

    while True:

        if p.hasMoreCommands():
            p.advance()
            commandType=p.commandType()
        else:
            break

        if commandType == 'C_ARITHMETIC':
            c.writeArithmetic(p.arg1())

        elif commandType == 'C_PUSH':
            c.writePushPop('push',p.arg1(),p.arg2())


c.close()

        

