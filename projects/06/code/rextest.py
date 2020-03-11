import re

NUM_REX=re.compile(r'^[\d]+$')

tsts=[]
tsts.append('123456')
tsts.append('234567')
tsts.append('a12345')
tsts.append('12345b')
tsts.append('12b45')

for tst in tsts:
    print(tst,NUM_REX.match(tst))


tmplist=['a','b','c','d']
print(tmplist[1:-1])

tmpstr='abcde'
print(tmpstr[1:-1])

if 'M' in 'A-1' 'M-1':
    print('list')

if 'b' in 'a' 'b':
    print('a')
