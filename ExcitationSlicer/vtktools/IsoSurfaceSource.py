# Written by Mikkel Bollinger (email: mbolling@fysik.dtu.dk)
"""Module containing classes for generating isosurfaces"""
import sys
try:
    from vtk import vtkContourFilter,vtkProbeFilter,vtkCastToConcrete,vtkPolyDataNormals,vtkPolyDataMapper,vtkPolyDataMapper,vtkLODActor
except ImportError:
    # Suppress ImportErrors if we are only creating documenation with pythondoc
    if not sys.modules.has_key('pythondoc'):
	#  No, this was a real error, reraise the exception
	raise  
from vtktools.ColorTableSource import ColorTableSource
from Numeric import array,asarray

class _IsoSurfaceSource_:
	"""Basis class for isosurfacesource"""

	def __init__(self,vtkstructuredgrid):
		self._vtkstructuredgrid=vtkstructuredgrid
		self.InitVTKMethods()

	def InitVTKMethods(self):
		"""Initializes the VTK methods to be used."""
		self._iso=vtkContourFilter()
		self._normals=vtkPolyDataNormals()
		self._mapper=vtkPolyDataMapper()
		self.actor=vtkLODActor()

	def GetIsoSurface(self):
		"""Returns the instance of vtkPolyDataNormals"""
		return self._normals

	def SetMapper(self,colorrange):
		"""Adds isosurfaces to the mapper"""
		self._mapper.SetInput(self.GetIsoSurface().GetOutput())
		# adding the colortable
                self._mapper.SetLookupTable(self.GetColorTable())
                # and finally the scalar range 
		self._mapper.SetScalarRange(tuple(colorrange))

	def GetMapper(self):
		"""Returns the instance of vtkPolyDataMapper"""
		return self._mapper

	def SetColorTable(self,colortable):
		"""Sets the colortable

		This method can be used to set the colortable. The colortable
		may either be an instance of 'ColorTableSource' or 
		vtkLookUpTable. The default is an instance of 
		'ColorTableSource' having a HSV colortable with the hue 
		ranging from 0.75 to 0.0. For more information see the 
		documentation for 'ColorTable'
		"""
		self.colortable=colortable
                self._mapper.SetLookupTable(colortable)
		
	def GetColorTable(self):
		"""Returns an instance of ColorTableSource"""
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
		"""Adds the mapper to the actor"""
		self.actor.SetMapper(self.GetMapper())
		self.actor.SetNumberOfCloudPoints(1000*self._vtkstructuredgrid.GetNumberOfPoints())
		
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


class IsoSurfaceSource(_IsoSurfaceSource_):
	"""Class for creating vtk isosurfaces

	This class contains the methods for transforming a vtkStructuredGrid 
	into isosurfaces. The vtkStructuredGrid should contain vtkPoints and 
	vtkScalars specifying a scalar value corresponding to each point.

	To create an instance of this class a vtkStructuredGrid is expected as
 	input. During the rendering process this instance should not be 
	deleted since this will cause the VTK pipeline to be broken.

	The following methods should always be available:

	* 'GetActor()'
	"""

	def SetIsoSurface1(self,contourrange,Ncontour):
		"""Transforms a vtkStructuredGrid into vtkPolyDataNormals"""
		contourmin,contourmax=contourrange

		self._iso.SetInput(self._vtkstructuredgrid)
		self._iso.GenerateValues(Ncontour,contourmin,contourmax)

		self._normals.SetInput(self._iso.GetOutput())
		self._normals.SetFeatureAngle(45)

	def SetIsoSurface2(self,contourlist):
		"""Transforms a vtkStructuredGrid into vtkPolyDataNormals"""
		self._iso.SetInput(self._vtkstructuredgrid)

		# Setting number of contours
		ncontours=len(contourlist)
		self._iso.SetNumberOfContours(ncontours)

		for i in range(ncontours):
			self._iso.SetValue(i,contourlist[i])		

		self._normals.SetInput(self._iso.GetOutput())
		self._normals.SetFeatureAngle(45)


class IsoSurfaceProbeSource(_IsoSurfaceSource_):
	"""Class for creating vtk isosurfaces with a probe

	This class contains the methods for transforming two 
	vtkStructuredGrids into isosurfaces being colored according to the 
	probe. Both vtkStructuredGrids are expected to contain vtkPoints and 
	vtkScalars specifying a scalar value for each point. The vtkScalars 
	represent the isosurface values and the probe values respectively. 

	To create an instance of this class two vtkStructuredGrids are 
	expected as input. During the rendering process neither of these 
	should be deleted since this will cause the VTK pipeline to be broken. 

	The following methods should always be available:

	* 'GetActor()'
	"""

	def __init__(self,vtkstructuredgrid,vtkstructuredgridprobe):
		_IsoSurfaceSource_.__init__(self,vtkstructuredgrid)
		self._vtkstructuredgridprobe=vtkstructuredgridprobe

	def InitVTKMethods(self):
		"""Initializes the VTK methods to be used."""
		self._probefilter=vtkProbeFilter()
		self._cast=vtkCastToConcrete()
		_IsoSurfaceSource_.InitVTKMethods(self)

	def SetIsoSurface1(self,contourrange,Ncontour):
		"""Transforms two vtkStructuredGrids into vtkPolyDataNormals"""
		contourmin,contourmax=contourrange
		self._iso.SetInput(self._vtkstructuredgrid)
		self._iso.GenerateValues(Ncontour,contourmin,contourmax)

		# Computes phase on the iso-surface
		self._probefilter.SetInput(self._iso.GetOutput())
		self._probefilter.SetSource(self._vtkstructuredgridprobe)

		# Putting the output of probe into the correct form
		self._cast.SetInput(self._probefilter.GetOutput())

		self._normals.SetInput(self._cast.GetPolyDataOutput())
		self._normals.SetFeatureAngle(45)

	def SetIsoSurface2(self,contourlist):
		"""Transforms two vtkStructuredGrids into vtkPolyDataNormals"""
		self._iso.SetInput(self._vtkstructuredgrid)

		ncontours=len(contourlist)
		self._iso.SetNumberOfContours(ncontours)

		for i in range(ncontours):
			self._iso.SetValue(i,contourlist[i])		

		# Computes phase on the iso-surface
		self._probefilter.SetInput(self._iso.GetOutput())
		self._probefilter.SetSource(self._vtkstructuredgridprobe)

		# Putting the output of probe into the correct form
		self._cast.SetInput(self._probefilter.GetOutput())

		self._normals.SetInput(self._cast.GetPolyDataOutput())
		self._normals.SetFeatureAngle(45)




