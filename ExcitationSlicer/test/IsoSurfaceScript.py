# simple test script for phonIsoSurfaceCalcor

from pyre.components.Component import Component
import ExcitationSlicer
from IsoSurfacePlotter import *
from phonIsoSurfaceCalcor import *

import UnitCell as UC
from Atom import Atom

path = ExcitationSlicer.__file__.strip('__init__.pyc')
    
cellvectors=[[3.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 3.0]]
uc = UC.UnitCell()
uc.setCellVectors(cellvectors)
uc.addAtom(Atom(Z=23), (0,0,0), '')
uc.addAtom(Atom(Z=23), (0.5,0.5,0.5), '')
print uc

myplotter = VTKIsoSurfacePlotter()    
calc = phonIsoSurfaceCalcor(unitcell=uc, tau=[1.0,0.0,0.0], plotter=myplotter)
calc.setDataFile(path+'data/phon_out.pkl')
calc.loadPhononData()
    
calc.plotEnergyIsoSurface(branchtoplot=3, energyvalues=[10,45])
