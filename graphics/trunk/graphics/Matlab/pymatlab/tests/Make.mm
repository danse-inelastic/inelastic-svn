# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

PROJECT = graphics/Matlab/pymatlab
PACKAGE = tests

PROJ_CLEAN += $(PROJ_CPPTESTS)

PROJ_PYTESTS = sam_evaltest.py sam_shapetest.py sam_whotest.py \
               sam_gettest.py samtest.py
PROJ_CPPTESTS = 
PROJ_TESTS = $(PROJ_PYTESTS) # $(PROJ_CPPTESTS)
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

# version
# $Id: Make.mm 227 2007-09-25 16:33:11Z brandon $

# End of file
