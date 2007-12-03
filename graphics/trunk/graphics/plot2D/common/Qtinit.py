#!/usr/bin/env python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#Created by:  Jiwu Liu (jliu@pa.msu.edu)
#description:  Required initialization when trying to use Qt together with thread
#                      Currently needed by Qwt 
#<LicenseText>
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#ensure that QApplication is created 
import qt,sys
try:
  qt.qApp.type()
except RuntimeError:
  import sys
  # a is dummy variable. It is required so that QApplication constructor would take effect
  a = qt.QApplication(sys.argv)

#version
__id__ = '$Id: qtinit.py,v 1.2 2005/08/31 19:44:54 jwliu Exp $'
