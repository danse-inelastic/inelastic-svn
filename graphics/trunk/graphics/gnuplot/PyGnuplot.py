#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 7/30/2005 version 0.2a
# mmckerns@caltech.edu
# (C) 2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
__author__ = 'Mike McKerns'
__doc__ = '''Instructions for Pyre gnuplot component:
Import the PyGnuplot class        >>> from PyGnuplot import PyGnuplot
Instantiate the PyGnuplot class   >>> pg = PyGnuplot()
Get help                          >>> pg.help()
'''
from pyre.components.Component import Component

class PyGnuplot(Component):
    '''pyre gnuplot prompt component

Inventory:
  none
Methods:
  prompt() --> start interactive session
  eval(command) --> execute a gnuplot command
  put(name,val) --> put variable into interactive session
  get(name) --> get variable from interactive session
  who([name]) --> return the existing gnuplot variables
  delete(name) --> destroy selected pylab variables
  restart() --> restart a gnuplot window
  exit() --> exit a gnuplot session
Notes:
  gnuplot, gnuplot-py, and Numeric must be installed
'''
    def prompt(self):
        '''prompt() --> start interactive session'''
        self.session.prompt()
        return

    def eval(self,command):
        '''eval(command) --> execute a gnuplot command'''
        self.session.eval(command)
        return

    def put(self,name,val):
        '''put(name,val) --> put variable into interactive session'''
        self.session.put(name,val)
        return

    def get(self,name):
        '''get(name) --> get variable from interactive session'''
        return self.session.get(name)

    def who(self,name=None):
        '''who([name]) --> return the existing gnuplot variables'''
        return self.session.who(name)

    def delete(self,name):
        '''delete(name) --> destroy selected gnuplot variables'''
        self.session.delete(name)
        return

    def restart(self):
        '''restart() --> restart a gnuplot window'''
        vars = self.session.who()
        self.session.restart()
        self.session.whos = vars
        return

    def exit(self):
        '''exit() --> exit a gnuplot session'''
        self.session.exit()
        return

    def __init__(self, name='PyGnuplot', **kwds):
        Component.__init__(self, name, facility='gnuprompt')
        from gnuprompt import gnuplot
        self.session = gnuplot()
        return

    def __getattr__(self, name):
        if name.count('('): method = name.split('(')[0]
        else: method = None
        if method in ['prompt','eval','get','put','who',
                      'delete','restart','help','exit']:
            exec 'attr = self.'+name
        else:
            exec 'attr = self.session.'+name
        return attr

    def help(self):
        print self.__doc__
        return

# main
if __name__ == '__main__':
    x = [1,4,9,16,25,36,49,64,81]
    mp = PyGnuplot('test')
    mp.put('x',x)
    print mp.who()
    mp.exit()

# version
__id__ = "$Id: PyGnuplot.py 227 2007-09-25 16:33:11Z brandon $"

# End of file 

