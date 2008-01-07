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


from numpy import array
from pyre.units.length import m


import unittest


from unittestX import TestCase
class parser_TestCase(TestCase):


    def test0(self):
        """
        sampleassembly.saxml.parser
        """
        from sampleassembly.saxml import parse_file
        sampleassembly = parse_file( 'Ni.xml' )
        return


    pass # end of parser_TestCase


import unittest

def pysuite():
    suite1 = unittest.makeSuite(parser_TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
    from instrument.elements import debug
    debug.activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: parser_TestCase.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file 
