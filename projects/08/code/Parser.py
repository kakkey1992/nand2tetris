import re
import io


nowline='\n'
filestream = None

# need to be implemented
C_ARITHMETIC_REX = re.compile(r'^(add|sub|not|gt|neg|eq|gt|lt|and|or|not)')
C_PUSH_REX = re.compile(r'^push[\s]+(local|argument|this|that|constant|pointer|temp|static)[\s]+[\d]+')
C_POP_REX =  re.compile(r'^pop[\s]+(local|argument|this|that|constant|pointer|temp|static)[\s]+[\d]+')
C_LABEL_REX = re.compile(r'^label[\s]+')
C_GOTO_REX = re.compile(r'^goto[\s]+')
C_IF_REX = re.compile(r'^if-goto[\s]+')
C_FUNCTION_REX = re.compile(r'^function[\s]+')
C_RETURN_REX = re.compile(r'^return')
C_CALL_REX =  re.compile(r'^call[\s]+')


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
        # delete spases at end of columns
        self.nowline=re.sub(r'[\s]+$','',self.nowline)
        print(self.nowline)


    def commandType(self):
        if C_ARITHMETIC_REX.search(self.nowline):
            return 'C_ARITHMETIC'
        elif C_PUSH_REX.search(self.nowline):
            return 'C_PUSH'
        elif C_POP_REX.search(self.nowline):
            return 'C_POP'
        elif C_LABEL_REX.search(self.nowline):
            return 'C_LABEL'
        elif C_GOTO_REX.search(self.nowline):
            return 'C_GOTO'
        elif C_IF_REX.search(self.nowline):
            return 'C_IF'
        elif C_CALL_REX.search(self.nowline):
            return 'C_CALL'
        elif C_FUNCTION_REX.search(self.nowline):
            return 'C_FUNCTION'
        elif C_RETURN_REX.search(self.nowline):
            return 'C_RETURN'
        else:
            return 'False Command!'

    def arg1(self):
        self.splitted_command=self.nowline.split(' ')
        print(self.splitted_command,len(self.splitted_command))
        print(self.commandType())
        if len(self.splitted_command)==1:
            return self.splitted_command[0]

        elif len(self.splitted_command)>1:
            return self.splitted_command[1]

    def arg2(self):
        self.splitted_command=self.nowline.split(' ')
        if len(self.splitted_command) >=3:
            return int(self.splitted_command[2])
