# Written by Mikkel Bollinger (email:mbolling@fysik.dtu.dk)
"""Implementations of Grid

These classes all implement grids. A grid represents a collection of values 
defined in an 'N' -dimensional space. A single value of the collection then 
represents the grid at a discrete position having coordinates given in terms 
of the space. The values may be scalars but can in general have any number of 
components. 

The following methods should always be available:

'GetSpace' -- Returns the space in which the grid is defined.

'GetArray' -- Returns an array representing the collection of values.

'GetOrigin' --  Returns the origin of the grid.

Other methods:

'GetCoordinates' -- Returns an array with the coordinates of the discrete points at which the collection of values are defined

'GetCartesianCoordinates' -- Returns an array with the cartesian coordinates of the discrete points at which the collection of points are defined.
"""

import copy
from Numeric import asarray
from vtktools.Vector import Vector
from vtktools.VectorSpaces import TheCartesianSpace

# Uses:	Numeric
#	Utilities.ArrayTools

class Grid:
	"""Class which represents grids

	An instance is created by 
	'Grid(array=' *array* ', space=' *vectorspace* ')' . Here *array* may 
	be a sequence or NumPy array specified according to the convention 
	that if the array contains multicomponent values this/these axis/axes 
	comes first, i.e. the shape of *array* should be of the form 
	'(<' *components* '>,<' *dimensions of vectorspace* '>)'. *vectorspace*
	is an instance of 'VectorSpaceWithBasis', 'TheCartesianSpace' (both 
	defined in 'Structures.VectorSpaces' ) or any derivation thereof. If
	'space' is not defined the three dimensional cartesian vectorspace 
	will be used. 
	
	'array' represents the coefficients in the specified
	function space. If no functionspace is specified the values of 
	*array* are assumed to be evenly distributed along each axis of the 
	provided space. 
	 
	By default the origin is the null-vector, an instance
	of 'Vector()', with the same dimension as the space (defined in 
	'Structures.Vector' ). 

	A number of mathematical operations have been implemented. It is 
	possible to multiply/add/subtract scalars values. Furthermore grids
	may be added/subtracted provided they are instances of the same class 
	and are defined with the same instances of space and origin. 
	"""

	def __init__(self,array=None,space=None,origin=None,functionspace=None):
		if array is not None:
			self.SetArray(array)
		# If no space use 3D cartesianspace.
		# dimension is used to set correct dimension of origin
		if space is not None:
			self.SetSpace(space)
			dimension=len(space.GetBasis())
		else:
			dimension=3
			self.SetSpace(TheCartesianSpace(dimension=dimension))
		# If no origin use the null vector
		if origin is not None:
			self.SetOrigin(origin)
		else:
			coordinates=dimension*[0]
			self.SetOrigin(Vector(coordinates))
		self.FunctionSpace=functionspace

	def __add__(self,other):
		a=copy.copy(self)
		if type(other) in [type(.0),type(1),type(1+1j)]:
			a.SetArray(self.GetArray()+other) 
		elif self.__class__==other.__class__ and self.GetSpace()==other.GetSpace() and self.GetOrigin()==other.GetOrigin() and self.GetFunctionSpace()==other.GetFunctionSpace():
			a.SetArray(self.GetArray()+other.GetArray())
			return a
		else:
			raise ValueError, '__add__ not defined for this operation'

	def __radd__(self,other):
		# Addition is commutative
		return self+other

	def __sub__(self,other):
		a=copy.copy(self)
		if type(other) in [type(.0),type(1),type(1+1j)]:
			a.SetArray(self.GetArray()-other)
			return a
		elif self.__class__==other.__class__ and self.GetSpace()==other.GetSpace() and self.GetOrigin()==other.GetOrigin() and self.GetFunctionSpace()==other.GetFunctionSpace():
			a.SetArray(self.GetArray()-other.GetArray())
			return a
		else:
			raise ValueError, '__sub__ not defined for this operation'

	def __rsub__(self,other):
		a=copy.copy(self)
		if type(other) in [type(.0),type(1),type(1+1j)]:
			a.SetArray(other-self.GetArray())
			return a
		# Implementation for grid not necessary since this will be 
		# taken done by __sub__
		else:
			raise ValueError, '__rsub__ not defined for this operation'

	def __mul__(self,other):
		a=copy.copy(self)
		if type(other) in [type(.0),type(1),type(1+1j)]:
			a.SetArray(self.GetArray()*other)
			return a
		else:
			raise ValueError, '__mul__ not defined for this operation'

	def __rmul__(self,other):
		# Multiplication is commutative
		return self*other

		
	def __repr__(self):
		text=str(self.__class__)+'('
		try:
			text=text+'grid= '+repr(self.GetArray())+'),'
		except AttributeError:
			pass
		try:
			text=text+'space='+repr(self.GetSpace())+','
		except AttributeError:
			pass
		if text[-1:]==",":
			text=text[:-1]
		text=text+')'
		return text

	def GetArray(self):
		"""Returns a NumPy array

		This method returns a NumPy array. The shape of the array
		has the form discussed in 'SetArray'. 
		"""
		return self.Array

	def SetArray(self,array):
		"""Sets the array

		This method sets the array. The array should have the shape
		( *a1* , *a2*,..., *ai* , *N1* , *N2* ,..., *NN* ) in case of 
		a grid having *i* components in a *N* dimensional space.
		*Ni* corresponds to the number of values along each axis.
		Note that even though the array is given in terms of a tuple 
		or a list it will be converted to a NumPy array.
		"""
		self.Array=asarray(array)

	def UnregisterArray(self):
		"""Unregisters the array

		This method removes the array from the attribute list.
		"""
		delattr(self,"Array")

	def GetGridValues(self):
		"""Returns the grid values in real space"""
		functionspace=self.GetFunctionSpace()
		if functionspace is not None:
			return functionspace.FunctionValuesFromCoordinates(self.GetArray())
		else:
			return self.GetArray()

	def SetGridValues(self,gridvalues):
		"""Sets the grid values in real space"""
		functionspace=self.GetFunctionSpace()
		if functionspace is not None:
			newarray=functionspace.CoordinatesFromFunctionValues(gridvalues)
			self.SetArray(newarray)
		else:
			self.SetArray(gridvalues)

	def GetSpace(self):
		"""Returns the space"""
		return self.Space

	def SetSpace(self,space):
		"""Sets the space"""
		self.Space=space

	def GetOrigin(self):
		"""Returns the origin"""
		return self.Origin

	def SetOrigin(self,origin):
		"""Sets the origin"""
		self.Origin=origin

	def SetFunctionSpace(self,functionspace=None):
		"""Sets the function space
		This will change the function coordinates, 'array' since
		the gridvalues are kept fixed. 
		Note that if no argument is given the 'array' will be assumed
		to be represented in real space, i.e. no interpolation 
		between the grid points. 
		"""

		if hasattr(self,"Array"):
		# If coordinates Array is set change according to the new space
			if functionspace!=self.GetFunctionSpace():
				gridvalues=self.GetGridValues()
				self.FunctionSpace=functionspace
				self.SetGridValues(gridvalues)
		else:
		# else: set the functionspace
			self.FunctionSpace=functionspace

	def GetFunctionSpace(self):
		"""Returns the function space"""
		return self.FunctionSpace

	def GetValueRange(self):
		"""Returns the min/max values of array as a tuple"""
		return (min(self.GetArray().flat),max(self.GetArray().flat))

	def GetAverage(self):
		"""Returns the average value of array."""
		from Numeric import add,multiply
		return add.reduce(self.GetArray().flat)/multiply.reduce(self.GetShape())

	def GetAverageAlongAxis(self,axis):
		"""Returns a NumPy array with the average of the grid points 
		along the specified axis."""
		from Numeric import add,multiply
		
		#Finding the axes to average, starting with the largest value
		otheraxes=range(len(self.GetShape())-1,-1,-1)
		otheraxes.remove(axis)

		#Finding the spape of otheraxes
		shape=list(self.GetShape())
		del shape[axis]

		# Averaging and number of entries along line
		array=self.GetArray()
		for averageaxis in otheraxes:
			array=add.reduce(array,averageaxis)
		return array/multiply.reduce(shape)

	def GetShape(self):
		"""Returns a tuple representing the shape of the array.
		"""
		return self.GetArray().shape

	def GetSpatialShape(self):
		"""Returns a tuple representing the shape of the array along
		the spatial axes.
		"""
		dim=len(self.GetSpace().GetBasis())
		return self.GetShape()[-dim:]

	def ValuesFromGridCoordinates(self,slicelist):
		"""
		Returns a NumPy array of shape ( *Nvalue* ,) containing the 
		values of the grid according to the slices specified in 
		'slicelist'. 

		**An example:**

		To slice a scalar grid having three dimensions, 
		(12:17,:,[13,26]), the slicelist should be written as:

		'slicelist=[range(12,17),None,(13,26)]'

		Note that 'None' implies that all the values along the given 
		axis are retained. 
		"""
		from vtktools.ArrayTools import SliceArray
		return SliceArray(self.GetArray(),slicelist).flat

	def GridCoordinatesFromCoordinates(self,scaledcoor):
		"""
		Returns a list containing the grid coordinates, i.e. the 
		indices of the array that correspond to the specified
		scaled coordinates, 'scaledcoor'. Note, that since the scaled 
		coordinates in general do not coincide with a grid point 
		the returned grid coordinates will be of type float.
		"""
		from Numeric import multiply
		return list(multiply(scaledcoor,self.GetSpatialShape()))

	def TruncatedGridCoordinatesFromCoordinates(self,scaledcoor):
		"""
		The same as 'GridCoordinatesFromCoordinates' except that
		in this method the returned coordinates will be truncated to 
		the nearest grid point. Hence the returned coordinates will be
		of type integer. 
		"""
		return map(lambda coor:int(round(coor)),self.GridCoordinatesFromCoordinates(scaledcoor))

	def CoordinatesFromGridCoordinates(self,gridcoor):
		"""Returns a list containing the scaled coordinates
		"""
		from Numeric import Float
		return list(asarray(gridcoor,Float)/self.GetSpatialShape())

	def GetCoordinates(self):
		"""
		Returns a NumPy array with the scaled coordinates of the
		grid points. The array will have the shape, 
		(< *dim*>,< *N1* , *N2* ,..., *Ndim* >) where *dim* is the 
		dimension of the space.
		"""
		from vtktools.ArrayTools import CoordinateArrayFromUnitVectors
		from Numeric import identity,Float
		
		shape=self.GetSpatialShape()
		gridunitcell=identity(len(shape)).astype(Float)/shape
		return CoordinateArrayFromUnitVectors(shape,gridunitcell)

	def GetCartesianCoordinates(self):
		"""
		Returns a NumPy array with the cartesian coordinates of the 
		grid points. The array will have the shape, 
		(< *dim*>,< *N1* , *N2* ,..., *Ndim* >),
		where *dim* is the dimension of the space.
		"""
		from vtktools.ArrayTools import CoordinateArrayFromUnitVectors
		return CoordinateArrayFromUnitVectors(shape=self.GetSpatialShape(),gridunitvectors=self.GetGridUnitVectors(),origin=self.GetOrigin().GetCartesianCoordinates())

	def GetGridUnitVectors(self):
		"""
		Returns a NumPy array with the grid unitvectors, i.e. the
		vectors between neighboring grid points. For a 'N' dimensional
		space the array is of the form 
		( *unitvector1*, *unitvector2* ,..., *unitvectorn* ).
		"""
		from Numeric import Float,array,add
		basis=self.GetSpace().GetBasis().astype(Float)
		return array(map(lambda unitvector,shape:unitvector/shape,basis,self.GetSpatialShape()))


	def TranslateCoordinates(self,translation,type):
		"""Returns a translated grid

		This method can be used to translate the coordinates of a 
		grid. Two different types of translation exist

		* 'active' : Translates every grid point according to 
		'translation'

		* 'passive' : Translates the origin of the grid according to 
		'translation'

		This method only supports a translation vector that matches
		the grid coordinates and for this reason 'translation' should
		be specified in terms of these coordinates.
		"""
		from vtktools import ArrayTools
		from Numeric import asarray
		from vtktools.Vector import Vector
		import copy

		# finding the output grid
		translategrid=copy.copy(self)

		# preparing for translation and calculating origin
		#trunctranslation=self._GetTruncatedTranslation(translation)
		if type=='active':
			translationnumbers=self._GetTranslationNumbers(-asarray(translation))		
			# origin
			translategrid.SetOrigin(self.GetOrigin())
		elif type=='passive':
			translationnumbers=self._GetTranslationNumbers(asarray(translation))		
			# origin
			transorigin=Vector(space=self.GetOrigin().GetSpace())
			transorigin.SetCartesianCoordinates(translategrid.GetSpace().CartesianCoordinatesFromCoordinates(self.CoordinatesFromGridCoordinates(translation)))
			translategrid.SetOrigin(self.GetOrigin()+transorigin)
		else:
			raise ValueError, 'translation type not defined'

		# finding the output array
		translatearray=ArrayTools.Translate(self.GetArray(),translationnumbers)
		translategrid.SetArray(translatearray)

		return translategrid

	def Repeat(self,periods):
		"""Returns a repeated grid

		This method can be used used to repeat the grid an integer 
		number of times according to the unit cell. Note that the unit
 		cell in the returned grid will also be expanded according to 
		'periods' . 
		"""
		from vtktools.ArrayTools import RepeatArray
		from Numeric import transpose,asarray
		a=copy.copy(self)
		# Finding the new grid
		valueorder=len(self.GetShape())-len(self.GetSpatialShape())
		# Only the spatial coordinates are repeated
		a.SetArray(RepeatArray(a.GetArray(),valueorder*[1]+periods))
		# Finding the new space
		newspace=copy.copy(self.GetSpace())
		newspace.SetBasis(transpose(transpose(self.GetSpace().GetBasis())*asarray(periods)))
		a.SetSpace(newspace)
		return a


	def IntegrateUnitCell(self,integralfunction):
		"""Integrates the unit cell using Cartesian coordinates

		This method can be used to obtain the integral of a single
		unit cell. The function is expected to take the position in
		cartesian coordinates as an argument. The function value is 
		then at each grid point multiplied with the value of the grid 
		"""

		from Numeric import add
		from vtktools.grid import RealFunction

		integratefunc=RealFunction(lambda grid,xyz,func=integralfunction : grid*func(xyz))
		integrategrid=self.Map(integratefunc)
		integral=add.reduce(integrategrid.flat)
		return integral

	def Map(self,mapfunction):
		"""Maps the grid using Cartesian coordinates

		This method can be used to map the grid values along with their
		coordinates. 'mapfunction' is expected to take the arguments, 
		'mapfunction(' *gridvalue* , *coordinate* ')' where coordinate
		is a NumPy array containing the Cartesian coordinates 
		corresponding to the grid point.
		"""
		from vtktools import ArrayTools
		return ArrayTools.Map(mapfunction,self.GetArray(),self.GetCartesianCoordinates())

	def _GetTruncatedTranslation(self,translation):
		"""Internal method used by TranslateCoordinates"""
		try:
			# Add origin to use transformation methods in Grid
			transcartesian=translation.GetCartesianCoordinates()
		except AttributeError:
			return translation
		else:
			transscale=self.GetSpace().CoordinatesFromCartesianCoordinates(transcartesian)
			trunctranslation=self.TruncatedGridCoordinatesFromCoordinates(transscale)
			# Printing change
			print 'Truncated translation to',trunctranslation,'on the FFT grid'
			return trunctranslation

	def _GetTranslationNumbers(self,translation):
		"""Internal method used by TranslateCoordinates"""
		from Numeric import array
		numbers=abs(array(self.GetSpatialShape())+translation)%array(self.GetSpatialShape())
		return tuple(numbers)

