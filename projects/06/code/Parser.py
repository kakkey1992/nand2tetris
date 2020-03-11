import re
import io



nowline='\n'
filestream = None
symbol = ''
A_COMMAND_REX = re.compile(r'^@[\w]+')
C_COMMAND_REX = re.compile(r'^[AMD0]') # 改良の余地あり
L_COMMAND_REX = re.compile(r'^\([\w]+\)$')
NUM_REX=re.compile(r'[\d]+')

class Parser:

    def __init__(self,filestream):
        self.filestream = filestream

    def hasMoreCommands(self):
        #入力を受け取る。
        self.nowline=self.filestream.readline()
        return self.nowline

    def advance(self):
        #改行削除
        self.nowline=self.nowline.replace('\n','')
    
    def commandType(self):
        
        if A_COMMAND_REX.match(self.nowline):
            return 'A_COMMAND'
        elif L_COMMAND_REX.match(self.nowline):
            return 'L_COMMAND'
        elif C_COMMAND_REX.match(self.nowline):
            return 'C_COMMAND'
        else:
            return "False Command!"
    
    def symbol(self)->str:
        self.searchobject=re.search(r'[\w]+',self.nowline)
        return self.searchobject.group()

    def dest(self):
        if '=' in self.nowline:
            return self.nowline.split('=')[0]
        else:
            return ''

    def comp(self):
        if '=' in self.nowline:
            return self.nowline.split('=')[1]
        elif ';' in self.nowline:
            return self.nowline.split(';')[0]
        else:
            return ''

    def jump(self):
        if ';' in self.nowline:
            return self.nowline.split(';')[1]
        else:
            return ''
