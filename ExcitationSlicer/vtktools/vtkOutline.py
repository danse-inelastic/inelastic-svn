# Written by Mikkel Bollinger (email:mbolling@fysik.dtu.dk)
"""Class for visualizing the outline of a vtkStructuredGrid

To create an instance of this class write:

'>>>avatar=vtkUnitCell(structuredgrid)'

where 'structuredgrid' is an instance of vtkStructuredGrid. vtkOutline has
a wide range of methods for adding other VTK avatars and manipulating the
rendering process. 
"""

from Visualization.VTK.OutlineSource import OutlineSource
from Visualization.Avatars.vtkAvatar import vtkAvatar

class vtkOutline(OutlineSource,vtkAvatar):

	def __init__(self,vtkstructuredgrid,parent=None):
		OutlineSource.__init__(self,vtkstructuredgrid)
		self.CreatePipeLine()
		vtkAvatar.__init__(self,parent)

	def CreatePipeLine(self):
		"""Creates the VTK pipeline."""
		self.SetVTKOutline()
		self.SetMapper()
		self.SetActor()

	def Update(self,object=None):
		"""Updates the avatar"""
		vtkAvatar.Update(self)
