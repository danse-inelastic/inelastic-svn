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


from DbObject import DbObject as base
class NeutronExperiment(base):

    name = 'neutronexperiments'

    import pyre.db

    instrument_id = pyre.db.varchar( name = 'instrument_id', length = 100 )
    instrument_id.meta['tip'] = 'reference id in the instrument table'

    sampleassembly_id = pyre.db.varchar( name = 'sampleassembly_id', length = 100 )
    sampleassembly_id.meta['tip'] = 'reference id in the sample assembly table'

    ncount = pyre.db.real( name = 'ncount', default = 1e6)

    constructed = pyre.db.varchar( name = 'constructed', length = 4 )

    job_id = pyre.db.varchar( name = 'job_id', length = 100 )

    pass # end of NeutronExperiment


# version
__id__ = "$Id$"

# End of file 
