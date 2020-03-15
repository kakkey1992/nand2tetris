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

    # @constant will be changed befor output in writePush method
    'constant' : ['@constant','D=A'],

    # @index will be changed befor output in writePush method
    'local'    : ['@LCL','D=M','@index','A=D+A','D=M'],
    'argument' : ['@ARG','D=M','@index','A=D+A','D=M'],
    'this'     : ['@THIS','D=M','@index','A=D+A','D=M'],
    'that'     : ['@THAT','D=M','@index','A=D+A','D=M'],
    'pointer'  : ['@3','D=A','@index','A=D+A','D=M'],
    'temp'     : ['@5','D=A','@index','A=D+A','D=M'],

    # @Xxx.index will be changed befor output in writePush method
    'static'   : ['@Xxx.index','D=M'],
    
    # after get valu, push D
    'pushD':['@SP','A=M','M=D','@SP','M=M+1']
}

PopDict={

    # @index will be changed in writePop method
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

    # @Xxx.index will be changed in writePop method
    'static'   : ['@SP','AM=M-1','D=M','@Xxx.index','M=D'],               

}


nowFunction=['null']

class CodeWriter:

    def __init__(self, inputfile):
        self.vmname = inputfile.split('.')[0]
        self.outfile = self.vmname + '.asm'
        self.filestream = open(self.outfile, 'w')
        self.cmpcount=0
        self.labelindex=0

    def writeInit(self):
        self.writeSetSymbol('SP',256)
        self.writeSetSymbol('LCL',300)
        self.writeSetSymbol('ARG',400)
        self.writeSetSymbol('THIS',3000)
        self.writeSetSymbol('THAT',4000)
        self.writeCall('Sys.init',0)

    def writeSetSymbol(self,symbol,initialValue):
        self.cmdlist=['@'+str(initialValue),'D=A','@'+symbol,'M=D']
        for cmd in self.cmdlist:
            self.filestream.write(cmd+'\n')
            

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
            self.writePush(segment,index)
        elif command=='pop':
            self.writePop(segment,index)

    def writeLabel(self,label): 
        self.filestream.write('('+label+')\n')

    def writeGoto(self,label):
        # self.Gotolist=['@'+nowFunction[-1]+'$'+label,'0;JMP']
        self.Gotolist=['@'+label,'0;JMP']
        for cmd in self.Gotolist:
            self.filestream.write(cmd+'\n')

    def writeIf(self,label):
        # self.Iflist=['@SP','AM=M-1','D=M','@'+nowFunction[-1]+'$'+label,'D;JNE']
        self.Iflist=['@SP','AM=M-1','D=M','@'+label,'D;JNE']

        for cmd in self.Iflist:
            self.filestream.write(cmd+'\n')

    def writeFunction(self,functionName,numVar):
        # nowFunction.append(functionName)
        self.filestream.write('('+functionName+')\n')
        for _ in range(numVar):
            self.writePush('constant',0)

    def writeCall(self,functionName,numArg):
        self.labelindex += 1
        # Push Retrun address
        self.cmdlist=['@return_address'+str(self.labelindex),'D=A']
        for cmd in self.cmdlist:
            self.filestream.write(cmd+'\n')
        for cmd in PushDict['pushD']:
                self.filestream.write(cmd+'\n')

        # push LCL, push ARG, push THIS push THAT
        self.writePushSymbol('LCL')
        self.writePushSymbol('ARG')
        self.writePushSymbol('THIS')
        self.writePushSymbol('THAT')

        #ARG=SP-numArg-5
        self.cmdlist=['@SP','D=M','@'+str(numArg+5),'D=D-A','@ARG','M=D']
        for cmd in self.cmdlist:
            self.filestream.write(cmd+'\n') 

        #LCL=SP
        self.cmdlist=['@SP','D=M','@LCL','M=D']
        for cmd in self.cmdlist:
            self.filestream.write(cmd+'\n') 

        self.writeGoto(functionName)

        self.filestream.write('(return_address'+str(self.labelindex)+')\n') 

    def writePushSymbol(self, symbolName):
        self.cmdlist=['@'+symbolName,'D=M']
        for cmd in self.cmdlist:
            self.filestream.write(cmd+'\n')

        for cmd in PushDict['pushD']:
            self.filestream.write(cmd+'\n')


    def writeReturn(self):
        # nowFunction.pop()
        self.cmdlist=[]
        # R14=LCL, R15=RET=*(FRAME-5)
        
        # FRAME = LCL
        self.cmdlist=['@LCL','D=M','@R14','M=D']
        for cmd in self.cmdlist:
            self.filestream.write(cmd+'\n')

        # RET = *(FRAME-5)
        self.cmdlist=['@R14','D=M','@5','A=D-A','D=M','@R15','M=D']
        for cmd in self.cmdlist:
            self.filestream.write(cmd+'\n')

        #*ARG=pop()
        self.writePop('argument',0)

        #SP=ARG+1 
        self.cmdlist=['@ARG','D=M+1','@SP','M=D']
        for cmd in self.cmdlist:
            self.filestream.write(cmd+'\n')

        # THAT = *(FRAME - 1), THIS = *(FRAME - 2), ARG = *(FRAME - 3), LCL = *(FRAME -4)
        self.writeSetFrame('THAT', 1)
        self.writeSetFrame('THIS', 2)
        self.writeSetFrame('ARG', 3)
        self.writeSetFrame('LCL', 4)

        #goto RET
        self.cmdlist=['@R15','A=M','0;JMP']
        for cmd in self.cmdlist:
            self.filestream.write(cmd+'\n')


    def writePush(self, segment, index):
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
        

    def writePop(self, segment, index):
        if segment in ['local','argument','this','that','pointer','temp']:
            PopDict[segment][2]='@'+str(index)

        elif segment == 'static':
            PopDict[segment][3]='@'+self.fileName+'.'+str(index)

        for cmd in PopDict[segment]:
            self.filestream.write(cmd+'\n')

    def writeSetFrame(self, symbolName, index):
        self.cmdlist=['@R14','D=M','@'+str(index),'A=D-A','D=M','@'+symbolName,'M=D']
        for cmd in self.cmdlist:
            self.filestream.write(cmd+'\n')


    def close(self):
        self.filestream.close()

