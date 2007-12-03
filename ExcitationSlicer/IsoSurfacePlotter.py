# Olivier Delaire 

__doc__ = "Interface to 3D iso-surface plotter."

from pyre.components.Component import Component

class IsoSurfacePlotter(Component):
    """Interface to an iso-surface plotter in 3D."""

    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        # inv stuff
        pass

    def __init__(self, field=None, contourvalues=None):
        self._field = field
        self._contourvalues = contourvalues

    def setField(self, field):
        self._field = field
        return

    def setContourValues(self, contourvalues):
        self._contourvalues = contourvalues
        return
        
    def plot(self,contourvalues=None):
        """Plots the isosurfaces for the field data, at corresponding contour values."""
        pass

    pass #endof class IsoSurfacePlotter


class VTKIsoSurfacePlotter(IsoSurfacePlotter):
    """Interface to a VTK-based iso-surface plotter in 3D (based on Atomic Simulation Environment)."""

    import vtktools.vtkGrid3D as vtkgrid

    def __init__(self, field=None, contourvalues=None):
        self._grid = field
        self._contvals = contourvalues
        # do rest of initialization
        return

    def setGrid(self, grid):
        """Sets the grid that's used in the ASE/VTK vtkScalarGrid3D isosurface renderer."""
        if grid is None:
            raise ValueError, "Grid should not be None."
        self._grid = grid
        return

    def plot(self,contours=None):
        """Plots the isosurfaces for the field data, at corresponding contour values."""
        #if contourvalues is not None:
        #    contvals = contourvalues
        #else:
        #    contvals = self._contvals

        gridtoplot = self._grid
        isosurf = VTKIsoSurfacePlotter.vtkgrid.vtkScalarGrid3D(gridtoplot, contourvalues=contours)
        return isosurf

    pass # End of class VTKIsoSurfacePlotter



class VTKIsoSurfaceIntensityPlotter(IsoSurfacePlotter):
    """Interface to a VTK-based isosurface plotter / intensity mapper in 3D (based on Atomic Simulation Environment).
    This is using the ASE vtkGrid3DProbeIsoSurface2 code."""

    import vtktools.vtkGrid3DwithProbe as vtkgrid3dprobe
    from  vtktools.vtkDataFromObject import vtkStructuredGridsFromGrid3DProbeArray

    def __init__(self, field=None, intensity=None, contourvalues=None):
        self._grid = field
        self._probe = intensity
        self._contvals = contourvalues
        # do rest of initialization if any
        return

    def setGrid(self, grid):
        """Sets the grid that's used in the ASE/VTK vtkScalarGrid3D isosurface renderer."""
        if grid is None:
            raise ValueError, "Grid for isosurface rendering should not be None."
        self._grid = grid
        return

    def setProbe(self, intensity):
        """Sets the probe that's used in the ASE/VTK vtkScalarGrid3DwithProbe renderer."""
        if intensity is None:
            raise ValueError, "Intensity data for intensity mapping should not be None."
        self._probe = intensity
        return

    def plot(self,contours=None):
        """Plots the isosurfaces for the field data, with mapped intensity, at corresponding contour values."""
        if contours is not None:
            contvals = contours
        else:
            contvals = self._contvals

        gridtoplot = self._grid
        intensity = self._probe

        # here we set up an instance of vtkStructuredGridsFromGrid3DProbeArray,
        # which is really a converter from regular Grid instances for the energy
        # eigenvalues and polarization intensity to vtkStructuredGrid instances,
        # required for the visualization
        structgrids = VTKIsoSurfaceIntensityPlotter.vtkStructuredGridsFromGrid3DProbeArray(grid3D=gridtoplot, probearray=intensity)

        # here we retrieve the structured grids,
        # both for the energy eigenvalues and the polarization intensities
        estructgrid = structgrids.GetvtkStructuredGrid()
        intstructgrid = structgrids.GetvtkStructuredGridProbe()

        # we can now plot the phonon energy isosurface for various energies,
        # with the scattering intensity color-mapped onto it:
        isosurfintens = VTKIsoSurfaceIntensityPlotter.vtkgrid3dprobe.vtkGrid3DProbeIsoSurface2(contourvalues=contvals,
                                                                                              vtkgrid=estructgrid,
                                                                                              vtkprobe=intstructgrid)

        return isosurfintens

    pass # End of class VTKIsoSurfacePlotter


class MlabIsoSurfacePlotter(IsoSurfacePlotter):
    """Interface to a Matlab-based Phonon iso-surface plotter in 3D."""

    def __init__(self, field=None, contourvalues=None):
        self._grid = field
        self._contvals = contourvalues
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


    def plot(self,contours=None):
        """Plots the isosurfaces for the field data, at corresponding contour values."""
        import ExcitationSlicer
        path = ExcitationSlicer.__file__
        path=path.strip('__init__.pyc')

        
        if contours is None:
            contours = self._contvals
        
        import sam
        import numpy as np

        try:
            contourvalue = contours[0]
        except:
            raise ValueError, "contourvalues is empty."

        #we first pass the data into Matlab as an array:
        array = np.array(self._getArray())
        (dim0, dim1, dim2) = array.shape
        q0 = np.arange(1, dim0 + 1)
        q1 = np.arange(1, dim1 + 1)
        q2 = np.arange(1, dim2 + 1)

        sam.put('dim0', [dim0])
        sam.put('dim1', [dim1])
        sam.put('dim2', [dim2])

        sam.put('q0', q0)
        sam.put('q1', q1)
        sam.put('q2', q2)
        sam.eval("[q0i, q1i, q2i] = meshgrid(q0, q1, q2);")

        # this causes a segmentation fault for an array of 20x20x20 doubles:
        #sam.putarray('array', array)
        # here is a temporary ugly(!) fix:
        array.shape=(dim0*dim1*dim2,)
        sam.put('array', array)
        sam.eval("earray = reshape(array', dim0, dim1, dim2)")
        # end of fix

        # pass the energy-value for which to draw the isosurface into matlab"
        sam.put('contourvalue', [contourvalue])

        # We use an M-file that gets called when we evaluate the name
        # of the corresponding function in Matlab via SAM

        print "path: ", path
        sam.eval("cd('"+path+"')")
        sam.eval("MlabPhonIsoSurfacePlotter(q0i,q1i,q2i, earray, contourvalue, 'blue')")
        waitforentry=raw_input("Press any key.")
        sam.eval("close")
        return 0

    pass # End of class MlabPhonIsoSurfacePlotter

