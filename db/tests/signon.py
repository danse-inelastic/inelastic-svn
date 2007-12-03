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

    import db
    from db import db as dbmodule

    print "copyright information:"
    print "   ", db.copyright()
    print "   ", dbmodule.copyright()

    print
    print "module information:"
    print "    file:", dbmodule.__file__
    print "    doc:", dbmodule.__doc__
    print "    contents:", dir(dbmodule)

    print
    print dbmodule.hello()

# version
__id__ = "$Id$"

#  End of file 
