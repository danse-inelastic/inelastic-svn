// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                        (C) 2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#include <sstream>
#include <iostream>
#include <Python.h>
#include "Iterator1D.h"

namespace numpyextmod{

  bool checkDataType( PyObject * obj, const char * name, int typecode )
  {
    std::ostringstream oss;

    if (!PyArray_Check(obj)) {
      oss << name <<  " is not a numpy array" << std::endl;
      PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
      return 1;
    }
    if (PyArray_TYPE( obj ) != typecode ) {
      oss << name << " must be a numpy array of type " 
	  << typecode << std::endl;
      PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
      return 1;
    }
    return 0;
  }

} // numpyextmod::

// version
// $Id$

// End of file 
