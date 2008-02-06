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


//numpy stuff
#define PY_ARRAY_UNIQUE_SYMBOL numpyext_ARRAY_API
#include "numpy/arrayobject.h"


char pynumpyext_module__doc__[] = "";

// Initialization function for the module (*must* be called initnumpyext)
extern "C"
void
initnumpyext()
{
    // create the module and add the functions
    PyObject * m = Py_InitModule4(
        "numpyext", pynumpyext_methods,
        pynumpyext_module__doc__, 0, PYTHON_API_VERSION);

    // get its dictionary
    PyObject * d = PyModule_GetDict(m);

    // check for errors
    if (PyErr_Occurred()) {
        Py_FatalError("can't initialize module numpyext");
    }

    // install the module exceptions
    pynumpyext_runtimeError = PyErr_NewException("numpyext.runtime", 0, 0);
    PyDict_SetItemString(d, "RuntimeException", pynumpyext_runtimeError);

    // numpy
    import_array();

    return;
}

// version
// $Id$

// End of file
