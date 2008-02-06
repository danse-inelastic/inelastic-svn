// -*- C++ -*-
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 
//                               Michael A.G. Aivazis
//                        California Institute of Technology
//                        (C) 1998-2005  All Rights Reserved
// 
//  <LicenseText>
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 

#include <portinfo>
#include <Python.h>

#include "bindings.h"

#include "misc.h"          // miscellaneous methods
#include "Iterator1D_Example.h"
#include "getdataptr.h"

// the method table

struct PyMethodDef pynumpyext_methods[] = {

    // dummy entry for testing
    {pynumpyext_hello__name__, pynumpyext_hello,
     METH_VARARGS, pynumpyext_hello__doc__},

    {pynumpyext_copyright__name__, pynumpyext_copyright,
     METH_VARARGS, pynumpyext_copyright__doc__},

    // print double array
    {numpyextmod::printdblarray__name__, numpyextmod::printdblarray,
     METH_VARARGS, numpyextmod::printdblarray__doc__},

    // getdataptr
    {numpyextmod::getdataptr__name__, numpyextmod::getdataptr,
     METH_VARARGS, numpyextmod::getdataptr__doc__},

    // print double array 2
    {numpyextmod::printdblarray2__name__, numpyextmod::printdblarray2,
     METH_VARARGS, numpyextmod::printdblarray2__doc__},


// Sentinel
    {0, 0}
};

// version
// $Id$

// End of file
