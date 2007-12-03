"""
Unified interface to Numeric, numarray, and numpy
=================================================

This module imports Numeric, numarray, or numpy, plus some other
useful functions for numerical computing. Numeric, numarray, and numpy
can be viewed as three different implementations of Numerical Python
functionality.  The present module enables writing scripts that are
independent of the particular choice of Numeric, numarray, or
numpy. That is, the idea is that any of these modules can be replaced
by one of the alternatives, and the script should still work. This
requires the script to only use the set of instructions that are
common to Numeric, numarray, and numpy.

One reason for wanting the flexibility is that the different
implementations may exhibit different computational efficiency in
different applications. It also makes it trivial to adopt new versions
of Numerical Python in old scripts.


Basic Usage
-----------

To achieve a script that makes transparent use of Numeric, numarray, and
numpy, one needs to do one of the following imports::

  from graphics.numpytools import *
  # or
  import graphics.numpytools as N

Then one should never explicitly import Numeric, numarray, or numpy,
and explicitly use functions in these modules as this may cause
different array types to be mixed in the same application. Only call
the functions that were imported by the star or prefix functions by
the N symbol.


What Gets Imported?
-------------------

All symbols from either Numeric, numarray, or numpy are imported
into the global namespace of this numpytools module::

  from Numeric import *
  #or
  from numarray import *
  #or
  from numpy import *

Also the RandomArray, LinearAlgebra, MLab, and FFT modules are imported.
One problem with switching between Numeric, numarray, and numpy is that
the mentioned modules have different names in the three packages. For
example::

  Numeric has LinearAlgebra
  numarray has numarray.linear_algebra.LinearAlgebra2
  numpy has numpy.linalg

By default, we use the old well-established names introduced by Numeric
and import the linear algebra modules of numarray and numpy under the
classic name LinearAlgebra. Similarly, the other modules are also
imported under the Numeric names: RandomArray, RNG, MLab, and FFT.
RNG is not supported by numarray, while with numpy RNG becomes identical
to RandomArray.

Note that the MA module is not imported since it redefines
the repr function (array([1,2]) becomes [1,2] as for a list) if
the Numeric is used. The user must always explicitly import this package
if Numeric is used as basic array module.

Note that the numpytools module also makes some extensions of Numerical
Python available, see the section "Functionality of this module that
extends Numerical Python" (below).


What to use: Numeric, numarray, or numpy?
-----------------------------------------

The present module defines a global variable basic_NumPy holding
either "Numeric", "numarray", or "numpy", depending on which module
that was actually imported.

To determine whether Numeric, numarray, or numpy is to be imported,
the following procedure is applied:

  1. The command line arguments are checked for a --numarray,
     --Numeric, or --numpy option.
   
  2. If the user has already imported Numeric or numarray by an::

     import Numeric
     #or
     import numarray
     #or
     import numpy

     statement, the present module continues to import from the same
     module (module in sys.modules is used to check whether it should
     be Numeric, numarray, or numpy). If the user has imported more than
     one of the three module alternatives, numpy is used.
   
  3. The environment variable NUMPYARRAY is checked.
     If this variable contains "numarray", "Numeric", or "numpy" the
     corresponding module is imported.

If neither 1., 2., nor 3. determines the import, i.e., the user has not
explicitly indicated what to use, old and safe Numeric is the default
choice.


Functionality of this module that extends Numerical Python:
-----------------------------------------------------------

Some frequently standard modules like sys, os, and operator are
imported into the namespace of the present module.

The following extensions to Numerical Python are also defined:

 - sequence:
           sequence(a,b,s, [type]) computes numbers from a up to and
           including b in steps of s and (default) type float
 - seq:
           same as sequence (short form)

 - isequence:
           as sequence, but integer counters are computed
           (isequence is an alternative to range where the
           upper limit is included in the sequence)
 - iseq:
           same as isequence (short form)

 - arr:
           simplified interface to creating NumPy arrays (see its doc string)

 - NumPyArray:
           the type used in isinstance(a,NumPyArray) for
           checking if a is a NumPy array

 - arrmin, arrmax:
           compute maximum and minimum of all array entries
           (same as amin(a,None) and amax(a,None) in scipy)

 - array_output_precision(n):
           print arrays with n decimals

 - solve_tridiag_linear_system:
           returns the solution of a tridiagonal linear system

 - wrap2callable:
           tool for turning constants, discrete data, string
           formulas, function objects, or plain functions
           into an object that behaves as a function

 - NumPy_array_iterator:
           allows iterating over all array elements using
           a single, standard for loop (for value, index in iterator)
             
 - basic_NumPy:
           string containing "Numeric", "numarray", or "numpy",
           depending on which of the modules that was imported

 - float_eq:
           operator == for float operands with tolerance,
           float_eq(a,b,tol) means abs(a-b) < tol
           works for both scalar and array arguments

 - norm_L2, norm_l2, norm_L1, norm_l1, norm_inf: 
           norms for multi-dimensional arrays viewed as vectors

 - NumPy_version:
           holds the version of Numeric, numarray, or numpy

 - NumPy_type:
           returns the type of an array, i.e., "Numeric", "numarray",
           or "numpy"
           
 - fortran_storage:
           transparent transform of an array to column major (Fortran) storage
           that preserves the nature (Numeric, numarray, numpy) of the array
"""
           
import os, sys, operator, math

# first task: determine whether to use Numeric or numarray

basic_NumPy = None  # will later hold 'Numeric' or 'numarray'

# check the command line (this code is similar to matplotlib.numerix):
if basic_NumPy is None:
    if hasattr(sys, 'argv'):  # Apache mod_python has no argv
        for _a in sys.argv:
            if _a in ["--Numeric", "--numeric", "--NUMERIC"]:
                basic_NumPy = 'Numeric'
                break
            if _a in ["--Numarray", "--numarray", "--NUMARRAY"]:
                basic_NumPy = 'numarray'
                break
            if _a in ["--NumPy", "--numpy", "--NUMPY"]:
                basic_NumPy = 'numpy'
                break
        del _a  # don't pollute the global namespace

# check if the user has already done an import Numeric, import numarray,
# or import numpy; use the module that was imported
#if basic_NumPy is None:
#    if 'numpy' in sys.modules:
#        basic_NumPy = 'numpy'
#    elif 'numarray' in sys.modules:
#        basic_NumPy = 'numarray'
#    elif 'Numeric' in sys.modules:
#        basic_NumPy = 'Numeric'

# check the environment variable NUMPYARRAY:
if basic_NumPy is None:
    if os.environ.has_key('NUMPYARRAY'):
        if   os.environ['NUMPYARRAY'] == 'numpy':
            basic_NumPy = 'numpy'
        elif os.environ['NUMPYARRAY'] == 'numarray':
            basic_NumPy = 'numarray'
        elif os.environ['NUMPYARRAY'] == 'Numeric':
            basic_NumPy = 'Numeric'

# final default choice:
if basic_NumPy is None:
    basic_NumPy = 'numpy'#'Numeric'

#print 'from', basic_NumPy, 'import *'

# table of equivalent names of Numerical Python modules:
# (used to import modules under Numeric, numarray, or numpy name)
_NumPy_modules = (
    ('Numeric', 'numarray', 'numpy'),
    # umath and Precision are included as part of Numeric, numarray, numpy
    ('LinearAlgebra', 'numarray.linear_algebra.LinearAlgebra2',
     'numpy.linalg'),
    ('RandomArray', 'numarray.random_array.RandomArray2', 'numpy.random'),
    ('RNG', '', 'numpy.random'),
    ('FFT', 'numarray.fft', 'numpy.fft'),
    #('MLab', 'numarray.linear_algebra.mlab', 'numpy.lib.mlab'),
    ('MA', 'numarray.ma.MA', 'numpy.core.ma'),
    )
     

if basic_NumPy == 'numpy':
    try:
        for Numeric_name, dummy1, numpy_name in _NumPy_modules[1:]:
            if numpy_name == 'RNG':
                import numpy.random
                RNG = numpy.random
            elif numpy_name != '':
                exec 'import %s as %s' % (numpy_name, Numeric_name)

        from numpy import *
        from numpy import newaxis as NewAxis
        from numpy import float as Float

    except ImportError, e:
        raise ImportError, '%s\nnumpy import failed!\n'\
        'see doc of %s module for how to choose Numeric instead' % \
        (e, __name__)

    def array_output_precision(no_of_decimals):
        """Set no of decimals in printout of arrays."""
        arrayprint.set_precision(no_of_decimals)

    def arrmax(a):
        """Compute the maximum of all the entries in a."""
        try:
            return a.max()
        except AttributeError:
            # not a NumPy array
            if operator.isSequenceType(a):
                return max(a)  # does not work for nested sequences
            elif operator.isNumberType(a):
                return a
            else:
                raise TypeError, 'arrmax of %s not supported' % type(a)        

    def arrmin(a):
        """Compute the minimum of all the entries in a."""
        try:
            return a.min()
        except AttributeError:
            # not a NumPy array
            if operator.isSequenceType(a):
                return min(a)  # does not work for nested sequences
            elif operator.isNumberType(a):
                return a
            else:
                raise TypeError, 'arrmin of %s not supported' % type(a)

    NumPyArray = ndarray

if basic_NumPy == 'numarray':
    try:
        for Numeric_name, numarray_name, dummy1 in _NumPy_modules[1:]:
            if numarray_name:
                exec 'import %s as %s' % (numarray_name, Numeric_name)

        # RNG is not supported, make an object that gives an error message:
        class __Dummy:
            def __getattr__(self, name):
                raise ImportError, 'You have chosen the numarray package, '\
                'but it does not have the functionality of the RNG module'
        RNG = __Dummy()
        
        from numarray import *

    except ImportError, e:
        raise ImportError, '%s\nnumarray import failed!\n'\
        'see doc of %s module for how to choose Numeric instead' % \
        (e, __name__)

    def array_output_precision(no_of_decimals):
        """Set no of decimals in printout of arrays."""
        arrayprint.set_precision(no_of_decimals)

    def arrmax(a):
        """Compute the maximum of all the entries in a."""
        try:
            return a.max()
        except AttributeError:
            # not a NumPy array
            if operator.isSequenceType(a):
                return max(a)  # does not work for nested sequences
            elif operator.isNumberType(a):
                return a
            else:
                raise TypeError, 'arrmax of %s not supported' % type(a)        

    def arrmin(a):
        """Compute the minimum of all the entries in a."""
        try:
            return a.min()
        except AttributeError:
            # not a NumPy array
            if operator.isSequenceType(a):
                return min(a)  # does not work for nested sequences
            elif operator.isNumberType(a):
                return a
            else:
                raise TypeError, 'arrmin of %s not supported' % type(a)

    NumPyArray = NumArray

if basic_NumPy == 'Numeric':
    try:
        for Numeric_name, dummy1, dummy2 in _NumPy_modules[1:]:
            if Numeric_name != 'MA':  # exclude MA, see comment above
                exec 'import %s' % Numeric_name

        from Numeric import *

        # the following is perhaps not a good idea;
        # Numeric.UserArray and numarray.NumArray have different
        # data attributes!
        from UserArray import UserArray as NumArray

        # hack - as long as LinearAlgebra.eigenvalues hang, try to
        # get functions from numarray or numpy:
        try:
            import numpy.linalg as _N
        except:
            try:
                import numarray.linear_algebra.LinearAlgebra2 as _N
            except:
                pass  # nothing to do :-(
        try:
            LinearAlgebra.eigenvalues = _N.eigenvalues
            LinearAlgebra.eigenvectors = _N.eigenvectors
            del _N
        except NameError:
            # no numarray or numpy:
            print 'WARNING: LinearAlgebra.eigenvalues hangs!'

        
    except ImportError, e:
        raise ImportError, '%s\nNumeric import failed!\n'\
        'see doc of %s module for how to choose numarray instead' % \
        (e, __name__)

    # fix of matrixmultiply bug in Numeric (according to Fernando Perez,
    # SciPy-dev mailing list, Sep 28, 2004:
    # http://www.scipy.net/pipermail/scipy-dev/2004-September/002267.html,
    # matrixmultiply is dot if not dotblas is used, otherwise dot is
    # imported from dotblas, and matrixmultiply becomes the unoptimized
    # version (Perez timed the difference to be 0.55 vs 122.6 on his
    # computer)):
    matrixmultiply = dot

    def array_output_precision(no_of_decimals):
        """Set no of decimals in printout of arrays."""
        sys.float_output_precision = no_of_decimals

    def arrmax(a):
        """Compute the maximum of all the entries in a."""
        # could set arrmax = amax in scipy if scipy is installed
        try:
            return max(a.flat)  # use Python's list min
        except AttributeError:
            # not a NumPy array
            if operator.isSequenceType(a):
                return max(a)
            elif operator.isNumberType(a):
                return a
            else:
                raise TypeError, 'arrmax of %s not supported' % type(a)

    def arrmin(a):
        """Compute the minimum of all the entries in a."""
        # could set arrmin = amin in scipy if scipy is installed
        try:
            return min(a.flat)
        except AttributeError:
            # not a NumPy array
            if operator.isSequenceType(a):
                return min(a)
            elif operator.isNumberType(a):
                return a
            else:
                raise TypeError, 'arrmin of %s not supported' % type(a)

    NumPyArray = ArrayType


_N = __import__(basic_NumPy)
NumPy_version = _N.__version__
del _N
    

#--------------------------------------------------------------------
# Utility functions
#--------------------------------------------------------------------

def sequence(min=0.0, max=None, inc=1.0, type=float,
             return_type='NumPyArray'):
    """
    Generate numbers from min to (and including!) max,
    with increment of inc. Safe alternative to arange/arrayrange.
    The return_type string governs the type of the returned
    sequence of numbers ('NumPyArray', 'list', or 'tuple').
    """
    if max is None: # allow sequence(3) to be 0., 1., 2., 3.
        # take 1st arg as max, min as 0, and inc=1
        max = min; min = 0.0; inc = 1.0
    r = arange(min, max + inc/2.0, inc, type)
    if return_type == 'NumPyArray':
        return r
    elif return_type == 'list':
        return r.tolist()
    elif return_type == 'tuple':
        return tuple(r.tolist())

seq = sequence # short form

def isequence(start=0, stop=None, inc=1):
    """
    Generate integers from start to (and including) stop,
    with increment of inc. Alternative to range/xrange.
    """
    if stop is None: # allow isequence(3) to be 0, 1, 2, 3
        # take 1st arg as stop, start as 0, and inc=1
        stop = start; start = 0; inc = 1
    return xrange(start, stop+inc, inc)

iseq = isequence


def arr(shape=None, element_type=float, data=None, copy=True, file_=None):
    """
    Compact and flexible interface for creating NumPy arrays.

    @param shape:        length of each dimension
    @type  shape:        tuple or int
    @param data:         list, tuple, or NumPy array with data elements
    @param copy:         copy data if true, share data if false
    @type  copy:         boolean
    @param element_type: float, Int, Complex, float32, etc.
    @param file_:        filename or file object containing array data
    @type  file_:        string
    @return:             created Numerical Python array

    The array can be created in three ways:
    
      1. as zeros (just shape specified),

      2. as a copy of or reference to (depending on copy=True,False resp.)
         a list, tuple, or NumPy array (provided as the data argument),

      3. from data in a file (for one- or two-dimensional real-valued arrays).

    The function calls the underlying NumPy functions zeros and array
    (see the NumPy manual for the functionality of these functions).
    In case of data in a file, the first line determines the number of
    columns in the array. The file format is just rows and columns
    with numbers, no decorations (square brackets, commas, etc.) are
    allowed.

    >>> arr((3,4))
    array([[ 0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.]])
    >>> somelist=[[0,1],[5,5]]
    >>> a = arr(data=somelist)
    >>> b = a + 1
    >>> c = arr(data=b, copy=False)  # let c share data with b
    >>> b is c
    True
    >>> id(b) == id(c)
    True
    >>> arr(4, element_type=Int) + 4  # integer array
    array([4, 4, 4, 4])

    >>> # make a file with array data:
    >>> f = open('tmp.dat', 'w')
    >>> f.write('''\
    ... 1 3
    ... 2 6
    ... 3 12
    ... 3.5 20
    ... ''')
    >>> f.close()
    >>> # read array data from file:
    >>> a = arr(file_='tmp.dat')
    >>> a
    array([[  1. ,   3. ],
           [  2. ,   6. ],
           [  3. ,  12. ],
           [  3.5,  20. ]])
    """
    if data is None and file_ is None and shape is None:
        return None
    
    if data is not None:

        if not operator.isSequenceType(data):
            raise TypeError, 'arr: data argument is not a sequence type'
        
        if isinstance(shape, (list,tuple)):
            # check that shape and data are compatible:
            if reduce(operator.mul, shape) != size(data):
                raise ValueError, \
                      'arr: shape=%s is not compatible with %d '\
                      'elements in the provided data' % (shape, size(data))
        elif isinstance(shape, int):
            if shape != size(data):
                raise ValueError, \
                      'arr: shape=%d is not compatible with %d '\
                      'elements in the provided data' % (shape, size(data))
        elif shape is None:
            if isinstance(data, (list,tuple)) and copy == False:
                # cannot share data (data is list/tuple)
                copy = True
            return array(data, element_type, copy=copy)
        else:
            raise TypeError, \
                  'shape is %s, must be list/tuple or int' % type(shape)
    elif file_ is not None:
        if not isinstance(file_, (basestring, file, StringIO)):
            raise TypeError, \
                  'file_ argument must be a string (filename) or '\
                  'open file object, not %s' % type(file_)

        if isinstance(file_, basestring):
            file_ = open(file_, 'r')
        # skip blank lines:
        while True:
            line1 = file_.readline().strip()
            if line1 != '':
                break
        ncolumns = len(line1.split())
        file_.seek(0)
        # we assume that array data in file has element_type=float:
        if not element_type == float:
            raise ValueError, 'element_type must be float/"%s", not "%s"' % \
                  (float, element_type)
        
        d = array([float(word) for word in file_.read().split()])
        if isinstance(file_, basestring):
            f.close()
        # shape array d:
        if ncolumns > 1:
            suggested_shape = (int(len(d)/ncolumns), ncolumns)
            total_size = suggested_shape[0]*suggested_shape[1]
            if total_size != len(d):
                raise ValueError, \
                'found %d array entries in file "%s", but first line\n'\
                'contains %d elements - no shape is compatible with\n'\
                'these values' % (len(d), file, ncolumns)
            d.shape = suggested_shape
        if shape is not None:
            if shape != d.shape:
                raise ValueError, \
                'shape=%s is not compatible with shape %s found in "%s"' % \
                (shape, d.shape, file)
        return d
    
    else:
        # no data, no file, just make zeros

        if isinstance(shape, NumPyArray):
            raise TypeError, \
           'arr: shape (1st arg) is NumPy array, must be tuple or int'
        if shape is None:
            raise ValueError, \
            'arr: either shape, data, or from_function must be specified'

        try:
            return zeros(shape, element_type)
        except MemoryError, e:
            # print more information (size of data):
            print e, 'of size %s' % shape

# squeeze is from pylab
def squeeze(a):
    "squeeze(a) returns a with any ones from the shape of a removed"
    a = asarray(a)
    b = asarray(a.shape)
    return reshape (a, tuple (compress (not_equal (b, 1), b)))
    
def meshgrid(x=None, y=None, z=None, sparse=True):
    """
    Make 1D/2D/3D coordinate arrays for vectorized evaluations of
    1D/2D/3D scalar/vector fields over 1D/2D/3D grids, given
    one-dimensional coordinate arrays x, y, and/or, z.

    >>> x=seq(0,1,0.5)   # coordinate along x axis
    >>> y=seq(0,1,1)     # coordinate along y axis
    >>> meshgrid(x,y)    # extend x and y for a 2D xy grid
    (array([[ 0. ],
           [ 0.5],
           [ 1. ]]), array([       [ 0.,  1.]]))
    >>> z=5
    >>> meshgrid(x,y,z)  # 2D slice of a 3D grid, with z=const
    (array([[ 0. ],
           [ 0.5],
           [ 1. ]]), array([       [ 0.,  1.]]), 5)
    >>> xv, yv, zc = meshgrid(x,y,z)  # typical usage

    >>> meshgrid(2,y,x)  # 2D slice of a 3D grid, with x=const
    (2, array([[ 0.],
           [ 1.]]), array([       [ 0. ,  0.5,  1. ]]))
    >>> meshgrid(0,1,5)  # just a 3D point
    (0, 1, 5)
    >>> meshgrid(3)
    3
    >>> meshgrid(y)      # 1D grid; y is just returned
    array([ 0.,  1.])
    >>> meshgrid(x,y,sparse=False)  # store the full N-D matrix
    ([[ 0. , 0. , 0. ,]
     [ 0.5, 0.5, 0.5,]
     [ 1. , 1. , 1. ,]], [[ 0. , 0.5, 1. ,]
     [ 0. , 0.5, 1. ,]
     [ 0. , 0.5, 1. ,]])

    """

    # NOTE: numpy.mgrid defines a similar functionality, should use
    # that function if numpy is imported??

    if False:
        # convert list/tuple to NumPy arrays:
        if isinstance(x, (list,tuple)):  x = array(x)
        if isinstance(y, (list,tuple)):  y = array(y)
        if isinstance(z, (list,tuple)):  z = array(z)

        # Make sure output is dense when inputarray types are different
        if not sparse:
            if not basic_NumPy == NumPy_type(x):
                print "Warning in meshgrid: converting x to %s" %basic_NumPy
                x = asarray(x)
            if not basic_NumPy == NumPy_type(y):
                print "Warning in meshgrid: converting y to %s" %basic_NumPy
                y = asarray(y)
            if (z is not None) and not (basic_NumPy == NumPy_type(z)):
                print "Warning in meshgrid: converting z to %s" %basic_NumPy
                z = asarray(z)
    else:
        x = asarray(x)
        y = asarray(y)
        if z is not None:
            z = asarray(z)

    # Only singleton dimensions is allowed if rank > 1
    def squeeze(a):
        "squeeze(a) returns a with any ones from the shape of a removed"
        a = asarray(a)
        b = asarray(a.shape)
        return reshape (a, tuple (compress (not_equal (b, 1), b)))
        
    if rank(x) > 1: 
        x = squeeze(x)
        assert rank(x) == 1 
    if rank(y) >1:
        y = squeeze(y)
        assert rank(y) == 1
    if z is not None:
        if rank(z) >1:
            z = squeeze(z)
            assert rank(z) == 1
    
    
    # if x,y,z are identical, make copies:
    if y is x:  y = x.copy()
    if z is x:  z = x.copy()
    if z is y:  z = y.copy()
    
    import types
    def fixed(coor):
        return isinstance(coor, (float, complex, int, types.NoneType))
    
    def arr1D(coor):
        if isinstance(coor, NumPyArray):
            if len(coor.shape) == 1:
                return True
        return False
    
    # if two of the arguments are fixed, we have a 1D grid, and
    # the third argument can be reused as is:

    if arr1D(x) and fixed(y) and fixed(z):
        return x
    if fixed(x) and arr1D(y) and fixed(z):
        return y
    if fixed(x) and fixed(y) and arr1D(z):
        return z

    mult_fact = 1
    # if the sparse argument is False, the full N-D matrix (not only the 1-D
    # vector) should be returned. The mult_fact variable should then be updated
    # as necessary.

    # if only one argument is fixed, we have a 2D grid:
    if arr1D(x) and arr1D(y) and fixed(z):
        if not sparse:
            mult_fact = ones((len(x),len(y)))
        if z is None:
            return x[:,NewAxis]*mult_fact, y[NewAxis,:]*mult_fact
        else:
            return x[:,NewAxis]*mult_fact, y[NewAxis,:]*mult_fact, z
        
    if arr1D(x) and fixed(y) and arr1D(z):
        if not sparse:
            mult_fact = ones((len(x),len(z)))
        if y is None:
            return x[:,NewAxis]*mult_fact, z[NewAxis,:]*mult_fact
        else:
            return x[:,NewAxis]*mult_fact, y, z[NewAxis,:]*mult_fact
        
    if fixed(x) and arr1D(y) and arr1D(z):
        if not sparse:
            mult_fact = ones((len(y),len(z)))
        if x is None:
            return y[:,NewAxis]*mult_fact, z[NewAxis,:]*mult_fact
        else:
            return x, y[:,NewAxis]*mult_fact, z[NewAxis,:]*mult_fact

    # or maybe we have a full 3D grid:
    if arr1D(x) and arr1D(y) and arr1D(z):
        if not sparse:
            mult_fact = ones((len(x),len(y),len(z)))
        return x[:,NewAxis,NewAxis]*mult_fact, \
               y[NewAxis,:,NewAxis]*mult_fact, \
               z[NewAxis,NewAxis,:]*mult_fact

    # at this stage we assume that we just have scalars:
    l = []
    if x is not None:
        l.append(x)
    if y is not None:
        l.append(y)
    if z is not None:
        l.append(z)
    if len(l) == 1:
        return l[0]
    else:
        return tuple(l)
     
        
def float_eq(a, b, rtol=1.0e-14, atol=1.0e-14):
    """
    Approximate test a==b for float variables.
    Returns true if abs(a-b) < atol + rtol*abs(b).
    atol comes into play when abs(b) is very small.
    When a and b are NumPy arrays, NumPy's allclose function is called
    (but float_eq's default tolerances are much stricter than those of
    allclose).
    """
    if isinstance(a, float):
        return math.fabs(a-b) < atol + rtol*math.fabs(b)
    elif isinstance(a, NumPyArray):
        return allclose(a, b, rtol, atol)
    elif isinstance(a, complex):
        return float_eq(a.real, b.real, rtol, atol) and \
               float_eq(a.imag, b.imag, rtol, atol)
    else:
        raise TypeError, 'Illegal types: a is %s and b is %s' % \
              (type(a), type(b))
    

def norm_l2(u):
    """
    l2 norm of a multi-dimensional array u viewed as a vector
    (norm=sqrt(dot(u.flat,u.flat))).
    """
    return math.sqrt(innerproduct(u.flat, u.flat))

def norm_L2(u):
    """
    L2 norm of a multi-dimensional array u viewed as a vector
    (norm=sqrt(dot(u.flat,u.flat)/n)).

    If u holds function values and the norm of u is supposed to
    approximate an integral (L2 norm) of the function, this (and
    not norm_l2) is the right norm function to use.
    """
    return norm_l2(u)/sqrt(float(size(u)))

def norm_l1(u):
    """
    l1 norm of a multi-dimensional array u viewed as a vector
    (norm=sum(abs(u.flat))).
    """
    return sum(abs(u.flat))

def norm_L1(u):
    """
    L1 norm of a multi-dimensional array u viewed as a vector
    (norm=sum(abs(u.flat))).

    If u holds function values and the norm of u is supposed to
    approximate an integral (L1 norm) of the function, this (and
    not norm_l1) is the right norm function to use.
    """
    return norm_l1(u)/float(size(u))

def norm_inf(u):
    """Infinity/max norm of a multi-dimensional array u viewed as a vector."""
    return arrmax(abs(u.flat))



def solve_tridiag_linear_system(A, b):
    """
    Solve a tridiagonal linear system of the form::
    
     A[0,1]*x[0] + A[0,2]*x[1]                                        = 0
     A[1,0]*x[0] + A[1,1]*x[1] + A[1,2]*x[2]                          = 0
     ...
     ...
              A[k,0]*x[k-1] + A[k,1]*x[k] + A[k,2]*x[k+1]             = 0
     ...
                  A[n-2,0]*x[n-3] + A[n-2,1]*x[n-2] + A[n-2,2]*x[n-1] = 0
     ...
                                    A[n-1,0]*x[n-2] + A[n-1,1]*x[n-1] = 0

    That is, the diagonal is stored in A[:,1], the subdiagonal
    is stored in A[1:,0], and the superdiagonal is stored in A[:n-2,2].

    The storage is not memory friendly in Python/C (diagonals in
    the columns of A, but when A is sent to F77 for high-performance
    computing, a copy is taken and the F77 routine works with the
    same algorithm and hence optimal Fortran storage.
    """
    n = len(b)
    x = zeros(n, float)  # solution
    d = zeros(n, float);  c = zeros(n, float);  m = zeros(n, float)

    d[0] = A[0,1]
    c[0] = b[0]

    for k in isequence(1, n-1, 1):
        m[k] = A[k,0]/d[k-1]
        d[k] = A[k,1] - m[k]*A[k-1,2]
        c[k] = b[k] - m[k]*c[k-1]
    x[n-1] = c[n-1]/d[n-1]

    # back substitution:
    for k in isequence(n-2, 0, -1):
        x[k] = (c[k] - A[k,2]*x[k+1])/d[k]
    return x




try:
    import Pmw
    class NumPy2BltVector(Pmw.Blt.Vector):
        """
        Copy a NumPy array to a BLT vector:
        # a: some NumPy array
        b = NumPy2BltVector(a)  # b is BLT vector
        g = Pmw.Blt.Graph(someframe)
        # send b to g for plotting
        """
        def __init__(self, array):
            Pmw.Blt.Vector.__init__(self, len(array))
            self.set(tuple(array))  # copy elements
except:
    class NumPy2BltVector:
        def __init__(self, array):
            raise ImportError, "Python is not compiled with BLT"

try:
    from graphics.StringFunction import StringFunction
except:
    pass  # wrap2callable may not work


class WrapNo2Callable:
    """Turn a number (constant) into a callable function."""
    def __init__(self, constant):
        self.constant = constant
        self._array_shape = None

    def __call__(self, *args):
        """
        >>> w = WrapNo2Callable(4.4)
        >>> w(99)
        4.4000000000000004
        >>> # try vectorized computations:
        >>> x = seq(1, 4, 1)
        >>> y = seq(1, 2)
        >>> xv = x[:,NewAxis]; yv = y[NewAxis,:]
        >>> xv + yv
        array([[ 2.,  3.],
               [ 3.,  4.],
               [ 4.,  5.],
               [ 5.,  6.]])
        >>> w(xv, yv)
        array([[ 4.4,  4.4],
               [ 4.4,  4.4],
               [ 4.4,  4.4],
               [ 4.4,  4.4]])

        If you want to call such a function object with space-time
        arguments and vectorized expressions, make sure the time
        argument is not the first argument. That is,
        w(xv, yv, t) is fine, but w(t, xv, yv) will return 4.4,
        not the desired array!
        """
        if isinstance(args[0], NumPyArray):
            if self._array_shape is None:
                self._set_array_shape()
            else:
                r = self.constant*ones(self._array_shape, float)
                # could store r (allocated once) and just return reference
                return r
        else:
            # scalar version:
            return self.constant

    def _set_array_shape(self, arg):
        # vectorized version:
        r = arg.copy()
        # to get right dimension of the return array,
        # compute with args in a simple formula (sum of args)
        for a in args[1:]:
            r = r + a  # in-place r+= won't work
            # (handles x,y,t - the last t just adds a constant)
            # an argument sequence t, x, y  will fail (1st arg
            # is not a NumPy array)
        self._array_shape = r.shape

    # The problem with this class is that, in the vectorized version,
    # the array shape is determined in the first call, i.e., later
    # calls may return an array with the wrong shape if the shape of
    # the input arguments change! Sometimes, when called along boundaries
    # of grids, the shape may change so the next implementation is
    # slower and safer.
    
class WrapNo2Callable:
    """Turn a number (constant) into a callable function."""
    def __init__(self, constant):
        self.constant = constant

    def __call__(self, *args):
        """
        >>> w = WrapNo2Callable(4.4)
        >>> w(99)
        4.4000000000000004
        >>> # try vectorized computations:
        >>> x = seq(1, 4, 1)
        >>> y = seq(1, 2)
        >>> xv = x[:,NewAxis]; yv = y[NewAxis,:]
        >>> xv + yv
        array([[ 2.,  3.],
               [ 3.,  4.],
               [ 4.,  5.],
               [ 5.,  6.]])
        >>> w(xv, yv)
        array([[ 4.4,  4.4],
               [ 4.4,  4.4],
               [ 4.4,  4.4],
               [ 4.4,  4.4]])

        If you want to call such a function object with space-time
        arguments and vectorized expressions, make sure the time
        argument is not the first argument. That is,
        w(xv, yv, t) is fine, but w(t, xv, yv) will return 4.4,
        not the desired array!
               
        """
        if isinstance(args[0], NumPyArray):
            # vectorized version:
            r = args[0].copy()
            # to get right dimension of the return array,
            # compute with args in a simple formula (sum of args)
            for a in args[1:]:
                r = r + a  # in-place r+= won't work
                # (handles x,y,t - the last t just adds a constant)
            r[:] = self.constant
            return r
        else:
            # scalar version:
            return self.constant


class WrapDiscreteData2Callable:
    """
    Turn discrete data on a uniform grid into a callable function,
    i.e., equip the data with an interpolation function.

    >>> from graphics.numpytools import *
    >>> x = seq(0,1,0.1)
    >>> y = 1+2*x
    >>> f = wrap2callable((x,y))
    >>> f(0.5)   # evaluate f(x)
    1.5
    >>> f(0.5, 0.1)  # discrete data with extra time prm: f(x,t)
    1.5
    """
    def __init__(self, data):
        self.data = data  # (x,y,f) data for an f(x,y) function
        from Scientific.Functions.Interpolation \
             import InterpolatingFunction # from ScientificPython
        self.interpolating_function = \
             InterpolatingFunction(self.data[:-1], self.data[-1])
        self.ndims = len(self.data[:-1])  # no of spatial dim.
        
    def __call__(self, *args):
        # allow more arguments (typically time) after spatial pos.:
        args = args[:self.ndims]
        # args can be tuple of scalars (point) or tuple of vectors
        if isinstance(args[0], (float, int)):
            return self.interpolating_function(*args)
        else:
            # args is tuple of vectors; Interpolation must work
            # with one point at a time:
            r = [self.interpolating_function(*a) for a in zip(*args)]
            return array(r)  # wrap in NumPy array

        
def wrap2callable(f, **kwargs):
    """
    Allow constants, string formulas, discrete data points,
    user-defined functions and (callable) classes to be wrapped
    in a new callable function. That is, all the mentioned data
    structures can be used as a function, usually of space and/or
    time.
    (kwargs is used for string formulas)

    >>> from graphics.numpytools import *
    >>> f1 = wrap2callable(2.0)
    >>> f1(0.5)
    2.0
    >>> f2 = wrap2callable('1+2*x')
    >>> f2(0.5)
    2.0
    >>> f3 = wrap2callable('1+2*t', independent_variables='t')
    >>> f3(0.5)
    2.0
    >>> f4 = wrap2callable('a+b*t')
    >>> f4(0.5)
    Traceback (most recent call last):
    ...
    NameError: name 'a' is not defined
    >>> f4 = wrap2callable('a+b*t', independent_variables='t', \
                           a=1, b=2)
    >>> f4(0.5)
    2.0

    >>> x = seq(0,1,0.5); y=1+2*x
    >>> f5 = wrap2callable((x,y))
    >>> f5(0.5)
    2.0
    >>> def myfunc(x):  return 1+2*x
    >>> f6 = wrap2callable(myfunc)
    >>> f6(0.5)
    2.0
    >>> f7 = wrap2callable(lambda x: 1+2*x)
    >>> f7(0.5)
    2.0
    >>> class MyClass:
            'Representation of a function f(x; a, b) =a + b*x'
            def __init__(self, a=1, b=1):
                self.a = a;  self.b = b
            def __call__(self, x):
                return self.a + self.b*x
    >>> myclass = MyClass(a=1, b=2)
    >>> f8 = wrap2callable(myclass)
    >>> f8(0.5)
    2.0
    >>> # 3D functions:
    >>> f9 = wrap2callable('1+2*x+3*y+4*z', \
                           independent_variables=('x','y','z'))
    >>> f9(0.5,1/3.,0.25)
    4.0
    >>> # discrete 3D data:
    >>> y = seq(0,1,0.5); z = seq(-1,0.5,0.1)
    >>> xc = x[:,NewAxis,NewAxis]; yc = y[NewAxis,:,NewAxis]
    >>> zc = z[NewAxis,NewAxis,:]
    >>> def myfunc3(x,y,z):  return 1+2*x+3*y+4*z

    >>> values = myfunc3(xc,yc,zc)
    >>> f10 = wrap2callable((x,y,z,values))
    >>> f10(0.5,1/3.,0.25)
    4.0

    One can also check what the object is wrapped as and do more
    specific operations, e.g.,
    
    >>> f9.__class__.__name__
    'StringFunction'
    >>> str(f9)     # look at function formula
    '1+2*x+3*y+4*z'
    >>> f8.__class__.__name__
    'MyClass'
    >>> f8.a, f8.b  # access MyClass-specific data
    (1, 2)

    Troubleshooting regarding string functions:
    If you use a string formula with a NumPy array, you typically get
    error messages like::
        
       TypeError: only rank-0 arrays can be converted to Python scalars.
    
    You must then make the right::

       from Numeric/numarray/graphics.numpytools import *
       
    in the calling code and supply the keyword argument::
        
       globals=globals()
       
    to wrap2callable. See also the documentation of class StringFunction
    for more information.
    """
    if isinstance(f, str):
        return StringFunction(f, **kwargs)
        # this is a considerable optimization (up to a factor of 3),
        # but then the additional info in the StringFunction instance
        # is lost in the calling code:
        # return StringFunction(f, **kwargs).__call__
    elif isinstance(f, (float, int)):
        return WrapNo2Callable(f)
    elif isinstance(f, (list,tuple)):
        return WrapDiscreteData2Callable(f)
    elif operator.isCallable(f):
        return f
    else:
        raise TypeError, 'f of type %s is not callable' % type(f)


# problem: setitem in ArrayGen does not support multiple indices
# relying on inherited __setitem__ works fine

def NumPy_array_iterator(a, **kwargs):
    """
    Iterate over all elements in a NumPy array a.
    Return values: generator function and the code of this function.

    The keyword arguments specify offsets in the start and stop value
    of the index in each dimension. Legal values are
    offset0_start, offset0_stop, offset1_start, offset1_stop, etc.
    Also offset_start and offset_stop are legal keyword arguments,
    these imply the same offset value for all dimensions.
    
    Examples::
    
    >>> q = seq(1, 2*3*4, 1);  q.shape = (2,3,4)
    >>> it, code = NumPy_array_iterator(q)
    >>> print code  # generator function with 3 nested loops:
    def nested_loops(a):
        for i0 in xrange(0, a.shape[0]-0):
            for i1 in xrange(0, a.shape[1]-0):
                for i2 in xrange(0, a.shape[2]-0):
                    yield a[i0, i1, i2], (i0, i1, i2)
    >>> type(it)
    <type 'function'>
    >>> for value, index in it(q):
    ...     print 'a%s = %g' % (index, value)
    ...
    a(0, 0, 0) = 1
    a(0, 0, 1) = 2
    a(0, 0, 2) = 3
    a(0, 0, 3) = 4
    a(0, 1, 0) = 5
    a(0, 1, 1) = 6
    a(0, 1, 2) = 7
    a(0, 1, 3) = 8
    a(0, 2, 0) = 9
    a(0, 2, 1) = 10
    a(0, 2, 2) = 11
    a(0, 2, 3) = 12
    a(1, 0, 0) = 13
    a(1, 0, 1) = 14
    a(1, 0, 2) = 15
    a(1, 0, 3) = 16
    a(1, 1, 0) = 17
    a(1, 1, 1) = 18
    a(1, 1, 2) = 19
    a(1, 1, 3) = 20
    a(1, 2, 0) = 21
    a(1, 2, 1) = 22
    a(1, 2, 2) = 23
    a(1, 2, 3) = 24

    Now let us try some offsets::

    >>> it, code = NumPy_array_iterator(q, offset1_stop=1, offset_start=1)
    >>> print code
    def nested_loops(a):
        for i0 in xrange(1, a.shape[0]-0):
            for i1 in xrange(1, a.shape[1]-1):
                for i2 in xrange(1, a.shape[2]-0):
                    yield a[i0, i1, i2], (i0, i1, i2)
    >>> # note: the offsets appear in the xrange arguments
    >>> for value, index in it(q):
    ...     print 'a%s = %g' % (index, value)
    ...
    a(1, 1, 1) = 18
    a(1, 1, 2) = 19
    a(1, 1, 3) = 20
    """
    # build the code of the generator function in a text string
    # (since the number of nested loops needed to iterate over all
    # elements are parameterized through len(a.shape))
    dims = range(len(a.shape))
    offset_code1 = ['offset%d_start=0' % d for d in dims]
    offset_code2 = ['offset%d_stop=0'  % d for d in dims]
    for d in range(len(a.shape)):
        key1 = 'offset%d_start' % d
        key2 = 'offset%d_stop' % d
        if key1 in kwargs.keys():
            offset_code1.append(key1 + '=' + str(kwargs[key1]))
        if key2 in kwargs.keys():
            offset_code2.append(key2 + '=' + str(kwargs[key2]))
        
    for key in kwargs:
        if key == 'offset_start':
            offset_code1.extend(['offset%d_start=%d' % (d, kwargs[key]) \
                            for d in range(len(a.shape))])
        if key == 'offset_stop':
            offset_code2.extend(['offset%d_stop=%d' % (d, kwargs[key]) \
                            for d in range(len(a.shape))])

    for line in offset_code1:
        exec line
    for line in offset_code2:
        exec line
    code = 'def nested_loops(a):\n'
    indentation = ' '*4
    indent = '' + indentation
    for dim in range(len(a.shape)):
        code += indent + \
        'for i%d in xrange(%d, a.shape[%d]-%d):\n' \
                % (dim, eval('offset%d_start' % dim),
                   dim, eval('offset%d_stop' % dim))
        indent += indentation
    index = ', '.join(['i%d' % d for d in range(len(a.shape))])
    code += indent + 'yield ' + 'a[%s]' % index + ', (' + index + ')'
    exec code
    return nested_loops, code


def NumPy_type(a):
    """
    @param a: NumPy array
    @return:  "Numeric", "numarray", or "numpy", depending on which
    module that was used to generate the a array
    """
    import Numeric
    if isinstance(a, Numeric.ArrayType):
        return 'Numeric'
    import numarray
    if isinstance(a, numarray.NumArray):
        return 'numarray'
    import numpy
    if isinstance(a, numpy.ndarray):
        return 'numpy'
    

def fortran_storage(a):
    """
    Transparent transform of a NumPy array to Fortran (column major)
    storage.

    @param a:  NumPy array (generated in Python or C with C storage)
    @return: a new NumPy array with column major storage.

    Method: If a is of numpy type, numpy.asarray(a, fortran=True)
    is used to produce the new array.
    If a is of Numeric or numarray type, we want to preserve the array type
    and use a simple (and slower) transpose(transpose(a).copy()) instead.
    """
    if NumPy_type(a) == 'Numeric' or NumPy_type(a) == 'numarray':
        return transpose(transpose(a).copy())
    else:
        import numpy
        return numpy.asarray(a, fortran=True)
    
            
def _doctest():
    import doctest, numpytools
    return doctest.testmod(numpytools)

# Short forms:
fft = FFT
#mlab = MLab
try:
    ma = MA
except NameError:
    # for Numeric we do not import MA since it affects output format
    pass
ra = RandomArray
la = LinearAlgebra 
    
def verify(N, namecheck = ['fft','mlab','ma','ra','la']):
    """
    Verify that some packages imported by numpytools 
    works for Numeric, numarray, or numpy.
    """
    print "\nUsing %s in %s" % (N.basic_NumPy, N.__name__)
    for name in namecheck:
	print "%s.%s : %s " % (
            N.__name__,
            name,
            eval("N.%s.__name__" %name))
    print ""

def _test1():
    """Call verify function for N as Numeric, numarray, and numpy."""
    sys.argv.append('--Numeric')
    import numpytools as N
    verify(N)
    sys.argv[-1] = '--numarray'
    reload(N)
    verify(N)
    sys.argv[-1] = '--numpy'
    reload(N)
    verify(N)


if __name__ == '__main__':

    #_test1()

    #test_ArrayGen()
    #_doctest()  # does not work properly with wrap2callable
    
    # Test meshgrid function
    import unittest
    import numpytools as N

    class numpytoolsTest(unittest.TestCase):
        def setUp(self):
            pass

        def testMeshgrid(self):
            #print 'testing Meshgrid'
            x = N.arange(10)
            y = N.arange(4)
            z = N.arange(3)
            X, Y, Z = N.meshgrid(x, y, z, sparse=False)
            assert N.rank(X) == 3

        def testMeshgrid_DenseFromMixedArrayTypes(self):
            # Other combination of arrays
            #print 'testing Meshgrid with mixed array implementations'
            y = N.arange(4)
            z = N.arange(3)
            
            import Numeric
            x = Numeric.arange(10)
            X, Y, Z = N.meshgrid(x, y, z, sparse=False)
            if not  N.rank(X) == 3:
                raise AssertionError, \
                      "Meshgrid failed with arraytype mix of  Numeric and %s"\
                      %N.basic_NumPy
            import numarray
            x = numarray.arange(10)
            X, Y, Z = N.meshgrid(x, y, z, sparse=False)

            if not  N.rank(X) == 3:
                raise AssertionError, \
                      "Meshgrid failed with arraytype mix of numarray and %s"\
                      %N.basic_NumPy

            import numpy
            x = numpy.arange(10)
            X, Y, Z = N.meshgrid(x, y, z, sparse=False)
            #assert N.rank(X) == 3
            if not  N.rank(X) == 3:
                raise AssertionError, \
                      "Meshgrid failed with arraytype mix of numpy and %s"\
                      %N.basic_NumPy
            
        def testMeshGrid_DenseFromNodenseMeshgridOutput(self):
            # sparse fails for dense output when input has singleton dimensions
            x = seq(-2,2,0.1)
            y = seq(-4,4,1)
            xx, yy = meshgrid(x,y) # xx and yy now has singleton dimension
            self.assertEqual(rank(xx), 2) 
            self.assertEqual(rank(yy), 2)
            self.assertEqual(multiply.reduce(xx.shape), size(xx)) 
            self.assertEqual(multiply.reduce(yy.shape), size(yy))
            # This one should fail when xx and yy is not flat as well
            xx, yy = meshgrid(xx.flat, yy.flat, sparse=False) # no singleton
            self.assertEqual(shape(xx), (size(x), size(y)))
            self.assertEqual(shape(yy), (size(x), size(y)))
            
            xx, yy = meshgrid(x,y) # Add singleton dimensions
            xx, yy = meshgrid(xx, yy, sparse=False) 
            self.assertEqual(shape(xx), (size(x), size(y)))
            self.assertEqual(shape(yy), (size(x), size(y)))

            #from IPython.Shell import IPythonShellEmbed as magic
            #magic()('from unittest')
            
    sys.argv.append('--Numeric')
    for arg in ['--Numeric', '--numarray', ' --numpy']:
        sys.argv[-1] = arg
        print '\nNow testing with system arg %10s\n%s' %(arg, '='*38)
        reload(N);  N.verify(N)
        suite = unittest.makeSuite(numpytoolsTest)
        unittest.TextTestRunner(verbosity=2).run(suite)





    
