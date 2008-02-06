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

#include "getdataptr.h"


namespace numpyextmod {

  void detachFromNumpyArray( void *data, void *npyarray)
  {
    PyObject * obj = static_cast<PyObject *> ( npyarray );
    Py_DECREF( obj );
  }

  // getdataptr
  char getdataptr__name__[] = "getdataptr";
  char getdataptr__doc__[] = "getdataptr(array)\n" ;

  PyObject * getdataptr(PyObject *, PyObject *args)
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
    
    Py_INCREF( pyarray );
    void *ptr = PyArray_DATA( pyarray );

    return PyCObject_FromVoidPtrAndDesc( ptr, pyarray, detachFromNumpyArray );
  }



  // printdblarray2
  char printdblarray2__name__[] = "printdblarray2";
  char printdblarray2__doc__[] = "printdblarray2(pycobject of double ptr, size)\n" ;

  PyObject * printdblarray2(PyObject *, PyObject *args)
  {
    PyObject *obj;
    int size;

    int ok = PyArg_ParseTuple
      (args, "Oi", &obj, &size);

    if (!ok) return 0;

    // check pointer
    if (!PyCObject_Check(obj)) {
      std::ostringstream oss;
      oss << "not a PyCObject" << std::endl;
      PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
      return 0;
    }

    // get void ponter
    void * ptr = PyCObject_AsVoidPtr( obj );

    double *arr = static_cast<double *> (ptr);

    for (int i=0; i<size; i++) 
      std::cout << arr[i] << ", ";
    std::cout << std::endl;

    return Py_None;
  }

}


// version
// $Id$

// End of file
