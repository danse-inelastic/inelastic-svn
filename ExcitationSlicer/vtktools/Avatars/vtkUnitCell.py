# Written by Mikkel Bollinger (email:mbolling@fysik.dtu.dk)
"""Class for visualizing a single unit cell of a BravaisLattice

To create an instance of this class write:

'>>>avatar=vtkUnitCell(bravaislattice)'

where 'bravaislattice' is an instance of 'VectorSpaces.BravaisLattice' . 
vtkUnitCell has a wide range of methods for combining different VTK avatars 
and manipulating the rendering process. 
"""

from ASE.Visualization.VTK.Avatars.vtkAvatar import vtkAvatar
from ASE.Visualization.VTK.OutlineSource import OutlineSource
from ASE.Visualization.VTK.vtkDataFromObject import vtkStructuredGridFromBravaisLattice
from ASE.Visualization.VTK.vtkDataFromObject import vtkStructuredGridFromUnitCellArray



class vtkUnitCell(OutlineSource,vtkAvatar):

	def __init__(self,unitcell,parent=None):
		self.SetUnitCell(unitcell)
		OutlineSource.__init__(self,self.GetVTKData().GetvtkStructuredGrid())
		self.CreatePipeLine()
		vtkAvatar.__init__(self,parent)

	def CreatePipeLine(self):
		"""Creates the VTK pipeline."""
		from LinearAlgebra import determinant
        	# Using that V = |det(J)| where J is the Jacobian
        	# For the basis set J=A, where r = A*x_i (x_i scaled coordinates)
        	volume= abs(determinant(self.GetUnitCell()))

		# The size of the unit cell determines the radius
		self.SetRadius(pow(volume,1.0/3)*0.01)
		self.SetVTKOutline()
		self.SetMapper()
		self.SetActor()

	def GetUnitCell(self):
		"""Returns the unit cell"""
		return self._unitcell_

	def SetUnitCell(self,unitcell):
		"""Sets the unit cell"""
		self._unitcell_=unitcell

	def GetVTKData(self):
		"""Returns the instance of vtkStructuredGridFromUnitCellArray"""
		try:
			return self._vtkdata
		except AttributeError:
			self._vtkdata=vtkStructuredGridFromUnitCellArray()
			return self._vtkdata

	def Update(self,object=None):
		"""Updates the avatar

		This method can be used if the unit cell has been changed or
		modified. It forces the vtk data to reread and afterwards 
		the added avatars are asked to update themselves.
		"""
		if object is not None:
			self.SetUnitCell(object)
		self.GetVTKData().ReadFromArray(self.GetUnitCell())
		vtkAvatar.Update(self)


