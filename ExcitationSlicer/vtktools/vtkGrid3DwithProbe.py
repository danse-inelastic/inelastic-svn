from vtktools.Avatars.vtkAvatar import vtkAvatar
from vtktools.Avatars.vtkOutline import vtkOutline
from vtktools.IsoSurfaceSource import IsoSurfaceProbeSource
from vtktools.vtkDataFromObject import vtkStructuredGridsFromGrid3DProbeArray
from vtktools.Avatars.vtkGrid3D import _vtkGrid3DChild_,_vtkGrid3DParent_

from Numeric import pi

class _vtkGrid3DProbeChild_(_vtkGrid3DChild_):
	"""Mix-in class for child avatars"""

	def __init__(self,grid3D=None,probe=None,vtkgrid=None,vtkprobe=None):
		if (grid3D is not None) and (probe is not None):
			self.SetGrid3D(grid3D)
			self.SetProbeArray(probe)
			self._vtkdata=vtkStructuredGridsFromGrid3DProbeArray()
		elif (vtkgrid is not None) and (vtkprobe is not None):
			self.SetvtkStructuredGrid(vtkgrid)
			self.SetvtkStructuredGridProbe(vtkprobe)
		else:
			raise NameError, "(grid3D,probe) or (vtkgrid,vtkprobe) must be defined"

	def GetProbeArray(self):
		"""Returns the probe for the grid"""
		return self._probearray

	def SetProbeArray(self,probearray):
		"""Sets the probe for the grid"""
		self._probearray=probearray

	def GetProbeValueRange(self):
		"""Returns the value range of the probe"""
		# Does the probearray exist ?
		if hasattr(self,'_probearray'): # Yes, return the value range
			probearray=self.GetProbeArray().flat
			return min(probearray),max(probearray)
		else:	# No, return the range of the vtkprobe
			return self.GetvtkStructuredGridProbe().GetScalarRange()

	def SetvtkStructuredGridProbe(self,vtkprobe):
		"""Set the vtkStructuredGrid used as probe"""
		self._vtkprobe=vtkprobe			

	def GetvtkStructuredGridProbe(self):
		"""Returns the vtkStructuredGrid used as probe"""
		if hasattr(self,'_probearray'):	# Does a probearray exist ?
			# Yes, return the corresponding grid3D
			return self.GetVTKData().GetvtkStructuredGridProbe()
		else:
			# No, return structured grid which has been set
			# externally.
			return self._vtkprobe
			
	def Update(self,object=None):
		"""Updates the avatar

		If the class was initialized with a (grid,probearray) they are
		forced to be reread. Then the child avatars are forced to
		update themselves.
		"""
		try: # Is the grid and probearray defined ?
			self.GetGrid3D()
			self.GetProbeArray()
		except AttributeError: # No, do nothing
			pass
		else:	# Yes, update the vtkstructuredgrids
			self.GetVTKData().ReadFromGrid3DProbeArray(self.GetGrid3D(),self.GetProbeArray())
		# Updating added avatars
		vtkAvatar.Update(self)


class vtkGrid3DProbeIsoSurface1(vtkAvatar,IsoSurfaceProbeSource,_vtkGrid3DProbeChild_):
	"""Class for visualizing the isosurfaces of a 3D grid with a probe

	An instance may be initialized in two different ways by either 
	specifying

	* an instance of 'Structures.Grid' or any derived class for contouring 
	and a NumPy array for probing the contours.

	* two vtkStructuredGrids for contouring and probing the contours 
	respectively.

	The visualized isosurfaces will be evenly distributed within a 
	specified interval, default is the value range of the grid or the 
	vtkStructuredGrid used for contouring. The number of isosurfaces
	may also be changed, default is 10. In addition 
	'vtkGrid3DProbeIsoSurface1' has a wide range of methods for combining
	different VTK avatars and manipulating the rendering process.

	Note that this class does not support any methods for neither 
	translating not repeating the (grid,probearray)/vtkStructuredGrids.
	Hence it is suitable for visualization of non-periodic data.
	"""

	def __init__(self,grid3D=None,probe=None,vtkgrid=None,vtkprobe=None,parent=None):
		_vtkGrid3DProbeChild_.__init__(self,grid3D=grid3D,probe=probe,vtkgrid=vtkgrid,vtkprobe=vtkprobe)
		IsoSurfaceProbeSource.__init__(self,self.GetvtkStructuredGrid(),self.GetvtkStructuredGridProbe())
		self.SetColorRange(self.GetProbeValueRange())
		self.CreatePipeLine()
		vtkAvatar.__init__(self,parent)

	def CreatePipeLine(self):
		"""Creates the VTK pipeline."""
		self.SetIsoSurface1(self.GetContourRange(),self.GetNumberOfContours())
		self.SetMapper(self.GetColorRange())
		self.SetActor()
		self.GetActorProperty().SetOpacity(0.1)

	def SetContourRange(self,contourrange):
		"""Sets the contour range

		This method can be used to set the range of the isosurfaces.
		The isosurfaces will be evenly distributed within this
		interval. The default is the value range of the grid or the
		vtkStructuredGrid used for contouring.
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
		# Pipin the data on to VTK
		self.SetIsoSurface1(self.GetContourRange(),ncontours)

	def GetNumberOfContours(self):
		"""Returns the number of contours"""
		if hasattr(self,'NContours'):
			return self.NContours
		else:
			return 10


class vtkGrid3DProbeIsoSurface2(vtkAvatar,IsoSurfaceProbeSource,_vtkGrid3DProbeChild_):
	"""Class for visualizing the isosurfaces of a 3D grid with a probe
	
	An instance may be initialized in two different ways by either 
	specifying 

	* an instance of 'Structures.Grid' or any derived class for contouring
	and a NumPy array for probing the contours.

	* two vtkStructuredGrids for contouring and probing the contours
	respectively.

	The visualized isosurfaces will be generated according to the specified
	contour list. 'vtkGrid3DProbeIsoSurface2' has a wide range of methods
	for combining different VTK avatars and manipulating the rendering
	process.

	Note that this class does not support any methods for neither 
	translating nor repeating the (grid,probearray)/vtkStructuredGrids. 
	Hence it is suitable for visualizing non-periodic data. 
	"""

	def __init__(self,contourvalues,grid3D=None,probe=None,vtkgrid=None,vtkprobe=None,parent=None):
		_vtkGrid3DProbeChild_.__init__(self,grid3D=grid3D,probe=probe,vtkgrid=vtkgrid,vtkprobe=vtkprobe)
		IsoSurfaceProbeSource.__init__(self,self.GetvtkStructuredGrid(),self.GetvtkStructuredGridProbe())
		self.SetContourValues(contourvalues)
		self.SetColorRange(self.GetProbeValueRange())
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


class vtkEigenState(vtkAvatar,_vtkGrid3DParent_):
	"""Class for visualizing an EigenState

	To create an instance of this class write:

	'>>>avatar=vtkWaveFunction(eigenstate)'

	where 'eigenstate' is an instance of the EigenState class. 

	This class acts as a container for concrete implementations for
	visualizing the eigenstate. These include visualizing the eigenstate by
	an outline and isosurfaces. The contours represent isosurfaces of the 
	absolute values of the wave function which are colored according to the
	phase. 

	'vtkEigenState' may be initialized in two different ways

	* Contourvalues specfied: 'vtkGrid3DIsoSurface2' is added to the
	avatar list. It shows isosurfaces of the eigenstate at the 
	contourvalues. 

	* Contourvalues not specified: 'vtkGrid3DIsoSurface1' is added to the
	avatar list. It will show the eigenstate by 10 evenly spaced 
	isosurfaces within the absolute value range of the wave function. 

	'vtkEigenState' has a wide range of methods for combining different 
	VTK avatars and manipulating the rendering process. 
	"""

	def __init__(self,eigenstate,contourvalues=None,parent=None,**keywords):
		self.SetEigenState(eigenstate)
		# Defining the vtkdata reader
		_vtkGrid3DParent_.__init__(self,vtkdata=vtkStructuredGridsFromGrid3DProbeArray())
		# Defining colors and colortable
		self.SetColorRange((-pi,pi))
		self.GetColorTable().SetHSVColors(huerange=[0.0,1.0])
		apply(vtkAvatar.__init__,[self,parent],keywords)
		if contourvalues is not None: # Are contourvalues set ? 
			# Yes, add the surfaces
			self.AddIsoSurface2(contourvalues) 
		else:
			# No, add 10 surfaces within the valuerange
			self.AddIsoSurface1()
		# Reseting the camera to obtain a nice view
		# and rendering the window to include the actor,
		# if parent is not specified
		if parent is None:
			# First propagate new actor to property assembly
			self.UpdatePropAssembly()
			try: # Does the window support reset camera ? 
				self.GetWindow().ResetCamera()
			except AttributeError: # Else, do nothing
				pass
			# Re-render to propagate changes to window
			self.Render()

	def SetEigenState(self,eigenstate):
		"""Sets the eigenstate"""
		self.Eigenstate=eigenstate

	def GetEigenState(self):
		"""Returns the eigenstate"""
		return self.Eigenstate

	def Update(self,object=None):
		if object is not None:
			self.SetEigenState(object)
		self.UpdateVTKData() # reading the vtkstructuredgrids
		vtkAvatar.Update(self) # updating added avatars

	def UpdateVTKData(self):
		"""Reads the vtkStructuredGrids"""
		# Repeating and translating
		eigenstate=self.GetEigenState().Repeat(list(self.GetPeriods())).TranslateCoordinates(list(self.GetTranslation()),'passive')
		# grid3d: the absolute values of the wave function
		grid3d=Grid(space=eigenstate.GetSpace(),origin=eigenstate.GetOrigin())
		#grid3d.SetArray(eigenstate.GetAbsoluteValues())
		grid3d.SetGridValues(eigenstate.GetAbsoluteValues())

		
		# probearray: the phase of the wave function
		probearray=eigenstate.GetPhaseValues()
		
		# Finally, convert to vtkStructuredGrids
		self.GetVTKData().ReadFromGrid3DProbeArray(grid3d,probearray)

	def RemoveAvatar(self,avatar):
		"""Removes the avatar. Reimplemented from _vtkGrid3DParent"""
		_vtkGrid3DParent_.RemoveAvatar(self,avatar)

	def AddIsoSurface1(self):
		"""Adds an vtkGrid3DProbeIsoSurface1 avatar

		This method can used to add isosurfaces to the avatar list. It
		will generate a number of evenly spaced isosurfaces 
		within a specified interval. The default number is 10 and the
		default interval is the valuerange of the grid. For more 
		information refer to the documentation for 
		'vtkGrid3DProbeIsoSurface1' .
		"""
		try: 	# Does the avatar already exist ? 
			isosurface1=self.GetIsoSurface1()
		except AttributeError: # No, create a new one
			isosurface1=vtkGrid3DProbeIsoSurface1(vtkgrid=self.GetVTKData().GetvtkStructuredGrid(),vtkprobe=self.GetVTKData().GetvtkStructuredGridProbe(),parent=self)
		# update the colortable and colorrange
		isosurface1.SetColorTable(self.GetColorTable())
		isosurface1.SetColorRange(self.GetColorRange())
		# Finally, the avatar is kept as isosurface1
		self._SetIsoSurface1(isosurface1)

	def AddIsoSurface2(self,contourvalues):
		"""Adds an vtkGrid3DProbeIsoSurface2 avatar

		This method can be used to add isosurfaces to the avatar list. 
		It will generate isosurfaces according to the specified 
		contour list. For more information refer to the documentation
		for 'vtkGrid3DProbeIsoSurface2' .
		"""
		try:	# Does the avatar already exist ?
			isosurface2=self.GetIsoSurface2()
			isosurface2.SetContourValues(contourvalues)
		except AttributeError: # No, create a new one
			isosurface2=vtkGrid3DProbeIsoSurface2(contourvalues=contourvalues,vtkgrid=self.GetVTKData().GetvtkStructuredGrid(),vtkprobe=self.GetVTKData().GetvtkStructuredGridProbe(),parent=self)
		# update the colortable and the colorrange
		isosurface2.SetColorTable(self.GetColorTable())
		isosurface2.SetColorRange(self.GetColorRange())
		# Finally, the avatar is kept as isosurface2
		self._SetIsoSurface2(isosurface2)

class vtkSTM(vtkAvatar,_vtkGrid3DParent_):

	def __init__(self,stmtool,parent=None,**keywords):
		self.SetSTMTool(stmtool)
		# Defining the vtkdata reader
		_vtkGrid3DParent_.__init__(self,vtkdata=vtkStructuredGridsFromGrid3DProbeArray())
		#vtkAvatar.__init__(self,parent)
		apply(vtkAvatar.__init__,[self,parent],keywords)
		self.SetColorRange(self.GetSTMTool().GetSearchInterval())
		self.GetColorTable().SetRGBColors(['black','red','yellow'])
		# Adding an iso surface of type 1
		self.AddIsoSurface()
		# Reseting the camera to get a nice view
		# and rendering to include the new actor, if parent is not
		# specified
		if parent is None:
			# First propagate changes to propertyassembly
			self.UpdatePropAssembly()
			try: # Does the window support ResetCamera
				self.GetWindow().ResetCamera()
			except AttributeError: # Else do nothing
				pass
			# Re-render to propagate changes to window
			self.Render()

	def SetSTMTool(self,stmtool):
		"""Sets the STM tool"""
		self._stmtool=stmtool

	def GetSTMTool(self):
		"""Returns the STM tool"""
		return self._stmtool

	def SetTranslation(self,translation):
		"""Sets the translation. Reimplemented from _vtkGrid3DParent"""
		# Converting translation to a mutable list
		translation=list(translation)
		if len(translation)!=2:
			raise ValueError, "Translation must be two dimensional"

		normalaxis=self._stmtool.GetNormalAxis()		
		# adding the translation of the normal axis to be zeros. 
		# Due to broken translational symmetry in this direction
		translation[normalaxis:normalaxis]=[0]
		_vtkGrid3DParent_.SetTranslation(self,tuple(translation))

	def SetPeriods(self,periods):
		"""Sets the number of periods. Reimplemented from _vtkGrid3DParent_"""
		# Converting list to a mutable list
		periods=list(periods)
		if len(periods)!=2:
			raise ValueError, "Translation must be two dimensional"
		normalaxis=self._stmtool.GetNormalAxis()		
		# adding the period of the normal axis to be one. 
		# Due to broken translational symmetry in this direction
		periods[normalaxis:normalaxis]=[1]
		_vtkGrid3DParent_.SetPeriods(self,tuple(periods))

	def SetColorTable(self,colortable):
		_vtkGrid3DParent_.SetColorTable(self,colortable)
		# updating the plane
		if hasattr(self,'plane'):
			self.plane.SetColorTable(colortable)

	def Update(self,object=None):
		if object is not None:
			self.SetSTMTool(object)
		# Updating contourvalues:
		contourvalues=[self.GetSTMTool().GetContourValue()]
		try: # Does IsoSurface2 exist ? 
			self.GetIsoSurface2().SetContourValues(contourvalues)
		except AttributeError: # No, do nothing
			pass
		self.UpdateVTKData()
		vtkAvatar.Update(self)

	def UpdateVTKData(self):
		# Using periods and translation
		stmtool=self.GetSTMTool().Repeat(list(self.GetPeriods())).TranslateCoordinates(list(self.GetTranslation()),'passive')
		# Finding grid3d and the probearray
		grid3d=stmtool.GetStrippedGrid()
		probearray=stmtool.GetHeightAbovePlaneGrid()
		# Converting to vtkStructuredGrids
		self.GetVTKData().ReadFromGrid3DProbeArray(grid3d,probearray)

	def RemoveAvatar(self,avatar):
		"""Removes the avatar from avatarlist
		Reimplemented from vtkAvatar
		"""
		if hasattr(self,'plane'): # does the plane exist ?
			if avatar==self.plane: # Yes: is it to be removed ?
				delattr(self,'plane') # Yes: remove the attr
		_vtkGrid3DParent_.RemoveAvatar(self,avatar)
		

	def GetvtkStructuredGridProbe(self):
		"""Returns the vtkStucturedGrid used as probe"""
		return self.GetVTKData().GetvtkStructuredGridProbe()

	def AddIsoSurface(self):
		contour=self.GetSTMTool().GetContourValue()
		# Does the isosurface avatar already exist ?
		try:	# Yes, use it
			isosurface2=self.GetIsoSurface2()
			isosurface2.SetContourValues([contour])
		except AttributeError: # No, create a new one
			isosurface2=vtkGrid3DProbeIsoSurface2(contourvalues=[contour],vtkgrid=self.GetVTKData().GetvtkStructuredGrid(),vtkprobe=self.GetVTKData().GetvtkStructuredGridProbe(),parent=self)
			isosurface2.GetActorProperty().SetOpacity(0.8)
		# Update colortable and colorrange
		isosurface2.SetColorTable(self.GetColorTable())
		isosurface2.SetColorRange(self.GetColorRange())
		# Finally, the avatar is kept as isosurface2
		self._SetIsoSurface2(isosurface2)

	def AddPlane(self,origin):
		from vtktools.Avatars.vtkGrid3D import vtkGrid3DPlane
		from Numeric import identity
		# Does the plane avatar already exist ?
		if hasattr(self,'plane'):
			# Yes, use it
			self.plane.SetOrigin(origin)
		else:	# No, add it
			normal=identity(3)[self.GetSTMTool().GetNormalAxis()]
			self.plane=vtkGrid3DPlane(normal,origin,vtkstructuredgrid=self.GetVTKData().GetvtkStructuredGrid(),parent=self)
			self.plane.SetColorTable(self.GetColorTable())











