# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Michael M. McKerns
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = graphics
PACKAGE = tests/grace

PROJ_CLEAN += $(PROJ_CPPTESTS)

PROJ_PYTESTS = gracetest.py
PROJ_CPPTESTS =
PROJ_TESTS = $(PROJ_PYTESTS) $(PROJ_CPPTESTS)
PROJ_LIBRARIES = -L$(BLD_LIBDIR)


#--------------------------------------------------------------------------
#

all: $(PROJ_TESTS)

test:
	for test in $(PROJ_TESTS) ; do $${test}; done

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#

# version
# $Id: Make.mm 71 2005-04-07 23:07:02Z mmckerns $

# End of file
