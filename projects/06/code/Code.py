class Code:

    def dest(self, mnemonic):
        self.binary=''
        self.destlist=['A','D','M']

        for value in self.destlist:
            if value in mnemonic:
                self.binary += '1'
            else:
                self.binary += '0'

        return self.binary



    def comp(self, mnemonic):
        self.binary = ''
        # determin firstbit
        if 'M' in mnemonic:
            self.binary+='1'
        else:
            self.binary+='0'

        # determin second-7thbit
        if mnemonic=='0':
            self.binary+='101010'
        elif mnemonic=='1':
            self.binary+='111111'
        elif mnemonic=='-1':
            self.binary+='111010'
        elif mnemonic=='D':
            self.binary+='001100'
        elif mnemonic == 'A' or mnemonic == 'M':
            self.binary+='110000'
        elif mnemonic == '!D':
            self.c='001101'
        elif mnemonic == '!A' or mnemonic == '!M':
            self.binary+='110001'
        elif mnemonic == '-D':
            self.binary+='001111'
        elif mnemonic == '-A' or mnemonic== '-M':
            self.binary+='110011'
        elif mnemonic == 'D+1':
            self.binary+='011111'
        elif mnemonic == 'A+1' or mnemonic == 'M+1':
            self.binary+='110111'
        elif mnemonic == 'D-1':
            self.binary+='001110'
        elif mnemonic == 'A-1' or mnemonic == 'M-1':
            self.binary+='110010'
        elif mnemonic == 'D+A' or mnemonic == 'D+M':
            self.binary+='000010'
        elif mnemonic == 'D-A' or mnemonic == 'D-M':
            self.binary+='010011'
        elif mnemonic == 'A-D' or mnemonic == 'M-D':
            self.binary+='000111'
        elif mnemonic == 'D&A' or mnemonic == 'D&M':
            self.binary+='000000'
        elif mnemonic == 'D|A' or mnemonic == 'D|M':
            self.binary+='010101'
        else:
            self.binary+='000000'

        return self.binary



    def jump(self, mnemonic):
        self.binary=''

        if mnemonic == 'JGT':
            self.binary+='001'
        elif mnemonic == 'JEQ':
            self.binary+='010'
        elif mnemonic == 'JGE':
            self.binary+='011'
        elif mnemonic == 'JLT':
            self.binary+='100'
        elif mnemonic == 'JNE':
            self.binary+='101'
        elif mnemonic == 'JLE':
            self.binary+='110'
        elif mnemonic == 'JMP':
            self.binary+='111'
        else:
            self.binary+='000'

        return self.binary

