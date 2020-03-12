import io 
import re

ArithmeticDict={
    'add': ['@SP','A=M-1','D=M','@SP','AM=M-1','A=A-1','M=D+M'],
    'sub': ['@SP','A=M-1','D=M','@SP','AM=M-1','A=A-1','M=D-M','M=-M'],
    'and': ['@SP','A=M-1','D=M','@SP','AM=M-1','A=A-1','M=D&M'],
    'or' : ['@SP','A=M-1','D=M','@SP','AM=M-1','A=A-1','M=D|M'],
    'not': ['@SP','A=M-1','M=!M'],
    'neg': ['@SP','A=M-1','M=-M'],

    'eq' : ['@SP','A=M-1','D=M','@SP','AM=M-1','A=A-1','D=D-M',
            '@TrueX','D;JEQ','D=0','@CMPENDX','0;JMP','(TrueX)',
            'D=-1','(CMPENDX)','@SP','A=M-1','M=D'],

    'gt' : ['@SP','A=M-1','D=M','@SP','AM=M-1','A=A-1','D=D-M',
            '@TrueX','D;JLT','D=0','@CMPENDX','0;JMP','(TrueX)',
            'D=-1','(CMPENDX)','@SP','A=M-1','M=D'],

    'lt' : ['@SP','A=M-1','D=M','@SP','AM=M-1','A=A-1','D=D-M',
            '@TrueX','D;JGT','D=0','@CMPENDX','0;JMP','(TrueX)',
            'D=-1','(CMPENDX)','@SP','A=M-1','M=D']
}

PushPopDict={
    'constant':['@constant','D=A'], #@constant is set by setDict method
    'pushD':['@SP','A=M','M=D','@SP','M=M+1']
}

class CodeWriter:

    def __init__(self, inputfile):
        self.outfile = inputfile.split('.')[0] + '.asm'
        self.filestream = open(self.outfile, 'w')
        self.cmpcount=0

    def setFileName(self, fileName):
        self.fileName=fileName

    def writeArithmetic(self, command):
        if command in ['eq','gt','lt']:
            self.cmpcount+=1
            self.counter = 0
            ArithmeticDict[command][7]='@True'+str(self.cmpcount)
            ArithmeticDict[command][10]='@COMPEND'+str(self.cmpcount)
            ArithmeticDict[command][12]='(True'+str(self.cmpcount)+')'
            ArithmeticDict[command][14]='(COMPEND'+str(self.cmpcount)+')'

        for cmd in ArithmeticDict[command]:
            self.filestream.write(cmd+'\n')
        
    def writePushPop(self, command, segment, index):
        if command=='push':
            if segment=='constant':
               PushPopDict[segment][0]='@'+str(index)

            for cmd in PushPopDict[segment]:
                self.filestream.write(cmd+'\n')
            
            for cmd in PushPopDict['pushD']:
                self.filestream.write(cmd+'\n')


    def close(self):
        self.filestream.close()

