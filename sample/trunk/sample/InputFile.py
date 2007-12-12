#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from pyre.components.Component import Component
from pyregui.inventory.extensions.InputFile import InputFile
from os import linesep

class InputFile(Component):
    '''On the first line input the number of atoms. On the second line input the three lattice vectors 
sequentially: x1 x2 x3 y1 y2 y3 z1 z2 z3.  On the third, fourth, etc. lines input the atoms: Zn 0.0 0.5'''
    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        inputFile = InputFile( 'inputFile', default = "" )
        inputFile.meta['tip'] = 'xyz file containing unit cell and atom positions'
        
#        fireballBasisSetPath = inv.str('Fireball Basis Set Path', default = None)
#        fireballBasisSetPath.meta['tip'] = 'directory containing Fdata'

    def __init__(self, name='InputFile'):
        Component.__init__(self, name, facility='facility')
        self.i=self.inventory

    def gulpFormatUcNAtoms(self,runType):
        try:
            f=file(self.i.inputFile)
        except:
            print "cannot open xyz file"
            raise
        lines=f.readlines()
        ax,ay,az,bx,by,bz,cx,cy,cz=lines[1].split()
        text='vectors'+linesep + ax+' '+ay+' '+az + linesep + bx+' '+by+' '+bz+linesep + cx+' '+cy+' '+cz+linesep
        if runType.runTypeIdentifier=='optimize':
            if runType.i.optimizeCell:
                #remove the last linesep and add the optimize flags
                text=text[:-1]+' 1 1 1 1 1 1'+linesep
        text+='cartesian'+linesep
        for line in lines[2:]:
            text+=line
        text+=linesep
        return text

    def _defaults(self):
        Component._defaults(self)

    def _configure(self):
        Component._configure(self)

    def _init(self):
        Component._init(self)


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Sun Jun 24 21:57:30 2007

# End of file 