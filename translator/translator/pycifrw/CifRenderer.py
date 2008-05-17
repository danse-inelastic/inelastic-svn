# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# depends on PyCifRW


class CifRenderer:

    '''renderer to render a cif representation from a crystal
    structure'''


    def render(self, crystal):
        self._rep = CifFile.CifFile()
        self._currentblock = None
        self.dispatch( crystal )
        return self._rep


    def dispatch(self, obj):
        handler = 'on%s' % obj.__class__.__name__
        handler = getattr(self, handler)
        return handler( obj )


    def onSample(self, sample):        
        block = CifFile.CifBlock()
        block['_chemical_name'] = sample.name
        block['_chemical_formula_sum'] = sample.chemical_formula
        self._currentblock = block
        self.dispatch(sample.unitcell)
        self._rep['sample'] = block
        return
    

    def onUnitCell(self, unitcell):
        block = self._currentblock
        av, bv, cv = unitcell.getCellVectors()

        from numpy.linalg import norm as length
        block['_cell_length_a'] = str(length( av ))
        block['_cell_length_b'] = str(length( bv ))
        block['_cell_length_c'] = str(length( cv ))

        block['_cell_angle_alpha'] = str(angle( bv, cv ))
        block['_cell_angle_beta'] = str(angle( cv, av ))
        block['_cell_angle_gamma' ] = str(angle( av, bv ))
        
        block['_cell_volume' ] = str(unitcell.getVolume())

        id2site = unitcell._siteIds
        labels = id2site.keys()
        sites = id2site.values()
        positions = [ site.getPosition() for site in sites ]
        xs = [ str(p[0]) for p in positions ]
        ys = [ str(p[1]) for p in positions ]
        zs = [ str(p[2]) for p in positions ]
        symbols = [ site.getAtom().symbol for site in sites ]
        
        cols = [ labels, xs, ys, zs, symbols ]

        block.AddCifItem( (
            [[ '_atom_site_label',
               '_atom_site_fract_x',
               '_atom_site_fract_y',
               '_atom_site_fract_z',
               '_atom_site_type_symbol',
               ]],
            [cols],) )
            
        return

    

def angle( v1, v2 ):
    'calculate angle between two vectors'
    import numpy as N, numpy.linalg as nl
    v1 = v1/nl.norm( v1 ) 
    v2 = v2/nl.norm( v2 )
    dotprod = N.dot( v1, v2 )
    return N.arccos( dotprod ) * 180 / N.pi


import CifFile

# version
__id__ = "$Id$"

# End of file 
