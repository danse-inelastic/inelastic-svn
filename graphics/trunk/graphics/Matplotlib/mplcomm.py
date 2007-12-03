#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# mplcomm.py
#
# 3/15/2005 version 0.0.2b
# mmckerns@caltech.edu
# (C) 2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
__author__='Mike McKerns'
__doc__='''Instructions for matplotlib scripting interface:
Import the matplotlib class     >>> from mplcomm import matplot
Instantiate the matplot class   >>> mp = matplot()
Get help                        >>> mp.doc()
'''
from matplotlib.numerix import *

class matplot:
    '''pylab interactive session
Methods:
  prompt() --> start interactive session
  eval(command) --> execute a pylab command
  put(name,val) --> put variable into interactive session
  get(name) --> get variable from interactive session
  who([name]) --> return the existing pylab variables
  delete(name) --> destroy selected pylab variables
'''
    _privdoc='''Private methods:
 _validate(name) --> raise NameError if is invalid python name
 _putlocal(name,value) --> add a variable to local store
 _getlocal(name) --> return variable value from local store
 _poplocal(name) --> delete variable from local store, return value
 _wholist() --> get list of strings containing pylab variables 
 _exists(name) --> True if is a variable in pylab
'''
    import pylab
 
    def __init__(self):
        self.whos = {}
        self.reserved = ['and','assert','break','class','continue','def','del',
                         'elif','else','except','exec','finally','for','from',
                         'global','if','import','in','is','lambda','not','or',
                         'pass','print','raise','return','try','while','yield',
                         'as','None']
        return

    def __getattr__(self, name):
        attr = None
        try:
            exec 'attr = self.pylab.'+name
        except:
            exec 'attr = self.get("'+name+'")'
        return attr

    def __setattr__(self,name,value):
        if name in ['whos','reserved']:
            self.__dict__[name] = value
            return
        self.put(name,value)
        return

    def __call__(self,*args):
        for arg in args:
            self.eval(arg)
        return

    def _validate(self,name):
        '''_validate(name) --> raise NameError if is invalid python name'''
        #a valid python name begins with a letter or underscore,
        #and can include only alphanumeric symbols and the underscore.
        #python also does not allow redefinition of reserved words.
        if not name: raise NameError, "invalid name"
        import re
        if re.compile('[_a-zA-Z]').sub('',name[0]):
            raise NameError, "invalid first character '%s'" % name[0]
        badc = re.compile('[_a-zA-Z0-9]').sub('',name)
        if badc: raise NameError, "invalid name '%s'; remove '%s'" % (name,badc)
        if name.lower() in self.reserved:
            raise NameError, "invalid name '%s'; is a reserved word" % name
        return

    def _putlocal(self,name,value):
        '''_putlocal(name,value) --> add a variable to local store'''
        self._validate(name)
        self.whos[name] = value
        return

    def _getlocal(self,name,skip=True):
        '''_getlocal(name) --> return variable value from local store'''
        if self.whos.has_key(name):
            return self.whos[name]
        if skip: return #name not found in local store
        raise NameError,"'%s' is not defined locally" % str(name)

    def _poplocal(self,name):
        '''_poplocal(name) --> delete variable from local store, return value'''
        return self.whos.pop(name,None)

    def _wholist(self):
        '''_wholist() --> get list of strings containing pylab variables'''
        return self.whos.keys()

    def _exists(self,name):
        '''_exists(name) --> True if is a variable in pylab'''
        exists = self._wholist().count(name)
        if exists: return True
        return False

    def doc(self):
        print self.__doc__
        return

    def put(self,name,val):
        '''put(name,val) --> add variable to pylab session'''
        if name.count('[') or name.count('.') or name.count('('):
            varlist = self._wholist()
            for var in varlist: #put whos into locals()
                exec var+" = self._getlocal('"+var+"')"
            if type(val) is type(array([])):
                val = val.tolist()
                exec name+' = array('+str(val)+')'
            else: exec name+' = '+str(val) #put new var value into locals()
            for var in varlist: #use varlist to update state variables
                exec 'self._putlocal("'+var+'",locals()["'+var+'"])'
            return
        return self._putlocal(name,val)

    def get(self,name):
        '''get(name) --> value; get value from pylab session'''
        varlist = self._wholist()
        for var in varlist: #put whos into locals()
            exec var+" = self._getlocal('"+var+"')"
        exec '___ = '+name #get from locals() as temp variable
        return ___

    def who(self,name=None):
        '''who([name]) --> return the existing pylab variables'''
        if name: return self._getlocal(name,skip=False)
        return self.whos

    def delete(self,name):
        '''delete(name) --> destroy selected pylab variables'''
        if not name.count(','):
            self._poplocal(name)
            return
        vars = name.split(',')
        for var in vars:
            self.delete(var.strip())
        return

    def eval(self,com):
        '''eval(command) --> execute a pylab command'''
        outlist = []
        if self.whos: #add to outlist
            for name,val in self.whos.items():
                if type(val) is type(array([])):
                    val = val.tolist()
                    exec name+' = array('+str(val)+')'
                else: exec name+' = '+str(val)
                exec 'outlist.append("'+name+'")'
        if com == 'exit':
            return
        try: #if intended for python
            exec com
            if com.startswith('del '):
                names = com.split('del ')[1].strip()
                self.delete(names)
                return
            if com.count('='):
                name = com.split('=')[0].strip()
                if not name.count('['):
                    outlist.append(name)
        except:
            try: #if intended for matplotlib
                exec 'self.pylab.'+com
            except: #is unknown command
                raise "CommandError", com
        for name in outlist: #use outlist to update state variables
            if name in locals().keys():
                exec 'self._putlocal("'+name+'",locals()["'+name+'"])'
        return

    def prompt(self):
        '''an interactive matplotlib session'''
        outlist = []
        print "MATPLOTLIB interface:"
        if self.whos: #print 'put' variables, add to outlist
            print "vars="
            for name,val in self.whos.items():
                if type(val) is type(array([])):
                    val = val.tolist()
                    exec name+' = array('+str(val)+')'
                else: exec name+' = '+str(val)
                exec 'print "    ","'+name+'"'
                exec 'outlist.append("'+name+'")'
        while 1:
            com = raw_input('>> ')
##          print com
            if com == 'exit':
                break
            else:
                try: #if intended for python
                    exec com
                    if com.startswith('del '):
                        names = com.split('del ')[1].strip()
                        vars = names.split(',')
                        for var in vars:
                            self.delete(var.strip())
                            outlist.remove(var.strip())
                    if com.count('='):
                        name = com.split('=')[0].strip()
                        if not name.count('['):
                            outlist.append(name)
                except:
                    try: #if intended for matplotlib
                        exec 'self.pylab.'+com
                    except: #is unknown command
                        print "CommandError: %s" % com
        for name in outlist: #use outlist to update state variables
            if name in locals().keys():
                exec 'self._putlocal("'+name+'",locals()["'+name+'"])'
        return


if __name__ == "__main__":
    x = [1,2,3,4,5]
    m = matplot()
    m.put('x',x)
    m.eval("y = array([1,4,9,16,25])")
    m.eval("z = array([[1,2],[3,4]])")
    m.prompt()
    print m.who()
