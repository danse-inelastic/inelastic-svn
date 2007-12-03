# Written by Mikkel Bollinger (email:mbolling@fysik.dtu.dk)
"""Module containing classes for visualizing a 3D grid"""


from ASE.Visualization.VTK.Avatars.vtkAvatar import vtkAvatar
from ASE.Visualization.VTK.Avatars.vtkOutline import vtkOutline
from ASE.Visualization.VTK.IsoSurfaceSource import IsoSurfaceSource
from ASE.Visualization.VTK.PlaneSource import PlaneSource
from ASE.Visualization.VTK.vtkDataFromObject import vtkStructuredGridFromGrid3D
from ASE.Visualization.VTK.ColorTableSource import ColorTableSource
from ASE.Visualization.VTK.VectorSpaces import BravaisLattice
from ASE.Visualization.VTK.Grid import Grid

class _vtkGrid3DParent_:
	"""Mix-in class for parent avatars

	This class contains methods which are used any parent avatar 
	visualizing a 3D grid. To create an instance of this class use:

	'_vtkGrid3DParent_(vtkdata)'

	where 'vtkdata' is an an instance converting a simulation object to 
	some vtk readable format. 'vtkdata' is expected to have the method
	'GetVTKStrucuturedGrid' .
	"""

	def __init__(self,vtkdata):
		self._vtkdata=vtkdata

	def _SetIsoSurface1(self,isosurface1):
		"""Internal method. Sets the isosurface1 avatar"""
		self.isosurface1=isosurface1

	def GetIsoSurface1(self):
		"""Returns the isosurface1 avatar"""
		return self.isosurface1

	def AddIsoSurface1(self):
		"""Derived classes should overload this method"""
		self._SetIsoSurface1(None)

	def _SetIsoSurface2(self,isosurface2):
		"""Internal method. Sets the isosurface2 avatar"""
		self.isosurface2=isosurface2

	def GetIsoSurface2(self):
		"""Returns the isosurface2 avatar"""
		return self.isosurface2
	
	def AddIsoSurface2(self):
		"""Derived classes should overload this method"""
		self._SetIsoSurface2(None)

	def _SetOutline(self,outline):
		"""Internal method. Sets the outline avatar"""
		self.outline=outline

	def GetOutline(self):
		"""Returns the outline avatar"""
		return self.outline

	def AddOutline(self):
		"""Add an vtkOutline avatar

		This method can be used to add the outline of the grid to the
		avatar list. For more information refer to the documentation
		for 'vtkOutline' .
		"""
		try:	# Does the outline already exist ?
			# Yes, do nothing
			self._GetOutlineAvatar()
		except AttributeError:
			# No, create a new one
			outline=vtkOutline(self.GetvtkStructuredGrid(),parent=self)
			self._SetOutline(outline)


	def SetRepresentationToIsoSurface1(self):
		"""Sets the representation to IsoSurface1

		This method can be used to change the representation of the
		object to IsoSurface1. If the object is already represented
		by an IsoSurface2 this avatar is removed.
		"""
		try:	# Does isosurface2 exist ? 
			# Yes, remove it		
			self.RemoveAvatar(self.GetIsoSurface2())
		except AttributeError: # No, do nothing
			pass
		# Add isosurface1 avatar
		self.AddIsoSurface1()

	def SetRepresentationToIsoSurface2(self,contourvalues):
		"""Sets the representation to isosurface2

		This method can be used to change the representation of the
		object to IsoSurface2. It the object is already represented
		by an IsoSurface1, this avatar is removed. 
		"""
		try:	# Does isosurface1 already exist ?
			# Yes, remove it
			self.RemoveAvatar(self.GetIsoSurface1()) 
		except AttributeError: # No, do nothing
			pass
		# Add isosurface2 avatar
		self.AddIsoSurface2(contourvalues)

	def GetTranslation(self):
		"""Return the translation"""
		try:	
			return self._translation
		except AttributeError:
			return (0,0,0)
	
	def SetTranslation(self,translation):
		"""Sets the translation

		This method can be used for translating the "window" in which
		the isosurfaces of the 3D grid are visualized. The
		window has the size of a single unit cell. The translation 
		must be specified in terms of the FFT grid points. Default is
		(0,0,0).
		
		**An Example**

 		'>>>plot.SetTranslation((22,-10,30))'

		will translate the "window" by (22,-10,30) according to the 
		FFT grid. 
		"""

		self._translation=translation
		self.UpdateVTKData()

	def GetPeriods(self):
		"""Returns the number of periods"""
		try:
			return self._periods
		except AttributeError:
			return (1,1,1)

	def SetPeriods(self,periods):
		"""Sets the number of periods

		This method specifies the number of times the grid is 
		repeated. Default is (1,1,1), i.e. meaning that only the 
		grid within the unit cell at the origin is retained. 

		**An example** 

		'>>>plot.SetPeriods((2,2,1))'

		will repeat the grid by 2x2x1 according to the unit cell.
		"""
		self._periods=periods
		self.UpdateVTKData()

	def SetColorRange(self,colorrange):
		"""Sets the colorrange

		This method can be used to set the colorrange. This interval
		specifies the range of the colortable. Scalar values greater
		than the maximum are clamped to the maximum value and scalar
		values smaller than the minimum are clamped to the minimum
		value. 
		"""
		self.ColorRange=colorrange
		# Propating the changes to the child avatars
		try:
			self.GetIsoSurface1().SetColorRange(colorrange)
		except AttributeError:
			pass
		try:
			self.GetIsoSurface2().SetColorRange(colorrange)
		except AttributeError:
			pass

	def GetColorRange(self):
		"""Returns the colorrange"""
		return self.ColorRange

	def SetColorTable(self,colortable):
		"""Sets the colortable

		This method can be used to set the colortable which can either
		be an instance of 'vtkLookupTable' or 'ColorTableSource' . The
		colortable will automatically be used by all the child avatars
		involving the visualization of the grid.
		"""
		self.ColorTable=colortable
		# Propagating the changes to the child avatars
		try:
			self.GetIsoSurface1().SetColorTable(colortable)
		except AttributeError:
			pass
		try:
			self.GetIsoSurface2().SetColorTable(colortable)
		except AttributeError:
			pass

	def GetColorTable(self):
		"""Returns the instance of the colortable"""
		try:
			return self.ColorTable
		except AttributeError:
			self.ColorTable=ColorTableSource()
			return self.ColorTable

	def RemoveAvatar(self,avatar):
		"""Removes an avatar. Reimplemented from vtkAvatar"""
		# loop over avatarattributes
		for avatarattr in ['isosurface1','isosurface2','outline']:
			# is the attribute defined ?
			if hasattr(self,avatarattr):
				# Yes: is the attribute the same as avatar ?
				if avatar==getattr(self,avatarattr):
					# Yes, delete it
					delattr(self,avatarattr)

		# Removing the avatar from the avatarlist
		vtkAvatar.RemoveAvatar(self,avatar)

	def GetVTKData(self):
		"""Returns the instance of vtkdata reader"""
		return self._vtkdata

	def GetvtkStructuredGrid(self):
		"""Returns the instance of vtkStructuredGrid"""
		return self.GetVTKData().GetvtkStructuredGrid()


class vtkScalarGrid3D(vtkAvatar,_vtkGrid3DParent_):
	"""Class for visualizing a 3D grid

	To create an instance of this class write:
	
	'>>>avatar=vtkScalarGrid3D(grid)'

	where 'grid' is an instance of 'Simulations.Dacapo.Grid' or any derived
	class having a 3D vectorspace. 

	This class acts as a container for concrete implementations for 
	visualizing the grid. These include visualizing the grid with 
	isosurfaces,  an outline and planes. 

	'vtkScalarGrid3D' may be initialized in two different ways:

	* Contourvalues specified: vtkGrid3DIsoSurface2 is added to the avatar
	list. It shows isosurfaces of the scalar grid at the contourvalues.

	* Contourvalues not specified: 'vtkGrid3DIsoSurface1' is added to the
	avatar list. It will show the scalar grid by 10 evenly spaced 
	isosurfaces within the value range of the array.

	'vtkScalarGrid' has a wide range of methods for combining different 
	VTK avatars and manipulating the rendering process.
	"""

	def __init__(self,scalargrid,parent=None,**keywords):
		# vtkStructuredGridFromGrid3D used as data reader 
		_vtkGrid3DParent_.__init__(self,vtkdata=vtkStructuredGridFromGrid3D())
		self.SetGrid3D(scalargrid)
		self.SetColorRange(self.GetGrid3D().GetValueRange())
		# Setting the value for contourvalues:
		contourvalues=None # Default for contourvalues is None
		if keywords.has_key('contourvalues'):
			contourvalues=keywords['contourvalues']
			del keywords['contourvalues']
		apply(vtkAvatar.__init__,[self,parent],keywords)
		if contourvalues is not None: # Are contourvalues set ? 
			# Yes, add the surfaces
			self.AddIsoSurface2(contourvalues) 
		else:
			# No, add 10 surfaces within the valuerange
			self.AddIsoSurface1()
		# Reseting the camera to obtain a proper view and rendering
		# to include the added isosurface, if parent not specified
		if parent is None:
			# First propagate new actor to property assembly
			self.UpdatePropAssembly()
			try: # Does the window support ResetCamera ? 
				self.GetWindow().ResetCamera()
			except AttributeError: # Else, do nothing
				pass
			# Finally propagate changes to the window
			self.Render()

	def SetGrid3D(self,grid3D):
		"""Sets the grid"""
		self._grid3D=grid3D

	def GetGrid3D(self):
		"""Returns the grid"""
		return self._grid3D

	def SetColorRange(self,colorrange):
		"""Sets the colorrange

		Reimplemented from '_vtkGrid3DParent_' .
		"""
		_vtkGrid3DParent_.SetColorRange(self,colorrange)
		if hasattr(self,'planes'):
			for plane in self.planes:
				plane.SetColorRange(colorrange)

	def SetColorTable(self,colortable):
		"""Sets the colortable

		Reimplemented from '_vtkGrid3DParent_'
		"""
		_vtkGrid3DParent_.SetColorTable(self,colortable)
		if hasattr(self,'planes'):
			for plane in self.planes:
				plane.SetColorTable(colortable)

	def RemoveAvatar(self,avatar):
		"""Removes an avatar. Reimplemented from _vtkGrid3DParent_"""
		# checking the planes 
		if hasattr(self,'planes'):
			if avatar in self.planes:
				self.planes.remove(avatar)
		_vtkGrid3DParent_.RemoveAvatar(self,avatar)

	def Update(self,object=None):
		"""Updates the avatar

		This method can be used if the grid has been changed or 
		modified. It forces the vtk data to be reread and then
		asks all the added avatars to update themselves.
		"""
		if object is not None:
			self.SetGrid3D(object)
		self.UpdateVTKData()
		vtkAvatar.Update(self)

	def UpdateVTKData(self):
		"""Read vtk data from grid"""
		# Repeating and translating the grid
		grid=self.GetGrid3D().Repeat(list(self.GetPeriods())).TranslateCoordinates(list(self.GetTranslation()),'passive')
		# Converting resulting grid to vtkStructuredGrid
		self.GetVTKData().ReadFromGrid3D(grid)

	def AddIsoSurface1(self):
		"""Adds an vtkGrid3DIsoSurface1 avatar

		This method can be used to add isosurfaces to the 
		avatar list. It will generate a given number of evenly spaced
		isosurfaces within a specified interval. The default number of
		isosurfaces is 10 and the default interval is the valuerange of
		the grid. For more information refer to the documentation for
		'vtkGrid3DIsoSurface1' .
		"""
		try:	# Does isosurface1 already exist?
			isosurface1=self.GetIsoSurface1()
		except AttributeError: # No, create a new one
			isosurface1=vtkGrid3DIsoSurface1(vtkstructuredgrid=self.GetvtkStructuredGrid(),parent=self)	
		# Propagate the colortable and the colorrange
		isosurface1.SetColorTable(self.GetColorTable())
		isosurface1.SetColorRange(self.GetColorRange())
		# The avatar is kept as isosurface1
		self._SetIsoSurface1(isosurface1)

	def AddIsoSurface2(self,contourvalues):
		"""Adds an vtkGrid3DIsoSurface2 avatar

		This method can be used to add isosurfaces to the avatar list.
		It will generate isosurfaces according to the specified 
		contourvalues. For more information refer to the documentation
		for 'vtkGrid3DIsoSurface2' .
		"""
		try:	# Does isosurface2 already exist?
			isosurface2=self.GetIsoSurface2()
			isosurface2.SetContourValues(contourvalues)
		except AttributeError: 	# No, add it
			isosurface2=vtkGrid3DIsoSurface2(contourvalues,vtkstructuredgrid=self.GetvtkStructuredGrid(),parent=self)
		# Propagate colortable and colorrange
		isosurface2.SetColorTable(self.GetColorTable())
		isosurface2.SetColorRange(self.GetColorRange())
		# The avatar is kept as isosurface2
		self._SetIsoSurface2(isosurface2)
		
	def AddPlane(self,normal=None,origin=None):
		"""Adds an vtkGrid3DPlane avatar

		This method can be used to add a plane to the avatar list.
		For more information refer to the documentation for
		'vtkGrid3DPlane' .
		"""
		plane=vtkGrid3DPlane(normal,origin,vtkstructuredgrid=self.GetvtkStructuredGrid(),parent=self)
		# Propagate the colortable and colorrange
		plane.SetColorTable(self.GetColorTable())
		plane.SetColorRange(self.GetColorRange())
		# If a planelist does not exist, define it
		if not hasattr(self,'planes'):
			self.planes=[]
		# Add the new plane to the plane list
		self.planes.append(plane)


class vtkNumericArray(vtkScalarGrid3D): 
	""" Class for visualizing a Numeric 3-dimensional array 
	 
        To create an instance of this class use: 

        >>> avatar = vtkNumericArray(array)
        """ 

        def __init__(self,array,unitcell,parent=None,**keywords):

                self.SetNumericArray(array)
                self.SetUnitCell(unitcell)

                # None is used as grid, it is automatically set in
                # the new implementation of GetGrid3D
                apply(vtkScalarGrid3D.__init__,[self,None,parent],keywords)
       
	def SetNumericArray(self,array): 
		self.array = array 

        def GetNumericArray(self): 
                return self.array

        def SetUnitCell(self,unitcell): 
                self.unitcell = unitcell

        def GetUnitCell(self): 
                return self.unitcell

        def GetGrid3D(self):
                """Reimplemented from vtkScalarGrid3D"""

                origin = None

                # translate ase2 unitcell to a VectorSpace unitcell
                vectorspace = BravaisLattice()
                vectorspace.SetBasis(self.GetUnitCell())

                grid3d=Grid(space=vectorspace,origin=origin)
                grid3d.SetGridValues(self.GetNumericArray()) 
                self.SetGrid3D(grid3d)
                return vtkScalarGrid3D.GetGrid3D(self)


class vtkElectronDensity(vtkScalarGrid3D):
	"""Class for visualizing an ElectronDensity

	To create an instance of this class use:

	'>>>avatar=vtkElectronDensity(electrondensity)'

	where 'electrondensity' is an instance of 
	'Simulations.Dacapo.ElectronDensity' . 
	"""

	def __init__(self,electrondensity,parent=None,**keywords):
		self.SetElectronDensity(electrondensity)
		# Setting default visualization mode
		self.visualizationmode = 0
		# None is used as grid, it is automatically set in 
		# the new implementation of GetGrid3D
		apply(vtkScalarGrid3D.__init__,[self,None,parent],keywords)

	def SetElectronDensity(self,electrondensity):
		"""Sets the electron density"""
		self._electrondensity=electrondensity

	def GetElectronDensity(self):
		"""Returns the electron density"""
		return self._electrondensity

	def GetGrid3D(self):
		"""Reimplemented from vtkScalarGrid3D"""
		if self.visualizationmode == 0:
			grid3d=self.GetElectronDensity().GetElectronDensityGrid()
		if self.visualizationmode == 1:
			grid3d=self.GetElectronDensity().GetSpinUpGrid()
		if self.visualizationmode == 2:
			grid3d=self.GetElectronDensity().GetSpinDownGrid()
		if self.visualizationmode == 3:
			grid3d=self.GetElectronDensity().GetSpinDensityGrid()
		self.SetGrid3D(grid3d)
		return vtkScalarGrid3D.GetGrid3D(self)

	def SetVisualizationMode(self,mode=0):
                self.visualizationmode=mode
		# Propagate changes to VTK
		self.UpdateVTKData()

        def GetVisualizationMode(self):
                return self.visualizationmode

        def SetVisualizationModeSpinUp(self):
                self.SetVisualizationMode(mode=1)

        def SetVisualizationModeSpinDown(self):
                self.SetVisualizationMode(mode=2)

        def SetVisualizationModeSpinDensity(self):
                self.SetVisualizationMode(mode=3)

	def Update(self,object=None):
		"""Reimplemented from vtkScalarGrid3D"""
		if object is not None:
			self.SetElectronDensity(object)
		vtkScalarGrid3D.Update(self)


class vtkPotential(vtkScalarGrid3D):
	"""Class for visualizing a Potential (Effective or Electrostatic) 

	To create an instance of this class use:

	'>>>avatar=vtkEffectivePotential(effectivepotential=effectivepotential)'
	where 'effectivepotential' is an instance of
	'Simulations.Dacapo.EffectivePotential', 

        or use 
	avatar=vtkElectrostaticPotential(effectivepotential=effectivepotential)'
        where 'effectivepotential' is an instance of
        'Simulations.Dacapo.ElectrostaticPotential.

	"""

	def __init__(self,potential,contourvalues=None,parent=None):
		self.SetPotential(potential)
		# Setting the default visualization mode
		self.visualizationmode=0
		# None is used as grid, it is automatically set in the
		# new implementation of GetGrid3D
		vtkScalarGrid3D.__init__(self,scalargrid=None,contourvalues=contourvalues,parent=parent)

	def SetPotential(self,potential):
		"""Sets the effective potential"""
		self.potential=potential

	def GetPotential(self):
		"""Returns the potential"""
		return self.potential

	def GetGrid3D(self):
		"""Reimplemented from vtkScalarGrid3D"""
		if self.GetVisualizationMode()==0:
			grid3d=self.GetPotential().GetPotentialGrid()
		elif self.GetVisualizationMode()==1:
			grid3d=self.GetPotential().GetPotentialSpinUp()
		elif self.GetVisualizationMode()==2:
			grid3d=self.GetPotential().GetPotentialSpinDown()
		self.SetGrid3D(grid3d)
		return vtkScalarGrid3D.GetGrid3D(self)

	def SetVisualizationMode(self,mode=0):
		"""Sets the visualization mode

		The default visualization mode it the total effective
		potential.
		"""
		self.visualizationmode=mode

	def GetVisualizationMode(self):
		"""Returns the visualization mode"""
		return self.visualizationmode

	def SetVisualizationModeSpinUp(self):
		"""Sets the visualization mode to spin up."""
		self.SetVisualizationMode(mode=1)

	def SetVisualizationModeSpinDown(self):
		"""Sets the visualization mode to spin down."""
		self.SetVisualizationMode(mode=2)

	def Update(self,object=None):
		"""Reimplemented from vtkScalarGrid3D"""
		if object is not None:
			self.SetPotential(object)
		vtkScalarGrid3D.Update(self)	

class _vtkGrid3DChild_:
	"""Mix-in class for child avatars"""

	def __init__(self,grid3D=None,vtkstructuredgrid=None):
		if grid3D is not None:
			self.SetGrid3D(grid3D)
			# defining the data reader
			self._vtkdata=vtkStructuredGridFromGrid3D()
		elif vtkstructuredgrid is not None:
			self.SetvtkStructuredGrid(vtkstructuredgrid)
		else:
			raise NameError, "grid3D or vtkStructuredGrid must be defined"

	def SetGrid3D(self,grid):
		"""Sets the 3D grid"""
		self._grid=grid

	def GetGrid3D(self):
		"""Returns the 3D grid"""
		return self._grid

	def SetvtkStructuredGrid(self,vtkstructuredgrid):
		"""Sets the vtkStructuredGrid"""
		self._vtkgrid=vtkstructuredgrid

	def GetvtkStructuredGrid(self):
		"""Returns the vtkStructuredGrid"""
		# Does a grid3D exist ?
		# Note: If both _grid and _vtkgrid exits _grid is used.
		if hasattr(self,'_grid'):
			# Yes, return the corresponding grid3D
			return self.GetVTKData().GetvtkStructuredGrid()
		else:
			# No, return structured grid which has been set
			# externally. 
			return self._vtkgrid

	def GetValueRange(self):
		"""Returns the value range

		Depending on the situation this method will return either the
		value range of the grid or the vtkStructuredGrid.
		"""
		if hasattr(self,'_grid'): # Is a grid defined ?
			return self.GetGrid3D().GetValueRange()
		else: # else use the structuredgrid
			return self.GetvtkStructuredGrid().GetScalarRange()
			
	def Update(self,object=None):
		"""Updates the avatar

		If the class was initializaed with a grid, it is forced to be 
		reread. Then the child avatars are asked to update themselves.
		"""
		# Is the grid set ?
		if hasattr(self,'_grid'): # Yes, update the vtkStructuredGrid
			self.GetVTKData().ReadFromGrid3D(self.GetGrid3D())
		# Update child avatars
		vtkAvatar.Update(self)

	def GetVTKData(self):
		"""Returns the vtk data reader"""
		return self._vtkdata

class vtkGrid3DIsoSurface1(_vtkGrid3DChild_,IsoSurfaceSource,vtkAvatar):
	"""Class for visualizing the isosurfaces of a 3D Grid/vtkStructuredGrid
	
	An instance may be created in two different ways by 
	either specifying  

	* an instance of 'Structures.Grid' or any derived class
	* a vtkStructuredGrid

	The visualized isosurfaces will be evenly distributed within a 
	specified interval, default is the value range of the grid or
	vtkStructuredGrid. The number of isosurfaces may also be changed, 
	default is 10. In addition 'vtkGrid3DIsoSurface1' has a wide range of 
	methods for combining different VTK avatars and manipulating the 
	rendering process. 
	
	Note that this class does not support any methods for
	neither translating nor repeating the grid/vtkStructuredGrid. Hence 
	it is suitable for visualization of non-periodic data. 
	"""

	def __init__(self,grid3D=None,vtkstructuredgrid=None,parent=None):
		_vtkGrid3DChild_.__init__(self,grid3D=grid3D,vtkstructuredgrid=vtkstructuredgrid)
		IsoSurfaceSource.__init__(self,self.GetvtkStructuredGrid())
		self.SetColorRange(self.GetValueRange())
		self.CreatePipeLine()
		vtkAvatar.__init__(self,parent)

	def CreatePipeLine(self):
		"""Creates the VTK pipeline."""
		self.SetIsoSurface1(self.GetContourRange(),self.GetNumberOfContours())
		self.SetMapper(self.GetColorRange())
		self.SetActor()
		self.GetActorProperty().SetOpacity(1.0/self.GetNumberOfContours())

	def SetContourRange(self,contourrange):
		"""Sets the contour range.

		This method can be used to set the range of the isosurfaces.
		The isosurfaces will be evenly distributed within this 
		interval. The default is the value range of the scalars
		constituting the grid/vtkStructuredGrid.
		"""
		self.ContourRange=contourrange
		# Piping the data on to VTK
		self.SetIsoSurface1(contourrange,self.GetNumberOfContours())

	def GetContourRange(self):
		"""Returns the contour range"""
		if hasattr(self,'ContourRange'):
			return self.ContourRange
		else:	# If nothing has been specified:
			try:	# If grid exists return the value range
				contourrange=self.GetGrid3D().GetValueRange()
			except AttributeError:
				# else return contourrange of structuredgrid
				contourrange=self.GetvtkStructuredGrid().GetScalarRange()
			return contourrange

	def SetNumberOfContours(self,ncontours):
		"""Sets the number of contours

		This method can be used to set the number of contours within
		the contour range. Default is 10. 
		"""
		self.NContours=ncontours
		# Piping the data on to VTK
		self.SetIsoSurface1(self.GetContourRange(),ncontours)

	def GetNumberOfContours(self):
		"""Returns the number of contours"""
		if hasattr(self,'NContours'):
			return self.NContours
		else:
			return 10

class vtkGrid3DIsoSurface2(vtkAvatar,IsoSurfaceSource,_vtkGrid3DChild_):
	"""Class for visualizing the isosurfaces of a 3D grid/vtkStructuredGrid

	An instance of this class may be initialized in two different way by
	either specifying 

	* an instance of 'Structures.Grid' or any derived class
	* vtkStructuredGrid

	The visualized isosurfaces will be generated according to the specified
	contour list. 'vtkGrid3DIsoSurface2' has a wide range of methods for
	combining different VTK avatars and manipulating the rendering 
	process.

	Note that this class does not support any methods for neither 
	translating nor repeating the grid/vtkStructuredGrid. Hence it is 
	suitable for visualizing non-periodic data. 
	"""
	def __init__(self,contourvalues,grid3D=None,vtkstructuredgrid=None,parent=None):
		_vtkGrid3DChild_.__init__(self,grid3D=grid3D,vtkstructuredgrid=vtkstructuredgrid)
		IsoSurfaceSource.__init__(self,self.GetvtkStructuredGrid())
		self.SetContourValues(contourvalues)
		self.SetColorRange(self.GetValueRange())
		self.CreatePipeLine()
		vtkAvatar.__init__(self,parent)

	def CreatePipeLine(self):
		"""Creates the VTK pipeline"""
		self.SetIsoSurface2(self.GetContourValues())
		self.SetMapper(self.GetColorRange())
		self.SetActor()
		self.GetActorProperty().SetOpacity(1.0/len(self.GetContourValues()))

	def SetContourValues(self,contourvalues):
		"""Sets the contour values

		This method can be used to set the isosurface values. 
		"""
		self.Contourvalues=contourvalues
		self.SetIsoSurface2(contourvalues)

	def GetContourValues(self):
		"""Returns the contour list"""
		return self.Contourvalues


class vtkGrid3DPlane(vtkAvatar,PlaneSource,_vtkGrid3DChild_):
	"""Class for visualizing a plane of a 3D grid/vtkStructuredGrid

	An instance of this class may be initialized in two different way be
	either specifying

	* an instance of 'Structures.Grid' or any derived class
	* vtkStructuredGrid

	The plane will be generated according to the specified normal and 
	origin. Defaults are (0,0,1) and the center of the 
	grid/vtkStructuredGrid respectively.

	Note that this class does not support any methods for neither 
	translating nor repeating the grid/vtkStructuredGrid. Hence it is 
	suitable for visualizing non-periodic data. 
	"""

	def __init__(self,normal=None,origin=None,grid3D=None,vtkstructuredgrid=None,parent=None):
		_vtkGrid3DChild_.__init__(self,grid3D=grid3D,vtkstructuredgrid=vtkstructuredgrid)
		PlaneSource.__init__(self,self.GetvtkStructuredGrid())
		if normal is not None:
			self.SetNormal(normal)
		if origin is not None:
			self.SetOrigin(origin)
		self.SetColorRange(self.GetValueRange())
		self.CreatePipeLine()
		vtkAvatar.__init__(self,parent)

	def CreatePipeLine(self):
		"""Creates the VTK pipeline"""
		self.SetSinglePlane(self.GetNormal(),self.GetOrigin())
		self.SetMapper(self.GetColorRange())
		self.SetActor()
		
	def GetNormal(self):
		"""Returns the plane normal"""
		try:
			return self.Normal
		except AttributeError:
			return (0.0,0.0,1.0)

	def SetNormal(self,normal):
		"""Sets the plane normal

		This method can be used to set the plane normal. Default is
		(0,0,1).
		"""
		self.Normal=normal
		# Piping the changes on to VTK
		self.SetSinglePlane(self.GetNormal(),self.GetOrigin())

	def GetOrigin(self):
		"""Returns the origin of the plane"""
		try:
			return self.Origin
		except AttributeError:
			return self.GetvtkStructuredGrid().GetCenter()

	def SetOrigin(self,origin):
		"""Sets the origin of the plane

		This method can be used to the origin of the plane. Default
		is the center of the grid/vtkStructuredGrid.
		"""
		self.Origin=origin
		# Piping the changes on to VTK
		self.SetSinglePlane(self.GetNormal(),self.GetOrigin())











