"""Module containing classes for visualizing a ListOfAtoms"""

from ASE.Visualization.VTK.vtkDataFromObject import vtkPolyDataFromListOfPositionsScalars
from ASE.Visualization.VTK.Avatars.vtkAvatar import vtkAvatar
from ASE.Visualization.VTK.Avatars.vtkUnitCell import vtkUnitCell
from ASE.Visualization.VTK.Avatars.vtkListOfPositions import vtkListOfPositions
from ASE.Visualization.VTK.Avatars.vtkListOfVectors import vtkListOfVectors
from ASE.ChemicalElements import Element
from ASE import ListOfAtoms

import copy
import Numeric

class vtkAtoms(vtkAvatar):
	"""Class for visualizing atoms

	This class can be used to visualize the atoms contained in a
	'ListOfAtoms'. The atoms will appear as spheres with a radius
	corresponding to their covalent radius (default).

	To create an instance of this class write:

	'atomavatar=vtkAtoms(listofatoms)'

	where 'listofatoms' is an instance of the class 'ListOfAtoms' . 

	This class acts as a container for avatars representing each atomic
	species in the list of atoms. The properties of the individual species
	avatars can be changed, see the documentation for
	'vtkAtomSpecies' for a complete list.
	"""


	def __init__(self,listofatoms,parent=None,forces=None,**keywords):
		self.SetListOfAtoms(listofatoms)
                self.showforces = forces

		# **NOTE** Keywords are propagated to vtkAvatar
		# Adding parent to the keyword dictionary:
		keywords['parent']=parent
		apply(vtkAvatar.__init__,[self],keywords)

	def GetListOfAtoms(self):
		"""Returns the listofatoms"""
		return self._atomlist
	
	def SetListOfAtoms(self,atomlist):
		"""Sets the listofatoms

		'listofatoms' is expected to be an instance of 'ListOfAtoms'.
		"""
		self._atomlist=atomlist

	def SortAtomListBySpecies(self):
		"""Returns a dictionary with atoms sorted according to species

		The dictionary will have the atomtypes of the different atomic
		species found in the list of atoms as keys. The corresponding
		values will be a list of atoms containing the atoms of the
		given type. 
		"""
		dictofspecies={}
		for atom in self.GetListOfAtoms():
			if dictofspecies.has_key(atom.GetChemicalSymbol()):
				dictofspecies[atom.GetChemicalSymbol()].append(atom.Copy())
			else:
				atomlist=self.GetListOfAtoms().Copy()
				atomlist.data=ListOfAtoms([atom.Copy()])
                                unitcell = copy.copy(atomlist.GetUnitCell())
                                atomlist.data.SetUnitCell(unitcell,fix=True)
				dictofspecies[atom.GetChemicalSymbol()]=atomlist.data
		return dictofspecies

	def GetPeriods(self):
		"""Returns a tuple with the number of periods."""
		try:
			return self.Periods
		except AttributeError:
			return (1,1,1)

	def SetPeriods(self,periods):
		"""Sets the number of periods
		
		This method can be used to specify the number of times the 
		atoms should be repeated. Default is (1,1,1), i.e. 
		corresponding to a single supercell at the origin.

		**An example** 

		'myavatar.SetPeriods([2,2,1])'

		will repeat the atomic configuration by 2x2x1 according to
		the unit vectors of the supercell.
		"""
		self.Periods=tuple(periods)
		# Propagating changes to child avatars
		for speciesavatar in self.GetDictOfSpecies().values():
			speciesavatar.SetPeriods(periods)

	def SetAtomColors(self,color=None):
		"""Sets the colors of atoms.

		This method can be used to set the color of all the atoms. If
		nothing is specified the color will be set according to the
		CPK color scheme. This is also the default color.
		"""
		for speciesavatar in self.GetDictOfSpecies().values():
		    speciesavatar.SetColor(color)

	def RemoveAvatar(self,avatar):
		"""Removes an avatar. Reimplemented from vtkAvatar"""
		atomavatars=self.GetDictOfSpecies()
		# Is the avatar an atomavatar ? 
		if avatar in atomavatars.values():
			# Yes, remove from the dictionary
			index=atomavatars.values().index(avatar)
			avatarkey=atomavatars.keys()[index]
			del atomavatars[avatarkey]
		# Continue remove avatar
		vtkAvatar.RemoveAvatar(self,avatar)

	def Update(self,object=None):
		"""Updates the avatar. Reimplemented from vtkAvatar.

		If 'object' is a list of atoms (instance of 'ListOfAtoms')
		it will replace the original and the window will be updated
		accordingly.

		Note that the 'Update' method will try represent all the atom
		types found in the list of atoms. This means that if a given
		atomic species has been removed from the avatar list, the
		'Update' method will add it again to the avatar list.
		"""
		if object is not None:
			self.SetListOfAtoms(object)

		dictofspecies=self.SortAtomListBySpecies()
		avatars=self.GetDictOfSpecies()

		#remove obsole avatars
		for species in avatars.keys():
		    if species not in dictofspecies.keys():
			self.RemoveAvatar(avatars[species])

		#Update the atomavatars and create new ones if necessary
		for species in dictofspecies.keys():
		    if species not in avatars.keys():
			avatars[species]=vtkAtomSpecies(listofatoms=dictofspecies[species],parent=self,periods=self.GetPeriods())
		    else:
		        avatars[species].SetListOfAtoms(dictofspecies[species])
		vtkAvatar.Update(self)

	def GetDictOfSpecies(self):
		"""Returns a dictionary with the species avatars

		The dictionary is indexed according to the atomic type.
		"""
		if not hasattr(self,'dictofspeciesavatars'):
			self.dictofspeciesavatars={}
		return self.dictofspeciesavatars

class vtkListOfAtoms(vtkAtoms):
    """An ListOfAtoms avatar including unitcell,forces, and velocities.

    This class can be used to visualize a listofatoms (class 'ListOfAtoms').
    The atoms will appear as spheres with a default radius corresponding to
    their covalent radius. The outline of the supercell at the origin will
    also be shown along with forces and velocities (if present) of the
    individual atoms. The latter are visualized as tubes.
    
    To create an instance of this class use:

    'loaavatar=vtkListOfAtoms(listofatoms)'

    where 'listofatoms' is an instance 'ListOfAtoms'. This class acts as a
    container for the avatars representing the list of atoms: each
    species is represented in the avatar list by an instance
    of the class 'vtkAtomSpecies'. The unit cell is represented by
    'vtkUnitCell'. Finally, if forces and/or velocities are present these will
    be represented by the 'vtkForces' and 'vtkVelocities', respectively.
    """

    def SetPeriods(self,periods):
	"""Sets the number of periods. Reimplemented from vtkAtoms

	See documentation for 'vtkAtoms'.
	"""
	# Overloading method from vtkAtoms: Periods need to be set in 
	# forces and velocities provided they exist	
	vtkAtoms.SetPeriods(self,periods)

	loa=self.GetListOfAtoms().Repeat(self.GetPeriods())
	# Propagating changes to forces

	if hasattr(self,'forces'):	# Are there any forces ?
		# Yes, pass the repeated forces
		self.forces.SetPositions(loa.GetCartesianPositions())
		self.forces.SetVectors(loa.GetCartesianForces())
		# Finally update the avatar
		self.forces.UpdateVTKData()

	# Propagating changes to velocities
	if hasattr(self,'velocities'):  # Are there any velocities ?
		# Yes, pass the repeated velocities
		self.velocities.SetPositions(loa.GetCartesianPositions())
		self.velocities.SetVectors(loa.GetCartesianVelocities())
		# Finally update the avatar
		self.velocities.UpdateVTKData()

    def RemoveAvatar(self,avatar):
	"""Removes an avatar from the avatar list. Reimplemented from vtkAtoms"""
	# deleting forces or velocities if necessary
	for avatarattr in ['unitcell','forces','velocities']:
		if hasattr(self,avatarattr):
                        if avatar==getattr(self,avatarattr):
				delattr(self,avatarattr)
	# Continue RemoveAvatar
	vtkAtoms.RemoveAvatar(self,avatar)

    def SetForceScaleFactor(self,factor): 
        self.forcescalefactor = factor	
        self.Update()

    def GetForceScaleFactor(self): 
        if not hasattr(self,'forcescalefactor'): 
            self.SetForceScaleFactor(1.0)
        return self.forcescalefactor


    def AddForces(self):
	"""Add forces to the avatar list

	This method can be used to add forces to the avatar list. If the force
	avatar already exists the positions and vectors are updated.
	"""

        if not self.showforces: 
            return
         
        if sum(self.GetPeriods())==3: 
            # keep forces
	    loa = self.GetListOfAtoms()
        else: 
	    loa=self.GetListOfAtoms().Repeat(self.GetPeriods())

        scale = self.GetForceScaleFactor()
	# Is there a forces avatar ?
	if hasattr(self,'forces'):  # Yes, use it
	   self.forces.SetPositions(loa.GetCartesianPositions())
	   self.forces.SetVectors(loa.GetCartesianForces()*scale)
	else: # No, create a new one
	   self.forces=vtkForces(loa.GetCartesianForces()*scale,
                                 loa.GetCartesianPositions(),self)

    def GetForces(self):
	"""Returns the instance of the force avatar"""
	return self.forces

    def AddVelocities(self):
	"""Add velocities to the avatar list

	This method can be used to add velocities to the avatar list. If the
	velocity avatar already exists its positions and vectors are updated.
	"""
	loa=self.GetListOfAtoms().Repeat(self.GetPeriods())
	# Is there a velocity avatar ?
	if hasattr(self,'velocities'): # Yes, use it
	   self.velocities.SetPositions(loa.GetCartesianPositions())
	   self.velocities.SetVectors(loa.GetCartesianVelocities())
	else: # No, create a new
	   self.velocities=vtkVelocities(loa.GetCartesianVelocities(),loa.GetCartesianPositions(),self)


    def GetVelocities(self):
	"""Returns the instance of the velocity avatar"""
	return self.velocities

    def Update(self,object=None):
	"""Updates the avatar. Reimplemented from vtkAtoms

	If 'object' has been set to a list of atoms it will replace the
	original one, and the window will be updated accordingly.
	Note also, that the 'Update' method will try to represent the
	list of atoms by all its atoms. This means that if one or several atom
	species have been removed they will be introduced again by this method.
	The same strategy applies to the supercell, forces, and velocities.
	"""
	if object is not None:
	    self.SetListOfAtoms(object)

	loa=self.GetListOfAtoms()

	if hasattr(self,'unitcell'): #Does the unit cell avatar exist ?
	    self.unitcell.SetUnitCell(loa.GetUnitCell())
	else:
	    # No, add the unit cell avatar to the list 
	    self.unitcell=vtkUnitCell(loa.GetUnitCell(),self)

	# loa is repeated since forces and velocities cant be set with periods
	loa=loa.Repeat(self.GetPeriods())

	try: #do we have forces ?
	    self.AddForces()
	# NOTE: ValueError is raised if all vectors are null-vectors and
	#	AttributeError when forces are not available
	except: # NO: remove avatar if present
	    try: 
		self.RemoveAvatar(self.GetForces())
	    except AttributeError:
		pass
	
#	try: #do we have velocities ?
#		self.AddVelocities()
	# NOTE: ValueError is raised if all vectors are null vectors
	#	AttributeError when forces are not available
#	except (AttributeError,ValueError):# NO: remove avatar if present
#	    try: 
#		self.RemoveAvatar(self.GetVelocities())
#	    except AttributeError:
#		pass
#	# Continue update

 	vtkAtoms.Update(self)


class vtkAtomSpecies(vtkListOfPositions):
	"""Class representing atoms of same species
	
	This class provides methods for controlling the properties for a
	collection of atoms of the same element. This includes color and
	radius. To create an instance of this class use

	'myspeciesavatar=vtkAtomSpecies(listofatoms)'

	where 'listofatoms' is an instance of 'ListOfAtoms' representing a
	single atomic species. 
	"""


	def __init__(self,listofatoms,parent=None,**keywords):
		self.SetListOfAtoms(listofatoms)
		# The avatar accepts the keyword periods
		if keywords.has_key('periods'):
			self.Periods=keywords['periods']
			del keywords['periods']
		# Setting the radius and color 
		if keywords.has_key('radius'):
			radius=keywords['radius']
			del keywords['radius']
		else: # Set default value
                        radius = Element(self.GetType()).covalent_radius
		if not keywords.has_key('color'):
			keywords['color']=self.GetCPKColor()
		# NOTE, that listofpositions is set to None, since
		# GetListOfPositions is overloaded in this class anyway.
		keywords['parent']=parent
		apply(vtkListOfPositions.__init__,[self,None,radius],keywords)

	def GetListOfAtoms(self):
		"""Returns a list of atoms"""
		return self.SpeciesAtomlist

	def SetListOfAtoms(self,listofatoms):
		"""Sets the list of atoms

		'listofatoms' is expected to be an instance of 'ListOfAtoms'.
		Furthermore, 'listofatoms' must only represent a single atomic
		species.
		"""
		self.SpeciesAtomlist=listofatoms

	def GetListOfPositions(self):
		"""Method overloaded from vtkListOfPositions

		Returns a list containing the Cartesian positions of the
		atoms.
		"""
		return self.GetListOfAtoms().Repeat(self.GetPeriods()).GetCartesianPositions()

	def GetListOfScalars(self):
		"""Method overloaded from vtkListOfPositions"""
		# Fast way for constructing the list of scalars
		Nrep=Numeric.multiply.reduce(self.GetPeriods())
		Nscalars=Nrep*len(self.GetListOfAtoms())
		return Nscalars*[self.GetRadius()] 

	def GetType(self):
		"""Returns the atomtype

		Note that the atoms represented be the list of atoms should
		all correspond to the same atomic species.
		"""
		return self.GetListOfAtoms()[0].GetChemicalSymbol()

	def SetPeriods(self,periods):
		"""Sets the number of periods

		This method can be used to specify the number of times the 
		atoms should be repeated. Default is (1,1,1), i.e. 
		corresponding to a single unit cell at the origin.

		**An example** 

		'speciesavatar.SetPeriods([2,2,1])'

		will repeat the atomic configuration by 2x2x1 according to
		the unit cell.
		"""
		self.Periods=periods
		self.UpdateVTKData()

	def GetPeriods(self):
		"""Returns the number of periods"""
		try:
			return self.Periods
		except AttributeError:
			return (1,1,1)

	def GetRadius(self):
		"""Returns the radius of the atoms

		This radius will be equal to the scalar value ('GetScalar'). 
		If the radius has not been specified the default value is used.
		Default is the radius from
		'Structures.ChemicalElements.CovalentRadius'
		"""
		return vtkListOfPositions.GetScalar(self)

	def SetRadius(self,radius):
		"""Sets the radius of the atoms.

		This method is equivalent to using the method 'SetScalar'. 
		"""
		self.SetScalar(radius)

	def SetColor(self,color=None):
		"""Method reimplemented from vtkListOfPositions

		If 'color' is not specified the colors are set according to
		the CPK scheme, see documentation for 'GetCPKColor'.
		"""
		if color is None:
			color=self.GetCPKColor()
		vtkListOfPositions.SetColor(self,color)


	def GetCPKColor(self):
		"""Returns the CPK color of the atomic species.

		This method return the CPK color of the relvant atomic species.
		The CPK color scheme is also used in RasMol. For more
		information, see 'http://www.umass.edu/microbio/rasmol/distrib/rasman.htm#cpkcolours'
		"""
		from ASE.ChemicalElements import Element
		return Element(self.GetType()).cpk_color


class	vtkForces(vtkListOfVectors):
	"""Class representing the forces

	For more information, see the documentation for 'vtkListOfVectors'.
	"""

	def CreatePipeLine(self):
		"""Create vtk pipeline"""
		vtkListOfVectors.CreatePipeLine(self)
		# By default forces are green and the scale set to 10
		self.GetActorProperty().SetColor(0,1,0)
		self.SetScale(10)

class	vtkVelocities(vtkListOfVectors):
	"""Class representing the velocities

	For more information, see the documentation for 'vtkListOfVectors'.
	"""

	def CreatePipeLine(self):
		"""Create vtk pipline"""
		vtkListOfVectors.CreatePipeLine(self)
		# By default forces are green and the scale set to 10
		self.GetActorProperty().SetColor(1,0,0)
		self.SetScale(100)



