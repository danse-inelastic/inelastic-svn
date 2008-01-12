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
PACKAGE = elements

#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	AbstractAttributeContainer.py \
	Attribute.py \
	AttributeContainer.py \
	Crystal.py \
	Element.py \
	ElementContainer.py \
	IdGenerator.py \
	Phase.py \
	PowderSample.py \
	SampleAssembly.py \
	Scatterer.py \
	__init__.py \
	_journal.py \
	elementTypes.py \
	phases.py \
	units.py \


export:: export-package-python-modules

# version
# $Id$

# End of file
