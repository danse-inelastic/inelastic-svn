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

struct PyMethodDef pysampleassembly_methods[] = {

    // dummy entry for testing
    {pysampleassembly_hello__name__, pysampleassembly_hello,
     METH_VARARGS, pysampleassembly_hello__doc__},

    {pysampleassembly_copyright__name__, pysampleassembly_copyright,
     METH_VARARGS, pysampleassembly_copyright__doc__},


// Sentinel
    {0, 0}
};

// version
// $Id$

// End of file
