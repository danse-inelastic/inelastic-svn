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

// the method table

struct PyMethodDef pysample_methods[] = {

    // dummy entry for testing
    {pysample_hello__name__, pysample_hello,
     METH_VARARGS, pysample_hello__doc__},

    {pysample_copyright__name__, pysample_copyright,
     METH_VARARGS, pysample_copyright__doc__},


// Sentinel
    {0, 0}
};

// version
// $Id$

// End of file
