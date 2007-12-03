#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  alltest.py
#  
#  4/6/2005 version 0.0.1e
#  mmckerns@caltech.edu
#  (C) 2005 All Rights Reserved
# 
#  <LicenseText>
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from Matplotlib import *
from grace import *

import unittest


if __name__ == "__main__":
    suite0 = unittest.makeSuite(Matplot_Matplot_TestCase)
    suite1 = unittest.makeSuite(PyGrace_PyGrace_TestCase)
    alltests = unittest.TestSuite((suite0,suite1))
    unittest.TextTestRunner(verbosity=2).run(alltests)


# version
__id__ = "$Id: alltest.py 71 2005-04-07 23:07:02Z mmckerns $"

#  End of file 
