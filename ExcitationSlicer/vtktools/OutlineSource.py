"""Class for creating an outline

This class contains the methods for transforming a vtkStructuredGrid into an
outline. The vtkStructuredGrid is expected to contain vtkPoints. 

To create an instance of this class a vtkStructuredGrid should be specified 
as input. During the rendering process this instance should not be deleted
since this will cause the VTK pipeline to be broken.

The following methods should always be available:

* 'GetActor()'
"""

import sys
try:
# Old import
#   from libVTKGraphicsPython import vtkStructuredGridOutlineFilter,vtkTubeFilter,vtkPolyDataMapper,vtkLODActor
    from vtk import vtkStructuredGridOutlineFilter,vtkTubeFilter,vtkPolyDataMapper,vtkLODActor
except ImportError:
    # Suppress ImportErrors if we are only creating documenation with pythondoc
    if not sys.modules.has_key('pythondoc'):
	#  No, this was a real error, reraise the exception
	raise  

class OutlineSource:

	def __init__(self,vtkstructuredgrid):
		self._vtkstructuredgrid=vtkstructuredgrid
		self.InitVTKMethods()
		
	def InitVTKMethods(self):
		"""Initializes the VTK methods to be used"""
		self._outline=vtkStructuredGridOutlineFilter()
		self._tube=vtkTubeFilter()
		self._mapper_=vtkPolyDataMapper()
		self.actor=vtkLODActor()

	def SetRadius(self,radius):
		"""Sets the radius of the tubes

		This method can be used to set the radius of the tubes. Default
		is 0.1.
		"""
		self.Radius=radius
		self.SetVTKOutline()

	def GetRadius(self):
		"""Returns the radius of the tubes."""
		try:
			return self.Radius
		except AttributeError:
			return 0.1

	def SetVTKOutline(self):
		"""Transforms vtkStructuredGrid into vtkTubeFilter"""
		self._outline.SetInput(self._vtkstructuredgrid)

		self._tube.SetInput(self._outline.GetOutput())
		self._tube.SetNumberOfSides(10)
		self._tube.SetCapping(1)
		self._tube.SetRadius(self.GetRadius())

	def GetVTKOutline(self):
		"""Returns the instance of vtkTubeFilter"""
		return self._tube

	def SetMapper(self):
		"""Add the tubes to the mapper"""
		self._mapper_.SetInput(self.GetVTKOutline().GetOutput())

	def GetMapper(self):
		"""Returns the instance of the vtkPolyDataMapper"""
		return self._mapper_

	def SetActor(self):
		"""Add the mapper to the actor"""
		self.actor.SetMapper(self.GetMapper())
		self.GetActorProperty().SetColor(0,0,0)

	def GetActor(self):
		"""Returns the instance of vtkLODActor"""
		return self.actor

	def GetActorProperty(self):
		"""Returns the instance of vtkProperty

		This methods returns an instance of vtkProperty which can
		be used to control the lighting and other surface properties
		of the actor. These properties include colors, 
		specular power, opacity etc.. For a complete list use 
		'dir(plot.GetActorProperty())' . A lot of the methods are 
		self-explaining - otherwise consult your favorite VTK manual. 

		An example: '>>>plot.GetActorProperty().SetColor(1,1,1)'

		changes the color of the actor to white. The (R,G,B)-scale is
		used to specify the color. 
		"""
		return self.actor.GetProperty()









