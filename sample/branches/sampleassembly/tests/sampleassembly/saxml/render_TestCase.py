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
        sampleassembly.saxml.render
        """
        from sampleassembly.saxml import render, parse_file
        sampleassembly = parse_file( 'Ni.xml' )
        text = render( sampleassembly )
        print >> open('Ni.xml.rendered','w'),  '\n'.join(text) 
        return


    def test2(self):
        """
        sampleassembly.saxml.weave
        """
        from sampleassembly.saxml import weave, parse_file
        sampleassembly = parse_file( 'Ni.xml' )
        weave(sampleassembly, open('Ni.xml.weaved', 'w') )
        return


    def test3(self):
        """
        parse weaved xml
        """
        from sampleassembly.saxml import parse_file
        sampleassembly = parse_file( 'Ni.xml.weaved')
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
