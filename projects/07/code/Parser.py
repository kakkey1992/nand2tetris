import re
import io


nowline='\n'
filestream = None

# need to be implemented
C_ARITHMETIC_REX = re.compile(r'add|sub|not|gt|neg|eq|gt|lt|and|or|not')
C_PUSH_REX = re.compile(r'^push[\s]+(local|argument|this|that|constant|pointer|temp|static)[\s]+[\d]+')
C_POP_REX =  re.compile(r'^pop[\s]+(local|argument|this|that|constant|pointer|temp|static)[\s]+[\d]+')

#C_LABEL_REX = re.compile(r'')
#C_GO_TO_REX = re.compile(r'')
#C_IF_REX = re.compile(r'')
#C_FUNCTION_REX = re.compile(r'')
#C_RETURN = re.compile(r'')
#C_CALL =  re.compile(r'')


class Parser:


    def __init__(self,filestream):
        self.filestream=filestream

    def hasMoreCommands(self):
        self.nowline=self.filestream.readline()
        return self.nowline

    def advance(self):
        # delete \n
        self.nowline=self.nowline.replace('\n','')
        # delete //
        self.nowline=self.nowline.split('//')[0]


    def commandType(self):
        if C_ARITHMETIC_REX.search(self.nowline):
            return 'C_ARITHMETIC'
        elif C_PUSH_REX.search(self.nowline):
            return 'C_PUSH'
        elif C_POP_REX.search(self.nowline):
            return 'C_POP'
        else:
            return 'False Command!'

    def arg1(self):
        self.splitted_command=self.nowline.split(' ')
        if len(self.splitted_command)==1:
            return self.splitted_command[0]

        elif len(self.splitted_command)>1:
            return self.splitted_command[1]

    def arg2(self):
        self.splitted_command=self.nowline.split(' ')
        if len(self.splitted_command) >=3:
            return self.splitted_command[2]
