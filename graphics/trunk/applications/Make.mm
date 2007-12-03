# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Michael M. McKerns
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = graphics
PACKAGE = graphics

#--------------------------------------------------------------------------
#

all: export
#	BLD_ACTION="all" $(MM) recurse

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
    __init__.py \
    PyIDL.py \
    Matlab.py \
    matplot.py \
    PyGrace.py \
    
EXPORT_BINS = \
	plot2DApp.py \
	ApiTester.py \
    

export:: export-binaries release-binaries #export-python-modules 

# version
# $Id: Make.mm 227 2007-09-25 16:33:11Z brandon $

# End of file
