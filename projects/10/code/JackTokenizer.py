import re
import os
from collections import deque 
import Token

keywordList = [ 'class','constructor','function','method','field','static',
               'var','int','char','boolean','void','true','false','null',
               'this','let','do','if','else','while','return']

symbolList = [ '{','}','(',')','[',']','.',',',';','+','-','*','/','&',
              '|', '<','>','=','~']

symbolMap = { '<':'&lt;', '>':'&gt;', '&':'&amp;'}


class JackTokenizer():
    def __init__(self, filepass):
        self.filepass = filepass
        self.readStream = open(self.filepass,'r')
        self.outfilepass = re.sub(r'\.jack','myT.xml',self.filepass)
        self.writeStream = open(self.outfilepass,'w')
        self.fileData=self.readStream.read()

        #remove comments
        self.fileData=re.sub(r'\/\/(.*?)\n','\n',self.fileData)
        self.fileData=re.sub(r'\n','',self.fileData)
        self.fileData=re.sub(r'\/\*(.*?)\*\/','',self.fileData)

        self.fileDeque=deque(self.fileData)

        self.readTokens()
        self.writeTokens()

        self.readStream.close()
        self.writeStream.close()

    def readTokens(self):
        self.tokens=deque()
        while self.fileDeque:
            self.chunk=''
            self.now = self.fileDeque.popleft()

            if self.now in [' ','\t']:
                continue

            if self.now in symbolList:
                self.tokens.append(Token.Token("symbol",self.now))
                continue

            if self.now == '"':

                while True:
                    first = self.fileDeque.popleft()                   
                    
                    if first == '"':
                        self.tokens.append(Token.Token("stringConstant",self.chunk)) 
                        break

                    self.chunk = self.chunk + first
                continue

            while True:
                self.chunk = self.chunk + self.now
                self.now = self.fileDeque.popleft()

                if self.now in symbolList or self.now in [' ','\t']:
                    if self.chunk.isnumeric():
                        self.tokens.append(Token.Token("integerConstant",self.chunk)) 
                        
                    elif self.chunk in keywordList:
                        self.tokens.append(Token.Token("keyword",self.chunk)) 

                    else:
                        #self.tokens.append(["identifier",self.chunk])
                        self.tokens.append(Token.Token("identifier",self.chunk)) 

                    if self.now in symbolList:
                        self.tokens.append(Token.Token("symbol",self.now)) 

                    break


    def writeTokens(self):
        self.writeStream.write('<tokens>\n') 

        for token in self.tokens:
            if token.getValue() in symbolMap.keys():
                self.writeStream.write("<%s> %s </%s>\n" % (token.getType(),symbolMap[token.getValue()],token.getType()))
            else:
                self.writeStream.write("<%s> %s </%s>\n" % (token.getType(),token.getValue(),token.getType()))

        self.writeStream.write('</tokens>\n')




