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


class CrossSectionCalculator:


    def __call__(self, scatterer):
        return scatterer.identify(self)


    def onPowderSample(self, powder):
        # a powder sample must have a crystal phase
        phase = powder.phase
        assert phase.type == 'crystal'
        crystal = phase
        return self.onCrystal(crystal)


    def onCrystal(self, crystal):
        #unit cell
        unitcell = crystal.unitcell
        return self.onUnitCell( unitcell )
    

    def onUnitCell(self, unitcell):
        #atoms
        atoms = unitcell.getAtoms()
        #
        abs = sum( [ atom.average_neutron_abs_xs for atom in atoms ] )
        coh = sum( [ atom.average_neutron_coh_xs for atom in atoms ] )
        inc = sum( [ atom.average_neutron_inc_xs for atom in atoms ] )

        #volumn of unit cell
        v = volume( * unitcell.getCellVectors() )
        import units
        barn = units.area.barn
        A = units.length.angstrom

        unit = barn / A**3
        
        return N.array( [abs, inc, coh] )/v * unit

    #end of CrossSectionCalculator


def volume( a, b, c ):
    return N.dot( a, N.cross(b,c) )

import numpy as N


# version
__id__ = "$Id$"

# End of file 
