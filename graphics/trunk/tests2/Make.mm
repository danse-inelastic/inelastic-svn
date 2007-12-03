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
PACKAGE = tests

TEST_DIRS = \
    grace \
    IDL \
    Matplotlib \


RECURSE_DIRS = $(TEST_DIRS)

#--------------------------------------------------------------------------
#

all:
	BLD_ACTION="all" $(MM) recurse

test:
	./alltest.py

distclean::
	BLD_ACTION="distclean" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

# version
# $Id: Make.mm 74 2005-04-08 19:18:52Z mmckerns $

# End of file
