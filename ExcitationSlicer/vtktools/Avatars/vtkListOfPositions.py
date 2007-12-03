"""Module containing the class for visualizing a list of positions and a scalar"""
from ASE.Visualization.VTK.Avatars.vtkAvatar import vtkAvatar
from ASE.Visualization.VTK.GlyphSource import SphereSource
from ASE.Visualization.VTK.vtkDataFromObject import vtkPolyDataFromListOfPositionsScalars

class vtkListOfPositions(SphereSource,vtkAvatar):
	"""Class representing a list of positions and a scalar.

        The list of positions will be visualized with a sphere placed at each
	of the positions. The radius of the sphere is scaled according to the
	scalar. Note also, that the scalars associated with each of the
	positions need not be equal. In this case a list of scalars
	('SetListOfScalars') should be specified.

        To create an instance of this class write:
        
        'myavatar=vtkListOfPositions(listofpositions,scalar=scalar)'

        where 'listofpositions' is a sequence of (three-dimensional) vectors.
        'scalar' should be a float. Also note that a scalar and a list of
	scalars cannot be set simultaneously.
	"""

	def __init__(self,listofpositions,scalar=None,listofscalars=None,parent=None,**keywords):
		self.SetListOfPositions(listofpositions)
		# Either scalars or listofscalars must be specified:
		if (scalar==None) and (listofscalars==None):
			raise TypeError, "Either scalar or listofscalars must be set."
		if listofscalars is not None:
			# Using the method will force an (unwanted) update
			self.listofscalars=listofscalars
		elif scalar is not None:
			self.scalar=scalar
		# End initializing scalars.
		# Setting the color
		if keywords.has_key('color'):
			self.Color=keywords['color']
		resolution=None
		if keywords.has_key('resolution'):
			resolution=keywords['resolution']
		SphereSource.__init__(self,self.GetVTKData().GetvtkPolyData(),resolution=resolution)
		self.CreatePipeLine()
                # Constructing keywords:
                keywords['parent']=parent
		apply(vtkAvatar.__init__,[self],keywords)

	def CreatePipeLine(self):
		"""Creating the VTK pipeline."""
		self.SetVTKSpheres()
		self.SetMapper()
		self.SetActor()
		# Finally, propagating the colors
		self.GetActorProperty().SetColor(self.GetColor())

        def SetListOfPositions(self,listofpositions):
		"""Sets the list of positions

		'listofpositions' is expected to be a sequence of
		three-dimensional vectors.
		"""
		self.lopositions=listofpositions

        def GetListOfPositions(self):
		"""Returns the list of positions"""
		return self.lopositions

        def SetScalar(self,scalar):
		"""Sets the scalar.

		This scalar will correspond to the radius of the spheres.
		"""
		self.scalar=scalar
		# Propagate changes:
		self.UpdateVTKData()

	def GetScalar(self):
		"""Returns the scalar value"""
		return self.scalar

	def SetListOfScalars(self,listofscalars):
		"""Sets the list of scalars.

		This list specifies a scalar value to each position. Its length
		must correspond to the number of positions. Note, that if only
		a single scalar value (see 'SetScalar') has been set the list
		of scalars will automatically be a list containing this value
		only. If both the attributes 'scalar' and 'listofscalars' have
		been set the 'listofscalars' will be used.
		"""
		# Number of scalars must correspond to number of positions
		if len(self.GetListOfPositions)!=len(listofscalars):
			raise ValueError, "Number of scalars must equal number of positions"
		self.listofscalars=listofscalars
		# Propagate changes:
		self.UpdateVTKData()

	def GetListOfScalars(self):
		"""Returns the list of scalars.

		The list will correspond to the number of positions. If a list
		of scalars has not been set this method will return a list
		containing replicated scalars defined via the method
		'SetScalar'.  
		"""
		if not hasattr(self,'listofscalars'):
			return [self.GetScalar()]*len(self.GetListOfPositions())
		return self.listofscalars

	def GetColor(self):
            """Returns the color of the atoms

            The color is specified according to the (R,G,B)-scale. Default
            is white, (R,G,B)=(1,1,1). 
            """
            if not hasattr(self,'Color'):
                return (1,1,1) # default value
            return self.Color

	def SetColor(self,color=None):
            """Sets the color of the atoms

            This method can be used to change the color of the spheres. The
            color is specified according to the (R,G,B)-scale.
            """
            self.Color=color
            # Propagating change to actor property
            r,g,b=color		
            self.GetActorProperty().SetColor(r,g,b)

	def UpdateVTKData(self):
            """Internal method. Converts the list of positions to vtkPolyData"""
            listofpositions=self.GetListOfPositions()
            self.GetVTKData().ReadFromPositionsScalars(listofpositions,self.GetListOfScalars())

	def GetVTKData(self):
            """Internal method. Returns the instance of vtkPolyDataFromListOfPositionsScalars"""
            if not hasattr(self,'_vtkdata'): # Define vtkdata converter
                self._vtkdata=vtkPolyDataFromListOfPositionsScalars()
            return self._vtkdata

	def Update(self,object=None):
            """Reimplemented from vtkAvatar

	    If 'object' is a list of positions, it will replace the existing
	    list of positions and update the window afterwards. 
	    """
	    if object is not None:
		    self.SetListOfPositions(object)
            self.UpdateVTKData()
            vtkAvatar.Update(self) 

