# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               T. M. Kelley
#                        (C) 1998-2003 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = dsm


BUILD_DIRS = \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	Chain.py \
	Chains.py \
	Composite.py \
	Connectable.py \
	DataStreamModel.py \
	Node.py \
	Passer.py \
	Runner.py \
	_convenient_functions.py \
	__init__.py \



export:: export-python-modules
	BLD_ACTION="export" $(MM) recurse



# version
# $Id: Make.mm 1404 2007-08-29 15:43:42Z linjiao $

# End of file
