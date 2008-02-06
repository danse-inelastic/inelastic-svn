// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                        (C) 2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


#ifndef NUMPYEXTMODULE_ITERATOR1D_H
#define NUMPYEXTMODULE_ITERATOR1D_H

// require headers:
// #include <iostream>
// #include <sstream>

//numpy stuff
#define PY_ARRAY_UNIQUE_SYMBOL numpyext_ARRAY_API
#ifndef STANDALONE_USE_OF_NUMPY_SUPPORT
#define NO_IMPORT_ARRAY
#endif
#include "Python.h"
#include "numpy/arrayobject.h"


namespace numpyextmod {

  class index_out_of_bound: public std::exception{

  public:
  
    index_out_of_bound( int index ) {
      std::ostringstream oss;
      oss << "index out of bound: " << index;
      _msg = oss.str();
    }
    const char *what() const throw()  { return _msg.c_str(); }
    ~index_out_of_bound() throw() {}

  private:
    std::string _msg;

  };


  class different_array: public std::exception{

  public:
  
    different_array( ) : _msg("Different array" ) {}
    const char *what() const throw()  { return _msg.c_str(); }
    ~different_array() throw() {}

  private:
    std::string _msg;

  };

  
  class iterator_unintialized: public std::exception{

  public:
  
    iterator_unintialized( ) : _msg("Iterator not initialized" ) {}
    const char *what() const throw()  { return _msg.c_str(); }
    ~iterator_unintialized() throw() {}

  private:
    std::string _msg;

  };

  

  int gotoIndex( PyArrayIterObject *it, int index );


  template <typename ValueType>
  class Array1DIterator {

  public:

    typedef Array1DIterator< ValueType> mytype;

    ~Array1DIterator() 
    {
      //std::cout << "destructor" << std::endl;
      if (m_it) {
	Py_DECREF( m_it );
	Py_DECREF( m_it->ao );
      }
    }

    Array1DIterator () : m_it(0), m_index(0)
    {
      //std::cout << "trivial constructor" << std::endl;
    }

    Array1DIterator ( const mytype & rhs ) 
      : m_it( rhs.m_it ), m_index( rhs.m_index )
    {
      if (m_it) {
	Py_INCREF( m_it );
	Py_INCREF( m_it->ao );
      }
      //std::cout << "copy constructor" << std::endl;
    }

    const mytype & operator= ( const mytype & rhs ) 
    {
      m_it = rhs.m_it;
      m_index = rhs.m_index;
      if (m_it) {
	Py_INCREF( m_it );
	Py_INCREF( m_it->ao );
      }
      return *this;
    }

    Array1DIterator ( PyObject * ao )
      : m_it( (PyArrayIterObject *)PyArray_IterNew( (PyObject *)ao ) ), 
	m_index(0)
    {
      Py_INCREF( ao );
      //std::cout << "constructor from numpy array instance" << std::endl;
    }
    
    Array1DIterator (PyArrayIterObject *it) 
      : m_it( (PyArrayIterObject *)PyArray_IterNew( (PyObject *)(it->ao) ) ),
	m_index( it->index )
    { 
      Py_INCREF( it->ao );
      //std::cout << "constructor from numpy array builtin iterator" << std::endl;
    }

    Array1DIterator<ValueType> operator+(int n) const
    {
      Array1DIterator<ValueType> ret (*this);
      ret.m_index = m_index + n;
      return ret;
    }

    Array1DIterator<ValueType> operator-(int n) const
    {
      Array1DIterator<ValueType> ret (*this);
      ret.m_index = m_index - n;
      return ret;
    }

    int operator-(const Array1DIterator & rhs) const
    {
      if (m_it != rhs.m_it) throw different_array();
      
      return  m_index - rhs.m_index;
    }
    
    Array1DIterator<ValueType> & operator++()
    {
      //??? Is this implementation correct? Should not I use PyArray_ITER_NEXT?
      ++m_index;
      return *this;
    }

    Array1DIterator<ValueType> operator++(int)
    {
      Array1DIterator ret(*this);
      ++m_index;
      return ret;
    }

    Array1DIterator<ValueType> & operator--()
    {
      // ???????
      // is this correct?
      // we don't have PyArray_ITER_PREVIOUS
      // this implementation is the best I can do for now...
      --m_index;
      return *this;
    }

    Array1DIterator<ValueType> operator--(int)
    {
      Array1DIterator ret(*this);
      --m_index;
      return ret;
    }

    ValueType operator*() const
    {
      checkIndex();
      gotoIndex( m_it, m_index );
      return ValueType( *((ValueType*)(m_it->dataptr)) );
    }

    ValueType & operator*()
    {
      checkIndex();
      gotoIndex( m_it, m_index );
      return (ValueType &)( *((ValueType*)(m_it->dataptr)) );
    }

    bool operator==(const Array1DIterator & rhs) const
    {
      return (m_it==rhs.m_it and m_index == rhs.m_index);
    }

    bool operator!=(const Array1DIterator & rhs) const
    {
      return !(*this==rhs);
    }
  
    bool operator<(const Array1DIterator & rhs) const
    {
      if (m_it != rhs.m_it) throw different_array();
      
      return (m_index < rhs.m_index);
    }
  
    bool operator>(const Array1DIterator & rhs) const
    {
      if (m_it != rhs.m_it) throw different_array();

      return (m_index > rhs.m_index);
    }

    void print ( std::ostream & os ) const 
    {
      os << "numarray iterator for numarray object " 
	 << m_it->ao 
	 << " at "
	 << m_index;
    }
    
  private:
    PyArrayIterObject *m_it;
    int m_index;

    void checkIndex( ) const
    {
      if (m_it ==0) throw iterator_unintialized();
      if (m_index < 0) throw index_out_of_bound( m_index );
    }

  };

  /// goto 1d index of "index" in the given array.
  /// This method make sure we discard the python
  /// behavior of indexing: a[-1] = a[size-1].
  /// We want to make sure a[-1] throws out-of-bound error.
  inline int gotoIndex( PyArrayIterObject *it, int index )
  {
    if (index < 0) {
      return index;
    }
    
    PyArray_ITER_GOTO1D( it, index  );
    return it->index;
  }


  bool checkDataType( PyObject * obj, const char * name, int typecode );

  template <typename Iterator>
  void print( Iterator begin, Iterator end )
  {
    for (Iterator it = begin; it<end; ++it) {
      std::cout << *it << ", ";
    }
    std::cout << std::endl;
  }

}

template <typename ValueType>
std::ostream &  operator <<
  ( std::ostream & os, const numpyextmod::Array1DIterator<ValueType> & it )
{
  it.print(os);
  return os;
}

#endif  // NUMPYEXTMODULE_ITERATOR1D_H

// version
// $Id$

// End of file
