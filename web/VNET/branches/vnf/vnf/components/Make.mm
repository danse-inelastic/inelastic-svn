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
PACKAGE = components


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	__init__.py \
	Actor.py \
	Clerk.py \
	CSAccessor.py \
	DBObjectForm.py \
	Form.py \
	FormActor.py \
	Geometer.py \
	Greeter.py \
	Instrument.py \
	InstrumentSimulationAppBuilder.py \
	Job.py \
	McstasSampleBuilder.py \
	McvineSampleAssemblyBuilder.py \
	McvineScattererXMLBuilder.py \
	NeutronExperiment.py \
	NeutronExperimentSimulationRunBuilder.py \
	PyHtmlTable.py \
	Run.py \
	SampleAssembly.py \
	SampleAssemblyXMLBuilder.py \
	SamplePreparation.py \
	Sample.py \
	Scheduler.py \
	Server.py \
	Scatterer.py \
	ScatteringKernel.py \
	ScatteringKernelInput.py \
	Shape.py \
	Scribe.py \
	SSHer.py \
	SupportingCalcs.py \
	TreeViewCreator.py \
	inventorylist.py \
	spawn.py \
	twodarr.py \
	wording.py \


export:: export-package-python-modules

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
