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
    c.setFileName(vmfile.split('/')[-1].split('.')[0])

    while p.hasMoreCommands():
        p.advance()
        if p.commandType() == 'C_ARITHMETIC':
            c.writeArithmetic(p.arg1())

        elif p.commandType() == 'C_PUSH':
            c.writePushPop('push',p.arg1(),p.arg2())

        elif p.commandType() == 'C_POP':
            c.writePushPop('pop',p.arg1(),p.arg2())

c.close()

        

