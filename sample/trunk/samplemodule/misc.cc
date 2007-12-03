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
#include "libsample/hello.h"


// copyright

char pysample_copyright__doc__[] = "";
char pysample_copyright__name__[] = "copyright";

static char pysample_copyright_note[] = 
    "sample python module: Copyright (c) 1998-2005 Michael A.G. Aivazis";


PyObject * pysample_copyright(PyObject *, PyObject *)
{
    return Py_BuildValue("s", pysample_copyright_note);
}
    
// hello

char pysample_hello__doc__[] = "";
char pysample_hello__name__[] = "hello";

PyObject * pysample_hello(PyObject *, PyObject *)
{
    return Py_BuildValue("s", hello());
}
    
// version
// $Id$

// End of file
