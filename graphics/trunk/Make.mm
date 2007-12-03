# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Michael M. McKerns
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

PROJECT = graphics

# directory structure

BUILD_DIRS = \
	etc \
    graphics \
#    HippoDraw \
#    IDL \
#    ISAW \
    

OTHER_DIRS = \
    tests \
    examples \
    applications 

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all:
	BLD_ACTION="all" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

# version
# $Id: Make.mm 249 2007-09-30 05:55:20Z brandon $

# End of file
