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


import unittest


from unittest import TestCase
class renderer_TestCase(TestCase):


    def test(self):
        """
        instrument.nixml.render
        """
        from instrument.nixml import render, parse_file
        instrument = parse_file( 'test.xml' )
        text = render( instrument )
        print >> open('test.xml.new','w'),  '\n'.join(text) 
        return


    def test2(self):
        """
        instrument.nixml.weave
        """
        from instrument.nixml import weave, parse_file
        instrument = parse_file( 'test.xml' )
        weave(instrument)
        return


    pass # end of renderer_TestCase


import unittest

def pysuite():
    suite1 = unittest.makeSuite(renderer_TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: renderer_TestCase.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file 
