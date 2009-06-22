#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import unittest

class TestCase(unittest.TestCase):

    def test(self):
        from idf2histogram.Polarizations import read
        material = 'fccNi-phonondisp-from-bvk-N20'
        h = read(material)

        out = '%s-pols.h5' % material
        import os
        if os.path.exists(out): os.remove(out)
        import histogram.hdf as hh
        hh.dump(h, out, '/', 'c')
        return
        
    def test2(self):
        from idf2histogram.Polarizations import read
        material = 'fccNi-phonondisp-from-phon-N10'
        h = read(material)

        out = '%s-pols.h5' % material
        import os
        if os.path.exists(out): os.remove(out)
        import histogram.hdf as hh
        hh.dump(h, out, '/', 'c')
        return
        
    pass # end of TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: Polarizations_TestCase.py 1421 2009-05-13 18:59:00Z linjiao$"

# End of file 
