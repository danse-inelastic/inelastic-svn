# Written by Mikkel Bollinger (email:mbolling@fysik.dtu.dk)
"""Module for transforming objects into VTK data"""

# Module uses:
# vtkFloatArray, vtkVectors,vtkScalars,vtkPolyData,vtkPoints,vtkStructureGrid,
# vtikFloatArray

from Numeric import Float32,transpose,NewAxis,asarray,array,matrixmultiply
import copy

class vtkStructuredGridsFromGrid3DProbeArray:
	"""Class for reading vtkStructuredGrids

	This class can be used for generating two vtkStructuredGrids from 
	an instance of 'Grid' defined in 'Structures.Grid' or any derived
	class and a NumPy array. The 'Grid' is expected to defined in a 3
	dimensional vectorspace. The vtkStructuredGrids share the same 
	instance of vtkPoints. This class is intended to be used for
	visualization of a grid with a probe.
	"""

	def __init__(self,grid3D=None,probearray=None):
		if (grid3D and probearray) is not None:
			self.ReadFromGrid3DProbeArray(grid3D,probearray)
		elif (grid3D and probearray) is None:
			pass
		else:
			raise ValueError, "(grid3D,proberray) must either be defined or None"

	def ReadFromGrid3DProbeArray(self,grid3D,probearray):
		"""Reads the vtkStructuredGrids from grid3D and probearray"""
		# Reading from grid3D for iso surfaces
		self.GetGrid3DReader().ReadFromGrid3D(grid3D)

		# Reading scalars for probearray
                # Preparing probearray:
                # **NOTE** VTK requires the additional axis 
                probearray_vtk=transpose(probearray)[...,NewAxis]
                self.scalardata=vtkFloatArrayFromNumPyArray(copy.copy(probearray_vtk))
		#self.scalardata=vtkScalarsFromArray(transpose(probearray))
		self.GetvtkStructuredGridProbe().GetPointData().SetScalars(self.scalardata.GetvtkFloatArray())

		# Inserting the points
		self.GetvtkStructuredGridProbe().SetPoints(self.GetGrid3DReader().GetvtkStructuredGrid().GetPoints())
		# and setting the dimension
		N1,N2,N3=grid3D.GetSpatialShape()
		self.GetvtkStructuredGridProbe().SetDimensions(N1,N2,N3)
		# Update the UpdateExtent of the probe
		# This is for some (unknown) reason not done during the
		# update of the probe
		self.GetvtkStructuredGridProbe().UpdateInformation()
		self.GetvtkStructuredGridProbe().SetUpdateExtentToWholeExtent()
		

	def GetGrid3DReader(self):
		try:
			return self.isogridreader
		except AttributeError:
			self.isogridreader=vtkStructuredGridFromGrid3D()
			return self.isogridreader

	def GetvtkStructuredGrid(self):
		"""Returns the instance of the vtkStructuredGrid"""
		return self.GetGrid3DReader().GetvtkStructuredGrid()

	def GetvtkStructuredGridProbe(self):
		"""Returns the instance of the vtkStructuredGrid"""
                from vtk import vtkStructuredGrid
		try:
			return self.probegrid
		except AttributeError:
			self.probegrid=vtkStructuredGrid()
			return self.probegrid

class vtkStructuredGridFromGrid3D:
	"""Class for reading a vtkStructuredGrid from a grid

	This class can be used to generate a vtkStructuredGrid from an instance
	of 'Grid' defined in 'Structures.Grid' or any derived class. The 
	grid is expected to be defined in a 3D vectorspace.
	"""

	def __init__(self,grid3D=None):
		if grid3D is not None:
			self.ReadFromGrid3D(grid3D)

	def ReadFromGrid3D(self,grid3D):
		"""Reads the vtkStructuredGrid from grid3D"""
		# Inserting the points
		# the grid is copied to make it contiguous and transposed
		# to make the flattened order: x0,y0,z0,x1,y1,z1,...
		self.pointdata=vtkPointsFromArray(copy.copy(transpose(grid3D.GetCartesianCoordinates())))
		self.GetvtkStructuredGrid().SetPoints(self.pointdata.GetvtkPoints())

		# Inserting the scalars
		#self.scalardata=vtkScalarsFromArray(transpose(grid3D.GetGridValues()))
                # Preparing input scalars:
                # **NOTE** VTK requires the final axis
                scalars=transpose(grid3D.GetGridValues())[...,NewAxis]
                self.scalardata=vtkFloatArrayFromNumPyArray(copy.copy(scalars))
                self.GetvtkStructuredGrid().GetPointData().SetScalars(self.scalardata.GetvtkFloatArray())

		# Setting the dimensions of the grid
		N1,N2,N3=grid3D.GetSpatialShape()
		self.GetvtkStructuredGrid().SetDimensions(N1,N2,N3)

	def GetvtkStructuredGrid(self):
		"""Returns the instance of vtkStructuredGrid"""
                from vtk import vtkStructuredGrid
		try:
			return self.vtkstructuredgrid
		except AttributeError:
			self.vtkstructuredgrid=vtkStructuredGrid()
			return self.vtkstructuredgrid


class vtkStructuredGridFromBravaisLattice:
	"""Class for reading vtkStructuredGrid from a bravaislattice

	This method can be used to genenerate a vtkStructuredGrid from an
	instance of the class 'BravaisLattice' defined in 
	'Structured.VectorSpaces' . 
	"""

	def __init__(self,bravaislattice=None):
		if bravaislattice is not None:
			self.ReadFromBravaisLattice(bravaislattice)

	def ReadFromBravaisLattice(self,bravaislattice):
		"""Reads the vtkPolyData from bravaislattice"""
		# Calculating the position of the corners
		edges=[[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]]
		corners=map(lambda edge,cell=bravaislattice,mul=matrixmultiply,transpose=transpose:mul(transpose(cell.GetBasis()),edge),edges) 

		# Reading the vtkPoints to the vtkStructuredGrid
		self.pointdata=vtkPointsFromArray(corners)
		self.GetvtkStructuredGrid().SetDimensions(2,2,2)
		self.GetvtkStructuredGrid().SetPoints(self.pointdata.GetvtkPoints())

	def GetvtkStructuredGrid(self):
		"""Returns the instance of vtkStructuredGrid"""
                from vtk import vtkStructuredGrid
		try:
			return self.vtkstructuredgrid
		except AttributeError:
			self.vtkstructuredgrid=vtkStructuredGrid()
			return self.vtkstructuredgrid


class vtkStructuredGridFromUnitCellArray:
        """Class for reading vtkStructuredGrid from a Numerical array
	representing the unitcell. 
        """

        def __init__(self,array=None):
                if array is not None:
                        self.ReadFromArray(array)

        def ReadFromArray(self,array):
                """Reads the vtkPolyData from 3x3 array"""
                # Calculating the position of the corners
                edges=[[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]]
                corners=map(lambda edge,cell=array,mul=matrixmultiply,transpose=transpose:mul(transpose(cell),edge),edges)

                # Reading the vtkPoints to the vtkStructuredGrid
                self.pointdata=vtkPointsFromArray(corners)
                self.GetvtkStructuredGrid().SetDimensions(2,2,2)
                self.GetvtkStructuredGrid().SetPoints(self.pointdata.GetvtkPoints())

        def GetvtkStructuredGrid(self):
                """Returns the instance of vtkStructuredGrid"""
                from vtk import vtkStructuredGrid
                try:
                        return self.vtkstructuredgrid
                except AttributeError:
                        self.vtkstructuredgrid=vtkStructuredGrid()
                        return self.vtkstructuredgrid


class vtkPolyDataFromListOfPositionsVectors:
	"""Class for reading vtkPolyData

	This class can be used to generate vtkPolyData containing vtkPoints
	and vtkVectors as point data. Note that the vectors are expected 
	to have the shape '<vectors>,<number of componentes>' and the positions
	the shape discussed in 'vtkPointsFromArray' .
	"""

	def __init__(self,positions=None,vectors=None):
		if (positions and vectors) is not None:
			self.ReadFromPositionsVectors(positions,vectors)
		elif (positions and vectors) is None:
			pass
		else:
			raise ValueError, "(positions,vectors) must either be defined or None"

	def ReadFromPositionsVectors(self,positions,vectors):
		"""Read vtkPolyData from positions and vectors"""
		# Inserting positions
		self.pointdata=vtkPointsFromArray(positions)
		self.GetvtkPolyData().SetPoints(self.pointdata.GetvtkPoints())

                # Inserting data attributes: vectors
		self.vectordata=vtkFloatArrayFromNumPyArray(vectors)
                pointdata=self.GetvtkPolyData().GetPointData()
                pointdata.SetVectors(self.vectordata.GetvtkFloatArray())

	def GetvtkPolyData(self):
		"""Return the instance of vtkPolyData"""
                from vtk import vtkPolyData
		try:
			return self.vtkpolydata
		except AttributeError:
			self.vtkpolydata=vtkPolyData()
			return self.vtkpolydata

class vtkPolyDataFromListOfPositionsScalars:
	"""Class for reading vtkPolyData

	This class can be used to generate vtkPolyData containing positions and
	scalars as pointdata. The points are expected have the same shape as 
	the input for 'vtkPointsFromArray' . 
	"""

	def __init__(self,positions=None,scalars=None):
		if (positions and scalars) is not None:
			self.ReadFromPositionsScalars(positions,scalars)
		elif (positions and scalars) is None:
			pass
		else:
			raise ValueError, "(positions,vectors) must either be defined or be None"

	def ReadFromPositionsScalars(self,positions,scalars):
		"""Reads vtkPolyData from positions and scalars"""
		# Inserting positions
		self.pointdata=vtkPointsFromArray(positions)

		# Inserting scalars
		#self.scalardata=vtkScalarsFromArray(scalars)
                self.scalardata=vtkFloatArrayFromNumPyArray(copy.copy(asarray(scalars)[...,NewAxis]))
		# Inserting positions and scalars in vtkPolyData
		self.GetvtkPolyData().SetPoints(self.pointdata.GetvtkPoints())
		#self.GetvtkPolyData().GetPointData().SetScalars(self.scalardata.GetvtkScalars())
                pointdata=self.GetvtkPolyData().GetPointData()
                pointdata.SetScalars(self.scalardata.GetvtkFloatArray())
                #self.GetvtkPolyData().SetPointData(self.scalardata.GetvtkScalars())


	def GetvtkPolyData(self):
		"""Returns the instance of vtkPolyData"""
                from vtk import vtkPolyData
		try:
			return self.vtkpolydata
		except AttributeError:
			self.vtkpolydata=vtkPolyData()
			return self.vtkpolydata


class vtkPointsFromArray:
	"""Class for reading vtkPoints

	This class can be used for generating vtkPoints from an array. The
	array is expected to have the shape '<points>,<dim>' where 'dim' is
	dimensionality of the input points.
	"""

	def __init__(self,array=None):
		if array is not None:
			self.ReadFromArray(array)

	def ReadFromArray(self,array):
		"""Read vtkPoints from array"""
		self.pointdata=vtkFloatArrayFromNumPyArray(asarray(array))
		self.GetvtkPoints().SetData(self.pointdata.GetvtkFloatArray())

	def GetvtkPoints(self):
		"""Returns the instance of vtkPoints"""
                from vtk import vtkPoints
		try:
			return self.vtkpoints
		except AttributeError:
			self.vtkpoints=vtkPoints()
			return self.vtkpoints
	
class vtkScalarsFromArrayOld:
	"""Class for reading vtkScalars. Class not used.

	This class can be used to generate vtkScalars from an array.
	"""

	def __init__(self,array):
		if array is not None:
			self.ReadFromArray(array)

	def ReadFromArray(self,array):
		"""Reads vtkScalars from array"""
		# The array is copied to make it contiguous
		self.scalardata=vtkFloatArrayFromNumPyArray(copy.copy(asarray(array)[...,NewAxis]))
		self.GetvtkScalars().SetScalars(self.scalardata.GetvtkFloatArray())

	def GetvtkScalars(self):
		"""Returns the instance of vtkScalars"""
                from vtk import vtkPointData
		try:
			return self.vtkscalars
		except AttributeError:
			self.vtkscalars=vtkPointData()
			return self.vtkscalars


class vtkFloatArrayFromNumPyArray:
	"""Class for reading vtkFloatArray

	This class can be used to generate a vtkFloatArray from a NumPy array.
	The NumPy array should be of the form 
	'<entries>,<number of components>'
	where 'number of components' indicates the number of components in 
	each entry in the vtkFloatArray. Note that this form is also expected
	even in the case of only a single component.
	"""
	def __init__(self,numpyarray):
		self.ReadvtkFloatArrayFromNumPyArray(numpyarray)

	def ReadvtkFloatArrayFromNumPyArray(self,numpyarray):
		"""Reads vtkFloatArray from NumPy array"""
		self.__floatstring=numpyarray.astype(Float32).tostring()
		self.GetvtkFloatArray().SetNumberOfComponents(numpyarray.shape[-1])
		self.GetvtkFloatArray().SetVoidArray(self.__floatstring,len(numpyarray.flat),1)

	def GetvtkFloatArray(self):
		"""Returns the vtkFloatArray"""
                from vtk import vtkFloatArray
		try:
			return self.__vtkfloatarray
		except AttributeError:
			self.__vtkfloatarray=vtkFloatArray()
			return self.__vtkfloatarray
	




