#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  matplottest.py
#  
#  4/5/2005 version 0.0.1a
#  mmckerns@caltech.edu
#  (C) 2005 All Rights Reserved
# 
#  <LicenseText>
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from graphics.Matplotlib import *

import unittest

class Matplot_Matplot_TestCase(unittest.TestCase):
    def setUp(self):
        '''Matplotlib: instantiate a pylab session'''
        self.session = pylab()
        self.int = 1
        self.list = [1,2]
        self.array = array(self.list)
        self.dict = {}
        self.matrix = [[1,2,3],[4,5,6]]
        self.none = None
        self.str = 'foo'
        self.bytearray = array(self.str)
        self.strlist = ["hello", "world"]
        return

    def tearDown(self):
        '''Matplotlib: destroy a pylab session'''
        self.session = None
        return

    def test_matplot_numerix(self):
        '''Matplotlib: call numerix method at global scope'''
        self.assert_(array([[1,2],[3,4]])[0,0] == 1, "'numerix' not found")
        return

    def test_matplot__getattr__(self):
        '''Matplotlib: call pylab method if matplot method is implicit'''
        self.assert_(self.session.ion() == None, "implicit method not found ")
        #self.assertRaises(AttributeError,self.session.foo,'x')
        return

    def test_matplot_validate(self):
        '''Matplotlib: fail upon invalid name'''
        self.assert_(self.session._validate("foo") == None,
                     "failure to validate a valid variable")
        self.assert_(self.session._validate("f_o1o") == None,
                     "failure to validate a valid variable")
        self.assertRaises(NameError,self.session._validate,'1foo')
        self.assertRaises(NameError,self.session._validate,'$foo')
        self.assertRaises(NameError,self.session._validate,'f.oo')
        self.assertRaises(NameError,self.session._validate,'foo!')
        self.assertRaises(NameError,self.session._validate,'for')
        return

    def test_matplot_putlocal(self):
        '''Matplotlib: add variable to local store'''
        Z = 666
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
        self.assert_(self.session._putlocal("z",Z) == None,
                     "failure to add to named local store")
        self.assertEqual(self.int, self.session.whos['a'])
        self.assertEqual(self.list, self.session.whos['b'])
        self.assertEqual(self.array.tolist(), self.session.whos['c'].tolist())
        self.assertEqual(self.none, self.session.whos['n'])
        self.assertEqual(self.str, self.session.whos['s'])
        self.assertEqual(Z, self.session.whos['z'])
        self.assertRaises(NameError,self.session._putlocal,'foo!',69)
        return

    def test_matplot_getlocal(self):
        '''Matplotlib: return variable value from local store'''
        Z = 666
        self.session.whos['a'] = self.int
        self.session.whos['b'] = self.list
        self.session.whos['c'] = self.array
        self.session.whos['n'] = self.none
        self.session.whos['s'] = self.str
        self.session.whos['z'] = Z
        self.assertEqual(self.int, self.session._getlocal('a'))
        self.assertEqual(self.list, self.session._getlocal('b'))
        self.assertEqual(self.array.tolist(),\
                         self.session._getlocal('c').tolist())
        self.assertEqual(self.none, self.session._getlocal('n'))
        self.assertEqual(self.str, self.session._getlocal('s'))
        self.assertEqual(Z, self.session._getlocal('z'))
        self.assertEqual(None, self.session._getlocal('x')) #KeyError not raised
        self.assertEqual(self.int, self.session._getlocal('a',skip=False))
        self.assertRaises(NameError, self.session._getlocal,'x',skip=False)
        return

    def test_matplot_poplocal(self):
        '''Matplotlib: delete variable from local store'''
        Z = 666
        self.session.whos['a'] = self.int
        self.session.whos['b'] = self.list
        self.session.whos['c'] = self.array
        self.session.whos['n'] = self.none
        self.session.whos['s'] = self.str
        self.session.whos['z'] = Z
        self.assertEqual(self.int, self.session._poplocal('a'))
        self.assertEqual(self.list, self.session._poplocal('b'))
        self.assertEqual(self.array.tolist(),\
                         self.session._poplocal('c').tolist())
        self.assertEqual(self.none, self.session._poplocal('n'))
        self.assertEqual(self.str, self.session._poplocal('s'))
        self.assertEqual(Z, self.session._poplocal('z'))
        self.assertEqual(None, self.session._poplocal('x')) #KeyError not raised
        self.assertEqual({},self.session.whos)
        return

    def test_matplot_wholist(self):
        '''Matplotlib: check list of string names for all pylab variables'''
        self.session.eval("a = 1")
        self.session.eval("b = [1,2]")
        self.session.eval("s = 'foo'")
        self.session.put("n",None)
        wholist = ['a', 's', 'b', 'n']
        self.assertEqual(wholist, self.session._wholist())
        return

    def test_matplot_exists(self):
        '''Matplotlib: check if pylab variable exists'''
        self.session.eval("a = 1")
        self.assertEqual(True, self.session._exists('a'))
        self.assertEqual(False, self.session._exists('b'))
        return

    def test_matplotput(self):
        '''Matplotlib: pass a variable into pylab'''
        self.assert_(self.session.put("a",self.int) == None,
                     "failure to pass an int to pylab")
        self.assert_(self.session.put("b",self.list) == None,
                     "failure to pass a list to pylab")
        self.assert_(self.session.put("c",self.array) == None,
                     "failure to pass an array to pylab")
        self.assert_(self.session.put("s",self.str) == None,
                     "failure to pass a string to IDL")
        whos = {'a': self.int, 'c': self.array, 'b': self.list, 's': self.str}
        self.assertEqual(whos, self.session.who())
        self.assertEqual(self.int, self.session.get('a'))
        self.assertEqual(self.list, self.session.get('b'))
        self.assertEqual(self.array.tolist(), self.session.get('c').tolist())
        self.assertEqual(self.str, self.session.get('s'))
        self.assertRaises(NameError,self.session.put,'x[0]',1)
        self.assertRaises(NameError,self.session.put,'a+a',2)
        self.assertRaises(TypeError,self.session.put,'a[1:3]',0)
        self.assertRaises(IndexError,self.session.put,'b[100]',0)
        self.assertRaises(SyntaxError,self.session.put,'b[]',0)
        self.assertEqual(whos, self.session.who())
        return

    def test_matplotget(self):
        '''Matplotlib: extract a variable from pylab'''
        self.session.put("a",self.int)
        self.session.put("b",self.list)
        self.session.put("c",self.array)
        self.session.put("s",self.str)
        whos = {'a': self.int, 'c': self.array, 'b': self.list, 's': self.str}
        self.assert_(self.session.get('a') == whos['a'],
                     "failure to extract an int from pylab")
        self.assert_(self.session.get('b') == whos['b'],
                     "failure to extract a list from pylab")
        self.assert_(type(self.session.get('c')) == type(whos['c']),
                     "failure to extract an array from pylab")
        self.assert_(list(self.session.get('c')) == list(whos['c']),
                     "failure to extract an array from pylab")
        self.assert_(self.session.get('s') == whos['s'],
                     "failure to extract a string from pylab")
        self.assertRaises(NameError,self.session.get,'x')
        self.assertRaises(NameError,self.session.get,'sin(x)')
        self.assertEqual(whos,self.session.who())
        self.assertEqual(self.list[0],self.session.get('b[0]'))
        self.assertEqual(self.list[0]+self.int,self.session.get('b[0]+a'))
        self.assertRaises(SyntaxError,self.session.get,'x[]')
        return

    def test_matplotwho(self):
        '''Matplotlib: inquire who are the pylab variables'''
        self.session.put('a',self.int)
        self.session.put('b',self.list)
        self.session.put('c',self.array)
        self.session.put('s',self.str)
        whos = {'a':self.int, 'b':self.list, 's':self.str, 'c':self.array}
        self.assertEqual(self.int,self.session.who('a'))
        self.assertEqual(self.list,self.session.who('b'))
        self.assertEqual(self.array.tolist(),self.session.who('c').tolist())
        self.assertEqual(self.str,self.session.who('s'))
        self.assertEqual(whos,self.session.who())
        whos['n'] = self.none
        self.session.put('n',None)
        self.assertEqual(self.none,self.session.who('n'))
        self.assertEqual(whos,self.session.who())
        self.assertRaises(NameError,self.session.who,'x')
        self.assertRaises(NameError,self.session.who,'a, b') #XXX: allow this?
        self.assertEqual(whos,self.session.who())
        return

    def test_matplotdelete(self):
        '''Matplotlib: delete pylab variables'''
        self.session.put("a",1)
        self.session.put("b",2)
        self.session.put("c",3)
        self.assert_(self.session.delete("c") == None,
                     "failure to delete a pylab variable")
        whos = {'a': 1, 'b': 2}
        self.assertEqual(whos, self.session.who())
        self.assert_(self.session.delete("a, b") == None,
                     "failure to delete a pylab variable tuple")
        whos = {}
        self.assertEqual(whos, self.session.who())
        self.assert_(self.session.delete("z") == None,
                     "failure to skip delete for unknown variable")
        whos = {}
        self.assertEqual(whos, self.session.who())
        self.assert_(self.session.delete("[0,1]") == None,
                     "failure to skip delete for bad syntax")
        whos = {}
        self.assertEqual(whos, self.session.who())
        return

#   def test_matploteval(self):
#       '''Matplotlib: eval TESTS NOT IMPLEMENTED'''
#       pass

    def test_matplotevalpython(self):
        '''Matplotlib: evaluate a python expression'''
        self.assert_(self.session.eval("a = 1") == None,
                     "failure to eval an int")
        self.assert_(self.session.eval("b = [1,2]") == None,
                     "failure to eval a list")
        self.assert_(self.session.eval("c = array([[1,2,3,4]])") == None,
                     "failure to eval a 2D array")
        self.assert_(self.session.eval("import os") == None,
                     "failure to eval a python builtin")
        whos = {'a': 1, 'c': array([[1, 2, 3, 4]]), 'b': [1, 2]}
        self.assertEqual(whos['a'], self.session.who('a'))
        self.assertEqual(whos['b'], self.session.who('b'))
        self.assertEqual(list(whos['c']), list(self.session.who('c')))
        return

    def test_matplotevalpylab(self):
        '''Matplotlib: evaluate a pylab expression'''
        self.assert_(self.session.eval("ion()") == None,
                     "failure to evaluate a pylab expression")
        return

    def test_matplotevalexit(self):
        '''Matplotlib: do nothing upon 'exit' command'''
        self.session.eval('a = 1')
        whos = {'a': 1}
        self.assert_(self.session.eval("exit") == None,
                     "failure to skip 'exit' command")
        self.assertEqual(whos, self.session.who())
        return

    def test_matplotevaldel(self):
        '''Matplotlib: delete a pylab variable upon 'del' command'''
        self.session.eval("a = 1")
        self.session.eval("b = 2")
        self.session.eval("c = 3")
        self.assert_(self.session.eval("del b, c") == None,
                     "failure to perform 'del' command")
        whos = {'a': 1}
        self.assertEqual(whos, self.session.who())
        return

    def test_matplotevalundefined(self):
        '''Matplotlib: fail when expression is undefined'''
        self.assertRaises('CommandError',self.session.eval,"foo()")
        self.assertRaises('CommandError',self.session.eval,"s = t")
        return

#   def test_matplotprompt(self):
#       '''Matplotlib: prompt TESTS NOT IMPLEMENTED'''
#       pass


if __name__ == "__main__":
    suite0 = unittest.makeSuite(Matplot_Matplot_TestCase)
    alltests = unittest.TestSuite((suite0,))
    unittest.TextTestRunner(verbosity=2).run(alltests)

# version
__id__ = "$Id: matplottest.py 148 2006-04-15 20:33:56Z mike $"

#  End of file 
