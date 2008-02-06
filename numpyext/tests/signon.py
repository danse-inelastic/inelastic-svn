#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


def test0():
    import numpyext
    from numpyext import numpyext as numpyextmodule

    print "copyright information:"
    print "   ", numpyext.copyright()
    print "   ", numpyextmodule.copyright()

    print
    print "module information:"
    print "    file:", numpyextmodule.__file__
    print "    doc:", numpyextmodule.__doc__
    print "    contents:", dir(numpyextmodule)

    print
    print numpyextmodule.hello()
    return


def testprintdblarray():
    from numpyext import numpyext as numpyextmodule
    from numpy import array, arange
    a = arange( 1, 10, 1.0 )
    numpyextmodule.printdblarray( a )
    return


def testprintdblarray2():
    from numpyext import numpyext as numpyextmodule
    from numpy import array, arange
    a = arange( 1, 10, 1.0 )
    ptr = numpyextmodule.getdataptr( a )
    size = len(a)
    del a
    numpyextmodule.printdblarray2( ptr, size )
    return


def testwrapptr( ):
    from numpyext import numpyext as numpyextmodule
    from numpy import array, arange
    a = arange( 1, 10, 1.0 )
    ptr = numpyextmodule.getdataptr( a )
    b = numpyextmodule.wrapdataptr( ptr, a.dtype.num, len(a) )
    a[4]= 999
    assert a[4] == b[4]
    return
    


def main():
    test0()
    testprintdblarray()
    testprintdblarray2()
    testwrapptr()
    return


if __name__ == "__main__": main()


# version
__id__ = "$Id$"

#  End of file 
