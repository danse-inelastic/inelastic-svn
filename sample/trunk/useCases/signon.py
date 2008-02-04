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

    import sample
    from sample import sample as samplemodule

    print "copyright information:"
    print "   ", sample.copyright()
    print "   ", samplemodule.copyright()

    print
    print "module information:"
    print "    file:", samplemodule.__file__
    print "    doc:", samplemodule.__doc__
    print "    contents:", dir(samplemodule)

    print
    print samplemodule.hello()

# version
__id__ = "$Id$"

#  End of file 
