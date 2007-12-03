# Written by Mikkel Bollinger (email: mbolling@fysik.dtu.dk)
from string import rfind

class Avatar:
	"""Abstract class for an avatar

	This class contains the methods which should be common for any 
	visualization avatar. These methods include:

	* Updating the avatar
	* Removing/adding other avatars
	"""

	def __init__(self,parent=None):
		self.parents=[]
		if parent is not None:
			parent.AddAvatar(self)

	def __str__(self):
		return self.__class__.__name__

	def GetParents(self):		
		"""Returns a list of the added parents"""
		return tuple(self.parents)

	def _GetAvatarList(self):
		"""Internal method: Returns a list with the added avatars."""
		if hasattr(self,'_avatarlist'):
			return self._avatarlist
		else:
			self._avatarlist=[]
			return self._avatarlist

	def GetAvatars(self):
		"""Returns a tuple of the added avatars.

		This method can be used to see, which methods have been added
		to the current avatar. The tuple contains the instances of 
		the added avatars. 
		"""
		return tuple(self._GetAvatarList())

	def AddAvatar(self,avatar):
		"""Adds an avatar to the current avatar.
		
		When subsequently rendering the window the added avatar will
		be combined with the current avatar. 

		**An example:** 

		To add 'newavatar' to 'myavatar' :

		'>>>myavatar.AddAvatar(newavatar)'
		"""
		# First add avatar to avatar list
		self._GetAvatarList().append(avatar)
		# Then register self as parent
		avatar.parents.append(self)

	def RemoveAvatar(self,avatar):
		"""Removes an avatar from the current avatar.

		To remove an avatar the instance of the avatar must be
		specified. A pointer to that instance may be established
		via the methods 'GetAvatars' or 'GetAvatarDict'.

		**Usage**

		* To remove the avatar named 'addedavatar.#1' from 
		'myavatar' : 

		'>>>oldavatar=myavatar.GetAvatarDict()[addedavatar.#1]'

		'>>>myavatar.RemoveAvatar(oldavatar)'

		* To remove avatar no. 2 in the avatar list from myavatar

		'>>>oldavatar=myavatar.GetAvatars()[2]'

		'>>>myavatar.RemoveAvatar(oldavatar)'
		"""
		# First unregister self as parent:
		avatar.parents.remove(self)
		# Then remove avatar from avatar list
		self._GetAvatarList().remove(avatar)


	def GetAvatarDict(self):
		"""Returns a dictionary with the added avatars

		The values in the dictionary are instances of the added 
		avatars. The key corresponding to the each added avatar
		is the name of the avatar. These names are intended to be
		self-explaining.

		**Usage**

		To get a list of the names of the added avatars:

		'>>>myavatar.GetAvatarDict().keys()'
		
		To get a pointer to the added avatar named 'addedavatar.#1':

		'>>>myavatar.GetAvatarDict()[addedavatar.#1]'
		"""

		from string import rfind
		avatardict={}
		for avatar in self._GetAvatarList():
			navatar=map(lambda x,rfind=rfind:x[:rfind(x,'.')],avatardict.keys()).count(str(avatar))
			avatardict[str(avatar)+'.#'+str(navatar+1)]=avatar
		return avatardict


	def Update(self,object=None):
	    """ Update all added/child avatars."""
	    for avatar in self.GetAvatars():
		avatar.Update(object)










