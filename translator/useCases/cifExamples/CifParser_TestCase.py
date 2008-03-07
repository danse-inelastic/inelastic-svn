#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Brandon Keith
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import unittest  
from pycifrw.Translator import Translator

appName = "CifTranslator"
caseName = "fulltest"

import unittest, journal
debug = journal.debug( "%s-%s" % (appName, caseName) )

#from shutil import copyfile
#copyfile( "%s.pml.%s" % (appName, caseName),  "%s.pml"%appName)

class Translator_TestCase(unittest.TestCase):

    def setUp(self):
        """do graphite full cell"""
        self.translator=Translator('/home/brandon/DANSE/pycifrw/tests/graphite.cif')
        
    def testCoords(self):
        coords=self.translator.cifToAtomAndCoordinateList()
        #print coords
        assert coords==[['C', '0.00000', '0.00000', '0.00000'], 
                        ['C', '0.33333', '0.66667', '0.00000']]

    def testAllCoords(self):
        coords=self.translator.generateAllCoordinates()
        #this is risky because of round off error problems
        #print coords 
        assert coords==[[0.0, 0.0, 0.0], [0.0, 0.0, 0.5], 
                        [0.33333000000000002, 0.66666999999999998, 0.0], 
                        [0.66666999999999998, 0.33333999999999997, 0.5]]
    
def pysuite():
    suite1 = unittest.makeSuite(Translator_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    #journal.debug('reduction.histCompat').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main() 
