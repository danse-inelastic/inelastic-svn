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

#include <iostream>
#include <sstream>

//numpy stuff
#define PY_ARRAY_UNIQUE_SYMBOL numpyext_ARRAY_API
#ifndef STANDALONE_USE_OF_NUMPY_SUPPORT
#define NO_IMPORT_ARRAY
#endif

#include "Python.h"
#include "numpy/arrayobject.h"

#include "wrapdataptr.h"


namespace numpyextmod {

  // wrapdataptr
  char wrapdataptr__name__[] = "wrapdataptr";
  char wrapdataptr__doc__[] = "wrapdataptr(ptr, type, size)\n" ;

  PyObject * wrapdataptr(PyObject *, PyObject *args)
  {
    PyObject *pycobj;
    int dtype; int size;

    int ok = PyArg_ParseTuple
      (args, "Oii", &pycobj, &dtype, &size );

    if (!ok) return 0;

    // check pycobj
    std::ostringstream oss;
    if (!PyCObject_Check(pycobj)) {
      oss << "not a PyCObject" << std::endl;
      PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
      return 0;
    }
    
    void *data = PyCObject_AsVoidPtr( pycobj );

    int nd = 1;
    int dims[1];
    dims[0] = size;
    return PyArray_FromDimsAndData( nd, dims, dtype, (char *)data);
  }

}


// version
// $Id$

// End of file
