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

    import ccp1gui
    from ccp1gui import ccp1gui as ccp1guimodule

    print "copyright information:"
    print "   ", ccp1gui.copyright()
    print "   ", ccp1guimodule.copyright()

    print
    print "module information:"
    print "    file:", ccp1guimodule.__file__
    print "    doc:", ccp1guimodule.__doc__
    print "    contents:", dir(ccp1guimodule)

    print
    print ccp1guimodule.hello()

# version
__id__ = "$Id$"

#  End of file 
