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

#include "exceptions.h"
#include "bindings.h"


char pysampleassembly_module__doc__[] = "";

// Initialization function for the module (*must* be called initsampleassembly)
extern "C"
void
initsampleassembly()
{
    // create the module and add the functions
    PyObject * m = Py_InitModule4(
        "sampleassembly", pysampleassembly_methods,
        pysampleassembly_module__doc__, 0, PYTHON_API_VERSION);

    // get its dictionary
    PyObject * d = PyModule_GetDict(m);

    // check for errors
    if (PyErr_Occurred()) {
        Py_FatalError("can't initialize module sampleassembly");
    }

    // install the module exceptions
    pysampleassembly_runtimeError = PyErr_NewException("sampleassembly.runtime", 0, 0);
    PyDict_SetItemString(d, "RuntimeException", pysampleassembly_runtimeError);

    return;
}

// version
// $Id$

// End of file
