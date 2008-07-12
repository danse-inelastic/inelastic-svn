# Written by Mikkel Bollinger (email: mbolling@fysik.dtu.dk)
"""Class for creating vtk planes

This class contains the methods for transforming a vtkStructuredGrid into
planes. The vtkStructuredGrid is expected to contain vtkPoints and vtkScalars
specifying a scalar value at each point. 

To create an instance of this class a vtkStructuredGrid is expected as input.
During the rendering process this instance should not be deleted since this
will cause the VTK pipeline to be broken. 

The following methods should always be available:

* 'GetActor()'
"""

import sys
try:
    from vtk import vtkCutter,vtkDataSetMapper,vtkLODActor,vtkPlane
except ImportError:
    # Suppress ImportErrors if we are only creating documenation with pythondoc
    if not sys.modules.has_key('pythondoc'):
	#  No, this was a real error, reraise the exception
	raise  
from ColorTableSource import ColorTableSource
from Numeric import array

class PlaneSource:

	def __init__(self,vtkstructuredgrid):
		self.__vtkstructuredgrid=vtkstructuredgrid
		self.InitVTKMethods()

	def InitVTKMethods(self):
		"""Initializes the VTK methods to be used."""
		self.colortable=ColorTableSource()
		self._plane=vtkPlane()
		self._cutter=vtkCutter()
		self._mapper=vtkDataSetMapper()
		self.actor=vtkLODActor()

	def SetSinglePlane(self,normal,origin):
		"""Transforms vtkStructuredGrid into vtkCutter"""

		self._plane.SetNormal(normal)
		self._plane.SetOrigin(origin)

		self._cutter.SetInput(self.__vtkstructuredgrid)
		self._cutter.SetCutFunction(self._plane)

	def SetMultiplePlanes(self,normal,origin,planerange,nplanes=50):
		"""Transforms vtkStructuredGrid into vtkCutter"""
		self._plane.SetNormal(normal)
		self._plane.SetOrigin(origin)

		self._cutter.SetInput(self.__vtkstructuredgrid)
		self._cutter.SetCutFunction(self._plane)
		planemin,planemax=planerange
		self._cutter.GenerateValues(nplanes,planemin,planemax)

	def GetPlane(self):
		"""Returns the instance of vtkCutter"""
		return self._cutter

	def SetMapper(self,colorrange):
		"""Add the cutter to the mapper"""
		self._mapper.SetInput(self.GetPlane().GetOutput())

		# adding the colortable
                #self._mapper.SetLookupTable(self.GetColorTable())
		#classname=self.GetColorTable().GetClassName()
		# Is the colortable a lookuptable ?
		#if classname=='vtkLookupTable':
		#	self._mapper.SetLookupTable(self.GetColorTable())
		# Is the colortable a ColorTable
		#elif classname=='ColorTableSource':
		#	self._mapper.SetLookupTable(self.GetColorTable()._GetColorTable())
		self._mapper.SetScalarRange(tuple(colorrange))

	def GetMapper(self):
		"""Returns the instance of vtkDataSetMapper"""
		return self._mapper

	def SetColorTable(self,colortable):
		"""Sets the colortable

		This method can be used to set the colortable. The default 
		is a HSV colortable with the hue ranging from 0.75 to
		0.0. For more information see the documentation
		for 'ColorTable'
		"""
		self.colortable=colortable
                self._mapper.SetLookupTable(colortable)
		#self._mapper.SetLookupTable(colortable._GetColorTable())
		
	def GetColorTable(self):
		"""Returns an instance of ColorTable"""
		try:
			return self.colortable
		except AttributeError:
			self.colortable=ColorTableSource()
			return self.colortable

	def SetColorRange(self,colorrange):
		"""Sets the color range
		
		This method can be used to set the color range. The interval
		specifies the range used by the color table. Scalar values
		greater than the maximum are clamped to the maximum value and
		scalar values smaller than the minimum are clamped to the
		minimum value.
		"""
		self.ColorRange=colorrange
		self.SetMapper(tuple(colorrange))

	def GetColorRange(self):
		"""Returnss the color range"""
		return self.ColorRange

	def SetActor(self):
		"""Add the mapper to the actor"""
		self.actor.SetMapper(self.GetMapper())
		self.actor.SetNumberOfCloudPoints(1000*self.__vtkstructuredgrid.GetNumberOfPoints())
		
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


