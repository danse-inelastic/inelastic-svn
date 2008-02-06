# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

PROJECT = numpyext
PACKAGE = numpyextmodule
MODULE = numpyext

include std-pythonmodule.def
include local.def

PROJ_CXX_SRCLIB = -lnumpyext

PROJ_SRCS = \
	bindings.cc \
	exceptions.cc \
	getdataptr.cc \
	misc.cc \
	Iterator1D_Example.cc \


# version
# $Id$

# End of file
