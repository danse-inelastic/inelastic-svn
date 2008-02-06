#ifndef NUMPYEXTMODULE_UTILS_H
#define NUMPYEXTMODULE_UTILS_H


#include "Python.h"


namespace numpyextmod {

  void detach( void *ptr, void *target)
  {
    PyObject * obj = static_cast<PyObject *> ( target );
    Py_DECREF( obj );
  }

}

#endif
