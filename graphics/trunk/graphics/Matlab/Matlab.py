#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Matlab.py
#
# 3/15/2005 version 0.0.2a
# mmckerns@caltech.edu
# (C) 2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
__author__='Mike McKerns'
__doc__ = '''Instructions for Pyre Matlab component:
Import the IDL class            >>> from Matlab import Matlab
Instantiate the IDL class       >>> ml = Matlab()
Get help                        >>> ml.help()
'''
from pyre.components.Component import Component

class Matlab(Component):
    '''Pyre Matlab (adapted from Matlab_mcomm.py)

Inventory:
  none
Methods:
  prompt([verbose]) --> start an interactive Matlab session
  eval(command,[verbose,stdout,buffersize]) --> eval a command
  put(name,val,[shape]) --> python into matlab
  get(name,[shape,array,reduce]) --> matlab into python
  who([name,terse,stdout]) --> show matlab ('whos'/'who')
  show([name,local,stdout,buffersize]) --> show Matlab variables
  delete(name) --> destroy the selected Matlab variable
  verbose([on]) --> get status of, or set, verbosity
  matlabhelp([name,buffersize]) --> print the Matlab help message
Notes:
  Reproduces Matlab in Python via the Simple API for Matlab (sam).
  Both Matlab and sam must be installed,
  and Matlab must be able to find a license.
'''
    def prompt(self,verbose=True):
        '''prompt([verbose]) --> start an interactive Matlab session'''
        return self.session.prompt(verbose)

    def eval(self,command,verbose=None,stdout=True,buffersize=1024):
        '''eval(command,[verbose,stdout,buffersize]) --> eval a command'''
        return self.session.eval(command,verbose,stdout,buffersize)

    def put(self,name,val,shape=None):
        '''put(name,val,[shape]) --> python into matlab'''
        return self.session.put(name,val,shape)

    def get(self,name,shape='?',array='?',reduce=False):
        '''get(name,[shape,array,reduce]) --> matlab into python'''
        return self.session.get(name,shape,array,reduce)

    def who(self,name=None,terse=True,stdout=True):
        '''who([name,terse,stdout]) --> show matlab ('whos'/'who')'''
        return self.session.who(name,terse,stdout)

    def show(self,name=None,local=False,stdout=False,buffersize=1024):
        '''show([name,local,stdout,buffersize]) --> show Matlab variables'''
        return self.session.show(name,local,stdout,buffersize)

    def delete(self,name):
        '''delete(name) --> destroy the selected Matlab variable'''
        return self.session.delete(name)

    def verbose(self,on=None):
        '''verbose([on]) --> get status of, or set, verbosity'''
        return self.session.verbose(on)

    def matlabhelp(self,name=None,buffersize=5120):
        '''matlabhelp([name,buffersize]) --> print the Matlab help message'''
        return self.session.help(name,buffersize)

    def __init__(self, name='Matlab', **kwds):
        Component.__init__(self, name, facility='matlab')
        import pymatlab
        self.session = pymatlab.matlab()
        return

    def help(self):
        print self.__doc__
        return

if __name__ == '__main__':
    mp = Matlab()
    mp.put('x',[1,2,3,4,5])
    print mp.show(local=True)
