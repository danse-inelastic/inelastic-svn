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

#include "misc.h"


// copyright

char pynumpyext_copyright__doc__[] = "";
char pynumpyext_copyright__name__[] = "copyright";

static char pynumpyext_copyright_note[] = 
    "numpyext python module: Copyright (c) 2007 Jiao Lin";


PyObject * pynumpyext_copyright(PyObject *, PyObject *)
{
    return Py_BuildValue("s", pynumpyext_copyright_note);
}
    
// hello

char pynumpyext_hello__doc__[] = "";
char pynumpyext_hello__name__[] = "hello";

PyObject * pynumpyext_hello(PyObject *, PyObject *)
{
    return Py_BuildValue("s", "hello");
}
    
// version
// $Id$

// End of file
