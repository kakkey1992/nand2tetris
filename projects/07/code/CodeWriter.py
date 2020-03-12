import io 
import re

ArithmeticDict={
    'add':['@SP','A=M-1','D=M','@SP','AM=M-1','A=A-1','M=D+M']
}

PushPopDict={
    'constant':['@constant','D=A'], #@constant is set by setDict method
    'pushD':['@SP','A=M','M=D','@SP','M=M+1']
}


class CodeWriter:

    def __init__(self, inputfile):
        self.outfile = inputfile.split('.')[0] + '.asm'
        self.filestream = open(self.outfile, 'w')

    def setFileName(self, fileName):
        self.fileName=fileName

    def writeArithmetic(self, command):
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

