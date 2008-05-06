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


from DbObject import DbObject
class AbInitio(DbObject):

    name = 'abInitio'

    import pyre.db
    
    engine = pyre.db.str('engine', default='vasp')
#    engine.validator=pyre.db.choice(['vasp', 'ab init'])
    engine.meta['tip'] = 'Ab initio engine'
    
    xcFunctional = pyre.db.str('xcFunctional', default='PAW-PBE')
#    xcFunctional.validator=pyre.db.choice(['PAW-PBE', 'PAW-GGA', 'LDA'])
    xcFunctional.meta['tip'] = 'Exchange correlation functional'
    
    kineticEnergyCutoff = pyre.db.float('kineticEnergyCutoff', default=140.0)
    kineticEnergyCutoff.meta['tip'] = 'Kinetic energy cutoff'
    
    monkhorstPackMesh = pyre.db.list('monkhorstPackMesh', default=[1,1,1])
    monkhorstPackMesh.meta['tip'] = 'Monkhorst pack mesh'
    
    supercell = pyre.db.list('supercell', default=[1,1,1])
    supercell.meta['tip'] = 'Supercell for phonon calculation'
    
    displacementAmplitude = pyre.db.float('displacementAmplitude', default=0.01)
    displacementAmplitude.meta['tip'] = 'Displacement amplitude'      
    
    qGrid = pyre.db.list('qGrid', default=[1,1,1])
    qGrid.meta['tip'] = 'Q grid for phonon calculation'       

    width = pyre.db.real( name = 'width', default = 0.05 )
    height = pyre.db.real( name = 'height', default = 0.1 )
    thickness = pyre.db.real( name = 'thickness', default = 0.002 )
    
    pass # end of Block


# version
__id__ = "$Id$"

# End of file 
