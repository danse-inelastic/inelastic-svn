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

if __name__ == "__main__":

    import sampleassembly
    from sampleassembly import sampleassembly as sampleassemblymodule

    print "copyright information:"
    print "   ", sampleassembly.copyright()
    print "   ", sampleassemblymodule.copyright()

    print
    print "module information:"
    print "    file:", sampleassemblymodule.__file__
    print "    doc:", sampleassemblymodule.__doc__
    print "    contents:", dir(sampleassemblymodule)

    print
    print sampleassemblymodule.hello()

# version
__id__ = "$Id$"

#  End of file 
