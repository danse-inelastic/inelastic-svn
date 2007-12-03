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

PROJECT = sampleassembly
PACKAGE = sampleassemblymodule
MODULE = sampleassembly

include std-pythonmodule.def
include local.def

PROJ_CXX_SRCLIB = -lsampleassembly

PROJ_SRCS = \
    bindings.cc \
    exceptions.cc \
    misc.cc


# version
# $Id$

# End of file
