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

#include "numpyext/Iterator1D.h"
#include "Iterator1D_Example.h"


namespace numpyextmod
{

  typedef Array1DIterator<npy_double> DblArrIt;

  // printdblarray
  char printdblarray__name__[] = "printdblarray";
  char printdblarray__doc__[] = "printdblarray(array)\n" ;

  PyObject * printdblarray(PyObject *, PyObject *args)
  {
    PyObject *pyarray;

    int ok = PyArg_ParseTuple
      (args, "O", &pyarray);

    if (!ok) return 0;

    // check array
    std::ostringstream oss;
    if (!PyArray_Check(pyarray)) {
      oss << "not a numpy array" << std::endl;
      PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
      return 0;
    }

    // create iterator
    DblArrIt it( pyarray );

    size_t n = PyArray_Size( pyarray );
    for (size_t i = 0; i<n; i++) std::cout << *(it+i) << "," ;
    std::cout << std::endl;
    return Py_None;
  }
    
} // numpyextmod::



// version
// $Id$

// End of file
