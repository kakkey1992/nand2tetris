import re
import os
from collections import deque 

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
                self.tokens.append(["symbol",self.now])
                continue

            if self.now == '"':

                while True:
                    first = self.fileDeque.popleft()                   
                    
                    if first == '"':
                        self.tokens.append(["stringConstant",self.chunk]) 
                        break

                    self.chunk = self.chunk + first
                continue

            while True:
                self.chunk = self.chunk + self.now
                self.now = self.fileDeque.popleft()

                if self.now in symbolList or self.now in [' ','\t']:
                    if self.chunk.isnumeric():
                        self.tokens.append(["integerConstant",self.chunk])

                    elif self.chunk in keywordList:
                        self.tokens.append(["keyword",self.chunk])

                    else:
                        self.tokens.append(["identifier",self.chunk])

                    if self.now in symbolList:
                        self.tokens.append(["symbol",self.now])

                    break


    def writeTokens(self):
        self.writeStream.write('<tokens>\n') 

        for token in self.tokens:
            if token[1] in symbolMap.keys():
                self.writeStream.write("<%s> %s </%s>\n" % (token[0],symbolMap[token[1]],token[0]))
            self.writeStream.write("<%s> %s </%s>\n" % (token[0],token[1],token[0]))

        self.writeStream.write('</tokens>\n')



    
 