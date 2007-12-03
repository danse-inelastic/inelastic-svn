# Written by Mikkel Bollinger (email:mbolling@fysik.dtu.dk) and
# 	     Sune Bahn        (email:bahn@fysik.dtu.dk)      
"""Class for visualizing a vector

To create an instance of this class write:

'>>>avatar=vtkUnitCell(vectors,positions)'

where 'vectors' and 'positions' are lists or NumPy arrays. They are expected
to have the shape, '<positions/vectors>,3' . vtkListOfVectors has a wide range
of methods for adding other VTK avatars and manipulating the rendering 
process. 
"""
from ASE.Visualization.VTK.Avatars.vtkAvatar import vtkAvatar
from ASE.Visualization.VTK.GlyphSource import LineSource
from ASE.Visualization.VTK.vtkDataFromObject import vtkPolyDataFromListOfPositionsVectors

class vtkListOfVectors(LineSource,vtkAvatar):

	def __init__(self,listofvectors,listofpositions,parent=None):
		self.SetPositions(listofpositions)
		self.SetVectors(listofvectors)
		LineSource.__init__(self,self.GetVTKData().GetvtkPolyData())
		self.CreatePipeLine()
		vtkAvatar.__init__(self,parent)

	def CreatePipeLine(self):
		"""Creates the VTK pipeline"""
		self.SetVTKLines()
		self.SetMapper()
		self.SetActor()

	def SetPositions(self,listofpositions):
		"""Sets the positions"""
		self._positions=listofpositions

	def GetPositions(self):
		"""Returns the positions"""
		return self._positions

	def SetVectors(self,listofvectors):
		"""Sets the vectors"""
		self._vectors=listofvectors

	def GetVectors(self):
		"""Returns the vectors"""
		return self._vectors	

	def SetScale(self,scale):
		"""Sets the scale

		This method can be used to set the scale factor by which
		the length of each vector is multiplied.
		"""
		self._scale=scale
		self.UpdateVTKData()

	def GetScale(self):
		"""Returns the scale"""
		if hasattr(self,'_scale'):
			return self._scale
		else:
			return 1

	def UpdateVTKData(self):
		"""Rereads the vtkPolyData"""
		from Numeric import concatenate,array,dot
		import copy
		# The null vector is omitted, can not be plotted
		# concatenating vectors and positions to a single list
		vecpos=concatenate((self.GetPositions(),self.GetVectors()),1)
		filtervecpos=array(filter(lambda vecpos,dot=dot:dot(vecpos[3:6],vecpos[3:6])!=0,vecpos))
		if len(filtervecpos)==0:
			raise ValueError, "All vectors are null-vectors"
		else:
			# Unpacking the filtered list, copied to be contiguous
			filterpos=copy.copy(filtervecpos[:,0:3])
			filtervec=copy.copy(filtervecpos[:,3:6])
			# The vectors scaled by scale
			self.GetVTKData().ReadFromPositionsVectors(filterpos,self.GetScale()*filtervec)

	def GetVTKData(self):
		"""Returns the instance of vtkPolyDataFromListOfPositionsVectors"""
		try:
			return self._vtkdata
		except AttributeError:
			self._vtkdata=vtkPolyDataFromListOfPositionsVectors()
			return self._vtkdata

	def Update(self,object=None):
		"""Updates the avatar

		This method can be used if the input, i.e. the positions or
		the vectors have been changed or modified. It forces the
		vtk data to be reread and afterwards the added avatars are
		asked to update themselves.
		"""
		self.UpdateVTKData()
		vtkAvatar.Update(self) # update childs

