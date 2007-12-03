#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 7/15/2005 version 0.0.2a
# mmckerns@caltech.edu
# (C) 2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
__author__='Mike McKerns'
__doc__='''Python-Matlab bindings.  instantiate with: ml = pymatlab.matlab()'''
#TODO: localstore should NOT hold duplicate copies of Matalb arrays if possible.
#      a much better approach would be to hold the buffer handle, and any
#      pertaining information like 'array' & 'shape'.
#TODO: create 'obj.getitem and obj.setitem within PyC bindings ?
#TODO: allow inheritance of functions and procedures from Matlab
#TODO: allow get("x'") and other similar shortcuts
#TODO: allow line continuation from open-bracket
#TODO: allow recognition of block quotes
#TODO: allow get/put of strings
#TODO: allow get/put of cell arrays
#TODO: check if 'plus' works as well as '+' (and similar for other ops)
#TODO: improve recognition of bad subexpressions
#TODO: allow get of Matlab tuple from function call
#TODO: allow/check creation of anonymous functions [need update matlab version]

import sam
import Numeric

class matlab:
    '''Python-Matlab bindings
* prompt([verbose]) --> start an interactive Matlab session
* eval(command,[verbose,stdout,buffersize]) --> eval a command
* put(name,val,[shape]) --> python into matlab
* get(name,[shape,array,reduce]) --> matlab into python
* who([name,terse,stdout]) --> show matlab ('whos'/'who')
* show([name,local,stdout,buffersize]) --> show Matlab variables
* delete(name) --> destroy the selected Matlab variable
* verbose([on]) --> get status of, or set, verbosity
* help([name,buffersize]) --> print the Matlab help message'''
    _privdoc='''private methods:
 _validate -> raise NameError if invalid name
 _putlocal -> add a variable to local store
 _getlocal -> return variable value from local store
 _poplocal -> delete variable from local store, return value
 _islist   -> True if self.whos[name] is a list
 _isarray  -> True if self.whos[name] is a Numeric.array
 _toarray  -> T/F validated against the default
 _totype   -> get type if self.whos[name] is a Numeric.array
 _wholist  -> get a list of strings of all Matlab variables
 _exists   -> True if variable in Matlab
 _getshape -> get Matlab shape tuple for given object
 _getminshape -> set shape to minimal shape
 _checkarray -> get (array,type)
 _synclocal -> update local variable with Matlab variables
 _processMatlabcommand -> preprocess '%' & '...' 
 _putevalbuff -> add command to evalbuff
 _processevalbuff -> prepare evalbuff as a single Matlab command
 _isexpr   -> True if contains Matlab subexpression syntax
 _istuple  -> True if valid form of Matlab tuple result
 _exprroot -> extract root variables
 _sortexists -> sort list into existing (and non-)
 _putexpr  -> set array portion
 _getexpr  -> get array portion'''

    def __init__(self):
        '''start a simple Matlab session'''
        sam.eval("")
        self.samobj = sam
        self.whos = {}
        self.evalbuff = []
        #self.operator = []
        self.reserved = ['break','case','catch','continue','else','elseif',
                         'end','for','function','global','if','otherwise',
                         'persistent','return','switch','try','while']
        self.typecode = {'int':'i1sl', 'float':'df', 'str':'c'} #byte, complex?

    def __del__(self):
        '''end a simple Matlab session'''
        sam.eval("clear all")   #SOFT reset; clears Matlab session
#       self.samobj.close()     #HARD reset; terminates Matlab session
        self.samobj = None
        return

    def _validate(self,name):
        '''_validate(name) --> raise NameError if invalid name'''
        #a valid Matlab name begins with a letter, and can include only
        #alphanumeric symbols along with the underscore. ("isvarname")
        #Matlab also does not allow redefinition of reserved words.
        if not name: raise NameError, "invalid name '%s'" % name
        if not isinstance(name,str): 
            raise NameError, "%r not a valid name string" % name
        import re
        if re.compile('[a-zA-Z]').sub('',name[0]):
            raise NameError, "invalid first character '%s'" % name[0]
        badc = re.compile('[_a-zA-Z0-9]').sub('',name)
        if badc: raise NameError, "invalid name '%s'; remove '%s'" % (name,badc)
        if name in self.reserved:
            raise NameError, "invalid name '%s'; is a reserved word" % name
        return

    def _putlocal(self,name,value):
        '''_putlocal(name,value) --> add a variable to local store'''
        self._validate(name)
        self.whos[name] = value
        return

    def _getlocal(self,name,skip=True):
        '''_getlocal(name) --> return variable value from local store'''
        haskey = self.whos.has_key(name)
        if not haskey:
            if skip: return
            raise NameError,"'%s' is not defined locally" % str(name)
        return self.whos[name]

    def _poplocal(self,name):
        '''_poplocal(name) --> delete variable from local store, return value'''
        return self.whos.pop(name,None)

    def _islist(self,name):
        '''_islist(name) --> True if self.whos[name] is a list'''
        if isinstance(self._getlocal(name),list): return True
        return False

    def _isarray(self,name):
        '''_isarray(name) --> True if self.whos[name] is a Numeric.array'''
        if isinstance(self._getlocal(name),Numeric.ArrayType): return True
        return False

    def _toarray(self,name,default='list'):
        '''_toarray(name,[default]) --> T/F validated against the default'''
        if default not in ['array', 'Numeric', 'ArrayType',\
                           'Numeric.array', 'Numeric.ArrayType']:
            if self._isarray(name): return True
            return False #default: convert to LIST/STRING
        if self._islist(name): return False
        return True #default: convert to Numeric.array

    def _totype(self,name):
        '''_totype(name) --> get type if self.whos[name] is a Numeric.array'''
        if not self._isarray(name): return None
        return self._getlocal(name).typecode()
        #typecode = self._getlocal(name).typecode()
        #for key,val in self.typecode.items():
        #    if typecode in val:  return key
        #return None

    def _wholist(self): 
        '''_wholist() --> get a list of strings of all Matlab variables'''
        wasVerbose = self.verbose()
        self.samobj.verbose()
        line = self.samobj.eval("who('')")
        self.samobj.setVerbose(wasVerbose)
        if not line: return []
        return line.split("Your variables are:")[1].split()

    def _exists(self,name,allowUndefined=False):
        '''_exists(name,[allowUndefined]) --> True if variable in Matlab'''
        if not isinstance(name,str): 
            raise NameError, "%r not a valid name string" % name
        tmp = 'q1w2e3r4t5y6u7i8o9p0'
        wasVerbose = self.verbose()
        self.samobj.verbose()
        answer = self.samobj.eval(tmp+" = exist('"+name+"')")
        answer = int(answer.split("=")[1].split()[0])
        self.delete(tmp)
        self.samobj.setVerbose(wasVerbose)
        #XXX: better to just return result from eval("exist(name)") ?
        if answer > 1: return False
        if answer == 0 and allowUndefined == False: return False
        return True
       ####ALTERNATE IMPLEMENTATION###
       #exists = self._wholist().count(name)
       #if exists: return True
       #return False
       ###############################

    def _getshape(self,val):
        '''_getshape(object) --> get Matlab shape tuple for given object'''
        shape = None
        if val == None: return shape
        if 'PyCObject' in repr(val): #has a PyCObject
            raise NotImplementedError
        shape = Numeric.asarray(val).shape
        if len(shape) == 0: shape = (1,1)
        elif len(shape) == 1:
            if shape[0]: shape = (1,shape[0])
            else: shape = (0,0)
        if not isinstance(shape,tuple):
            raise TypeError, "%r not a valid shape tuple" % shape
        return shape

    def _getminshape(self,shape):
        '''_getminshape(shape) --> set shape to minimal shape'''
        if not isinstance(shape,tuple):
            raise TypeError, "%r not a valid shape tuple" % shape
        shape = list(shape)
        while shape.count(1): shape.remove(1)
        while shape.count(0) > 1: shape.remove(0)
        return tuple(shape)

    def _checkarray(self,name,value,array=None,type=None):
        '''_checkarray(name,value,[array,type]) --> get (array,type)'''
        if array == None: #check if value is an array
            if isinstance(value,Numeric.ArrayType): array = True
            else: array = False #value not array, don't get array
        if array == '?': #check what is stored locally
            array = self._toarray(name)
        if not array: return False,None #non-arrays don't have types!
        if type == None and isinstance(value,Numeric.ArrayType):
            type = value.typecode()
            #typecode = value.typecode()
            #for key,val in self.typecode.items():
            #    if typecode in val:
            #        type = key #set type to value's type
            #        break
        if type == '?': type = self._totype(name) #check local type
        return array,type

    def _synclocal(self,name=None):
        '''_synclocal() --> update local variable with Matlab variables'''
        if name: varlist = [name]
        else: varlist = self._wholist()
        for varname in varlist: #update local store with Matlab variable values
            vn = varname.strip()
            try: self.get(vn)
            except ValueError: #shape has changed significantly
                self.get(vn,shape=None)
        if not name:
            for key in self.whos.keys():
                if key not in varlist: #delete local not in Matlab
                    self.delete(key)
        return

### 'PUBLIC' METHODS ###

    def delete(self,name):
        '''delete(name) --> destroy the selected Matlab variable'''
        #name = 'all' will clear all variables, functions, etc...
        self._validate(name)
        command = 'clear '+name
        self.samobj.eval(command)
        self._poplocal(name)
        return

    def verbose(self,on=None):
        '''verbose([on]) --> get status of, or set, verbosity'''
        if on == None: return self.samobj.isVerbose()
        if on in ['off','Off','False','false','no','No','f','F','n','N']:
            on = False
        return self.samobj.setVerbose(bool(on))

    def help(self,name=None,buffersize=5120):
        '''help([name,buffersize]) --> print the Matlab help message'''
        command = 'help'
        if name: command += ' '+name
        self.eval(command,verbose=True,buffersize=buffersize)
        return

    def who(self,name=None,terse=False,stdout=True):
        '''who([name,terse,stdout]) --> show matlab ('whos'/'who')'''
        #self.samobj.whos()
        if name == None: name = ''
        if terse: command = "who('"+name+"')"
        else: command = "whos('"+name+"')"
        return self.eval(command,verbose=True,stdout=stdout)

    def show(self,name=None,local=False,stdout=False,buffersize=1024):
        '''show([name,local,stdout,buffersize]) --> show Matlab variables'''
        if not local:
            self._synclocal(name)
            if not stdout:
                return self.show(name,local=True,stdout=False)
            command = ''
            if name: command += name
            else:
                for varname in self.whos.keys():
                    vn = varname.strip()
                    command += vn+", "
            self.eval(command,verbose=True,buffersize=buffersize)
            return
        if name: vars = self._getlocal(name,skip=False)
        else: vars = self.whos
        if not stdout: return vars #then return the object
        print vars #otherwise, just print to stdout & return None
        return

    def put(self,name,val,shape=None): #XXX: add type? (implement w/ eval?)
        '''put(name,val,[shape]) --> python into matlab'''
        if self._isexpr(name): #contains 'expression' syntax
            return self._putexpr(name,val,shape)
        #XXX: how create Empty matrix: 1-by-0 ???
        self._validate(name)
        retain = False
        if shape == None:
            retain = True
            if not 'PyCObject' in repr(val): shape = self._getshape(val)
        #XXX: allow shape='?' to check local shape? (needs _getlocalshape)
        if 'PyCObject' in repr(val): #has a PyCObject
            dim = [0,0] #default for unknown size of PyCObject in sam
            for i in range(min(2,len(shape))): dim[i] = shape[i]
            self.samobj.put(name,val,dim[0],dim[1])
            #val = self.samobj.get(name) #get reshaped C array
        else:
            value = Numeric.reshape(val,shape)
            self.samobj.putarray(name,value)
        if retain: return self._putlocal(name,val)
        #XXX: option to save as array?
        array,type = self._checkarray(name,val) #was original an array?
        if not array:
            if len(shape): value = value.tolist()
            else: value = value.toscalar()
        self._putlocal(name,value)
        return

    def get(self,name,shape='?',array='?',reduce=False): #XXX: add type?
        '''get(name,[shape,array,reduce]) --> matlab into python'''
        if self._isexpr(name): #contains 'expression' syntax
            return self._getexpr(name,shape,array,reduce)
        #shape='?' checks what array shape exists in local store
        #array='?' checks what object type exists in local store
        self._validate(name)
        if array == 'C':
            value = self.samobj.get(name)
            self._putlocal(name,value)
            return value
        if shape == '?': #check locally
            value = self._getlocal(name)
            if value != None: shape = Numeric.asarray(value).shape
            else: #is a new local variable
                shape = None
        try:
            value = self.samobj.getarray(name)
        except:
            raise NameError, "Unable to get %r from Matlab workspace" % name
        if shape == None: shape = value.shape
        if reduce: shape = self._getminshape(shape)
        value = Numeric.reshape(value,shape)
        #cast to different type here with value = asarray(value,type) ?
        array,type = self._checkarray(name,value,array)
        if not array:
            if len(shape): value = value.tolist()
            else: value = value.toscalar()
        self._putlocal(name,value)
        return value

    def eval(self,command,verbose=None,stdout=True,buffersize=1024):
        '''eval(command,[verbose,stdout,buffersize]) --> eval a command'''
        command = self._processMatlabcommand(command)
        if not command: return #do nothing, is just a comment or NULL
        self._putevalbuff(command)
        matlabcommand = self._processevalbuff()
        if not matlabcommand: return #wait on next line
        wasVerbose = self.verbose()
        self.samobj.verbose()
        line = self.samobj.eval(matlabcommand,buffersize)
        self.samobj.setVerbose(wasVerbose)
        self._synclocal()
        if verbose == None: verbose = wasVerbose
        if verbose and line:
            if stdout: print line
            else: return line
        return

    def prompt(self,verbose=True):
        '''prompt([verbose]) --> start an interactive Matlab session'''
        #Access to python is given with the 'python()' command
        print "MATLAB interface:"
        if self.whos: self.who(terse=False)
        wasVerbose = self.samobj.isVerbose()
        while 1:
            com = raw_input('>> ')
##          print com
            if com == 'exit':
                break
            elif com == 'verbose(True)':
                verbose = True
            elif com == 'verbose(False)':
                verbose = False
            else:
                self.eval(com,verbose)
        self.samobj.setVerbose(wasVerbose)
        return

### END 'PUBLIC' METHODS ###

    def _processMatlabcommand(self,command): #preprocess command
        '''_processMatlabcommand(command) --> preprocess '%' & '...' '''
        import re
        #if is '%{', ignore EVERYTHING until '%}' #XXX: block quotes in v6.13?
        #if begins with '%', then ignore whole line
        p_iscomment = re.compile('^\s*%')
        if p_iscomment.match(command): return
        #if has os command ('!'), don't touch
        pattern = "[^'!%(\.)]*?(\.(\.)?)?[^'!%(\.)]*?"
        p_hasos = re.compile(pattern+"('[^']*'"+pattern+")*!")
        if p_hasos.match(command):  return command
        #delete all after '%'; but don't delete if within string
        pattern = "[^'%]*?"
        p_hascomment = re.compile(pattern+"('[^']*'"+pattern+")*%")
        p_hasmatch = p_hascomment.match(command)
        if p_hasmatch:
            command = p_hasmatch.group()[:-1]
        #delete all after '...'; but don't delete if within string
        pattern = "[^'(/.)]*?(\.(\.)?)?[^'(\.)]*?"
        p_hascontinue = re.compile(pattern+"('[^']*'"+pattern+")*\.\.\.")
        p_hasmatch = p_hascontinue.match(command)
        if p_hasmatch:
            command = p_hasmatch.group() #keep '...' as indicator
        #FIXME: recognize transpose (') instead of quote
        if command.count("'")%2: return command #XXX: raises Matlab error
        #check if has unbalanced open bracket '['
        p_hasstr = re.compile("'[^']*'")
        cmd = p_hasstr.sub('__',command) #remove all strings
        evalb = self._processevalbuff(dry=True) #fetch evalbuff
        if evalb: evalb = p_hasstr.sub('__',evalb) #remove all strings
        else: evalb = ''
        cmd = evalb + cmd
        if cmd.count('[') > cmd.count(']'): command += ';...'
        #return processed command
        return command

    def _putevalbuff(self,command):
        '''_putevalbuff(command) --> add command to evalbuff'''
        return self.evalbuff.append(command)

    def _processevalbuff(self,dry=False):
        '''_processevalbuff([dry]) --> prepare as a single Matlab command'''
        #don't launch when last line ends with '...'
        if not self.evalbuff: return
        if self.evalbuff[-1].endswith('...'):
            if dry: return
            self.evalbuff[-1] = self.evalbuff[-1].rstrip('...') #kill '...'
            return
        command = ' '.join(self.evalbuff)
        if not dry: self.evalbuff = []
        return command

    def _isexpr(self,expr):
        '''_isexpr(expr) --> True if contains Matlab subexpression syntax'''
        #FIXME: allow get("x+y") ???;  allow get("x'") ???
        if not expr.count('(') and not expr.count(')'): return False
        if expr.count('(') != expr.count(')') or \
           expr.index('(') > expr.index(')'):
            raise SyntaxError, "unbalanced parenthesis in %r" % expr
        import re
        #FIXME: should raise error on 'a{b(c})'
        pattern = '[_a-zA-Z0-9]+\(+[^\(\)]+\)+?' #XXX: foo() not allowed
        newexpr = re.compile(pattern).sub('x',expr) #detect arrays & functions
        #FIXME: check for cell arrays (i.e. {}) 
        if newexpr == expr: return False
        return True

    def _istuple(self,expr): #FIXME: this code is not used -- use it!
        '''_istuple(expr) --> True if valid form of Matlab tuple result'''
        import re
        pattern = '\[([_a-zA-Z0-9]+(\([^\(\)]+?\))*[\s\,]*)+\]'
        newexpr = re.compile(pattern).sub('x',expr) #detect [var var2]
        if newexpr == expr: return False
        return True

    def _exprroot(self,expr,allowUndefined=True):
        '''_exprroot(expression,[allowUndefined]) --> extract root variables'''
        #extracts the root(s) of an IDL expression
        import re
        #remove all math and logical operators
        pattern = "\.[\*\'\/\^\[\]]"
        expr = re.compile(pattern).sub('  ',expr)
        pattern = "[\+\-\*\:\'\/\^\[\]\&\|]"
        expr = re.compile(pattern).sub(' ',expr)
        #pattern = "[\~\<\>]\=*"  #don't use relational operators
        #pattern = "=="           #don't use relational operators
        #remove all () and [] #FIXME: allow cell and string arrays
        pattern = "[\)\]\[\(]"
        #remove all digits not attached to valid name
        expr = re.compile(pattern).sub(' ',expr)
        expr = re.compile('\s\d+[\s\d]*').sub('  ',expr)
        expr = re.compile('\A\d+[\s\d]*').sub('  ',expr)
        namelist = []
        for name in expr.split():
            try: #check if name is valid; and not a function or builtin
                self._validate(name)
                if not self._exists(name,allowUndefined): raise NameError
                namelist.append(name)
            except NameError:
                pass #skip any non-valid names
        return namelist

    def _sortexists(self,namelist):
        '''_sortexistis(namelist) --> sort list into existing (and non-)'''
        if not isinstance(namelist,list):
            raise TypeError, "'%s' is not a list of names" % str(namelist)
        defined = []
        undefined = []
        for name in namelist:
            if self._exists(name): defined.append(name)
            else: undefined.append(name)
        return defined,undefined

    def _putexpr(self,name,value,shape=None):
        '''_putexpr(name,value,[shape]) --> set array portion'''
        ### BETTER IF THIS METHOD USES SOMETHING LIKE obj.setitem ? ###
        #self._validateexpr(name)
        tmp = 'q1w2e3r4t5p0o9i8u7y6'
        rootlist = self._exprroot(name)
        rootlist,undefined = self._sortexists(rootlist)
        try:
            self.put(tmp,value,shape)
            self.samobj.eval(name+' = '+tmp)
        except: #AttributeError, NameError #FIXME
            for var in undefined: self.delete(var)
            self.delete(tmp)
            raise
        self.delete(tmp)
        for var in undefined: self.delete(var)
        for root in rootlist:
            self._synclocal(root)
        return

    def _getexpr(self,name,shape='?',array='?',reduce=False):
        '''_getexpr(name,[shape,array,reduce]) --> get array portion'''
        ### BETTER IF THIS METHOD USES SOMETHING LIKE obj.getitem ? ###
        #self._validateexpr(name)
        tmp = 'a1s2d3f4g5p0o9i8u7y6'
        rootlist = self._exprroot(name)
        rootlist,undefined = self._sortexists(rootlist)
        try:
            self.samobj.eval(tmp+' = '+name)
            value = self.get(tmp,shape,array,reduce)
        except: #AttributeError, NameError #FIXME
            for var in undefined: self.delete(var)
            self.delete(tmp)
            raise
        self.delete(tmp)
        return value
