import io 
import re

ArithmeticDict={
    'add': ['@SP','A=M-1','D=M','@SP','AM=M-1','A=A-1','M=D+M'],
    'sub': ['@SP','A=M-1','D=M','@SP','AM=M-1','A=A-1','M=D-M','M=-M'],
    'and': ['@SP','A=M-1','D=M','@SP','AM=M-1','A=A-1','M=D&M'],
    'or' : ['@SP','A=M-1','D=M','@SP','AM=M-1','A=A-1','M=D|M'],
    'not': ['@SP','A=M-1','M=!M'],
    'neg': ['@SP','A=M-1','M=-M'],

    # TrueX and CMPENDX will be changed befor output in writeArithmetic method
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

PushDict={

    # @constant will be changed befor output in writePushPop method
    'constant' : ['@constant','D=A'],

    # @index will be changed befor output in writePushPop method
    'local'    : ['@LCL','D=M','@index','A=D+A','D=M'],
    'argument' : ['@ARG','D=M','@index','A=D+A','D=M'],
    'this'     : ['@THIS','D=M','@index','A=D+A','D=M'],
    'that'     : ['@THAT','D=M','@index','A=D+A','D=M'],
    'pointer'  : ['@3','D=A','@index','A=D+A','D=M'],
    'temp'     : ['@5','D=A','@index','A=D+A','D=M'],

    # @Xxx.index will be changed befor output in writePushPop method
    'static'   : ['@Xxx.index','D=M'],
    
    # after get valu, push D
    'pushD':['@SP','A=M','M=D','@SP','M=M+1']
}

PopDict={

    # @index will be changed in write PushPop method
    'local'    : ['@LCL','D=M','@index','D=D+A','@R13','M=D',
                  '@SP','AM=M-1','D=M','@R13','A=M','M=D'],
    'argument' : ['@ARG','D=M','@index','D=D+A','@R13','M=D',
                  '@SP','AM=M-1','D=M','@R13','A=M','M=D'],
    'this'     : ['@THIS','D=M','@index','D=D+A','@R13','M=D',
                  '@SP','AM=M-1','D=M','@R13','A=M','M=D'],
    'that'     : ['@THAT','D=M','@index','D=D+A','@R13','M=D',
                  '@SP','AM=M-1','D=M','@R13','A=M','M=D'],
    'pointer'  : ['@3','D=A','@index','D=D+A','@R13','M=D',
                  '@SP','AM=M-1','D=M','@R13','A=M','M=D'],
    'temp'     : ['@5','D=A','@index','D=D+A','@R13','M=D',
                  '@SP','AM=M-1','D=M','@R13','A=M','M=D'],

    # @Xxx.index will be changed in writePushPop method
    'static'   : ['@SP','AM=M-1','D=M','@Xxx.index','M=D'],               

}

class CodeWriter:

    def __init__(self, inputfile):
        self.vmname = inputfile.split('.')[0]
        self.outfile = self.vmname + '.asm'
        self.filestream = open(self.outfile, 'w')
        self.cmpcount=0

    def setFileName(self, fileName):
        self.fileName=fileName

    def writeArithmetic(self, command):
        if command in ['eq','gt','lt']:
            self.cmpcount+=1
            ArithmeticDict[command][7]='@True'+str(self.cmpcount)
            ArithmeticDict[command][10]='@COMPEND'+str(self.cmpcount)
            ArithmeticDict[command][12]='(True'+str(self.cmpcount)+')'
            ArithmeticDict[command][14]='(COMPEND'+str(self.cmpcount)+')'

        for cmd in ArithmeticDict[command]:
            self.filestream.write(cmd+'\n')
        
    def writePushPop(self, command, segment, index):
        if command=='push':
            if segment == 'constant':
                PushDict[segment][0]='@'+str(index)     
            elif segment in ['local','argument','this','that','pointer','temp']:
                PushDict[segment][2]='@'+str(index)
            elif segment == 'static':
                PushDict[segment][0]='@'+self.fileName+'.'+str(index)

            for cmd in PushDict[segment]:
                self.filestream.write(cmd+'\n')
            
            for cmd in PushDict['pushD']:
                self.filestream.write(cmd+'\n')

        elif command=='pop':
            if segment in ['local','argument','this','that','pointer','temp']:
                PopDict[segment][2]='@'+str(index)

            elif segment == 'static':
                PopDict[segment][3]='@'+self.fileName+'.'+str(index)

            for cmd in PopDict[segment]:
                self.filestream.write(cmd+'\n')

    def close(self):
        self.filestream.close()

