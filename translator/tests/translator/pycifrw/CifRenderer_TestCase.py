#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



import unittestX as unittest

#import journal

#debug = journal.debug( "CifRenderer_TestCase" )
#warning = journal.warning( "CifRenderer_TestCase" )



class CifRenderer_TestCase(unittest.TestCase):

    def test(self):

        from crystal.UnitCell import UnitCell, Site
        from crystal.Atom import Atom
        
        uc = UnitCell( )
        
        at1 = Atom(symbol='Fe', mass=57)
        at2 = Atom(symbol='Al')
        at3 = Atom(symbol="Zr")
        
        site1 = Site((0,0,0), at1)
        site2 = Site((0.5,0.5,0.5), at2)
        site3 = Site((0.5, 0.5, 0.0), at3)
        site4 = Site((0.5, 0.0, 0.5), at3)
        site5 = Site((0.0, 0.5, 0.5), at3)
        
        uc.addSite(site1, "Fe1" )
        uc.addSite(site2, "Al1" )
        uc.addSite(site3, "")
        uc.addSite(site4, "")
        uc.addSite(site5, "")

        class Sample: pass
        sample = Sample()
        sample.unitcell = uc
        sample.name = 'test'
        sample.chemical_formula = 'FeAlZr'

        from translator.pycifrw import weaveCif
        weaveCif( sample )
        return
    
    pass  # end of CifRenderer_TestCase



def pysuite():
    suite1 = unittest.makeSuite(CifRenderer_TestCase)
    return unittest.TestSuite( (suite1,) )


def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id$"

# End of file 
