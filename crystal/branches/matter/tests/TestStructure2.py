##############################################################################
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################


"""Unit tests for Structure class.
"""

__id__ = "$Id: TestStructure.py 2825 2009-03-09 04:33:12Z juhas $"

from numpy.ma.testutils import assert_almost_equal, assert_array_almost_equal
import os, sys
import unittest
import numpy

# useful variables
thisfile = locals().get('__file__', 'TestStructure2.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
testdata_dir = os.path.join(tests_dir, 'testdata')

sys.path.insert(0,os.path.abspath('..'))# this should put the source code first on the path
from matter.Structure import Structure

##############################################################################
class TestStructure(unittest.TestCase):
    """test methods of Structure class"""

    def setUp(self):
        
        xyzfile = os.path.join(testdata_dir, 'scf3.xyz')
        self.stru = Structure()
        self.stru.read(xyzfile)
        #print self.stru5
        
        file = os.path.join(testdata_dir, 'Pb.cif')
        self.stru2 = Structure()
        self.stru2.read(file)
        #print self.stru2
        
#        xyzfile = os.path.join(testdata_dir, 'KC24PosAndCharges.xyz')
#        self.stru2 = Structure()
#        self.stru2.read(xyzfile)

        self.places = 12  
        
    def testRS(self):
        """reciprocal space tests"""
        # print self.stru2.lattice
        recbase = self.stru2.lattice.recbase
        expected = \
            [[ 0.20242669, 0.,         0.        ],
             [ 0.,         0.20242669, 0.        ],
             [ 0.,         0.,         0.20242669]]
        from numpy import array
        expected = array(expected)

        self.assertArrayEqual(recbase, expected)
        
        from math import pi
        self.assertArrayEqual(
            self.stru2.lattice.recbase2pi,
            expected * 2 * pi,
            )
        return
    
        
    def test_charges(self):
        charges = [0.0, 0.0, 0.0, 0.0]
        self.stru.charges = charges
        self.assertAlmostEqual(self.stru[0].charge, charges[0])
        #print self.stru2.charges

    def test_writeStr(self):
        """check Structure.writeStr()"""
        s = self.stru.writeStr('xyz')
        expected = '''4
F_3 Sc_1
Sc  0 0 0
F   0 8.04246 8.17697
F   8.04246 0 8.17697
F   8.04246 8.04246 0
'''
        self.assertEqual(s, expected)
        return

    def assertListAlmostEqual(self, l1, l2, places=None):
        """wrapper for list comparison"""
        if places is None: places = self.places
        self.assertEqual(len(l1), len(l2))
        for i in range(len(l1)):
            self.assertAlmostEqual(l1[i], l2[i], places)
        
        
    def assertArrayEqual(self, v1, v2):
        from numpy.testing import assert_array_almost_equal
        assert_array_almost_equal(v1, v2)
        return


# End of class TestStructure

if __name__ == '__main__':
    unittest.main()

# End of file
