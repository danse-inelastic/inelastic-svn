# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Object import Object
class Crystal(Object):

    name = 'crystals'

    import pyre.db

    chemical_formula = pyre.db.varchar( name='chemical_formula', length = 1024 )
    chemical_formula.meta['tip'] = "chemical formula"

    datafile = pyre.db.varchar( name='datafile', length = 1024 )
    datafile.meta['tip'] = 'data file name'

    pass # end of Crystal


# version
__id__ = "$Id$"

# End of file 
