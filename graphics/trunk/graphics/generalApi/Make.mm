# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = graphics
PACKAGE = graphics


BUILD_DIRS = \
	
OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
    __init__.py \
    auiTest.py \
    AxesEditor.py \
    AxesEditorTable.py \
    common.py \
    EfficiencyTable.py \
    errorcheck.py \
    examples_vtk.py \
    examples.py \
    gnuplot_.py \
    GnuplotWrap.py \
    langTest.py \
    MainPlotWindow.py \
    matplotlib_.py \
    MatplotlibPropertyModel.py \
    MatplotlibWrap.py \
    misc.py \
    miscUp.py \
    movie.py \
    mplqtplotter.py \
    numpytools.py \
    Options.py \
    PlotBrowser.py \
    PlotItemRegistry.py \
    PropertyEditor.py \
    MatplotlibPropertyTable.py \
    run.py \
    SettingsPanel.py \
    SizeReportCtrl.py \
    StringFunction.py \
    utils.py \
    vtk_.py \
    VtkPropertyModel.py \
    vtkTest.py \
    VtkWrap.py \


export:: export-python-modules

# version
# $Id: Make.mm 260 2007-10-17 04:10:41Z brandon $

# End of file
