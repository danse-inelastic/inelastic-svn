#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 

def copyright():
    return "bpext pyre module: Copyright (c) 2004-2007 Jiao Lin";

try:
    import boost.python
except ImportError, msg:
    print msg
    print '''
Warning:
    This module is an extension of boost.python.
    for example, it extracts pointer from boost.python object.
    Sometimes, a module of boost.python must be loaded before this
    module can be successfully loaded.
'''


import _bpext as binding


def extract_ptr( bpobject, typename ):
    '''Extract pointer out of a boost python object and return a PyCObject
holding that pointer. pointer is shared.

Parameters:

  bpobject: boost python object
  typename: type name

Examples:

  extract_ptr( bpo, 'vec_double' )
  '''
    return binding.extract_ptr( bpobject, typename )



def wrap_ptr( pycobject, typename ):
    '''Wrap a pointer in a PyCObject to become a boost python object.
pointer is shared.

Parameters:

  pycobject: PyCObject instance
  typename: type name

Examples:

  wrap_ptr( pycobj, 'vec_double' )
  '''
    return binding.wrap_ptr( pycobject, typename )


def wrap_native_ptr( pycobject ):
    '''Wrap a pointer of a native type (for example, double *)
in a simple c struct which only contains one void pointer.
Then return a boost python object of that c struct.
pointer is shared.

Parameters:

  pycobject: PyCObject instance

Examples:

  wrap_ptr( pycobj )
  '''
    return binding.wrap_native_ptr( pycobject )


# version
__id__ = "$Id: __init__.py 17 2005-06-01 23:58:56Z linjiao $"

#  End of file 
