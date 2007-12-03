#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  gnuplottest.py
#  
#  8/3/2005
#  esetzer@its.caltech.edu
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#####from graphics.gnuplot import *
from gnuprompt import *

# needed for gnuplot and not for matplotlib because matplotlib apparently
# includes a "numerix" version of array.
from Numeric import array

import unittest

gnuplotNoOp = "cd '.'"

class gnuplot_gnuplot_TestCase(unittest.TestCase):
    def setUp(self):
        '''gnuplot: create a gnuplot session'''
        self.session = gnuplot()
        self.int = 1
        self.list = [1,2]
        self.array = array(self.list)
        self.dict = {}
        self.matrix = [[1,2,3],[4,5,6]]
        self.none = None
#        self.str = 'foo'            # gnuplot does not support string variables
#        self.bytearray = array(self.str)
#        self.strlist = ["hello", "world"]
        return

    def tearDown(self):
        '''gnuplot: destroy a gnuplot session'''
        self.session = None
        return

# gnuplot does not have "numerix":

#    def test_gnuplot_numerix(self):
#        '''gnuplot: call numerix method at global scope'''
#        self.assert_(array([[1,2],[3,4]])[0,0] == 1, "'numerix' not found")
#        return

    def test_gnuplot__getattr__(self):
        '''gnuplot: call implicit method from gnuplot'''
        self.assert_(self.session.reset() is None, "implicit method not found ")
        #self.assertRaises(AttributeError,self.session.foo,'x')
        return

    def test_gnuplot_validate(self):
        '''gnuplot: fail upon invalid name'''
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

    def test_gnuplot_putlocal(self):
        '''gnuplot: add variable to local store'''
        Z = 666
        self.assert_(self.session._putlocal("a",self.int) == None,
                     "failure to add scalar to local store")
        self.assert_(self.session._putlocal("b",self.list) == None,
                     "failure to add list to local store")
        self.assert_(self.session._putlocal("c",self.array) == None,
                     "failure to add array to local store")
        self.assert_(self.session._putlocal("n",self.none) == None,
                     "failure to add None to local store")
#        self.assert_(self.session._putlocal("s",self.str) == None,
#                     "failure to add string to local store")
        self.assert_(self.session._putlocal("z",Z) == None,
                     "failure to add to named local store")
        self.assertEqual(self.int, self.session.whos['a'])
        self.assertEqual(self.list, self.session.whos['b'])
        self.assertEqual(self.array.tolist(), self.session.whos['c'].tolist())
        self.assertEqual(self.none, self.session.whos['n'])
#        self.assertEqual(self.str, self.session.whos['s'])
        self.assertEqual(Z, self.session.whos['z'])
        self.assertRaises(NameError,self.session._putlocal,'foo!',69)
        return

    def test_gnuplot_getlocal(self):
        '''gnuplot: return variable value from local store'''
        Z = 666
        self.session.whos['a'] = self.int
        self.session.whos['b'] = self.list
        self.session.whos['c'] = self.array
        self.session.whos['n'] = self.none
#        self.session.whos['s'] = self.str
        self.session.whos['z'] = Z
        self.assertEqual(self.int, self.session._getlocal('a'))
        self.assertEqual(self.list, self.session._getlocal('b'))
        self.assertEqual(self.array.tolist(),\
                         self.session._getlocal('c').tolist())
        self.assertEqual(self.none, self.session._getlocal('n'))
#        self.assertEqual(self.str, self.session._getlocal('s'))
        self.assertEqual(Z, self.session._getlocal('z'))
        self.assertEqual(None, self.session._getlocal('x')) #KeyError not raised
        self.assertEqual(self.int, self.session._getlocal('a',skip=False))
        self.assertRaises(NameError, self.session._getlocal,'x',skip=False)
        return

    def test_gnuplot_poplocal(self):
        '''gnuplot: delete variable from local store'''
        Z = 666
        self.session.whos['a'] = self.int
        self.session.whos['b'] = self.list
        self.session.whos['c'] = self.array
        self.session.whos['n'] = self.none
#        self.session.whos['s'] = self.str
        self.session.whos['z'] = Z
        self.assertEqual(self.int, self.session._poplocal('a'))
        self.assertEqual(self.list, self.session._poplocal('b'))
        self.assertEqual(self.array.tolist(),\
                         self.session._poplocal('c').tolist())
        self.assertEqual(self.none, self.session._poplocal('n'))
#        self.assertEqual(self.str, self.session._poplocal('s'))
        self.assertEqual(Z, self.session._poplocal('z'))
        self.assertEqual(None, self.session._poplocal('x')) #KeyError not raised
        self.assertEqual({},self.session.whos)
        return

    def test_gnuplot_wholist(self):
        '''gnuplot: check list of string names for all variables'''
        self.session.eval("a = 1")
        self.session.eval("b = [1,2]")
#        self.session.eval("s = 'foo'")
        self.session.put("n",None)
#        wholist = ['a', 's', 'b', 'n']
        wholist = ['a', 'b', 'n']
        self.assertEqual(wholist, self.session._wholist())
        return

    def test_gnuplot_exists(self):
        '''gnuplot: check if gnuplot variable exists'''
        self.session.eval("a = 1")
        self.assertEqual(True, self.session._exists('a'))
        self.assertEqual(False, self.session._exists('b'))
        return

    def test_gnuplotput(self):
        '''gnuplot: pass a variable into gnuplot'''
        self.assert_(self.session.put("a",self.int) == None,
                     "failure to pass an int to gnuplot")
        self.assert_(self.session.put("b",self.list) == None,
                     "failure to pass a list to gnuplot")
        self.assert_(self.session.put("c",self.array) == None,
                     "failure to pass an array to gnuplot")
#        self.assert_(self.session.put("s",self.str) == None,
#                     "failure to pass a string to IDL")
#        whos = {'a': self.int, 'c': self.array, 'b': self.list, 's': self.str}
        whos = {'a': self.int, 'c': self.array, 'b': self.list}
        self.assertEqual(whos, self.session.who())
        self.assertEqual(self.int, self.session.get('a'))
        self.assertEqual(self.list, self.session.get('b'))
        self.assertEqual(self.array.tolist(), self.session.get('c').tolist())
#        self.assertEqual(self.str, self.session.get('s'))
        self.assertRaises(NameError,self.session.put,'x[0]',1)
        self.assertRaises(NameError,self.session.put,'a+a',2)
        self.assertRaises(TypeError,self.session.put,'a[1:3]',0)
        self.assertRaises(IndexError,self.session.put,'b[100]',0)
        self.assertRaises(SyntaxError,self.session.put,'b[]',0)
        self.assertEqual(whos, self.session.who())
        return

    def test_gnuplotget(self):
        '''gnuplot: extract a variable'''
        self.session.put("a",self.int)
        self.session.put("b",self.list)
        self.session.put("c",self.array)
#        self.session.put("s",self.str)
#        whos = {'a': self.int, 'c': self.array, 'b': self.list, 's': self.str}
        whos = {'a': self.int, 'c': self.array, 'b': self.list}
        self.assert_(self.session.get('a') == whos['a'],
                     "failure to extract an int from gnuplot")
        self.assert_(self.session.get('b') == whos['b'],
                     "failure to extract a list from gnuplot")
        self.assert_(self.session.get('c') == whos['c'],
                     "failure to extract an array from gnuplot")
#        self.assert_(self.session.get('s') == whos['s'],
#                     "failure to extract a string from gnuplot")
        self.assertRaises(NameError,self.session.get,'x')
        self.assertRaises(NameError,self.session.get,'sin(x)')
        self.assertEqual(whos,self.session.who())
        self.assertEqual(self.list[0],self.session.get('b[0]'))
        self.assertEqual(self.list[0]+self.int,self.session.get('b[0]+a'))
        self.assertRaises(SyntaxError,self.session.get,'x[]')
        return

    def test_gnuplotwho(self):
        '''gnuplot: inquire who are the gnuplot variables'''
        self.session.put('a',self.int)
        self.session.put('b',self.list)
        self.session.put('c',self.array)
#        self.session.put('s',self.str)
#        whos = {'a':self.int, 'b':self.list, 's':self.str, 'c':self.array}
        whos = {'a':self.int, 'b':self.list, 'c':self.array}
        self.assertEqual(self.int,self.session.who('a'))
        self.assertEqual(self.list,self.session.who('b'))
        self.assertEqual(self.array.tolist(),self.session.who('c').tolist())
#        self.assertEqual(self.str,self.session.who('s'))
        self.assertEqual(whos,self.session.who())
        whos['n'] = self.none
        self.session.put('n',None)
        self.assertEqual(self.none,self.session.who('n'))
        self.assertEqual(whos,self.session.who())
        self.assertRaises(NameError,self.session.who,'x')
        self.assertRaises(NameError,self.session.who,'a, b') #XXX: allow this?
        self.assertEqual(whos,self.session.who())
        return

    def test_gnuplotdelete(self):
        '''gnuplot: delete gnuplot variables'''
        self.session.put("a",1)
        self.session.put("b",2)
        self.session.put("c",3)
        self.assert_(self.session.delete("c") == None,
                     "failure to delete a gnuplot variable")
        whos = {'a': 1, 'b': 2}
        self.assertEqual(whos, self.session.who())
        self.assert_(self.session.delete("a, b") == None,
                     "failure to delete a gnuplot variable tuple")
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
#       '''gnuplot: eval TESTS NOT IMPLEMENTED'''
#       pass

    def test_gnuplotevalpython(self):
        '''gnuplot: evaluate a python expression'''
        self.assert_(self.session.eval("a = 1") == None,
                     "failure to eval an int")
        self.assert_(self.session.eval("b = [1,2]") == None,
                     "failure to eval a list")
        self.assert_(self.session.eval("c = array([[1,2,3,4]])") == None,
                     "failure to eval a 2D array")
        self.assert_(self.session.eval("import os") == None,
                     "failure to eval a python builtin")
        whos = {'a': 1, 'c': array([[1, 2, 3, 4]]), 'b': [1, 2]}
        self.assertEqual(whos, self.session.who())
        return

    def test_gnuplotevalgnuplot(self):
        '''gnuplot: evaluate a gnuplot expression'''
        self.assert_(self.session.eval(gnuplotNoOp) == None,
                     "failure to evaluate a gnuplot expression")
        return

    def test_gnuplotevalexit(self):
        '''gnuplot: do nothing upon variations of the 'exit' command'''
        self.session.eval('a = 1')
        whos = {'a': 1}
        for quitCommand in ['quit', 'exit', 'q', 'qu', 'qui', 'ex', 'exi']:
            self.assert_(
                self.session.eval(quitCommand) == None,
                "failure to skip '" + quitCommand + "' command"
            )
            self.assertEqual(whos, self.session.who())
            self.assert_(
                self.session.eval(gnuplotNoOp) == None,
                "failure to evaluate a gnuplot expression after running '" + \
		                                             quitCommand + "'."
            )
        return

# XXX:
# gnuplot does not seem to have a command for unsetting variables.

#    def test_gnuplotevaldel(self):
#        '''gnuplot: delete a pylab variable upon 'del' command'''
#        self.session.eval("a = 1")
#        self.session.eval("b = 2")
#        self.session.eval("c = 3")
#        self.assert_(self.session.eval("del b, c") == None,
#                     "failure to perform 'del' command")
#        whos = {'a': 1}
#        self.assertEqual(whos, self.session.who())
#        return

# XXX:
# gnuplot currently does not produce an exception in these cases...

#    def test_gnuplotevalundefined(self):
#        '''gnuplot: fail when expression is undefined'''
#        self.assertRaises('CommandError',self.session.eval,"foo()")
#        self.assertRaises('CommandError',self.session.eval,"s = t")
#        return

#   def test_matplotprompt(self):
#       '''gnuplot: prompt TESTS NOT IMPLEMENTED'''
#       pass


if __name__ == "__main__":
    suite0 = unittest.makeSuite(gnuplot_gnuplot_TestCase)
    alltests = unittest.TestSuite((suite0,))
    unittest.TextTestRunner(verbosity=2).run(alltests)

# version
__id__ = "$Id: gnuplottest.py 227 2007-09-25 16:33:11Z brandon $"

#  End of file 
