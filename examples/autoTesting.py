'''
This file performs the automatic testing for all the cases in .........
'''

import numpy as np
import glob
import os 
import re
import pytest

def readstp(fn):
  f = open(fn, 'r')
  for i in f:
    exec(i)
  f.close()
  globals().update(locals())

def readin(fn,nin):
  f = open(fn, 'r')
  data = f.readlines()
  return data[nin]

def modin(fn,nin,strIn):
  f = open(fn, 'r')
  data = f.readlines()
  f.close()
  data[nin] = strIn
  with open(fn, 'w') as file:
    file.writelines( data )
  return

def chkRes():
  return
#############################################################
# define execution variables
wfold = os.getcwd()
mainFold = wfold[:[_.start() for _ in re.finditer('/',wfold)][-1]]
compiler = 'generic-laptop'
tfold = 'utils/testing/templateTest/'
#
doDBG = ['0']#,'1']
doCuda= ['0']
doProc= ['1 1\n']#,'2 2\n']
#
cdir = os.getcwd()
apps = [ name for name in os.listdir() if os.path.isdir(os.path.join(name))]

os.system('rm '+wfold+'/test.out')
fileOut = open('test.out','w')
for dbgFlag    in doDBG:
  for cudaFlag in doCuda:
    for app  in apps:
        os.chdir(wfold+'/'+app)
        testcases = [ name for name in os.listdir() if os.path.isdir(os.path.join(name))]
    #          print(testcases)
        os.chdir(mainFold+'/src')
        os.system('make  clean>/dev/null;'+
                  'make APP='+app+' ARCH='+compiler+ ' Do_DBG='+dbgFlag+' -j8>/dev/null')
        if 'flutas' in os.listdir():
          print('app '+app+', debug='+dbgFlag+' : compiled-------> PASSED')
          fileOut.write('app '+app+', debug='+dbgFlag+' : compiled -------> PASSED\n')
          for case in testcases:
            os.chdir(wfold+'/'+app+'/'+case)
            if len(glob.glob('test*'))>0:
              os.system('cp '+mainFold+'/src/flutas .')
              for procN  in doProc:
                tmp = procN.split(' ')
                nmpi = int(tmp[0])*int(tmp[1])
                modin('dns.in',-2,procN)
                os.system('mpirun -np '+str(nmpi)+' flutas>/dev/null')
                testout = pytest.main()
                testout = str(testout)[str(testout).find('.')+1:]
                fileOut.write('test '+case+' np='+str(nmpi)+'-------> '+testout+'\n') 
                os.system('rm -rf data __pycache__ flutas;'+
                          'git checkout *.in')
    #'test '+tn+': compiled [debug='+dbgFlag+' cuda='+cudaFlag+' mpi='+str(nmpi)+' comp='+compiler+']')
        else:
          print('test '+app+', debug='+dbgFlag+' : compilation failed \n')
          exit()
##        dbgFlag  = '0'
##        cudaFlag = '0'
#        readstp(cdir+'/'+tn+'/test.stp')
##        a = readin(cdir+'/'+tn+'/dns.in',-2)
#        a = procN.split(' ')
#        nmpi = int(a[0])*int(a[1])
#        os.chdir(wfold+'src')
#        os.system('cp '+conf+'/* .')
#        os.system('make -f Makefile.mc clean>/dev/null; make -f Makefile.mc COMP='+compiler+ ' DBG_FLAG='+dbgFlag+'USE_CUDA='+cudaFlag+'>/dev/null')

#        os.system('cp flutas '+cdir+'/'+tn)
#        os.chdir(cdir+'/'+tn)
#        modin('dns.in',-2,procN)
#        os.system('mpirun -np '+str(nmpi)+' cans>/dev/null')
#        print('test '+tn+': run [debug='+dbgFlag+' cuda='+cudaFlag+' mpi='+str(nmpi)+' comp='+compiler+']')
#        fileOut.write('test '+tn+': run [debug='+dbgFlag+' cuda='+cudaFlag+' mpi='+str(nmpi)+' comp='+compiler+']')
#        chkRes()
#        os.system('rm -r data cans')
#        os.chdir(cdir)
fileOut.close()
