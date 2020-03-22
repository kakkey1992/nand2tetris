import re
from collections import deque
import JackTokenizer

symbolMap = { '<':'&lt;', '>':'&gt;', '&':'&amp;'}
unaryOpList = ['-','~']
keywordConstList = ['true','false','null','this']
opList = ['+','-','*','/','&','|','>','<','=']

class CompilationEngine():

    def __init__(self,filepass):
        self.outfilename =  re.sub(r'\.jack','my.xml',filepass)
        self.writeStream = open(self.outfilename,'w')
        self.jt = JackTokenizer.JackTokenizer(filepass)
        self.tokens=self.jt.tokens
        self.level=0
        self.writeBeginNonTerminalTag('class',self.level)
        self.compileClass(self.level+1)
        self.writeEndNonTerminalTag('class',self.level)

    def compileClass(self,level):

        if self.valueCheck('class'):
            self.writeToken(level)

        if self.categoryCheck('identifier'):
            self.writeToken(level)
        
        if self.valueCheck('{'):
            self.writeToken(level)

        while  self.valueCheck('static') or self.valueCheck('field'):
            self.writeBeginNonTerminalTag("classVarDec",level)
            self.compileClassVarDec(level+1)
            self.writeEndNonTerminalTag("classVarDec",level)

        while self.valueCheck('constructor') or self.valueCheck('function') or self.valueCheck('method'):
            self.writeBeginNonTerminalTag("subroutineDec",level)
            self.compileSubroutine(level+1)
            self.writeEndNonTerminalTag("subroutineDec",level)

        if self.tokenCheck('symbol','}'):
            self.writeToken(level)


    def compileClassVarDec(self,level):
        if self.valueCheck('static') or self.valueCheck('field'):
            self.writeToken(level)

        #type    
        self.writeToken(level)
        #varName
        self.writeToken(level)
        while self.valueCheck(','):
            #','
            self.writeToken(level)
            #varName,identifier
            self.writeToken(level)

        if self.valueCheck(';'):
            self.writeToken(level)



    def compileSubroutine(self,level):
        self.writeToken(level) #constructor or function or method
        self.writeToken(level) # void or type
        self.writeToken(level) # subroutineName
        self.writeToken(level) #'('
        
        
        self.writeBeginNonTerminalTag("parameterList",level)
        self.compileParameterList(level+1)
        self.writeEndNonTerminalTag("parameterList",level)

        self.writeToken(level)  #')'

        self.writeBeginNonTerminalTag("subroutineBody",level)
        self.compileSubroutineBody(level+1)
        self.writeEndNonTerminalTag("subroutineBody",level)

    def compileSubroutineBody(self,level):
        self.writeToken(level) #'{'
        while self.valueCheck('var'):
            self.writeBeginNonTerminalTag('varDec',level)
            self.compileVarDec(level+1)
            self.writeEndNonTerminalTag('varDec',level)
        self.writeBeginNonTerminalTag("statements",level)
        self.compileStatements(level+1)
        self.writeEndNonTerminalTag("statements",level)
        self.writeToken(level+1)#'}'

    def compileParameterList(self,level):  
        if not self.valueCheck(')'):
            self.writeToken(level) # type  
            self.writeToken(level+1) # varName
            while self.valueCheck(','):
                self.writeToken(level) # ','
                self.writeToken(level) # 'type'
                self.writeToken(level) # varName

    def compileVarDec(self,level):
        if self.valueCheck('var'):
            #var
            self.writeToken(level)
            #type
            self.writeToken(level)
            #varname
            self.writeToken(level)
            
            while self.valueCheck(','):
                #,
                self.writeToken(level)
                #varname
                self.writeToken(level)

            #;
            self.writeToken(level)
            


    def compileStatements(self,level):
        while True:
            if self.valueCheck('let'):
                self.writeBeginNonTerminalTag('letStatement',level)
                self.compileLet(level+1)
                self.writeEndNonTerminalTag('letStatement',level)
            elif self.valueCheck('if'):
                self.writeBeginNonTerminalTag('ifStatement',level)
                self.compileIf(level+1)
                self.writeEndNonTerminalTag('ifStatement',level)
            elif self.valueCheck('while'):
                self.writeBeginNonTerminalTag('whileStatement',level)
                self.compileWhile(level+1)
                self.writeEndNonTerminalTag('whileStatement',level)
            elif self.valueCheck('do'):
                self.writeBeginNonTerminalTag('doStatement',level)
                self.compileDo(level+1)
                self.writeEndNonTerminalTag('doStatement',level)
            elif self.valueCheck('return'):
                self.writeBeginNonTerminalTag('returnStatement',level)
                self.compileReturn(level+1)
                self.writeEndNonTerminalTag('returnStatement',level)
            else:
                break
        
            

    def compileDo(self,level):
        self.writeToken(level) #do
        self.compileSubroutineCall(level)
        self.writeToken(level) #;

    def compileSubroutineCall(self,level):
        if self.getTokenValue(2) == '(':
            self.writeToken(level) # subroutineName
            self.writeToken(level) # ( 
            self.writeBeginNonTerminalTag('expressionList',level)
            self.compileExpressionList(level+1)
            self.writeEndNonTerminalTag('expressionList',level)
            self.writeToken(level) # )

        elif self.getTokenValue(2) == '.':
            self.writeToken(level) # className or Varname
            self.writeToken(level) # . 
            self.writeToken(level) # subroutineName
            self.writeToken(level) # (
            self.writeBeginNonTerminalTag('expressionList',level)
            self.compileExpressionList(level+1)
            self.writeEndNonTerminalTag('expressionList',level)
            self.writeToken(level) # )





    def compileLet(self,level):
        self.writeToken(level) #let
        self.writeToken(level) #verName

        if self.valueCheck('['):
            self.writeToken(level) #[
            self.writeBeginNonTerminalTag("expression",level)
            self.compileExpression(level+1)
            self.writeEndNonTerminalTag("expression",level)
            self.writeToken(level) #]

        self.writeToken(level) #=
        self.writeBeginNonTerminalTag("expression",level)
        self.compileExpression(level+1)
        self.writeEndNonTerminalTag("expression",level)
        self.writeToken(level) #;
        

    def compileWhile(self,level):
        self.writeToken(level) #while

        self.writeToken(level) #(
        self.writeBeginNonTerminalTag("expression",level)
        self.compileExpression(level+1)
        self.writeEndNonTerminalTag("expression",level)
        self.writeToken(level) #)

        self.writeToken(level) #{
        self.writeBeginNonTerminalTag("statements",level)
        self.compileStatements(level+1)
        self.writeEndNonTerminalTag("statements",level)
        self.writeToken(level) #}



    def compileReturn(self,level):
        self.writeToken(level) #retrun
        if not self.valueCheck(';'):
            self.writeBeginNonTerminalTag('expression',level)
            self.compileExpression(level+1)
            self.writeEndNonTerminalTag('expression',level)
        self.writeToken(level) #;

    def compileIf(self,level):
        self.writeToken(level) #if

        self.writeToken(level) #(
        self.writeBeginNonTerminalTag("expression",level)
        self.compileExpression(level+1)
        self.writeEndNonTerminalTag("expression",level)
        self.writeToken(level) #)

        self.writeToken(level) #{
        self.writeBeginNonTerminalTag("statements",level)
        self.compileStatements(level+1)
        self.writeEndNonTerminalTag("statements",level)
        self.writeToken(level) #}

        if self.valueCheck('else'):
            self.writeToken(level) #else
            self.writeToken(level) #{
            self.writeBeginNonTerminalTag('statements',level)
            self.compileStatements(level+1)
            self.writeEndNonTerminalTag('statements',level)
            self.writeToken(level) #}


    def compileExpression(self,level):
        self.writeBeginNonTerminalTag("term",level)
        self.compileTerm(level+1)
        self.writeEndNonTerminalTag("term",level)

        while self.getTokenValue(1) in opList:
            self.writeToken(level) #op
            self.writeBeginNonTerminalTag("term",level)
            self.compileTerm(level+1)
            self.writeEndNonTerminalTag("term",level)


    def compileTerm(self,level):
        if self.categoryCheck('integerConstant'):
            self.writeToken(level) # integerConstant
        elif self.categoryCheck('stringConstant'):
            self.writeToken(level) # stringConstant
        elif self.getTokenValue(1) in keywordConstList:
            self.writeToken(level) # keywordConstant
        
        elif self.valueCheck('('):
            self.writeToken(level) #(
            self.writeBeginNonTerminalTag('expression',level)
            self.compileExpression(level+1)
            self.writeEndNonTerminalTag('expression',level)
            self.writeToken(level) #)

        elif self.getTokenValue(1) in unaryOpList:
            self.writeToken(level) # unaryOp
            self.writeBeginNonTerminalTag('term',level)
            self.compileTerm(level+1)
            self.writeEndNonTerminalTag('term',level)

        elif self.categoryCheck('identifier'):
            if self.getTokenValue(2) in ['(','.']:
                self.compileSubroutineCall(level)
            elif self.getTokenValue(2) == '[':
                self.writeToken(level) # varName
                self.writeToken(level) # [
                self.writeBeginNonTerminalTag('expression',level)
                self.compileExpression(level+1)
                self.writeEndNonTerminalTag('expression',level)
                self.writeToken(level) # ]
            else:
                self.writeToken(level) # varName



    def compileExpressionList(self,level):
        if not self.valueCheck(')'):
            self.writeBeginNonTerminalTag('expression',level)
            self.compileExpression(level+1)
            self.writeEndNonTerminalTag('expression',level)

            while self.valueCheck(','):
                self.writeToken(level) #,
                self.writeBeginNonTerminalTag('expression',level)
                self.compileExpression(level+1)
                self.writeEndNonTerminalTag('expression',level)

    

    def tokenCheck(self,category,value):
        self.firsttoken = self.tokens[0]
        return category==self.firsttoken[0] and value==self.firsttoken[1]

    def categoryCheck(self,category):
        self.firsttoken = self.tokens[0]
        return category==self.firsttoken[0]

    def valueCheck(self,value):
        self.firsttoken = self.tokens[0]
        return value==self.firsttoken[1]

    def getTokenCategory(self,index):
        self.token = self.tokens[index-1]
        return self.token[0]
    
    def getTokenValue(self,index):
        self.token = self.tokens[index-1]
        return self.token[1]

    def writeToken(self,level):
        self.nowtoken = self.tokens.popleft()
        if self.nowtoken[1] in symbolMap.keys():
            self.nowtoken[1] = symbolMap[self.nowtoken[1]]
        self.writeStream.write("  "*level+"<%s> %s </%s>\n" % (self.nowtoken[0],self.nowtoken[1],self.nowtoken[0]))

    def writeBeginNonTerminalTag(self,value,level):
        self.writeStream.write("  "*level+"<"+value+">\n")
    
    def writeEndNonTerminalTag(self,value,level):
        self.writeStream.write("  "*level+"</"+value+">\n")




