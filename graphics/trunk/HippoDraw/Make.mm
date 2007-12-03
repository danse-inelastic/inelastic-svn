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

PROJECT = graphics/HippoDraw
PACKAGE = HippoDraw
#RECURSE_DIRS = 

#--------------------------------------------------------------------------
#

all: export
#	BLD_ACTION="export" $(MM) recurse

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
    __init__.py      \
    HippoDraw_Plot2D.py \

export:: export-python-modules

# version
# $Id: Make.mm 227 2007-09-25 16:33:11Z brandon $

# End of file
