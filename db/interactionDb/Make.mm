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

PROJECT = interaction
PACKAGE = interactionDb


#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
#
# export

CP_RF = cp -rf
DEST_DIR = interactionDb
EXPORT_DATADIRS = \
	oneAtom \
	twoAtom \
	threeAtom \
	fourAtom \

EXPORT_SHAREDIR = $(EXPORT_ROOT)/share

RESOURCE_DEST =  $(EXPORT_SHAREDIR)/$(PROJECT)/$(DEST_DIR)

export:: export-package-data

export-package-data:: $(EXPORT_DATADIRS)
	mkdir -p $(RESOURCE_DEST); \
	for x in $(EXPORT_DATADIRS); do { \
            if [ -d $$x ]; then { \
	        $(CP_RF) $$x $(RESOURCE_DEST); \
            } fi; \
        } done


# version
# $Id$

# End of file
