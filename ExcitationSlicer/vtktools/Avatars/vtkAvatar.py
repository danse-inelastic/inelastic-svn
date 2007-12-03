# Written by Mikkel Bollinger (email:mbolling@fysik.dtu.dk)
"""Module containing the base class for VTK avatars"""


from ASE.Visualization.VTK import vtkAssembly
from ASE.Visualization.VTK.Avatars.Avatar import Avatar


class vtkAvatar(Avatar):
	"""Basis class for vtk avatars

	This basis class contains the methods which all vtk avatars are 
	expected to have. These methods include:

	- Updating the avatar itself and added avatars
	
	- Removing/adding the relevant actors from added avatars

	- Taking the vtkProp's in the avatar tree and pipe them into
	  a renderwidget, see VTK.RenderWidget.
	  
	**General structure**

	The class is designed to be used in two different ways. First of all 
	it may form the basis for an 'active' vtk avatar which contains the 
	methods for both reading data and converting the data into some 
	geometric object. The inheritance diagram for such an avatar will look
	like:

	vtkAvatar <--- vtk<simulation object>avatar <--- <geometic object> Source

	The vtk<simulation object>avatar should be responsible for converting
	a simulation object into a vtk dataobject. The <geometric object>
	Source then takes the vtk dataobject and converts it into a geometrical
	representation. This should should be a derived class of 'vtkProp' 
	i.e. an instance of either 'vtkActor' , 'vtkActor2D' or 'vtkVolume' . 
	They are in turn expected to be accesible from the 'Source' via a 
	method named 'GetActor' , 'GetActor2D' or 'GetVolume' . Examples of
	this type of avatar is 'vtkUnitCell' and 'vtkListOfVectors' .
 
	However, the 'Source' is not always required - the vtkavatar may just 
	act as a container for other avatars controlling in some way the 
	rendering process. In this case the inheritance diagram will look
	like:

	vtkAvatar <--- vtk<simulation object>Avatar

	Examples on this type of avatar are 'vtkGrid3D' and 'vtkEigenState' .

	**Updating**

	All avatars have an 'Update' method. This method forces the input data,
 	e.g. the simulation object, of the avatar to be read and then request 
	all of the added/child avatars to update themselves. Finally, *if* the 
	avatar has a window it is rendered again. During the rendering process
 	any changes within the vtk pipepline are updated.    

	**Initializing**

	An avatar may be initialized in two different ways. 

	- Without a 'parent' : The avatar is updated and a window will pop up.

	- With a 'parent' : The avatar is updated and added to the parent
	(which must be another instance of a dervied vtkAvatar). However, no
	window will pop up. If this is desired at some time later, it can be
	done by calling the 'Render' method (see description below).

	The vtkAvatar also accepts a number of keywords. For instance the
	'windowmode' can be specified. The keywords not recognized by
	'vtkAvatar' will be passed to the renderwidget on initialization. 
	"""

	def __init__(self,parent=None,**keywords):
	    if keywords.has_key("windowmode"):
		    self.windowmode=keywords["windowmode"]
		    del keywords['windowmode']
	    else: # Default windowmode is TkRenderWidget
		    self.windowmode=0
	    Avatar.__init__(self,parent)
            self.Update()
	    if parent is None:# if no parent popup window and do a rendering
		# Initialize window explicitly to pass keyword arguments
		apply(self.InitWindow,[],keywords)
		# Then do a render
                self.Render()

# PROGRAMMERS NOTE:
# If a new window mode is introduced the following methods should be modified:
# InitWindow, DestroyWindow, Render, and SaveAsBMP


        def SetWindowMode(self,windowmode,**keywords):
	    """Sets the window mode.

	    This method can be used to set the window mode. The window mode
	    specifies the type of window to be used. The window controls the
	    vtk rendering process. Currently four different window modes
	    are available:

	    - **'windowmode=0'** : Uses the TkRenderWidget
	    (in VTK.RenderWidget). Requires Tkinter to be installed and is
	    based on 'vtkTkRenderWidget' found in the VTK distribution.

	    - **'windowmode=1'** : Uses the TkRenderWidgetSimple (in
	    VTK.RenderWidget). Requires Tkinter to be installed and is a thin
	    shell around the 'vtkTkRenderWidget' found in the VTK distribution.

	    - **'windowmode=2'** : Uses Bonanza (in Visualization.Bonanza).
	    A more advanced window tool that allows one to simultaneously
	    view the objects from different perspectives. It requires Tkinter
	    to be installed.

	    - **'windowmode=-1'** : No window is opened.
	    """
            # First close the old window
            self.DestroyWindow()
            # Set the new windowmode
            self.windowmode=windowmode
	    # initialize the new window with keywords:
	    print keywords
	    apply(self.InitWindow,[],keywords)
            # and rerender it
            self.Render()

        def GetWindowMode(self):
	    """Returns the window mode"""	
            return self.windowmode

        def SetWindowModeNone(self):
	    """Changes the window mode to None

	    If initialized in this window mode the vtkavatar will not open a
	    window, even if a parent is not specified.  
	    """	
	    self.SetWindowMode(-1)	

        def SetWindowModeTkRenderWidget(self,**keywords):
	    """Changes the window mode to TkRenderWidget (default).

	    See SetWindowMode and refer also to the documentation in
	    Visualization.VTK.RenderWidget.
	    """
            apply(self.SetWindowMode,[0],keywords)

        def SetWindowModeTkRenderWidgetSimple(self):
	    """Changes the window mode to TkRenderWidgetSimple.

	    Set SetWindowMode and refer also  to the documentation of this
	    renderwidget in Visualization.VTK.RenderWidget.
	    """
            self.SetWindowMode(1)

        def SetWindowModeBonanza(self):
	    """Changes the window mode to Bonanza (in Visualization.Bonanza)"""
            self.SetWindowMode(2)

  	def InitWindow(self,**keywords):
            """Initialize the the window used by VTK.

	    This method will initialize the window according to the specified
	    window mode. All keywords are passed to the renderwidget (if
	    possible).
	    """
            windowmode=self.GetWindowMode()
            if windowmode==0: # Initialize TkRenderWidget
		apply(self.InitWindow_TkRenderWidget,[],keywords)
            elif windowmode==1: # Initialize TkRenderWidgetSimple
                #self.InitWindow_TkRenderWidgetSimple()
		apply(self.InitWindow_TkRenderWidgetSimple,[],keywords)
            elif windowmode==2: # Initialize Bonanza
                self.InitWindow_Bonanza()
	    elif windowmode==-1: # No window
		self._window=None    
                    
        def InitWindow_TkRenderWidget(self,**keywords):
            """Internal method. Initialize the TkRenderWidget"""
            from ASE.Visualization.VTK.RenderWidget import TkRenderWidget
            #self._window=TkRenderWidget(vtkavatar=self)
	    keywords['vtkavatar']=self
	    self._window=apply(TkRenderWidget,[],keywords)
	    
        def InitWindow_TkRenderWidgetSimple(self,**keywords):
            """Internal method. Initialize the TkRenderWidgetSimple"""
            from ASE.Visualization.VTK.RenderWidget import TkRenderWidgetSimple
	    keywords['vtkavatar']=self
            #self._window=TkRenderWidgetSimple(vtkavatar=self)
	    self._window=apply(TkRenderWidgetSimple,[],keywords)

        def InitWindow_Bonanza(self):
	    """Internal method. Initializes Bonanza in
	    ASE.Visualization.Bonanaza."""
            from ASE.Visualization.Bonanza import Bonanza
            # Initialize the window 
            self._window=Bonanza.Bonanza()
            # and add the propertyassembly
            self._window.SetNeutralProps([self.GetPropAssembly()])

  	def GetWindow(self):
  		"""Returns the instance of RenderWidget"""
  		if not hasattr(self,'_window'):
  			self.InitWindow()
                return self._window

        def DestroyWindow(self):
                """Destroys the window

		This method returns the avatar to its state before the window
		was initialized.
		"""
                windowmode=self.GetWindowMode()
                # Try to destroy window:
                if hasattr(self,"_window"):
                    if windowmode in [0,1]: # Is window a TkRenderWidget ?
                        self._window.DestroyWindow()
                    elif windowmode==2: # Is window an instance of     
                        # Firstdelete Bonanza
                        self._window.Quit()
		    elif windowmode==-1: # No window
			pass    
                # Finally delete instance of window
                    delattr(self,'_window')

	def HasActiveWindow(self):
	    """Returns 1 if the vtkavatar has an active window"""
	    active=0
	    if hasattr(self,'_window'): # Is window defined ?
		    if self.GetWindowMode()!=1: # Is the window mode None ?
			    active=1
	    return active

        def _GetAvatarsWithActiveWindow(self):
	    """Internal method. Returns a tuple with active avatars in parent list and self"""
	    activeavatars=[]
	    # First see if self is active
	    if self.HasActiveWindow():
		    activeavatars.append(self)
	    # Then search the parents:
	    for parent in self.GetParents():
		    activeavatars.extend(parent._GetAvatarsWithActiveWindow())
	    return activeavatars	    

        def GetActiveWindows(self):
	    """Returns a tuple with active windows"""
	    return map(lambda avatar:avatar.GetWindow(),self._GetActiveAvatars())

        def RemoveAvatar(self,avatar):
	    """Method reimplemented from Avatar"""
	    # First unregister the vtkProps from active windows:
	    props=avatar._GetAllProps()
	    for parentavatar in self._GetAvatarsWithActiveWindow():
		    window=parentavatar.GetWindow()
		    # Does not work for Bonanza
		    if parentavatar.GetWindowMode()!=2:
			    # Unregister all props associated with avatar
			    for prop in props:
				    window.UnregisterProp(prop)
	    # Finally, call method implemented in Avatar:
	    Avatar.RemoveAvatar(self,avatar)

        def Render(self):
	    """Renders the window

	    The method passes the command to the relevant renderwidget. If the
	    window is not already set, it will be initialized by this method.
	    (If windowmode=-1 this method will only update the
	    'vtkPropAssembly'.) Furthermore, the method will cause the complete
	    VTK pipeline to be updated. 
	    """
            # Update all actors in the assembly
            self.UpdatePropAssembly()
            # Then notity the window to render
            windowmode=self.GetWindowMode()
            if windowmode in [0,1]: # Is window a Wx or TkRenderWidget ? 
                self.GetWindow().Render()
            elif windowmode==2: # Bonanza ?   
                self.GetWindow()._scene.Notify()
	    elif windowmode==-1: # No window mode
	        pass

        def GetPropAssembly(self):
	    """Returns a vtkPropAssembly

	    The vtkPropAssembly (VTK object) will contain all the vktProp's
	    that can be found in the avatar list and the one obtained from the
	    avatar itself.
	    """
            if not hasattr(self,'_propassembly'):
                self._propassembly=vtkAssembly()
            return self._propassembly    

        def UpdatePropAssembly(self):
	    """Updates the vtkPropAssembly

	    This method takes a flash of the avatar tree and inserts all the
	    'vtkProp's currently found in the treee and inserts them into the
	    avatars appearing in the 'vtkPropAssembly'.
	    """
            # First remove all the properties in the assembly
            self.GetPropAssembly().GetParts().RemoveAllItems()
            # Then add all the properties, including new
            for prop in self._GetAllProps():
                self._propassembly.AddPart(prop)

	def GetProp(self):
	    """Returns a vtkProp

	    Convenience method that can be used to obtain the 'vtkProp'
	    associated with the 'vtkAvatar'. 
	    """
	    # Looks though the methods:
	    # GetActor, GetActor2D, GetVolume
	    try:  # Is there an actor ?
		prop=self.GetActor()
	    except AttributeError:
		    try: # Is there a actor2D
			    prop=self.GetActor2D()
		    except AttributeError: # Is there a volume
			    try: # Is there a volume
				    prop=self.GetVolume()
			    except AttributeError:
				    raise AttributeError, "Avatar does not have a prop"
	    return prop

	def _GetAllProps(self):
		"""Internal method. Returns a list with all the props doing a
		recursive search in the avatar list."""
		try:	# Is there a vtkProp ?
			proplist=[self.GetProp()]
		except AttributeError: # Else return an empty list
			proplist=[]
		# Look for additional actors in avatar list
		for avatar in self.GetAvatars():
			proplist.extend(avatar._GetAllProps())

		return proplist
	
	def SaveAsBMP(self,filename,resolution=1):
		"""Saves the window as bmp-file.

		Resolution is an integer representing the number of squares
		that the window is divided into when writing to the bmp-file. 
		Thus choosing a higher number improves the quality of the 
		saved image.
		"""
                # Attempting to make window save image
                window=self.GetWindow()
                windowmode=self.GetWindowMode()
                if windowmode in [0,1]: # Is window a TkRenderWidget ? 
                    window.SaveAsBMP(filename=filename,resolution=resolution)
                    # Render to return window to normal status
                    self.Render()
                elif windowmode==2: # Is window an instance of Bonanza ?
                    from ASE.Visualization.Bonanza import BonanzaBase
                    BonanzaBase.BonanzaBase._outputMagnification=resolution
                    window.SaveAsBMP(filename=filename)
		elif windowmode==-1: # No window
		    raise TypeError, "Avatar has no window to save to a bmp file."	
                else:
                    raise AttributeError, "SaveAsBMP not implemented in the current renderwidget."


	def Update(self,object=None):
	    """ Update the avatar. Reimplemented from Avatar"""
	    Avatar.Update(self,object) # Updates all child avatars

            # Is the window open ?
            if hasattr(self,'_window'):
                # Yes, render it
                self.Render()




