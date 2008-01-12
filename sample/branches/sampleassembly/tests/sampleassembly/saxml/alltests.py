#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import os

#get current directory
curdir = os.path.abspath( os.curdir )

#get all files
files = os.listdir( curdir )

#get names of all test cases
tests = []
for f in files:
    if f.endswith("TestCase.py"): tests.append( f.rstrip('.py') )
    continue

#make a list of test suites
allsuites = []
import sys
sys.path = [curdir] + sys.path
for test in tests:
    testmodule = __import__( test )
    suite = testmodule.pysuite()
    allsuites.append( suite )
    continue
sys.path = sys.path[1:]

import unittest
alltests = unittest.TestSuite( allsuites )


def main():
    #run test
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == "__main__": main()


# version
__id__ = "$Id: alltests.py 1064 2006-08-07 20:23:34Z linjiao $"

# End of file 
