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

PROJECT = graphics
PACKAGE = plot2D

BUILD_DIRS = \
    qwt \
    common \

OTHER_DIRS = 

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
    __init__.py         \
    Matplotlib.py          \
    Qwtplot.py          \
    Gnuplot.py          \
    Plot2d.py           \
    Curve.py           


export:: export-package-python-modules

# version
# $Id: Make.mm,v 1.2 2005/05/24 21:22:31 jwliu Exp $

# End of file
