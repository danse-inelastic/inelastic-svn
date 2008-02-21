import sys
import os
import numpy as np
import pickle
import types
import string

from pyre.components.Component import Component
import ExcitationSlicer
from ExcitationSlicer.IsoSurfacePlotter import *
from ExcitationSlicer.phonIsoSurfaceCalcor import *


__doc__ = """Tests for the isosurface calculator module."""

def test1():
    import crystal.UnitCell as UC
    from crystal.Atom import Atom

    print "This test should plot some phonon isosurfaces."
    path = ExcitationSlicer.__file__.strip('__init__.pyc')
    
    cellvectors=[[3.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 3.0]]
    #uc = UC.create_unitcell(cellvectors, [Atom(Z=23), Atom(Z=23)], [(0,0,0), (0.5, 0.5, 0.5)])
    uc = UC.UnitCell()
    uc.setCellVectors(cellvectors)
    uc.addAtom(Atom(Z=23), (0,0,0), '')
    uc.addAtom(Atom(Z=23), (0.5,0.5,0.5), '')
    print uc

    myplotter = VTKIsoSurfacePlotter()    
    calc = phonIsoSurfaceCalcor(unitcell=uc, tau=[1.0,0.0,0.0], plotter=myplotter)
    calc.setDataFile(path+'data/phon_out.pkl')
    calc.loadPhononData()

    print "Plot phonon eigen-energy isosurfaces."
    calc.plotEnergyIsoSurface(branchtoplot=3, energyvalues=[10,45])
    #wait for input
    input = raw_input("Finished test1.")

    return

    
def test2():
    import crystal.UnitCell as UC
    from crystal.Atom import Atom

    path = ExcitationSlicer.__file__.strip('__init__.pyc')
    cellvectors=[[3.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 3.0]]
    #uc = UC.create_unitcell(cellvectors, [Atom(Z=23), Atom(Z=23)], [(0,0,0), (0.5, 0.5, 0.5)])
    uc = UC.UnitCell()
    uc.setCellVectors(cellvectors)
    uc.addAtom(Atom(Z=23), (0,0,0), '')
    uc.addAtom(Atom(Z=23), (0.5,0.5,0.5), '')

    #Now we want to plot the isosurface with intensity mapped on it:
    myplotter2 = VTKIsoSurfaceIntensityPlotter()

    calc2 = phonIsoSurfaceCalcor(unitcell=uc, tau=[1.0,0.0,0.0], plotter=myplotter2)
    calc2.setDataFile(path+'data/phon_out.pkl')
    calc2.loadPhononData()

    calc2.plotIsoSurfaceIntensity(branchtoplot=3, atomtoplot=0, energyvalues=[30])
    #wait for input
    input = raw_input("Finished test2.")

    return

def test3():
    import crystal.UnitCell as UC
    from crystal.Atom import Atom

    path = ExcitationSlicer.__file__.strip('__init__.pyc')
    cellvectors=[[3.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 3.0]]
    uc = UC.UnitCell()
    uc.setCellVectors(cellvectors)
    uc.addAtom(Atom(Z=23), (0,0,0), '')
    uc.addAtom(Atom(Z=23), (0.5,0.5,0.5), '')
    myslicer = VTKPlaneSlicer()
    calc = phonIsoSurfaceCalcor(unitcell=uc, tau=[1.0,0.0,0.0], slicer=myslicer)
    calc.setDataFile(path+'data/phon_out.pkl')
    calc.loadPhononData()
    calc.plotIntensityPlaneCut(branchtoplot=3,atomtoplot=0)
    input = raw_input("Finished test3.")
    return

def test4():
    import crystal.UnitCell as UC
    from crystal.Atom import Atom

    path = ExcitationSlicer.__file__.strip('__init__.pyc')
    cellvectors=[[3.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 3.0]]
    uc = UC.UnitCell()
    uc.setCellVectors(cellvectors)
    uc.addAtom(Atom(Z=23), (0,0,0), '')
    uc.addAtom(Atom(Z=23), (0.5,0.5,0.5), '')
    myslicer = VTKPlaneSlicer()
    calc = phonIsoSurfaceCalcor(unitcell=uc, tau=[1.0,0.0,0.0], slicer=myslicer)
    calc.setDataFile(path+'data/phon_out.pkl')
    calc.loadPhononData()
    scatteringVector=np.array([1.,0.,0.])
    calc.plotIntensityPlaneCut(branchtoplot=3, atomtoplot=0, tau=scatteringVector)
    input = raw_input("Finished test4.")
    return

def test5():
    import crystal.UnitCell as UC
    from crystal.Atom import Atom

    print "This test plots a phonon isosurface with Matlab."
    path = ExcitationSlicer.__file__.strip('__init__.pyc')
    
    cellvectors=[[3.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 3.0]]
    #uc = UC.create_unitcell(cellvectors, [Atom(Z=23), Atom(Z=23)], [(0,0,0), (0.5, 0.5, 0.5)])
    uc = UC.UnitCell()
    uc.setCellVectors(cellvectors)
    uc.addAtom(Atom(Z=23), (0,0,0), '')
    uc.addAtom(Atom(Z=23), (0.5,0.5,0.5), '')
    print uc

    myplotter = MlabIsoSurfacePlotter()
    calc = phonIsoSurfaceCalcor(unitcell=uc, tau=[1.0,0.0,0.0], plotter=myplotter)
    calc.setDataFile(path+'data/phon_out.pkl')
    calc.loadPhononData()

    print "Plot phonon eigen-energy isosurfaces."
    calc.plotEnergyIsoSurface(branchtoplot=3, energyvalues=[45])
    #wait for input
    input = raw_input("Finished test5.")

    return



if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    test5()

#end of file
