#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                    Jiao Lin, Olivier Delaire, Brandon Keith
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class SampleAssembly:

    '''Sample assembly

    A sample assembly represents everything installed on the sample
    position of an instrument. It is a container of sample, sample holder,
    and maybe furnace, and more.

    A sample assembly is assumed to be installed at a fixed position
    and orientation in the instrument. That position and orientation
    is defined by convention, and is fixed for an instrument. 
    For an experiment done in that instrument, we may want to
    rotate or move sample or other things in the assembly, and that
    should be done with the geometer associated with this sample
    assembly.
    '''

    def getOrientation(self, scatterer):
        raise NotImplementedError
    

    pass # end of SampleAssembly

# version
__id__ = "$Id$"

# End of file 
