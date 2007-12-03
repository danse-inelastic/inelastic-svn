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
#include "libsampleassembly/hello.h"


// copyright

char pysampleassembly_copyright__doc__[] = "";
char pysampleassembly_copyright__name__[] = "copyright";

static char pysampleassembly_copyright_note[] = 
    "sampleassembly python module: Copyright (c) 1998-2005 Michael A.G. Aivazis";


PyObject * pysampleassembly_copyright(PyObject *, PyObject *)
{
    return Py_BuildValue("s", pysampleassembly_copyright_note);
}
    
// hello

char pysampleassembly_hello__doc__[] = "";
char pysampleassembly_hello__name__[] = "hello";

PyObject * pysampleassembly_hello(PyObject *, PyObject *)
{
    return Py_BuildValue("s", hello());
}
    
// version
// $Id$

// End of file
