import re
from collections import deque
import JackTokenizer
import Token

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
        self.compileClass()

    def compileClass(self):
        self.writeBeginNonTerminalTag('class')
        self.compileKeyword('class')
        self.compileClassName()
        self.compileSymbol('{')

        while  self.getTokenValue(1) in ['static', 'field']:
            self.compileClassVarDec()

        while self.getTokenValue(1) in ['constructor','function','method']:
            self.compileSubroutine()

        self.compileSymbol('}')
            
        self.writeEndNonTerminalTag('class')


    def compileClassVarDec(self):
        self.writeBeginNonTerminalTag("classVarDec") 
        self.compileKeyword(['static','field'])
        self.compileType()
        self.compileVarName()

        while self.getTokenValue(1)==',':
            self.compileSymbol(',')
            self.compileVarName()

        self.compileSymbol(';')
        self.writeEndNonTerminalTag("classVarDec")



    def compileSubroutine(self):
        self.writeBeginNonTerminalTag("subroutineDec")

        self.compileKeyword(['constructor','function','method'])
        if self.getTokenValue(1) == 'void':
            self.compileKeyword('void')
        else:
            self.compileType()

        self.compileSubroutineName()

        self.compileSymbol('(')        
        self.compileParameterList()
        self.compileSymbol(')')
        
        self.compileSubroutineBody()

        self.writeEndNonTerminalTag("subroutineDec")

    def compileSubroutineBody(self):
        self.writeBeginNonTerminalTag("subroutineBody")
        
        self.compileSymbol('{')
        while self.getTokenValue(1)=='var':
            self.compileVarDec()
        self.compileStatements()
        self.compileSymbol('}')
        
        self.writeEndNonTerminalTag("subroutineBody")

    def compileParameterList(self):
        self.writeBeginNonTerminalTag("parameterList")
        if not self.getTokenValue(1)==')':
            self.compileType() 
            self.compileVarName()
            while self.getTokenValue(1)==',':
                self.compileSymbol(',') 
                self.compileType() 
                self.compileVarName() 
        self.writeEndNonTerminalTag("parameterList")

    def compileVarDec(self):
        self.writeBeginNonTerminalTag('varDec')

        self.compileKeyword('var')
        self.compileType()
        self.compileVarName()
    
        while self.getTokenValue(1)==',':
            self.compileSymbol(',')
            self.compileVarName()

        self.compileSymbol(';')

        self.writeEndNonTerminalTag('varDec')
            


    def compileStatements(self):
        self.writeBeginNonTerminalTag("statements")
        while self.getTokenValue(1) in ['if','do','let','return','while']:
            if self.getTokenValue(1)=='let':
                self.compileLet()
            elif self.getTokenValue(1)=='if':
                self.compileIf()
            elif self.getTokenValue(1)=='while':
                self.compileWhile()
            elif self.getTokenValue(1)=='do':
                self.compileDo()
            elif self.getTokenValue(1)=='return':
                self.compileReturn()
            
        self.writeEndNonTerminalTag("statements")
        
            

    def compileDo(self):
        self.writeBeginNonTerminalTag('doStatement')
        self.compileKeyword('do')
        self.compileSubroutineCall()
        self.compileSymbol(';')
        self.writeEndNonTerminalTag('doStatement')

    def compileSubroutineCall(self):
        if self.getTokenValue(2) == '(':
            self.compileSubroutineName()
            self.compileSymbol('(')
            self.compileExpressionList()
            self.compileSymbol(')')

        elif self.getTokenValue(2) == '.':
            self.compileIdentifier() # className or Varname
            self.compileSymbol('.') # . 
            self.compileSubroutineName() # subroutineName
            self.compileSymbol('(') 
            self.compileExpressionList()
            self.compileSymbol(')') 


    def compileLet(self):
        self.writeBeginNonTerminalTag('letStatement')
        self.compileKeyword('let')
        self.compileVarName()

        if self.getTokenValue(1)=='[':
            self.compileSymbol('[') 
            self.compileExpression()
            self.compileSymbol(']')

        self.compileSymbol('=')
        self.compileExpression()
        self.compileSymbol(';')

        self.writeEndNonTerminalTag('letStatement')
        

    def compileWhile(self):
        self.writeBeginNonTerminalTag('whileStatement')

        self.compileKeyword('while')

        self.compileSymbol('(') 
        self.compileExpression()
        self.compileSymbol(')')

        self.compileSymbol('{') 
        self.compileStatements()
        self.compileSymbol('}') 

        self.writeEndNonTerminalTag('whileStatement')

    def compileReturn(self):
        self.writeBeginNonTerminalTag('returnStatement')
        self.compileKeyword('return')
        if not self.getTokenValue(1)==';':
            self.compileExpression()
        self.compileSymbol(';') #;
        self.writeEndNonTerminalTag('returnStatement')

    def compileIf(self):
        self.writeBeginNonTerminalTag('ifStatement')

        self.compileKeyword('if') 
        self.compileSymbol('(') 
        self.compileExpression()
        self.compileSymbol(')')

        self.compileSymbol('{') 
        self.compileStatements()
        self.compileSymbol('}') 

        if self.getTokenValue(1)=='else':
            self.compileKeyword('else') 
            self.compileSymbol('{') 
            self.compileStatements()
            self.compileSymbol('}') 
        
        self.writeEndNonTerminalTag('ifStatement')


    def compileExpression(self):
        self.writeBeginNonTerminalTag("expression")
        self.compileTerm()

        while self.getTokenValue(1) in opList:
            self.compileSymbol(opList) 
            self.compileTerm()

        self.writeEndNonTerminalTag("expression")


    def compileTerm(self):
        self.writeBeginNonTerminalTag("term")

        if self.getTokenCategory(1)=='integerConstant':
            self.compileIntegerConstatnt() 
        elif self.getTokenCategory(1)=='stringConstant':
            self.compileStringConstant()
        elif self.getTokenValue(1) in keywordConstList:
            self.compileKeyword(keywordConstList) # keywordConstant
        
        elif self.getTokenValue(1)=='(':
            self.compileSymbol('(')
            self.compileExpression()
            self.compileSymbol(')')

        elif self.getTokenValue(1) in unaryOpList:
            self.compileSymbol(unaryOpList)
            self.compileTerm()

        elif self.getTokenCategory(1)=='identifier':
            if self.getTokenValue(2) in ['(','.']:
                self.compileSubroutineCall()
            elif self.getTokenValue(2) == '[':
                self.compileVarName()
                self.compileSymbol('[')
                self.compileExpression()
                self.compileSymbol(']')
            else:
                self.compileVarName()

        self.writeEndNonTerminalTag("term")



    def compileExpressionList(self):
        self.writeBeginNonTerminalTag('expressionList')
        if not self.getTokenValue(1)==')':
            self.compileExpression()

            while self.getTokenValue(1)==',':
                self.writeToken() #,
                self.compileExpression()

        self.writeEndNonTerminalTag('expressionList')

    def compileIdentifier(self):
        if self.getTokenCategory(1)=='identifier':
            self.writeToken()
        else:
            self.raise_syntax_error('identifier is required')
        
    def compileKeyword(self,value):
        if not self.getTokenCategory(1)=='keyword':
            self.raise_syntax_error('keyword is required')

        if type(value) is str:
            if self.getTokenValue(1) == value:
                self.writeToken()
            else:
                self.raise_syntax_error('unexpected keyword(str)')
        elif type(value) is list: 
            if self.getTokenValue(1) in value:
                self.writeToken()
        else:
            self.raise_syntax_error('unexpected keyword(list)')

    def compileClassName(self):
        self.compileIdentifier()

    def compileSymbol(self,value):
        if not self.getTokenCategory(1)=='symbol':
            self.raise_syntax_error('symbol is required')

        if type(value) is str:
            if self.getTokenValue(1) == value:
                self.writeToken()
            else:
                self.raise_syntax_error('unexpected symbol')
        elif type(value) is list: 
            if self.getTokenValue(1) in value:
                self.writeToken()
        else:
            self.raise_syntax_error('unexpected symbol')


    def compileType(self):
        if self.getTokenValue(1) in ['int','char','boolean']:
            self.compileKeyword(['int','char','boolean'])
        elif self.getTokenCategory(1)=='identifier':
            self.compileIdentifier()
        else:
            self.raise_syntax_error('unexpected type(not int or char or boolean or classname)')


    def compileVarName(self):
        self.compileIdentifier()

    def compileSubroutineName(self):
        self.compileIdentifier()
  
    def compileIntegerConstatnt(self):
        if self.getTokenCategory(1)=='integerConstant' and (0 <= int(self.getTokenValue(1)) <= 32767):
            self.writeToken()
        else:
            self.raise_syntax_error('Type is not integerConstant or notin [0,32767]')

    def compileStringConstant(self):
        if self.getTokenCategory(1)=='stringConstant':
            self.writeToken()
        else:
            self.raise_syntax_error('Type is not stringConstant')

    def getTokenCategory(self,index):
        self.token = self.tokens[index-1]
        return self.token.getType()
    
    def getTokenValue(self,index):
        self.token = self.tokens[index-1]
        return self.token.getValue()

    def writeToken(self):
        self.nowtoken = self.tokens.popleft()
        if self.nowtoken.getValue() in symbolMap.keys():
            self.writeStream.write("<%s> %s </%s>\n" % (self.nowtoken.getType(),symbolMap[self.nowtoken.getValue()],self.nowtoken.getType()))
        else:
            self.writeStream.write("<%s> %s </%s>\n" % (self.nowtoken.getType(),self.nowtoken.getValue(),self.nowtoken.getType()))

    def writeBeginNonTerminalTag(self,value):
        self.writeStream.write("<"+value+">\n")
    
    def writeEndNonTerminalTag(self,value):
        self.writeStream.write("</"+value+">\n")

    def raise_syntax_error(self, msg):
        msg += '\n the token type is : '
        msg += self.getTokenCategory(1)
        msg += '\n the token value is : '
        msg += self.getTokenValue(1)
        raise Exception('%s ' % msg)




