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


from Table import Table
class Crystal(Table):

    name = 'crystals'

    import pyre.db

    id = pyre.db.varchar(name="id", length=100)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    creater = pyre.db.varchar(name='creater', length = 32)
    creater.meta['tip'] = 'creater of sample assembly'

    date = pyre.db.date( name='date' )
    date.meta['tip'] = 'date of creation'

    chemical_formula = pyre.db.varchar( name='chemical_formula', length = 1024 )
    chemical_formula.meta['tip'] = "chemical formula"

    datafile = pyre.db.varchar( name='datafile', length = 1024 )
    datafile.meta['tip'] = 'data file name'

    pass # end of Crystal


# version
__id__ = "$Id$"

# End of file 
