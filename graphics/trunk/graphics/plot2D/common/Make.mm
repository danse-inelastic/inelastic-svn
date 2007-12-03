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

PROJECT = demoplot/common
PACKAGE = common

#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
    __init__.py         \
    Qtinit.py           \
    Gtkinit.py          \


export:: export-python-modules

# version
# $Id: Make.mm,v 1.1 2005/05/24 21:23:15 jwliu Exp $

# End of file
