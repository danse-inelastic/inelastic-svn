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

PROJECT = sampleassembly
PACKAGE = geometers

BUILD_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS)


#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES =    \
	AbstractGeometer.py \
	AbstractGlobalGeometer.py \
	CoordinateSystem.py \
	Geometer.py \
	GlobalGeometer.py \
	LocationRegistry.py \
	PositionalInfo.py \
	__init__.py \
	_journal.py \
	mcstasRotations.py \
	rotateVector.py \
	units.py \
	utils.py \


export:: export-package-python-modules

# version
# $Id: Make.mm 1274 2007-10-31 20:23:22Z linjiao $

# End of file
