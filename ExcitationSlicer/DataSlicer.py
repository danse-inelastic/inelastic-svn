# Olivier Delaire 

__doc__ = "Interface to 3D iso-surface plotter."

from pyre.components.Component import Component

class DataSlicer(Component):
    """Interface (base class) to a generic data slicer."""

    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        # inv stuff
        pass

    def __init__(self, field=None, cutsurface=None):
        self._field = field
        self._cutsurf = cutsurface

    def setField(self, field):
        self._field = field
        return

    def setCutSurface(self, cutsurface):
        self._cutsurf = cutsurface
        return

    def plot(self):
        """Plots the slice of the field data on the intersecting surface."""
        raise NotImplementedError

    pass # End of class DataSlicer


class VTKPlaneSlicer(DataSlicer):
    """Interface to a VTK-based slicer implemented in ASE."""

    def __init__(self, field=None, cutplaneorigin=None, cutplanenormal=None):
        self._grid = field
        if cutplaneorigin is None:
            cutplaneorigin = (0,0,0)
        if cutplanenormal is None:
            cutplanenormal = (1,0,0)
        self._origin = cutplaneorigin
        self._normal = cutplanenormal
        #do rest of initialization
        return

    def setGrid(self, grid):
        """Sets the grid that's used in the ASE/VTK plane slicer."""
        if grid is None:
            raise ValueError, "Grid should not be None."
        self._grid = grid
        return

    def setCutPlane(self, origin=(0,0,0), normal=(1,0,0)):
        """Sets the cut plane defined by an origin and a plane normal."""
        self._origin = origin
        self._normal = normal
        return

    def plot(self):
        """Plots a cut of the field data by the cutsurface."""
        from vtktools.vtkGrid3D import vtkGrid3DPlane
        from  vtktools.vtkDataFromObject import vtkStructuredGridFromGrid3D

        gridConverter = vtkStructuredGridFromGrid3D(self._grid)
        structGrid = gridConverter.GetvtkStructuredGrid()
        
        planecut = vtkGrid3DPlane(vtkstructuredgrid=structGrid)
        #planecut.SetNormal(self._normal)
        #planecut.SetOrigin(self._origin)
        #planecut.Update()
        return planecut

    pass # End of class VTKPlaneSlicer
            
