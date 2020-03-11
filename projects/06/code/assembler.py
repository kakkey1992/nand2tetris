import re
import sys
import Parser
import Code

f = open(sys.argv[1], 'r')
p = Parser.Parser(f)
c = Code.Code() 

out = open(sys.argv[1].split('.')[0]+'.hack','w')

while True:
    if p.hasMoreCommands():
        p.advance()
        commandType = p.commandType()
        print(commandType)
    else:
        break

    if commandType == 'A_COMMAND' or commandType == 'L_COMMAND':
        binary=''
        binary=binary+bin(int(p.symbol()))[2:].zfill(16)
        print(binary)
        out.write(binary+'\n')

    elif commandType == 'C_COMMAND':
        binary='111'
        binary=binary+c.comp(p.comp())+c.dest(p.dest())+c.jump(p.jump())
        print(binary)
        out.write(binary+'\n')

f.close()