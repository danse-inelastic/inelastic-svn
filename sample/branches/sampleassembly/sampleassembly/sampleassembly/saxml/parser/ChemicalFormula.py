#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin   
#                      California Institute of Technology
#                      (C)   2007    All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.xml.Node import Node
from AbstractNode import debug
import urllib


class ChemicalFormula(Node):

    tag = 'ChemicalFormula'

    def __init__(self, document, attributes):
        Node.__init__(self, document)
        return


    def notify(self, parent):
        return parent.onChemicalFormula( self.formula )


    def content(self, content):
        debug.log( "content=%s" % content )
        content = content.strip()
        if len(content)==0: return
        content = urllib.unquote(content).strip()
        self.formula = content
        self.locator = self.document.locator
        return

    pass # end of ChemicalFormula



# version
__id__ = "$Id$"

# End of file 
