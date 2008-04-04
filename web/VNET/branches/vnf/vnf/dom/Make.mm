# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = vnf
PACKAGE = dom



BUILD_DIRS = \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	__init__.py \
	Block.py \
	Crystal.py \
	IDFPhononDispersion.py \
	Instrument.py \
	Component.py \
	IQEMonitor.py \
	Job.py \
	MonochromaticSource.py \
	Object.py \
	VirtualObject.py \
	PhononDispersion.py \
	PolyXtalScatterer.py \
	PolyXtalCoherentPhononScatteringKernel.py \
	ReferenceSet.py \
	SampleAssembly.py \
	Scatterer.py \
	ScatteringKernel.py \
	Server.py \
	Shape.py \
	Table.py \
	User.py \



export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
