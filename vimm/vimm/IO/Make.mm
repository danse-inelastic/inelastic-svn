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
#

PROJECT = vimm
PACKAGE = IO

#--------------------------------------------------------------------------
#

PROJ_TIDY += *.log *.pyc
PROJ_CLEAN =

BUILD_DIRS = \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)


#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse

docs: 
	BLD_ACTION="docs" $(MM) recurse

#--------------------------------------------------------------------------
#

EXPORT_PYTHON_MODULES = \
	__init__.py \
	AbinitInput.py \
	AbinitOutput.py \
	BGF.py \
	CML.py \
	CTab.py \
	CXYZ.py \
	JaguarOutputReader.py \
	Mol.py \
	Molf.py \
	MPQCOutput.py \
	NWChemOutput.py \
	PDB.py \
	PickledStructure.py \
	POVOutput.py \
	ScatteringFunction.py \
	SeqquestHist.py \
	SeqquestInput.py \
	SeqquestOutput.py \
	Towhee.py \
	TowheeDatabaseFile.py \
	TowheeInput.py \
	TowheeInputFile.py \
	TowheeLammpFile.py \
	XYZ.py \
	
	

EXPORT_BINS = \



export:: export-binaries release-binaries export-package-python-modules 


# version
# $Id$

# End of file
