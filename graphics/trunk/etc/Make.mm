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
PACKAGE =

#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
#
# export

EXPORT_ETC = \
    plot2d.odb           \
    qwtplot.odb          \
    matplot.odb          \
    gnuplot.odb          \
    __vault__.odb        

export:: export-etc

# version
# $Id: Make.mm,v 1.1 2005/06/06 23:32:03 jwliu Exp $

# End of file
