#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  samtest.py
#  
#  7/18/2005 version 0.0.1a
#  mmckerns@caltech.edu
#  (C) 2005 All Rights Reserved
# 
#  <LicenseText>
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from graphics.Matlab.pymatlab import matlab as Matlab
from Numeric import *

import unittest

class PyMatlab_samlab_TestCase(unittest.TestCase):
    def setUp(self):
        '''Matlab: instantiate a pymatlab session'''
        self.session = Matlab()
        self.int = 1
        self.list = [1,2]
        self.array = array(self.list)
        self.dict = {'foo':1, 'bar':2}
        self.matrix = [[1,2,3],[4,5,6]]
        self.none = None
        self.str = 'foo'
        self.bytearray = array(self.str)
        self.strlist = ["hello", "world"]
        return #FIXME: do I want a new session for each test?

    def tearDown(self):
        '''Matlab: destroy a pymatlab session'''
        self.session = None
        return #FIXME: do I want a new session for each test?

#   def test_SAMdependancy(self):
#       '''Matlab: check package dependancies'''
#       self.assert_(exec 'import Numeric' == None,
#                    "failure to import Numeric")
#       return

    def test_SAM_validate(self):
        '''Matlab: fail upon invalid name'''
        self.assert_(self.session._validate("foo") == None,
                     "failure to validate a valid variable")
        self.assert_(self.session._validate("f_o1o") == None,
                     "failure to validate a valid variable")
        self.assertRaises(NameError,self.session._validate,'1foo')
        self.assertRaises(NameError,self.session._validate,'$foo')
        self.assertRaises(NameError,self.session._validate,'f.oo')
        self.assertRaises(NameError,self.session._validate,'foo!')
        self.assertRaises(NameError,self.session._validate,'for')
        self.assertRaises(NameError,self.session._validate,self.int)
        self.assertRaises(NameError,self.session._validate,self.list)
        return

    def test_SAM_putlocal(self):
        '''Matlab: add variable to local store'''
        self.assert_(self.session._putlocal("a",self.int) == None,
                     "failure to add scalar to local store")
        self.assert_(self.session._putlocal("b",self.list) == None,
                     "failure to add list to local store")
        self.assert_(self.session._putlocal("c",self.array) == None,
                     "failure to add array to local store")
        self.assert_(self.session._putlocal("n",self.none) == None,
                     "failure to add None to local store")
        self.assert_(self.session._putlocal("s",self.str) == None,
                     "failure to add string to local store")
        self.assertEqual(self.int, self.session.whos['a'])
        self.assertEqual(self.list, self.session.whos['b'])
        self.assertEqual(self.array, self.session.whos['c'])#XXX: alltrue(a==b)?
        self.assertEqual(self.none, self.session.whos['n'])
        self.assertEqual(self.str, self.session.whos['s'])
        self.assertRaises(NameError,self.session._putlocal,'foo!',69)
        return

    def test_SAM_getlocal(self):
        '''Matlab: return variable value from local store'''
        self.session.whos['a'] = self.int
        self.session.whos['b'] = self.list
        self.session.whos['c'] = self.array
        self.session.whos['n'] = self.none
        self.session.whos['s'] = self.str
        self.assertEqual(self.int, self.session._getlocal('a'))
        self.assertEqual(self.list, self.session._getlocal('b'))
        self.assertEqual(self.array, self.session._getlocal('c'))
        self.assertEqual(self.none, self.session._getlocal('n'))
        self.assertEqual(self.str, self.session._getlocal('s'))
        self.assertEqual(None, self.session._getlocal('x')) #KeyError not raised
        self.assertEqual(self.int, self.session._getlocal('a',skip=False))
        self.assertRaises(NameError, self.session._getlocal,'x',skip=False)
        return

    def test_SAM_poplocal(self):
        '''Matlab: delete variable from local store'''
        self.session.whos['a'] = self.int
        self.session.whos['b'] = self.list
        self.session.whos['c'] = self.array
        self.session.whos['n'] = self.none
        self.session.whos['s'] = self.str
        self.assertEqual(self.int, self.session._poplocal('a'))
        self.assertEqual(self.list, self.session._poplocal('b'))
        self.assertEqual(self.array, self.session._poplocal('c'))
        self.assertEqual(self.none, self.session._poplocal('n'))
        self.assertEqual(self.str, self.session._poplocal('s'))
        self.assertEqual(None, self.session._poplocal('x')) #KeyError not raised
        self.assertEqual({},self.session.whos)
        return

    def test_SAM_islist(self):
        '''Matlab: check if local variable is list'''
        self.session._putlocal("a",self.int)
        self.session._putlocal("b",self.list)
        self.session._putlocal("c",self.array)
        self.session._putlocal("n",self.none)
        self.session._putlocal("s",self.str)
        self.session._putlocal("t",self.bytearray)
        self.session._putlocal("u",self.strlist)
        self.assertEqual(False, self.session._islist('a'))
        self.assertEqual(True, self.session._islist('b'))
        self.assertEqual(False, self.session._islist('c'))
        self.assertEqual(False, self.session._islist('n'))
        self.assertEqual(False, self.session._islist('s'))
        self.assertEqual(False, self.session._islist('t'))
        self.assertEqual(True, self.session._islist('u'))
        self.assertEqual(False, self.session._islist('x'))
        return

    def test_SAM_isarray(self):
        '''Matlab: check if local variable is array'''
        self.session._putlocal("a",self.int)
        self.session._putlocal("b",self.list)
        self.session._putlocal("c",self.array)
        self.session._putlocal("n",self.none)
        self.session._putlocal("s",self.str)
        self.session._putlocal("t",self.bytearray)
        self.session._putlocal("u",self.strlist)
        self.assertEqual(False, self.session._isarray('a'))
        self.assertEqual(False, self.session._isarray('b'))
        self.assertEqual(True, self.session._isarray('c'))
        self.assertEqual(False, self.session._isarray('n'))
        self.assertEqual(False, self.session._isarray('s'))
        self.assertEqual(True, self.session._isarray('t'))
        self.assertEqual(False, self.session._isarray('u'))
        self.assertEqual(False, self.session._isarray('x'))
        return

    def test_SAM_toarray(self):
        '''Matlab: check against the default if convert to array'''
        self.session._putlocal("a",self.int)
        self.session._putlocal("b",self.list)
        self.session._putlocal("c",self.array)
        self.assertEqual(False,self.session._toarray('a',default='list'))
        self.assertEqual(False,self.session._toarray('b',default='list'))
        self.assertEqual(True,self.session._toarray('c',default='list'))
        self.assertEqual(True,self.session._toarray('a',default='array'))
        self.assertEqual(False,self.session._toarray('b',default='array'))
        self.assertEqual(True,self.session._toarray('c',default='array'))
        return

    def test_SAM_totype(self):
        '''Matlab: check array type'''
        self.session._putlocal("a",self.int)
        self.session._putlocal("b",self.list)
        self.session._putlocal("c",self.array)
        self.session._putlocal("d",self.dict)
        self.session._putlocal("s",self.str)
        self.session._putlocal("t",self.bytearray)
        self.assertEqual(None,self.session._totype('a'))
        self.assertEqual(None,self.session._totype('b'))
        self.assertEqual('l',self.session._totype('c'))
        self.assertEqual(None,self.session._totype('d'))
        self.assertEqual(None,self.session._totype('s'))
        self.assertEqual('c',self.session._totype('t'))
        return

    def test_SAM_wholist(self):
        '''Matlab: check list of string names for all Matlab variables'''
        self.session.samobj.eval("a = 1")
        self.session.samobj.eval("b = [1,2]")
        self.session.samobj.eval("s = 'foo'")
        self.session.samobj.eval("x = []")
        wholist = ['a', 'b', 's', 'x']
        self.assertEqual(wholist, self.session._wholist())
        return

    def test_SAM_exists(self):
        '''Matlab: check if Matlab variable exists'''
        self.session.samobj.eval("a = 1")
        self.assertEqual(True, self.session._exists('a'))
        self.assertEqual(False, self.session._exists('b'))
        self.assertEqual(True, self.session._exists('b',allowUndefined=True))
        self.assertEqual(False, self.session._exists('if',allowUndefined=True))
        self.assertRaises(NameError,self.session._exists,self.int)
        self.assertRaises(NameError,self.session._exists,self.list)
        return

    def test_SAM_getshape(self): #FIXME: allow extract shape from PyCObject
        '''Matlab: get Matlab shape tuple for given object'''
        self.session.put('a',1)
        cobj = self.session.get('a',array='C')
        self.assertRaises(NotImplementedError,self.session._getshape,cobj[0])
        self.assertEqual((1,1), self.session._getshape(1))
        self.assertEqual((1,1), self.session._getshape([1]))
        self.assertEqual((1,1), self.session._getshape([[1]]))
        self.assertEqual((1,1,1), self.session._getshape([[[1]]]))
        self.assertEqual((1,3), self.session._getshape([1,2,3]))
        self.assertEqual((1,3), self.session._getshape([[1,2,3]]))
        self.assertEqual((3,1), self.session._getshape([[1],[2],[3]]))
        self.assertEqual((2,3), self.session._getshape([[1,2,3],[4,5,6]]))
        self.assertEqual((1,6), self.session._getshape('foobar'))
        self.assertEqual(None, self.session._getshape(None))
        self.assertEqual((0,0), self.session._getshape([]))
        self.assertEqual((0,0), self.session._getshape(reshape([],(0,))))
        self.assertEqual((1,0), self.session._getshape(reshape([],(1,0))))
        self.assertEqual((1,2), self.session._getshape(array([1,2])))
        return #FIXME: what to do with dict?  currently all {...} returns (1,1)

    def test_SAM_getminshape(self):
        '''Matlab: set shape to minimal shape'''
        self.assertEqual((2,3), self.session._getminshape((2,3)))
        self.assertEqual((2,), self.session._getminshape((2,)))
        self.assertEqual((2,), self.session._getminshape((2,1)))
        self.assertEqual((2,), self.session._getminshape((1,2)))
        self.assertEqual((), self.session._getminshape((1,1)))
        self.assertEqual((), self.session._getminshape((1,)))
        self.assertEqual((), self.session._getminshape(()))
        self.assertEqual((0,3), self.session._getminshape((0,3)))
        self.assertEqual((3,0), self.session._getminshape((3,0)))
        self.assertEqual((0,), self.session._getminshape((0,0)))
        self.assertEqual((0,), self.session._getminshape((0,)))
        self.assertEqual((0,), self.session._getminshape((0,1)))
        self.assertEqual((2,3,4), self.session._getminshape((2,3,1,4,1)))
        self.assertEqual((3,4,0), self.session._getminshape((0,3,1,4,0)))
        self.assertRaises(TypeError,self.session._getminshape,self.int)
        self.assertRaises(TypeError,self.session._getminshape,self.list)
        self.assertRaises(TypeError,self.session._getminshape,self.none)
        return

    def test_SAM_checkarray(self):
        '''Matlab: check array and type'''
        self.assertEqual((False,None),self.session._checkarray('a',self.int))
        self.assertEqual((False,None),self.session._checkarray('b',self.list))
        self.assertEqual((True,self.array.typecode()),\
             self.session._checkarray('c',self.array))
        #array=False
        self.assertEqual((False,None),\
             self.session._checkarray('a',self.int,array=False))
        self.assertEqual((False,None),\
             self.session._checkarray('b',self.list,array=False))
        self.assertEqual((False,None),\
             self.session._checkarray('c',self.array,array=False))
        #array=False, type
        self.assertEqual((False,None),\
             self.session._checkarray('a',self.int,array=False,type='l'))
        self.assertEqual((False,None),\
             self.session._checkarray('b',self.list,array=False,type='l'))
        self.assertEqual((False,None),\
             self.session._checkarray('c',self.array,array=False,type='l'))
        #array=True
        self.assertEqual((True,None),\
             self.session._checkarray('a',self.int,array=True))
        self.assertEqual((True,None),\
             self.session._checkarray('b',self.list,array=True))
        self.assertEqual((True,self.array.typecode()),\
             self.session._checkarray('c',self.array,array=True))
        #array=True, type
        self.assertEqual((True,'Int16'),\
             self.session._checkarray('a',self.int,array=True,type='Int16'))
        self.assertEqual((True,'Int16'),\
             self.session._checkarray('b',self.list,array=True,type='Int16'))
        self.assertEqual((True,'Int16'),\
             self.session._checkarray('c',self.array,array=True,type='Int16'))
        #XXX: tests for '?' same as _toarray & _totype
        self.assertEqual((False,None),\
             self.session._checkarray('a',self.int,array='?',type='?'))
        self.assertEqual((False,None),\
             self.session._checkarray('c',self.array,array='?',type='?'))
        self.session.put('c',self.array)
        self.assertEqual((True,self.array.typecode()),\
             self.session._checkarray('c',self.array,array='?',type='?'))
        #blank fields ('?' requires name, None requires value)
        self.assertEqual((True,self.array.typecode()),\
             self.session._checkarray(None,self.array,array=None,type=None))
        self.assertEqual((True,None),\
             self.session._checkarray('c',None,array='?',type=None))
        self.assertEqual((True,self.array.typecode()),\
             self.session._checkarray('c',None,array='?',type='?'))
        self.assertEqual((False,None),\
             self.session._checkarray('c',None))
        self.assertRaises(TypeError,self.session._checkarray,[],None,'?','?')
        return

    def test_SAM_synclocal(self):
        '''Matlab: update local store value to Matlab value'''
#       Q = 'bar' #FIXME: should work with str
        Q = []
        W = [6,9]
        X = 666
        Y = 'baz'
        Z = 69
        self.session.put('z',Z)
        self.session.put('c',self.array)
        self.session.put('q',Q)
        self.session.samobj.eval("a = 1")
        self.session.samobj.eval("b = [1,2]")
#       self.session.samobj.eval("s = 'foo'") #FIXME: should work with str
        self.session._putlocal('w',W)
        self.session._putlocal('x',X)
        self.session._putlocal('y',Y)
        whos = {'z':Z, 'q':Q, 'w':W, 'x':X, 'y':Y}
        self.assertEqual(self.array, self.session.whos['c'])
        self.session._poplocal('c')
        self.assertEqual(whos,self.session.whos)
        self.session._synclocal('z')
        whos['z'] = float(Z) #XXX: Matlab casts to float
        self.assertEqual(whos,self.session.whos)
        self.session._synclocal('a')
        whos['a'] = [[float(self.int)]] #XXX: _synclocal uses default 'get'
        self.assertEqual(whos,self.session.whos)
        self.session._synclocal('c')
        whos['c'] = [asarray(self.array,'d').tolist()] #XXX: uses default 'get'
        self.assertEqual(whos,self.session.whos)
        self.assertRaises(NameError,self.session._synclocal,'f')
        self.assertEqual(whos,self.session.whos)
        self.assertRaises(AttributeError,self.session._synclocal,self.int)
        self.assertEqual(whos,self.session.whos)
        self.session._synclocal()
        whos = {'a':[[float(self.int)]], 'z':float(Z), \
                'q':Q, 'b':[asarray(self.list,'d').tolist()] } #,\
#               's':self.str}
        self.assertEqual(self.array, self.session.whos['c'])
        self.session.delete('c')
        self.assertEqual(whos,self.session.whos)
        return

    def test_SAMdelete(self): #FIXME: add tests for str, dict, ...
        '''Matlab: delete Matlab variables'''
        self.session.put('a',self.int)
        self.session.put('b',self.list)
        self.session.put('c',self.array)
        self.session.put('n',[],shape=(1,0))
#       self.session.put('s',self.str)
#       self.session.put('t',self.bytearray)
#       self.session._putstringarr('u',self.strlist)
        self.assert_(self.session.delete("a") == None,
                     "failure to delete int")
        self.assert_(self.session.delete("b") == None,
                     "failure to delete list")
        self.assert_(self.session.delete("c") == None,
                     "failure to delete array")
        self.assert_(self.session.delete("n") == None,
                     "failure to delete empty matrix")
#       self.assert_(self.session.delete("s") == None,
#                    "failure to delete string")
#       self.assert_(self.session.delete("t") == None,
#                    "failure to delete bytearray")
#       self.assert_(self.session.delete("u") == None,
#                    "failure to delete strlist")
        self.assert_(self.session.delete("x") == None,
                     "failure to pass on delete of undefined")
        whos = {}
        self.assertEqual(whos,self.session.whos)
        self.assertEqual(whos,self.session.show())
        self.assertRaises(NameError,self.session.delete,'a, b')
        self.assertEqual(whos,self.session.whos)
        self.assertEqual(whos,self.session.show())
        return

    def test_SAMverbose(self):
        '''Matlab: get status of, or set, verbosity'''
        self.session.samobj.verbose()
        self.assertEqual(True,self.session.verbose())
        self.session.samobj.silent()
        self.assertEqual(False,self.session.verbose())
        self.assert_(self.session.verbose(True) == None,
                     "failure to turn on verbosity")
        line = "??? Undefined function or variable 'a'.\n\n"
        self.assertEqual(line, self.session.samobj.eval('a'))
        self.assert_(self.session.verbose(False) == None,
                     "failure to turn off verbosity")
        self.assertEqual(None, self.session.samobj.eval('a'))
        #XXX: on='' -> False & on='foo' -> True; is this acceptable?
        return

    def test_SAMhelp(self): #TODO: test buffersize
        '''Matlab: print the Matlab help message'''
#       self.assert_(self.session.help('a') == None,
#                    "failure to print help for undefined variable")
#       self.session.put('z',69)
#       self.assert_(self.session.help('z') == None,
#                    "failure to print help for known variable")
#       self.assert_(self.session.help('a,z') == None,
#                    "failure to print help for string sequence")
#       self.assert_(self.session.help() == None,
#                    "failure to print full help message")
        self.assertRaises(TypeError,self.session.help,self.int)
        return #TODO: need to catch Matlab's stdout, then uncomment tests

    def test_SAMwho(self):
        '''Matlab: show the Matlab help for a variable'''
        self.assert_(self.session.who('a') == None,
                     "failure to print who for undefined variable")
        self.assert_(self.session.who('a',terse=False) == None,
                     "failure to print whos for undefined variable")
        self.session.put('z',69)
        short_who = '\nYour variables are:\n\nz  \n\n'
        long_who = '  Name      Size                   Bytes  Class\n\n'
        long_who += '  z         1x1                        8  double array\n\n'
        long_who += 'Grand total is 1 element using 8 bytes\n\n'
        self.assert_(self.session.who('z',terse=True,stdout=False) == short_who,
                     "failure to print who for known variable")
        self.assert_(self.session.who('z',terse=False,stdout=False) == long_who,
                     "failure to print whos for known variable")
        self.assert_(self.session.who('a,z') == None,
                     "failure to print who for string sequence")
        self.assert_(self.session.who('a,z',terse=False) == None,
                     "failure to print whos for string sequence")
        self.assert_(self.session.who(terse=True,stdout=False) == short_who,
                     "failure to print full who message")
        self.assert_(self.session.who(terse=False,stdout=False) == long_who,
                     "failure to print full whos message")
        self.assertRaises(TypeError,self.session.who,self.int)
        self.assertRaises(TypeError,self.session.who,self.int,False)
        return #XXX: should include tests for stdout=True

    def test_SAMshow(self): #FIXME: add tests for str, dict, ...
        '''Matlab: show the Matlab variables'''
        self.session.samobj.eval("a = 1")
        self.session.samobj.eval("b = [1,2]")
#       self.session.samobj.eval("s = 'foo'")
#       self.session.samobj.eval("t = BYTE(s)")
#       self.session.samobj.eval("u = STRING(b)")
#       whos = {'a':self.int, 'b':self.list, 's':self.str, 't':self.str}
        A = [[float(self.int)]]
        B = [asarray(self.list,'d').tolist()]
        whos = {'a':A, 'b':B}
#       whos['u'] = ['1','2']
        self.assertEqual(whos['a'],self.session.show('a'))
        self.assertEqual(whos['b'],self.session.show('b'))
#       self.assertEqual(self.str,self.session.show('s'))
#       self.assertEqual(self.str,self.session.show('t'))
#       self.assertEqual(whos['u'],self.session.show('u'))
        self.assertEqual(whos,self.session.show())
        whos['n'] = []
        self.session.put('n',whos['n'])
        self.assertEqual(whos['n'],self.session.show('n'))
        self.assertEqual(whos,self.session.show())
        #local changes
        self.session._putlocal('a',self.list)
        self.session._putlocal('b',self.str)
        self.session._putlocal('c',self.int)
        self.session._putlocal('n',self.str)
        self.session._putlocal('s',self.int)
        self.assertEqual(self.list,self.session.show('a',local=True))
        self.assertEqual(self.str,self.session.show('b',local=True))
        self.assertEqual(self.int,self.session.show('c',local=True))
        self.assertEqual(self.str,self.session.show('n',local=True))
        self.assertEqual(self.int,self.session.show('s',local=True))
#       self.assertEqual(self.str,self.session.show('t',local=True))
#       self.assertEqual(whos['u'],self.session.show('u',local=True))
        self.session._poplocal('b')
        self.assertRaises(NameError,self.session.show,'b',local=True)
        self.assertEqual(whos,self.session.show())
        self.assertEqual(whos,self.session.show(local=True))
        #failures
        self.assertRaises(NameError,self.session.show,'x')
        self.assertRaises(NameError,self.session.show,'a, b') #XXX: allow this?
        self.assertEqual(whos,self.session.show())
        self.assertEqual(whos,self.session.show(local=True))
        #stdout
#       self.assert_(self.session.show('a',stdout=True) == None,
#                    "failure to print Matlab show for int")
#       self.assert_(self.session.show('a',local=True,stdout=True) == None,
#                    "failure to print local show for int")
#       self.assert_(self.session.show(stdout=True) == None,
#                    "failure to print Matlab show")
#       self.assert_(self.session.show(local=True,stdout=True) == None,
#                    "failure to print local show")
        return #TODO: need to catch stdout, then uncomment tests

    def test_SAMget(self): #FIXME: add tests for str, dict, ...
        '''Matlab: get a variable from Matlab'''
        self.session.samobj.eval("a = 1")
#       self.session.samobj.eval("s = 'foo'")
#       whos = {'a':self.int, 's':self.str}
        A = [[float(self.int)]]
        whos = {'a':self.int}
        self.assertEqual(A,self.session.get('a'))
        self.assertEqual(array(A),self.session.get('a',array=True))
        self.assertEqual(array(self.int),\
                         self.session.get('a',array=True,reduce=True))
        self.assertEqual(self.int,self.session.get('a',array=False,reduce=True))
#       self.assertEqual(self.str,self.session.get('s'))
        self.assertEqual(whos,self.session.show())
        self.assertEqual(whos,self.session.show(local=True))
        self.session.samobj.eval("b = [1,2]")
        B = [asarray(self.list,'d').tolist()]
        whos['b'] = self.list
        self.assertEqual(array(B),self.session.get('b',array=True))
        self.assertEqual(array(B),self.session.show('b'))
        self.assertEqual(array(B),self.session.show('b',local=True))
        self.assertEqual(self.list,\
                         self.session.get('b',array=False,reduce=True))
        self.assertEqual(whos,self.session.show())
        self.assertEqual(whos,self.session.show(local=True))
        #not exists
        self.assertRaises(NameError,self.session.get,'x')
        self.assertRaises(NameError,self.session.get,'x',None,None)
        self.assertEqual(whos,self.session.show())
        self.assertEqual(whos,self.session.show(local=True))
        #None, Inf, NaN
        self.session.eval('n = []')
        whos['n'] = []
        self.assertEqual(whos['n'],self.session.get('n'))
        self.session.eval('m = inf')
        large = 1e300
        inf = large*large
        whos['m'] = inf
        self.assertEqual([[whos['m']]],self.session.get('m'))
        self.assertEqual(whos['m'],self.session.get('m',reduce=True))
        self.session.eval('o = nan')
        nan = inf - inf
        whos['o'] = nan
        self.assertEqual([[whos['o']]],self.session.get('o'))
        self.assertEqual(whos['o'],self.session.get('o',reduce=True))
        self.assertEqual(whos,self.session.show())
        self.assertEqual(whos,self.session.show(local=True))
        #shape
        shapeB = array(B).shape
        rshapeB = list(shapeB)
        rshapeB.reverse()
        rshapeB = tuple(rshapeB)
        self.assertEqual(B,self.session.get('b',shape=shapeB))
        self.assertEqual(array(B),self.session.get('b',array=True,shape=shapeB))
        self.assertEqual(transpose(array(B)),
                         self.session.get('b',array=True,shape=rshapeB))
        self.assertEqual(whos,self.session.show())
        self.assertEqual(whos,self.session.show(local=True))
        self.assertRaises(ValueError,self.session.get,'b',shape=())
        #STRING Arrays and BYTE Arrays
#       self.session.samobj.eval("t = BYTE(s)") #FIXME: testing for array=True?
#       self.session.samobj.eval("u = STRING(b)")
#       whos['t'] = self.str
#       whos['u'] = ['1', '2']
#       self.assertEqual(self.str,self.session.get('t'))
#       self.assertEqual(whos['u'],self.session.get('u'))
#       self.assertEqual(whos,self.session.show())
#       self.assertEqual(whos,self.session.show(local=True))
        return

    def test_SAMput(self): #FIXME: add str, dict, ...
        '''Matlab: put a variable into Matlab'''
        self.assert_(self.session.put("a",self.int) == None,
                     "failure to pass an int to Matlab")
        self.assert_(self.session.put("b",self.list) == None,
                     "failure to pass a list to Matlab")
        self.assert_(self.session.put("c",self.array) == None,
                     "failure to pass an array to Matlab")
#       self.assert_(self.session.put("s",self.str) == None,
#                    "failure to pass a string to Matlab")
#       self.assert_(self.session.put("t",self.bytearray) == None,
#                    "failure to pass a byte array to Matlab")
#       self.assert_(self.session.put("u",self.strlist) == None,
#                    "failure to pass a string list to Matlab")
        C = asarray(self.array,'d')
        self.assertEqual(self.int, self.session.get('a'))
        self.assertEqual(self.int, self.session._getlocal('a'))
        self.assertEqual(self.list, self.session.get('b'))
        self.assertEqual(self.list, self.session._getlocal('b'))
        self.assertEqual(C, self.session.get('c'))
        self.assertEqual(C, self.session._getlocal('c'))
        self.assertEqual(self.session._checkarray('',C),\
                         self.session._checkarray('',self.session.get('c')))
        self.assertEqual(self.session._checkarray('',C),\
                         self.session._checkarray('',self.session.whos['c']))
#       self.assertEqual(self.str, self.session.get('s'))
#       self.assertEqual(self.str, self.session._getlocal('s'))
#       self.assertEqual(self.bytearray, self.session.get('t'))
#       self.assertEqual(self.bytearray, self.session._getlocal('t'))
#       self.assertEqual(self.session._checkarray('',self.bytearray),\
#                        self.session._checkarray('',self.session.get('t')))
#       self.assertEqual(self.session._checkarray('',self.bytearray),\
#                        self.session._checkarray('',self.session.whos['t']))
#       self.assertEqual(self.strlist, self.session.get('u'))
#       self.assertEqual(self.strlist, self.session._getlocal('u'))
#       self.assertRaises(TypeError,self.session.put,'d',self.dict) #FIXME!!!
        self.assertRaises(ValueError,self.session.put,'n',self.none)
#       whos = {'a':self.int, 'b':self.list, 's':self.str}
        whos = {'a':self.int, 'b':self.list}
#       whos['u'] = self.strlist
        #now check how who & whos are affected...
        self.assertEqual(C, self.session.show('c'))
        self.assertEqual(C, self.session.show('c',local=True))
        self.session.delete('c')
#       self.assertEqual(self.bytearray, self.session.show('t'))
#       self.assertEqual(self.bytearray, self.session.show('t',local=True))
#       self.session.delete('t')
        self.assertEqual(whos, self.session.show())
        self.assertEqual(whos, self.session.show(local=True))
        #None, Inf, NaN
        self.assert_(self.session.put("n",[]) == None,
                     "failure to pass empty list to Matlab")
        whos['n'] = []
        self.assertEqual(whos['n'], self.session.get('n'))
        self.assertEqual(whos['n'], self.session._getlocal('n'))
        large = 1e300
        inf = large*large
        self.assert_(self.session.put("m",inf) == None,
                     "failure to pass Inf to Matlab")
        whos['m'] = inf
        self.assertEqual(whos['m'], self.session.get('m',reduce=True))
        self.assertEqual(whos['m'], self.session._getlocal('m'))
        nan = inf - inf
        self.assert_(self.session.put("o",nan) == None,
                     "failure to pass NaN to Matlab")
        whos['o'] = nan
        self.assertEqual(whos['o'], self.session.get('o',reduce=True))
        self.assertEqual(whos['o'], self.session._getlocal('o'))
        self.assertEqual(whos, self.session.show())
        self.assertEqual(whos, self.session.show(local=True))
        #shape
        self.assert_(self.session.put("b",self.list,shape=None) == None,
                     "failure to pass a list to Matlab")
        self.assertEqual(self.list, self.session.show('b'))
        B = [asarray(self.list,'d').tolist()]
        shapeB = asarray(B).shape
        self.assert_(self.session.put("b",self.list,shape=shapeB) == None,
                     "failure to change shape for a passed list")
        self.assertEqual(B, self.session.show('b'))
        self.assertRaises(ValueError, self.session.put, 'b', B, shape=())
        return

    def test_SAMeval(self): #verbose, stdout, buffersize
        '''Matlab: eval a command'''
        self.assert_(self.session.eval("b = [0,2]") == None,
                     "failure to eval a Matlab command")
        whos = {'b':[[0,2]]}
        self.assertEqual(whos['b'],self.session._getlocal('b'))
        self.assertEqual(whos['b'],self.session.show('b'))
        self.assert_(self.session.eval("b(1) = 1") == None,
                     "failure to eval a Matlab subarray command")
        whos = {'b':[[1,2]]}
        self.assertEqual(whos['b'],self.session._getlocal('b'))
        self.assertEqual(whos['b'],self.session.show('b'))
        self.assert_(self.session.eval("") == None,
                     "failure to eval an empty Matlab command")
        self.assert_(self.session.eval("% b = 1") == None,
                     "failure to eval a Matlab comment command")
        self.assertEqual(whos,self.session.show(local=True))
        self.assertEqual(whos,self.session.show())
        #TODO: test additional specific use cases at end of test suite...
        #verbose (w/stdout = False)
        self.session.samobj.verbose()
        response = '\nb =\n\n     1     2\n\n'
        self.assertEqual(response,self.session.eval("b",stdout=False))
        self.assertEqual(None,self.session.eval("b",verbose=False,stdout=False))
        self.assertEqual(response,self.session.eval("b",stdout=False))
        self.assertEqual(whos['b'],self.session._getlocal('b'))
        self.assertEqual(whos['b'],self.session.show('b'))
        self.session.samobj.silent()
        self.assertEqual(None,self.session.eval("b",stdout=False))
        self.assertEqual(response,\
                         self.session.eval("b",verbose=True,stdout=False))
        self.assertEqual(None,self.session.eval("b",stdout=False))
        self.assertEqual(whos['b'],self.session._getlocal('b'))
        self.assertEqual(whos['b'],self.session.show('b'))
        #stdout
#       self.assert_(self.session.eval('b') == None,
#                    "failure to print Matlab list")
        return #TODO: need to catch stdout, then uncomment tests

#   def test_SAMprompt(self):
#       '''Matlab: prompt TESTS NOT IMPLEMENTED'''
#       pass

###WORKING###
#
    def test_SAM_processMatlabcommand(self): #FIXME: check validity & failures!
        '''Matlab: preprocess '%' and '...' in Matlab command'''
        command = ''
        self.assertEqual(command,self.session._processMatlabcommand(command))
        command = 'foo'
        self.assertEqual(command,self.session._processMatlabcommand(command))
        command = 's = foo'
        self.assertEqual(command,self.session._processMatlabcommand(command))
        command = 's = "foo"'
        self.assertEqual(command,self.session._processMatlabcommand(command))
        command = "s = 'foo'"
        self.assertEqual(command,self.session._processMatlabcommand(command))
        command = 'foo...'
        self.assertEqual(command,self.session._processMatlabcommand(command))
        command = 'foo%'
        self.assertEqual('foo',self.session._processMatlabcommand(command))
        command = 'foo......'
        self.assertEqual('foo...',self.session._processMatlabcommand(command))
        command = 'foo%%'
        self.assertEqual('foo',self.session._processMatlabcommand(command))
        command = 'foo...bar'
        self.assertEqual('foo...',self.session._processMatlabcommand(command))
        command = 'foo%bar'
        self.assertEqual('foo',self.session._processMatlabcommand(command))
        command = 'foo...bar%'
        self.assertEqual('foo...',self.session._processMatlabcommand(command))
        command = 'foo%bar...'
        self.assertEqual('foo',self.session._processMatlabcommand(command))
        command = 'foo...bar...'
        self.assertEqual('foo...',self.session._processMatlabcommand(command))
        command = 'foo%bar%'
        self.assertEqual('foo',self.session._processMatlabcommand(command))
        #comments
        command = '%'
        self.assertEqual(None,self.session._processMatlabcommand(command))
        command = '%foo'
        self.assertEqual(None,self.session._processMatlabcommand(command))
        command = '%foo...'
        self.assertEqual(None,self.session._processMatlabcommand(command))
        command = '%foo...bar'
        self.assertEqual(None,self.session._processMatlabcommand(command))
        command = '%foo%bar'
        self.assertEqual(None,self.session._processMatlabcommand(command))
        #os commands
        self.session.evalbuff = []
        command = '!'
        self.assertEqual(command,self.session._processMatlabcommand(command))
        self.session.evalbuff = []
        command = '!foo'
        self.assertEqual(command,self.session._processMatlabcommand(command))
        self.session.evalbuff = []
        command = '!foo...'
        self.assertEqual(command,self.session._processMatlabcommand(command))
        self.session.evalbuff = []
        command = '!foo...bar'
        self.assertEqual(command,self.session._processMatlabcommand(command))
        self.session.evalbuff = []
        command = '!foo%bar'
        self.assertEqual(command,self.session._processMatlabcommand(command))
        #NOT os commands, but comments
        self.session.evalbuff = ['X']
        command = '...!'
        self.assertEqual('...',self.session._processMatlabcommand(command))
        self.session.evalbuff = ['X']
        command = '...!foo'
        self.assertEqual('...',self.session._processMatlabcommand(command))
        self.session.evalbuff = ['X']
        command = '...!foo...'
        self.assertEqual('...',self.session._processMatlabcommand(command))
        self.session.evalbuff = ['X']
        command = '...!foo...bar'
        self.assertEqual('...',self.session._processMatlabcommand(command))
        self.session.evalbuff = ['X']
        command = '...!foo...bar'
        self.assertEqual('...',self.session._processMatlabcommand(command))
        #leading whitespace
        command = ' '
        self.assertEqual(command,self.session._processMatlabcommand(command))
        command = ' foo'
        self.assertEqual(command,self.session._processMatlabcommand(command))
        command = ' %foo'
        self.assertEqual(None,self.session._processMatlabcommand(command))
        self.session.evalbuff = []
        command = ' ...foo'
        self.assertEqual(' ...',self.session._processMatlabcommand(command))
        self.session.evalbuff = ['X']
        command = ' ...foo'
        self.assertEqual(' ...',self.session._processMatlabcommand(command))
        #variations on ... and %
        command = '..'
        self.assertEqual(command,self.session._processMatlabcommand(command))
        command = 'foo.bar...'
        self.assertEqual(command,self.session._processMatlabcommand(command))
        command = "foo'.'bar..."
        self.assertEqual(command,self.session._processMatlabcommand(command))
        command = "foo'...'bar..."
        self.assertEqual(command,self.session._processMatlabcommand(command))
        command = "foo'%bar'..."
        self.assertEqual(command,self.session._processMatlabcommand(command))
        return #FIXME: test openbracket & continued bracket

### TESTING USE CASES FOR EVAL ###
#TODO

if __name__ == "__main__":
    suite0 = unittest.makeSuite(PyMatlab_samlab_TestCase)
    alltests = unittest.TestSuite((suite0,))
    unittest.TextTestRunner(verbosity=2).run(alltests)

# version
__id__ = "$Id: samtest.py 227 2007-09-25 16:33:11Z brandon $"

#  End of file 
