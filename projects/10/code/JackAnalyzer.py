import os
import sys
import glob
import CompilationEngine

inputname = sys.argv[1]
filepasses=[]

if '.jack' not in inputname:
    os.chdir(inputname)
    filepasses=glob.glob(os.getcwd() + '/*.jack')  
else:
    filepasses.append(os.getcwd()+'/'+inputname)

for filepass in filepasses:
    ce=CompilationEngine.CompilationEngine(filepass)





    
    #while jt.hasMoreTokens():
     #   jt.advance()

