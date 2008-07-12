# Olivier Delaire 
#
# Things that need to be done:
#
# - clean up the implemetation of grid containers, and interface to plotters/slicers
# - implement the case of a non cubic phonon dataset
# - implement BZ and IBZ-restricted data
# - implement rendering of axes, reciprocal lattice vectors, BZ/IBZ
# - implement the intersection of the phonon data and scattering intensity by a cylindrical surface
#   and by a mode complex surface representing the ARCS detector surface
# - add a color scale "thermometer" to plots
# - allow user to change the color map ranges
# - interface to other rendering packages than ASE-VTK
#
##################################

import sys
import numpy as np
import cPickle
import types

from vtktools.Grid import *
import vtktools.VectorSpaces as VectorSpaces
from vtktools.Vector import Vector
import vtktools.vtkGrid3D as vtkgrid
import vtktools.vtkGrid3DwithProbe as vtkgridprobe

from IsoSurfacePlotter import VTKIsoSurfacePlotter
from IsoSurfacePlotter import VTKIsoSurfaceIntensityPlotter
from DataSlicer import VTKPlaneSlicer

# load VTK stuff
from vtk import *
# load VTK extensions
from vtk.libvtkCommonPython import *
from vtk.libvtkGraphicsPython import *


from pyre.components.Component import Component

__doc__ = """Provides facilities to plot phonon iso-energy surfaces and neutron scattering intensity,
from phonon energies on a grid."""

class phonIsoSurfaceCalcor(Component):
    """Provides facilities to plot phonon iso-energy surfaces from phonon energies on a grid."""

    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        unitcell = inv.str('Unit cell', default='')
        unitcell.meta['tip'] = 'string dscribing the unit cell'
        phonondatasource = inv.str('phonon data source file', default='phon_out.pkl')
        phonondatasource.meta['tip'] = 'Pickle file where the phonon grids are stored.'
        tau = inv.array('reciprocal lattice vector', default=[0.0, 0.0, 0.0])
        tau.meta['tip'] = 'reciprocal lattice vector to shift origin of data set by'
    pass # end of inventory


    def __init__(self, name='phonIsoSurfaceCalcor',
                 unitcell=None, phonondatasource=None, tau=None,
                 plotter=None, slicer=None,
                 Ei=50, Etransfer=20):
                 #branchtoplot=None, atomtoplot=None, energies=None):
        Component.__init__(self, name, facility='facility')
        self._uc = unitcell
        if phonondatasource is not None:
            self._phonondatasource = phonondatasource
        self._nkts = None
        self._tau = tau
        self._phonondata = None
        self._kptGrid = None
        self._energyGrid = None
        self._polarizationGrid = None
        self._intensityGrid = None
        try:
            self._numatoms = unitcell.getNumAtoms()
        except:
            raise ValueError, "Unit cell is not valid: invalid number of atoms."
        #self._branchtoplot = branchtoplot
        #self._atomtoplot = atomtoplot
        #self._energies = energies
        if plotter is None:
            plotter = VTKIsoSurfacePlotter()
        self._plotter = plotter

        if slicer is None:
            slicer = VTKPlaneSlicer()
        self._slicer = slicer

        # neutron scattering parameters:
        self.Ei = Ei
        self.Etransfer = Etransfer


    def setDataFile(self, filename):        
        """Sets the name of the data file to read phonon data from."""
        if type(filename) is not types.StringType:
            raise ValueError, "The filename must be a string."

        self._phonondatasource = filename
        return
        
    def loadPhononData(self):
        """Loads the phonon data.
        Loads the data from an output pickle file if phonondatasource is a string."""
        if type(self._phonondatasource) is types.StringType:
            try:
                file = open(self._phonondatasource, "r")
            except: print "Could not open Phon output pickle file: ", self._phonondatasource
            self._phonondata = cPickle.load(file)
            self._nkpt = len(self._phonondata)
            self._setPhonyKptGrid()

        else: pass
            # here: handle cases where data do not come from a pickle file
        return

    def setPlotter(self, plotter):
        """Sets the plotter used to render the isosurfaces in 3D."""
        self._plotter = plotter
        return

    def setSlicer(self, slicer):
        """Sets the slicer used to render the cut planes in 3D."""
        self._slicer = slicer
        return

    def _setKptGrid(self):
        """Sets the k-point grid from the loaded data."""
        # do the phony one for now:
        self._setPhonyKptGrid()
        return

    def _setPhonyKptGrid(self):
        """This is a phony helper function to build a grid of k-points.
        This really should come from the phonon data set passed to the calculator."""
        recipvectors = self._uc.getRecipVectors()
        space = VectorSpaces.VectorSpaceWithBasis(recipvectors.tolist())
        origin = Vector(np.array([0,0,0]))
        kptgrid = Grid(space=space, origin=origin)

        nkpt = self._nkpt
        print "Number of k-points:", nkpt
        
        # we assume that the kpt-grid is a Monkhorst-Pack
        # with as many points in each dimension
        kgriddims = (int(round(nkpt ** (1./3.),3)),
                     int(round(nkpt ** (1./3.),3)),
                     int(round(nkpt ** (1./3.),3)))
        print "k-grid dimensions = ", kgriddims
        kptarray = self._uc.getMonkhorstPackGrid(kgriddims)
        kptgrid.SetArray(kptarray)
        self._kptGrid = kptgrid
        return

    def setEnergyGridForBranch(self, branchindex, thz2tomev=True):
        """This is a helper function to build the grid of eigenvalues,
        corresponding to a certain branch index.
        thz2tomev is a flag:
        set it to True to convert the data from Thz^2 to meV (data from Phon),
        set it to False otherwise.
        """
        THztomeV = 4.1357
        recipvectors = self._uc.getRecipVectors()
        space = VectorSpaces.VectorSpaceWithBasis(recipvectors.tolist())
        origin = Vector(np.array([0,0,0]))
        egrid = Grid(space=space, origin=origin)
        phonlist = self._phonondata

        nkpt = len(phonlist)
        print "Number of k-points:", nkpt
        
        # we assume that the kpt-grid is a regular grid
        # with as many points in each dimension:
        kgriddims = (int(round(nkpt ** (1./3.),3)),
                     int(round(nkpt ** (1./3.),3)),
                     int(round(nkpt ** (1./3.),3)))
        print "k-grid dimensions = ", kgriddims
        
        nbranches = len(phonlist[0])
        print "Number of branches: ", nbranches
        print "Branch used for plotting: ", branchindex
        
        elist = []

        if thz2tomev:
            #convert from thz^2 to meV
            for kpt in range(nkpt):
                row=[]
                for nb in range(nbranches):
                    row.append(THztomeV*np.sqrt(np.abs(phonlist[kpt][nb][0])))
                elist.append(row)
        else:
            for kpt in range(nkpt):
                row=[]
                for nb in range(nbranches):
                    row.append(phonlist[kpt][nb][0])
                elist.append(row)

        print "Number of energies read: ", len(elist)
        earray = np.array(elist)
        
        if (branchindex < 0) or (branchindex > nbranches):
            raise ValueError, "index of branch to plot incompatible with input file."
        else:
            energy = np.array(earray[:, branchindex])
            energy.shape = kgriddims

        print "Energy array shape from loaded list of phonon energies:", energy.shape

        egrid.SetArray(energy)

        print "grid shape: ", egrid.GetShape()
        print "grid values range: ", egrid.GetValueRange()
        print "grid average value: ", egrid.GetAverage()

        self._energyGrid = egrid

        return

    def setPolarizationGridForBranchAtom(self, branchindex, atomindex):
        """This is a helper function to build the grid of polarization vectors,
        corresponding to a certain branch index and a certain atom index."""

        # If basis vectors are left unspecified,
        # the default cartesian basis is used to construct the vector space 
        #cellvectors = np.array([[1,0,0],[0,1,0],[0,0,1]])
        recipvectors = self._uc.getRecipVectors()
        space = VectorSpaces.VectorSpaceWithBasis(recipvectors.tolist())
        origin = Vector(np.array([0,0,0]))
        polgrid = Grid(space=space, origin=origin)
        
        phonlist = self._phonondata

        nkpt = len(phonlist)
        print "Number of k-points:", nkpt
        # we assume that the kpt-grid is a regular grid
        # with as many points in each dimension:
        kgriddims = (int(round(nkpt ** (1./3.),3)),
                     int(round(nkpt ** (1./3.),3)),
                     int(round(nkpt ** (1./3.),3)))
        print "k-grid dimensions = ", kgriddims
        
        nbranches = len(phonlist[0])
        print "Number of branches: ", nbranches
        print "Branch used for plotting: ", branchindex
        
        natoms = self._uc.getNumAtoms()

        pollist = []
        for kpt in range(nkpt):
            row=[]
            for nb in range(nbranches):
                col=[]
                for atom in range(natoms):
                    col.append(phonlist[kpt][nb][atom+1])
                row.append(col)
            pollist.append(row)
        print "Number of polarizations read: ", len(pollist)
        # make this into an np.array:
        polarray = np.array(pollist)

        # now get the subset of polarization vectors (complex) for one atom and one branch:
        polarization = np.array(polarray[:,branchindex,atomindex, :,:])
        dim0 = kgriddims[0] ; dim1 = kgriddims[1] ; dim2 = kgriddims[2]
        polarization.shape = (dim0, dim1, dim2, 3, 2)

        polgrid.SetArray(polarization)
        self._polarizationGrid = polgrid

        return

    def calcIntensityGrid(self, tau=None):
        """This is a helper function to calculate the scattering intensity,
        from the polarization vectors and the scattering vector Q = q + tau.
        It requires that the polarization vectors have been set,
        for a given atom and branchindex.
        The reciprocal lattice vector tau is a shift in reciprocal space."""
        #if tau is None:
        #    tauvec = self._tau
        #else:
        #    tauvec = tau
        if tau is not None:
            kshift = tau
        else:
            kshift = [0,0,0]

        cellvectors = self._uc.getCellVectors()
        space = VectorSpaces.VectorSpaceWithBasis(cellvectors.tolist())
        origin = Vector(np.array([0,0,0]))
        intgrid = Grid(space=space, origin=origin)

        kptarray = self._kptGrid.GetArray()
        polarray = self._polarizationGrid.GetArray()
        
        intensitylist = []

        nkpt = len(self._phonondata)
        # we assume that the kpt-grid is a cubic grid:
        kgriddims = (int(round(nkpt ** (1./3.),3)),
                     int(round(nkpt ** (1./3.),3)),
                     int(round(nkpt ** (1./3.),3)))

        intensity = np.zeros(kgriddims, dtype=float)

        for k0 in range(kgriddims[0]):
            for k1 in range(kgriddims[1]):
                for k2 in range(kgriddims[2]):
                    # for a non-monataomic crystal we only plot the orientation-dependent part of the
                    # scattering intensity for each atom and branch.
                    # The relative intensities for scattering from different atoms are not preserved.
                    # We need to compute the Debye-Waller factor for each atom to get this.
                    # Here we do the dot-product with the "full" imaginary polarization vector,
                    # since the real polarization vector is obtained by a unitary transfo, wich
                    # does not change the value of | q_vec . e_vec |^2
                    # intensitylist.append(np.dot(polarization[kpt][:,0], qvec)**2)
                    dot = np.dot(( kshift + kptarray[k0][k1][k2]), polarray[k0][k1][k2])
                    z = dot[0] + dot[1] * 1j
                    intensity[k0][k1][k2] = abs(z)**2

        intgrid.SetArray(intensity)
        self._intensityGrid = intgrid

        return
    

    def plotEnergyIsoSurface(self, branchtoplot, energyvalues):
        """Plots iso-energy surface from the output of a phon computation.
        The data (list) must have the same format as created by the phon results parser.
        It assumes (for now) that the phonon energies were computed on a cubic k-point grid."""

        self.setEnergyGridForBranch(branchtoplot)
        
        self._plotter.setGrid(self._energyGrid)

        print "Plotter type:"
        print self._plotter.__class__
        print "Plotter grid shape: ", self._plotter._grid.GetShape()
        
        isosurf = self._plotter.plot(contours=energyvalues)
        input = raw_input("Press enter to close plot window.")
        isosurf.DestroyWindow()

        return #end of plotEnergyIsoSurface()


    def plotIsoSurfaceIntensity(self, branchtoplot, atomtoplot, energyvalues, tau=None):
        """Plots iso-energy surface from the output of a phon computation.
        Also maps the scattering intensity onto the isosurface. 
        The data (list) must have the same format as created by the phon results parser.
        It assumes (for now) that the phonon energies were computed on a cubic k-point grid."""

        self.setEnergyGridForBranch(branchtoplot)
        self.setPolarizationGridForBranchAtom(branchtoplot,atomtoplot)
        self.calcIntensityGrid(tau=tau)
       
        self._plotter.setGrid(self._energyGrid)

        print "Plotter type:"
        print self._plotter.__class__
        print "Plotter grid shape: ", self._plotter._grid.GetShape()


        # set the intensity array for the plotter
        # !!! the interface should be homogenized between the plotting of isosurface only
        # and the plotting of isosurface with intensity mapping
        # ie: the intensity needs to be an array for the ASE vtkGrid3DProbeIsoSurface2
        # but the energy is a grid type...
        # maybe the ASE grids should be built inside the ASE/VTK isosurface plotter wrappers?
        self._plotter.setProbe(self._intensityGrid.GetGridValues())
        
        isosurfint = self._plotter.plot(contours=energyvalues)
        input = raw_input("Press enter to close plot window.")
        isosurfint.DestroyWindow()


        #from ASE.Visualization.VTK.vtkDataFromObject import vtkStructuredGridsFromGrid3DProbeArray
        # here we set up an instance of vtkStructuredGridsFromGrid3DProbeArray,
        # which is really a converter from regular Grid instances for the energy
        # eigenvalues and polarization intensity to vtkStructuredGrid instances,
        # required for the visualization
        #structgrids = vtkStructuredGridsFromGrid3DProbeArray(grid3D=egrid, probearray=intensity)

        # here we retrieve the structured grids,
        # both for the energy eigenvalues and the polarization intensities
        #estructgrid = structgrids.GetvtkStructuredGrid()
        #intstructgrid = structgrids.GetvtkStructuredGridProbe()

        #isosurfint = vtkgridprobe.vtkGrid3DProbeIsoSurface2(contourvalues=energyvalues,
        #                                                        vtkgrid=estructgrid,
        #                                                        vtkprobe=intstructgrid)
        
        return #end of plotIsoSurfaceIntensity()

    def plotEnergyPlaneCut(self, branchtoplot, origin=None, normal=None):
        """Plots a cut of the energy grid on a plane, specified by an origin and a normal."""

        self.setEnergyGridForBranch(branchtoplot)
 
        self._slicer.setGrid(self._energyGrid)

        print "Slicer type:"
        print self._slicer.__class__
        print "Slicer grid shape: ", self._slicer._grid.GetShape()
        
        planecut = self._slicer.plot()
        input = raw_input("Press enter to close plot window.")
        planecut.DestroyWindow()

        return #end of plotPlaneCut()

    def plotIntensityPlaneCut(self, branchtoplot=0, atomtoplot=0,
                              tau=None, origin=None, normal=None):
        """Plots a cut of the scattering intensity on a plane, specified by an origin and a normal."""

        self.setPolarizationGridForBranchAtom(branchtoplot,atomtoplot)
        self.calcIntensityGrid(tau=tau)

        print "Slicer type:"
        print self._slicer.__class__
        self._slicer.setGrid(self._intensityGrid)
        print "Slicer grid shape: ", self._slicer._grid.GetShape()
        
        if (origin is not None) and (normal is not None):
            self._slicer.setCutPlane(origin, normal)

        planecut = self._slicer.plot()
        input = raw_input("Press enter to close plot window.")
        planecut.DestroyWindow()
        return

    def plotIsoSufaceAndDetector(self, branchtoplot, energyvalues, detectorGeometry='spherical'):
        """Show the detector surface mapped into the reciprocal space of the crystal."""
        if detectorGeometry is not 'spherical':
            raise NotImplementedError

        self.setEnergyGridForBranch(branchtoplot)
        self._plotter.setGrid(self._energyGrid)

        print "Plotter type:"
        print self._plotter.__class__
        print "Plotter grid shape: ", self._plotter._grid.GetShape()
        
        plot = self._plotter.plot(contours=energyvalues)
        window = plot.GetWindow()
        renderer = window.GetRenderer()
        detectorActor = self._getVtkDetectorActor()
        renderer.AddActor(detectorActor)
        input = raw_input("Press enter to close plot window.")
        plot.DestroyWindow()

        return #end of plotIsoSurfaceAndDetector()

    def _getVtkDetectorActor(self):
        "returns a VTK Actor for the detector surface."""
        from SphereDetectorSurfaceMapper import SphereDetectorSurfaceMapper
        print "Ei: ", self.Ei
        print "Etransfer: ", self.Etransfer
        sphDetector = SphereDetectorSurfaceMapper(Ei=self.Ei, Etransfer=self.Etransfer)
        sphMapper = sphDetector.getVtkMapper()
        detActor = vtkActor()
        detActor.SetMapper(sphMapper)
        return detActor
        
    pass # end of class phonIsoSurfaceCalcor()
        

# end of file

