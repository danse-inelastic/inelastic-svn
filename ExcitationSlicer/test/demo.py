import crystal.UnitCell as UC
from crystal.Atom import *
from IsoSurfacePlotter import *
from DataSlicer import *
import phonIsoSurfaceCalcor as isocalc
from phonIsoSurfaceCalcor import *
#import sam   # <<< not installed on upgrayedd...

cellvectors=[[3.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 3.0]]
uc = UC.UnitCell()
uc.setCellVectors(cellvectors)
uc.addAtom(Atom(Z=23), (0,0,0), '')
uc.addAtom(Atom(Z=23), (0.5,0.5,0.5), '')
print uc

#myplotter = MlabIsoSurfacePlotter()    
myplotter = VTKIsoSurfacePlotter()
myslicer = VTKPlaneSlicer()

#calc = phonIsoSurfaceCalcor(unitcell=uc, tau=[1.0,0.0,0.0], plotter=myplotter)
calc = phonIsoSurfaceCalcor(unitcell=uc, tau=[0.0,0.0,0.0], plotter=myplotter, slicer=myslicer)
calc.setDataFile('phon_out.pkl')
calc.loadPhononData()

#calc.setEnergyGridForBranch(branchindex=3)
#calc.setPolarizationGridForBranchAtom(branchindex=3, atomindex=0)
#calc.calcIntensityGrid()


# Plot energy iso-surface for a particular "branch" of phonon dataset:
calc.plotEnergyIsoSurface(branchtoplot=3, energyvalues=[30.0])
calc.plotEnergyIsoSurface(branchtoplot=3, energyvalues=[10.0, 20.0, 30.0, 40.0])

# Plot the scattering intensity for that branch on a plane detector surface:
calc.plotIntensityPlaneCut(branchtoplot=3, atomtoplot=0)

# Map the phonon scattering intensity onto an iso-surface of given energy:
newplotter = VTKIsoSurfaceIntensityPlotter()
calc.setPlotter(newplotter)
calc.plotIsoSurfaceIntensity(branchtoplot=3, atomtoplot=0, energyvalues=[35.0])

calc.plotIsoSurfaceIntensity(branchtoplot=3, atomtoplot=0, energyvalues=[10.0, 40.0])


