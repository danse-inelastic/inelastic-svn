# Olivier Delaire - 07/08

__doc__ = "Interface to a 3D mapper of scattering intensity onto a detector surface."

from pyre.components.Component import Component

class ScatteringIntensityMapper(Component):
    """Interface to an iso-surface plotter in 3D."""

    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        # inv stuff
        pass

    def __init__(self, field=None, energyvalues=None):
        self._field = field
        self._energyvalues = energyvalues

    def setField(self, field):
        self._field = field
        return

    def setEnergyValues(self, contourvalues):
        self._energyvalues = energyvalues
        return
        
    def render(self,energyvalues=None):
        """Plots the intersection of the energy isosurface at given energy(ies) 
        with the detector surface."""
        pass

    pass #endof class ScatteringIntensityMapper


class MlabScatteringIntensityContourMapper(ScatteringIntensityMapper):
    """Interface to a Matlab-based scattering intensity mapper."""

    def __init__(self, field=None, energyvalues=None, surface=None):
        self._grid = field
        self._evals = energyvalues
        self._surface = surface
        self._FaceColor='blue'
        self._EdgeColor='none'
        self._FaceAlpha=1.0
        self._lighting='gouraud'
        
        # do rest of initialization
        return

    def setGrid(self, grid):
        """Sets the grid."""
        if grid is None:
            raise ValueError, "Grid should not be None."
        self._grid = grid
        return

    def _getArray(self):
        """returns the data from the grid as an array."""
        return self._grid.GetArray()


    def render(self,energies=None):
        """Plots the scattering intensity on detector surface,
        at corresponding energy values."""
        # this needs to compute the detector surface in reciprocal space for the
        # given energy transfer values (energy transfer to the sample).
        # It will call the renderOnSurface() method.
        return

    def renderOnSurface(self, surface):
        """Renders the scattering intensity on given detector surface in reciprocal space."""

        import sam
        import numpy as np

        ########################
        ###
        ### this is to be implemented using the 'slice()' method of Matlab.
        ###
        ########################

        #we first pass the data into Matlab as an array:
        array = np.array(self._getArray())
        (dim0, dim1, dim2) = array.shape
        q0 = np.arange(1, dim0 + 1)
        q1 = np.arange(1, dim1 + 1)
        q2 = np.arange(1, dim2 + 1)
        # set up the ranges for the grid in reciprocal space
        # these are some dummy ranges for now ([-0.5,0.5])
        q0 = (q0 - (dim0+1)/2.0) / dim0 
        q1 = (q1 - (dim1+1)/2.0) / dim1
        q2 = (q2 - (dim2+1)/2.0) / dim2

        sam.put('dim0', [dim0])
        sam.put('dim1', [dim1])
        sam.put('dim2', [dim2])

        sam.put('q0', q0)
        sam.put('q1', q1)
        sam.put('q2', q2)
        sam.eval("[qxi, qyi, qzi] = meshgrid(q0, q1, q2);")

        # this causes a segmentation fault for an array of 20x20x20 doubles:
        #sam.putarray('array', array)
        # here is a temporary ugly(!) fix:
        array.shape=(dim0*dim1*dim2,)
        sam.put('array', array)
        sam.eval("scattarray = reshape(array', dim0, dim1, dim2)")
        # end of fix

        # we need to pass the detector surface into Matlab:
        sam.eval("[sxi,syi] = meshgrid(q0,q1);")
        sam.eval("szi = sqrt(1.0-(sxi.^2))-0.75 ;")

        # We use an M-file that gets called when we evaluate the name
        # of the corresponding function in Matlab via SAM
        sam.eval("MlabScatteringIntensitySurfaceSlicer(qxi,qyi,qzi,scattarray, sxi, syi,szi)")

        waitforentry=raw_input("Press any key.")
        sam.eval("close")
        return 0

    pass # End of class MlabScatteringIntensityContourMapper

