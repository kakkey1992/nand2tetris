class Symboltable:

    def __init__(self):
        self.symboltable={}
        self.symboltable['R0']=0
        self.symboltable['R1']=1
        self.symboltable['R2']=2
        self.symboltable['R3']=3
        self.symboltable['R4']=4
        self.symboltable['R5']=5
        self.symboltable['R6']=6
        self.symboltable['R7']=7
        self.symboltable['R8']=8
        self.symboltable['R9']=9
        self.symboltable['R10']=10
        self.symboltable['R11']=11
        self.symboltable['R12']=12
        self.symboltable['R13']=13
        self.symboltable['R14']=14
        self.symboltable['R15']=15
        self.symboltable['SCREEN']=16384
        self.symboltable['KBD']=24576
        self.symboltable['SP']=0
        self.symboltable['LCL']=1
        self.symboltable['ARG']=2
        self.symboltable['THIS']=3

    def addEntry(self, symbol, address):
        self.symboltable[symbol]=address

    def contains(self,symbol):
        return symbol in self.symboltable.keys()

    def getAddress(self,symbol):
        return self.symboltable[symbol]
