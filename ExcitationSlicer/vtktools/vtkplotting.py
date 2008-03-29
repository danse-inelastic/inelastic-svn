__docformat__ = 'reStructuredText'
"""  VTK 3D plotting 

``Methods`` for 3D grid plotting.
All functions takes ListOfAtoms as input, possible with a attached 
calculator (for the wave function and density plot).
All methods are based on the VTKAvatar modules written by
Mikkel Bollinger. 

Method implemented: 

``VTKPlotWaveFunction``: 
VTKPlotWaveFunction uses the method ``GetWaveFunction`` from a general 
DFT Calculator. 

``VTKPlotAtoms``:
A general ASE ListOfAtoms can be plotted. 

"""
import Numeric as num
from Avatars.vtkListOfAtoms import vtkListOfAtoms
#from ElectronicState import ElectronicState
#from ASE.Visualization.VTK.Avatars.vtkGrid3DwithProbe import vtkEigenState
#from ASE.Visualization.VTK.Avatars.vtkGrid3DwithProbe import vtkSTM
#from Avatars.vtkGrid3D import vtkNumericArray

## def VTKPlotWaveFunction(atoms,band=0,kpointnumber=0,spin=0,contourvalues=None,
##                         showatoms=None,parent=None,**keywords):
##     """ A listofatoms object ``atoms`` is given, together with ``band``,
##     ``kpointnumber`` and ``spin``. This method uses the ``GetWaveFunction``
##     method of the Calculator attached to ``atoms``.
##     It is assumed that it is the Bloch function that is returned by
##     the calc.GetWaveFunction. This method plots the wavefunction, ie.
##     the Bloch function multiplied by the phase-factor 'exp(ikx)' """

##     calc = atoms.GetCalculator()
##     unitcell = atoms.GetUnitCell()
##     blochfunction = calc.GetWaveFunctionArray(band,kpt=kpointnumber,spin=spin)
##     kpoint = calc.GetIBZKPoints()[kpointnumber]

##     electronicstate = ElectronicState(band=band,kpointnumber=kpointnumber,spin=spin,
##                                       blochfunction=blochfunction,kpoint=kpoint, 
##                                       unitcell=unitcell) 

##     # Building keyword dict:
##     keywords['contourvalues']=contourvalues
##     keywords['parent']=parent
##     # return electronicstate.GetVTKAvatar(keywords)

##     plot = apply(vtkEigenState,[electronicstate],keywords) 

##     if showatoms is not None:
##         atomplot = VTKPlotAtoms(atoms,parent=plot)
##         plot.Update()

##     return plot

def VTKPlotAtoms(atoms,parent=None,**keywords): 
    """ A listofatoms object ``atoms`` is plottet using VTK
    """
    keywords['parent'] = parent
    return apply(vtkListOfAtoms,[atoms],keywords)

## def VTKPlotArray(array,unitcell,parent=None,**keywords):
##     """ A Numerical array ``array`` is plottet using VTK
##     """
##     keywords['parent'] = parent
##     return apply(vtkNumericArray,[array,unitcell],keywords)

## def VTKPlotDensity(atoms,spin=None,showatoms=None,parent=None,**keywords):
##     """ The density is plottet using VTK.
##     For a spin-polarized calculation: 
##     If the ``spin`` argument is given the density for the specified
##     spin (0 or 1) is returned. If ``spin```is None the sum is returned. 
    
##     """

##     calc = atoms.GetCalculator()

##     if spin is not None: 
## 	if calc.GetSpinPolarized()==False: 
## 	    print 'Non spin-polarized calculation: spin argument must be None'
##             return

##     unitcell = atoms.GetUnitCell()


##     if calc.GetSpinPolarized()==True:   
##         if spin is not None:
##             density = calc.GetDensityArray()[spin]
##         else:
##             density = calc.GetDensityArray()[0] + calc.GetDensityArray()[1]
##     else:
##         density =  calc.GetDensityArray()
            
##     keywords['parent'] = parent

##     plot = apply(vtkNumericArray,[density,unitcell],keywords)

##     if showatoms is not None:
##         atomplot = VTKPlotAtoms(atoms,parent=plot)
##         plot.Update()
        
##     return plot



## def VTKPlotElectronicState(state, parent=None,contourvalues=None,**keywords):
##     """ A electronic state object ``state`` is plottet using VTK. 
##     This method plots the wave function, ie.
##     the Bloch function multiplied by the phase-factor 'exp(ikx)' """

##     unitcell = state.GetUnitCell()
##     blochfunction = state.GetWaveFunctionOnGrid()
##     kpoint = state.GetKPoint()

##     electronicstate = ElectronicState(band=0,kpointnumber=0,spin=0,
##                                       blochfunction=blochfunction,kpoint=kpoint,
##                                       unitcell=unitcell)

##     # Building keyword dict:
##     keywords['contourvalues']=contourvalues
##     keywords['parent']=parent
##     # return electronicstate.GetVTKAvatar(keywords)
##     return apply(vtkEigenState,[electronicstate],keywords)


## def VTKPlotSTM(stmtool,parent=None,**keywords): 
##     """ A STMTool object is plottet using VTK
##     """
##     keywords['parent']=parent
##     return apply(vtkSTM,[stmtool],keywords)
    
