#!/usr/bin/env python
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


def cross_sections( scatterer, calculator = None ):
    '''calculate cross sections of the given scatterer

    return:
      absorption_cross_section
      incoherent_scattering_cross_section
      coherent_scattering_cross_section
    '''
    
    if calculator is None:
        from CrossSectionCalculator import CrossSectionCalculator
        calculator = CrossSectionCalculator()
        pass
    return calculator( scatterer )



# version
__id__ = "$Id$"

# End of file 
