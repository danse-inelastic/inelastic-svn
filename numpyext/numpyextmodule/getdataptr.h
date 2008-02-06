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


#ifndef NUMPYEXTMODULE_GETDATAPTR_H
#define NUMPYEXTMODULE_GETDATAPTR_H


#include "Python.h"


namespace numpyextmod
{
  // getdataptr
  extern char getdataptr__name__[];
  extern char getdataptr__doc__[];
  extern "C"
    PyObject * getdataptr(PyObject *, PyObject *args);

  // examples to use void ptr
  // printdblarray2
  extern char printdblarray2__name__[];
  extern char printdblarray2__doc__[];
  extern "C"
    PyObject * printdblarray2(PyObject *, PyObject *args);

} // numpyextmod::


#endif // NUMPYEXTMODULE_GETDATAPTR_H


// version
// $Id: RebinTof2E_bdgs.h 512 2005-07-08 20:19:55Z tim $

// End of file
