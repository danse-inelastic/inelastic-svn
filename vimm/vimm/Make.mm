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

PROJECT = vimm

#--------------------------------------------------------------------------
#

BUILD_DIRS = \
	engines \
	IO \
	
OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
    __init__.py \
    AlkaneBuilder.py \
    Animation.py \
    Atom.py \
    Bins.py \
    Bond.py \
    BondAdjustor.py \
    Camera.py \
    Canvas.py \
    Cartesians.py \
    Cell.py \
    Constants.py \
    CoordEditor.py \
    CrystalBuilder.py \
    Element.py \
    FileIO.py \
    FortranIO.py \
    Frame.py \
    FrameSep.py \
    Gaussian.py \
    Geometry.py \
    MarchingCubes.py \
    Material.py \
    Measurements.py \
    NanoBuilder.py \
    NumWrap.py \
    OrbitalViewer.py \
    PlotCanvas.py \
    POVRay.py \
    Renderers.py \
    Shapes.py \
    Sketcher.py \
    Utilities.py \
    vimmLib.py \
    ZBuilder.py \
    ZMatrix.py \
    


export:: export-package-python-modules

# version
# $Id$

# End of file
