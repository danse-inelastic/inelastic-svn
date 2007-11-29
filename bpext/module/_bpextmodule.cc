// -*- C++ -*-
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 
//                               Michael A.G. Aivazis
//                        California Institute of Technology
//                        (C) 1998-2004  All Rights Reserved
// 
//  <LicenseText>
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 

#include <portinfo>

#include <Python.h>

#include "exceptions.h"
#include "bindings.h"

#include "register_converters.h"


void **PyArray_API;

char pybpext_module__doc__[] = "";

// Initialization function for the module (*must* be called initbpext)
extern "C"
void
init_bpext()
{
    // create the module and add the functions
    PyObject * m = Py_InitModule4(
        "_bpext", pybpext_methods,
        pybpext_module__doc__, 0, PYTHON_API_VERSION);

    // get its dictionary
    PyObject * d = PyModule_GetDict(m);

    // check for errors
    if (PyErr_Occurred()) {
        Py_FatalError("can't initialize module bpext");
    }

    // install the module exceptions
    pybpext_runtimeError = PyErr_NewException("bpext.runtime", 0, 0);
    PyDict_SetItemString(d, "RuntimeException", pybpext_runtimeError);

    wrap::register_converters();
    return;
}

// version
// $Id: bpextmodule.cc 2 2004-12-07 22:46:28Z linjiao $

// End of file
