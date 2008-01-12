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

PROJECT = sampleassembly
PACKAGE = sampleassembly

BUILD_DIRS = \
	crystal \
	elements \
	geometers \
	predefined \
	saxml \

RECURSE_DIRS = $(BUILD_DIRS)


#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	units.py \
	__init__.py \


export:: export-python-modules
	BLD_ACTION="export" $(MM) recurse


# version
# $Id$

# End of file
