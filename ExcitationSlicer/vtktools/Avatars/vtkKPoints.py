"""Module containing the class for visualizing k points"""

from ASE.Visualization.Avatars.vtkListOfPositions import vtkListOfPositions
from ASE.Visualization.Avatars.vtkAvatar import vtkAvatar
from ASE.Visualization.VTK.GlyphSource import SphereSource
from ASE.Visualization.VTK.Avatars.vtkUnitCell import vtkUnitCell
import Numeric

class vtkKPoints(vtkListOfPositions):
    """Class for visualizing k points using vtk

    This class can be used to visualize a collection of k points with vtk.
    Each k point is represented by a sphere. To create an instance of this
    class write

    'kpointavatar=vtkKPoints(kpoints=kpoints)'

    where 'kpoints' is an instance of 'KPoints' defined in 'Structures.KPoints'
    or any derived class. The radii of the spheres is then set to the
    default value 0.1. However, 'vtkKPoints' also accepts the keyword 'scalar'
    allowing the user to specify this radius. Furthermore, if the k points are
    also defined with a k point weight the sphere radii will also be scaled
    according to these values. This latter feature is turned off by the
    method 'ScaleByKPointWeightOff'.

    Note also that the reciprocal unit cell associated with the collection of k
    points will also by default be visualized.
    """

    def __init__(self,kpoints,parent=None,**keywords):
        # Do the k points have weights ?
        try: # Yes, scale the radii by their weight
            kpoints.GetKPointWeights()
            self.scalekpweight=1
        except AttributeError: # No, scale all k points equally
           self.scalekpweight=0 
        self.SetKPoints(kpoints)
        # Accepted keywords: scalar.
        # Use default if this scalar has not been specified.
        if not keywords.has_key('scalar'): 
            keywords['scalar']=0.10
        keywords['parent']=parent
        # To ease the rendering the resolution of spheres is
        # decreased from the default (20,20)
        if len(self.GetKPoints())>100:
            keywords['resolution']=(5,5)
        else:
            keywords['resolution']=(10,10)
        # NOTE, that listofpositions is set to None, since GetListOfPositions
        # is overloaded in this class anyway.
        apply(vtkListOfPositions.__init__,[self,None],keywords)

    def SetKPoints(self,kpoints):
        """Sets the k points

        The collection of k points are expected to be an instance of 'KPoints'
        defined in 'Structures.KPoints' or any derived class.
        """
        self.kpoints=kpoints

    def GetKPoints(self):
        """Returns the k points"""
        return self.kpoints
    
    def GetListOfPositions(self):
        """Method reimplemented from vtkListOfPositions"""
        return self.GetKPoints().GetCartesianCoordinates()

    def GetListOfScalars(self):
        """Method reimplemented from vtkListOfPositions"""
        # Scale k point radii by weight ?
        if self.ScaleByKPointWeight(): # Yes, scale them
            listofscalars=Numeric.array(vtkListOfPositions.GetListOfScalars(self))
            kpweights=Numeric.array(self.GetKPoints().GetKPointWeights())
            kpweight_ave=Numeric.add.reduce(kpweights)/len(kpweights)
            kpweight_scale=kpweights/kpweight_ave
            return listofscalars*kpweight_scale
        else: # No, return the usual scale
            return vtkListOfPositions.GetListOfScalars(self)

    def ScaleByKPointWeightOn(self):
        """Turns on scaling by k point weights

        This method can be used to turn on the scaling the radii of the k point
        spheres according to their k point weight. Note that not all k points
        will support this method. Note, that the list of radii applied by VTK
        may be obtained from the method 'GetListOfScalars'.
        """
        self.scalekpweight=1
        # Force an update of data
        self.UpdateVTKData()

    def ScaleByKPointWeightOff(self):
        """Turns off scaling by k point weights

        For more information on the scaling by k point weights, see the
        documentation for 'ScaleByKPointWeightOn'.
        """
        self.scalekpweight=0
        # Force an update of data
        self.UpdateVTKData()

    def ScaleByKPointWeight(self):
        """Internal method."""
        return self.scalekpweight

    def RemoveAvatar(self,avatar):
        """Reimplemented from vtkAvatar"""
        if hasattr(self,'reciprocal'): # Is reciprocal defined ?
            # Yes, is the avatar the reciprocal avatar ? 
            if avatar==self.GetReciprocalCellAvatar():
                delattr(self,'reciprocal')
        # Proceed with usual procedure:
        vtkListOfPositions.RemoveAvatar(self,avatar)

    def GetReciprocalCellAvatar(self):
        """Returns the instance of the reciprocal cell avatar

        Return the instance of the vtkavatar for the reciprocal unit cell. It
        will be an instance of 'vtkUnitCell'.
        """
        return self.reciprocal
        
    def AddReciprocalCell(self):
        """Adds the reciprocal cell to the avatar list

        This method will add the reciprocall unitcell to the avatar list
        (instance of the class 'vtkUnitCell'). If it already exists the
        reciprocal unit cell associated with the k points will be propagated
        to the avatar.
        """
        kpoints=self.GetKPoints()
        # Does the reciprocal cell avatar exist ?
        if hasattr(self,'reciprocal'): # Yes, update reciprocal cell
            self.reciprocal.SetUnitCell(kpoints.GetReciprocalUnitCell())
        else: # No, initialize the avatar
            self.reciprocal=vtkUnitCell(unitcell=kpoints.GetReciprocalUnitCell(),parent=self)

    def Update(self,object=None):
        """Reimplemented from vtkListOfPositions

        If 'object' is set to a k point collection, it will replace the
        existing k points and update the changes in the window.
        """
        if object is not None:
            self.SetKPoints(object)
        # Add reciprocal cell avatar (if necessary)
        self.AddReciprocalCell()
        # Continue with update
        vtkListOfPositions.Update(self)
            

        
