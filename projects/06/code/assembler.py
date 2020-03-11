import re
import sys
import Parser
import Code
import SymbolTable

f = open(sys.argv[1], 'r')
p = Parser.Parser(f)
c = Code.Code() 
s = SymbolTable.SymbolTable()
NUM_REX=re.compile(r'^[\d]+$')
address=0
VAL_BASE=16

# loop for making symboltable
while True:
    if p.hasMoreCommands():
        p.advance()
        commandType = p.commandType()
    else:
        break

    if commandType == 'A_COMMAND' or commandType == 'C_COMMAND':
        address+=1
    
    if commandType == 'L_COMMAND':
        label=p.getLabel()
        if not s.contains(label):
            s.addEntry(label,address)        


f.close()
f = open(sys.argv[1], 'r')
p = Parser.Parser(f)
out = open(sys.argv[1].split('.')[0]+'.hack','w')

# loop for assemble
while True:
    if p.hasMoreCommands():
        p.advance()
        commandType = p.commandType()
    else:
        break

    if commandType == 'A_COMMAND':
        binary='0'
        value=p.symbol()
        IsNum=NUM_REX.search(value)

        if IsNum:
            # remove 0b and padding 0 to 16bit
            binary+=bin(int(value))[2:].zfill(15)
        else:
            if s.contains(value):
                binary+=bin(s.getAddress(value))[2:].zfill(15)
            else:
                s.addEntry(value,VAL_BASE)
                binary+=bin(VAL_BASE)[2:].zfill(15)
                VAL_BASE+=1
        out.write(binary+'\n')

    elif commandType == 'C_COMMAND':
        binary='111'
        binary=binary+c.comp(p.comp())+c.dest(p.dest())+c.jump(p.jump())
        out.write(binary+'\n')
