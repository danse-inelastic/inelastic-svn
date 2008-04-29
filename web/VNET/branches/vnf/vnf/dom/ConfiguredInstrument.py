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


from OwnedObject import OwnedObject


class ConfiguredInstrument(OwnedObject):
    
    name = "configuredinstruments"
    
    import pyre.db

    instrument = pyre.db.varchar( name = 'instrument', length = 100 )
    instrument.meta['tip'] = 'id of instrument in the instrument table'
    
    configuration = pyre.db.varchar( name = 'configuration', length = 100 )
    configuration.meta['tip'] = 'id of configuration in the "<instrument>configuration" table'
    
    pass # end of Instrument


# version
__id__ = "$Id$"

# End of file 
