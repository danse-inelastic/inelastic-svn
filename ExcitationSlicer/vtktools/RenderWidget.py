# Written by Mikkel Bollinger (email: mbolling@fysik.dtu.dk)
"""Module for render widgets.

This module contains the render widgets used by vtkAvatar (or any class related
to it by inheritance). The render widgets should all be based on the mix-in
class 'RenderWidget' or implement a corresponding functionality. The
'RenderWidget' class contains most of the basic functionality that is
expected to be handled by the renderwidgets. They should be able
receive either a 'vtkAvatar' (or any derived class) or a 'vtkProperty'
(VTK object), and it is then responsible for the VTK rendering
process. In the current implementations the renderwidgets use either Tkinter or
Wxpython to display the 'vtkRenderWindow' and are based on the renderwidgets
included in the VTK distribution. 
"""

from vtk import vtkRenderer,vtkRenderWindow

try: # Try to import Tkinter
    import Tkinter
except ImportError: # If this fails the module may still work
    pass
try: # Try to import wxPython
    from wxPython import wx
except ImportError: # If this fails the module may still work
    pass
try: # Try to import vtkTkRenderWidget
    from vtk.tk.vtkTkRenderWidget import vtkTkRenderWidget
except ImportError:
    pass


import math
import os

# Using:
# wxVTKRenderWindow
# vtkTkRenderWidget

class RenderWidget:
    """Mix-in class for RenderWidgets

    This mix-in class is used to control the VTK rendering process. It contains
    instances of 'vtkRenderer' and 'vtkRenderWindow' (VTK objects) and the
    class sets up the following VTK pipe line:

    'vtkProp' <--- 'vtkRenderer' <--- 'vtkRenderWindow'.

    The last part, i.e. the initialization of the vtkRenderWindow will depend
    on the concrete implementation. This class may be linked to e.g. GUI
    windows like Tkinter of wxPython.

    The class can initialized in two different ways:

    - By a 'vtkAvatar' or any derived class. Note that when initialized by a
      'vtkAvatar' the concrete implementation of this class is expected to
      have the method 'Render' available.

    - By a vktProp or any related class. This includes vtkAssembly, vtkActor,
      vtkPropAssembly, etc.

      **Programmers note** Concrete implementations of this class are expected
      to have the 'GetRenderWindow'.
    """
    def __init__(self,vtkproperty=None,vtkavatar=None,**kw):
        if vtkavatar is not None:
            self.SetVTKAvatar(vtkavatar)
        if vtkproperty is not None:
            self.SetVTKProperty(vtkproperty)
        # Either the vtkproperty or the vtkavatar must be set:
        if vtkproperty is None and vtkavatar is None:
            raise TypeError, "Either vtkproperty or vtkavatar must be set"
        if vtkproperty is not None and vtkavatar is not None:
            raise TypeError, "vtkproperty and vtkavatar must not be set simultaneously"
        # Finally set the keyword arguments:
        if kw.has_key('backgroundcolor'):
            self.SetBackGroundColor(kw['backgroundcolor'])
            del kw['backgroundcolor']
        if kw.has_key('windowsize'):
            self._SetWindowSize(kw['windowsize'])
            del kw['windowsize']

    def SetBackGroundColor(self,backgroundcolor):
        """Sets the background color of the rendering window 

        This method can be used to change the background color of the
        window according to the (R,G,B)-scale.

        Usage: '>>>window.SetBackGround((0,0,0))'

        changes the background of the window to black. 
        """
        self.background=backgroundcolor
        # Propagate changes to the renderer
        R,G,B=backgroundcolor
        self.GetRenderer().SetBackground(R,G,B)

    def GetBackGroundColor(self):
        """Returns the background color as a tuple
        
        Default is white.
        """
        if not hasattr(self,'background'):
            self.background=(1,1,1) # White
        return tuple(self.background)

    def _SetWindowSize(self,windowsize):
        """Internal method."""
        self.windowsize=windowsize

    def GetWindowSize(self):
        """Returns the window size

        Note that once the renderwidget has been initialized the window size
        cannot be changed.

        Programmers note: In a future development this could be a dersirable
        feature. 
        """
        if not hasattr(self,'windowsize'):
            return (600,600)
        return self.windowsize

    def InitRenderer(self):
        """Inintializing the vtkRenderer. Internal method."""
        self.renderer=vtkRenderer()
        # Things to do with the renderer after initialization
        # Add the property assembly
        self.renderer.SetBackground(self.GetBackGroundColor())
        self.renderer.AddProp(self.GetVTKProperty())

    def GetRenderer(self):
        """Returns the instance of vtkRenderer"""
        # Is the vtkRenderer initialized ? 
        if not hasattr(self,'renderer'): # No, create one
            self.InitRenderer()
        return self.renderer    

    def UnregisterProp(self,prop):
        """Internal method. Unregister vtkProp from vtkRenderWindow"""
        renderwindow=self.GetRenderWindow()
        # If this method is not called it **sometimes** (but certainly not
        # always) results in a core dump from VTK (??). 
        prop.ReleaseGraphicsResources(renderwindow)

    def GetCamera(self):
        """Returns an instance of vtkCamera.
	
        vtkCamera has a wide range of methods for manipulating the 
        camera. Write: '>>>dir(plot.GetCamera())' to see which. A lot 
        of the methods are self-explaining - otherwise consult your 
        favorite VTK manual.

        An example: '>>>plot.GetCamera().Azimuth(90)'

        changes the azimuthal angle by 90 degrees. 
        """
        return self.GetRenderer().GetActiveCamera()

    def ResetCamera(self):
        """Resets the camera

        This method will set up the camera to make all actors 
        visible. This is done by repositioning the camera along its 
        initial view plane normal. 
        """
        self.GetRenderer().ResetCamera()

    def GetLight(self):
        """Returns the light

        This method returns the instance of vtkLight used by the renderer.
        """
        # Get the vtkLightCollection
        lights=self.GetRenderer().GetLights()
        # Retrieve the first vtkLight in the collection
        lights.InitTraversal()
        return lights.GetNextItem()

    def UpdateLight(self):
        """Updates the light

        This method will update the ligth according to the position and focal
        point of the camera. 
        """
        light=self.GetLight()
        camera=self.GetCamera()
        light.SetPosition(camera.GetPosition())
        light.SetFocalPoint(camera.GetFocalPoint())
        

    def GetVTKAvatar(self):
        """Returns the vtkavatar"""
        return self.vtkavatar

    def SetVTKAvatar(self,vtkavatar):
        """Sets the vtkavatar.

        This method will also automatically set the vtkProp.
        """
        # Propopagate the property assembly:
        self.SetVTKProperty(vtkavatar.GetPropAssembly())
        self.vtkavatar=vtkavatar

    def GetVTKProperty(self):
        """Returns the vtkProp (VTK object)

        This VTK property will be the one rendered in the window.
        """
        return self.vtkproperty

    def SetVTKProperty(self,vtkproperty):
        """Set the vtkProp (VTK object)"""
        self.vtkproperty=vtkproperty

    def SaveAsBMP(self,filename,resolution=1):
        """Saves the window as bmp-file.

        Resolution is an integer representing the number of squares
        that the window is divided into when writing to the bmp-file. 
        Thus choosing a higher number improves the quality of the 
        saved image.
        """
        from vtk import vtkRenderLargeImage,vtkBMPWriter
        #self.UpdateLight()

        renderLarge = vtkRenderLargeImage()
        renderLarge.SetInput(self.GetRenderer())
        renderLarge.SetMagnification(resolution)

        writer = vtkBMPWriter()
        writer.SetFileName(filename)
        writer.SetInput(renderLarge.GetOutput())
        writer.Write()


class TkRenderWidgetSimple(RenderWidget,vtkTkRenderWidget):
    """Tk render widget

    This class is a very thin shell around the vtkTkRenderWidget provided in
    the VTK distribution. It provides a vtkRenderWindow linked to a Tk widget.
    TkRenderWidgetSimple generates the Tk root and has the necessary
    functionality to work with a 'vtkAvatar'. The latter is achieved by
    inheritance to 'RenderWidget'.

    This class can be initialized by specifying either a 'vtkAvatar' or a
    'vtkProp' (or instances of any related classes). Note that setting the
    'vtkAvatar' will automatically also set the 'vtkProp'. 

    **Known bugs**

    - The Tk render window cannot be opened several times during a single
    python session. For some (unknown) reason the dynamically loaded Tk
    object cannot be found.

    - Gives an annoying error message when 'DestroyWindow' is used.
    """
# A very thin shell around the vtkTkRenderWidget from the VTK distribution

    def __init__(self,vtkproperty=None,vtkavatar=None,**keywords):
        # Adding  keys to keyword
        keywords['vtkproperty']=vtkproperty
        keywords['vtkavatar']=vtkavatar
        apply(RenderWidget.__init__,[self],keywords)
        width,height=self.GetWindowSize()
        # Initializing Tk window
        self.__root=Tkinter.Tk()
        vtkTkRenderWidget.__init__(self,self.__root,width=width,height=height)
        # Adding renderer to the window
        self.GetRenderWindow().AddRenderer(self.GetRenderer())
        self.pack()

    def GetRoot(self):
        """Returns the Tk root"""
        return self.__root

    def DestroyWindow(self):
        """Destroys the Tk window"""
        # First destroy the RenderWindow
        self.destroy()
        # Then the tk root
        self.GetRoot().destroy()

class TkRenderWidget(RenderWidget,Tkinter.Widget):
    """Tk render widget

    This class is based on the vtkTkRenderWidget provided in the VTK
    distribution where the vtkRenderWindow is linked to a Tk widget. However,
    'TkRenderWidget' requires that the environment variable VTK_TK_WIDGET_PATH
    is set. This variable specifies the location of the file:
    'libvtkRenderingPythonTkWidgets.so' coming with the VTK distribution.
    
    This class can be initialized by specifying either a 'vtkAvatar' or a
    'vtkProp' (or instances of any related classes). Note that setting the
    'vtkAvatar' will automatically also set the 'vtkProp'.
    """

    def __init__(self,vtkavatar=None,vtkproperty=None,**keywords):
        if keywords.has_key('windowsize'):
            self._SetWindowSize(keywords['windowsize'])
            del keywords['windowsize']
        # Adding keywords:
        keywords['vtkproperty']=vtkproperty
        keywords['vtkavatar']=vtkavatar
        apply(RenderWidget.__init__,[self],keywords)
        #RenderWidget.__init__(self,vtkproperty=vtkproperty,vtkavatar=vtkavatar)
        width,height=self.GetWindowSize()

        # Initializing Tk window
        self.__root=Tkinter.Tk()

        # Finding the location of the wrapped vtkTkRenderWidget
        filename="libvtkRenderingPythonTkWidgets.so"
        # This file is usually in /usr/lib/vtk
        # The location must be set through the environment variable:
        # "VTK_TK_WIDGET_PATH"
        try:
            widgetpath=os.environ["VTK_TK_WIDGET_PATH"]
        except KeyError:
            widgetpath="/usr/lib/vtk"
            if not os.path.isfile(os.path.join(widgetpath,filename)):
                errormessage="Environment variable VTK_TK_WIDGET_PATH not set. Specifies the location of "+str(filename)+". This file will usually be in /usr/lib/vtk/python/."
                raise KeyError, errormessage
        # Constructing the full path for the Tk renderwidget:
        fullpath=os.path.join(widgetpath,filename)
        try:
            self.__root.tk.call('load',fullpath)
        except:
            errormessage="Could not load "+filename+" in "+widgetpath+". Find the correct location of the file and change the VTK_TK_WIDGET_PATH accordingly."
            raise IOError, errormessage

        # Building keyword arguments to Tkinter.Widget call:
        kw={"width":width,"height":height}
        # Get the address of the vtkRenderWindow in the storage
        renderwindow=vtkRenderWindow()
        kw["rw"]=renderwindow.GetAddressAsString('vtkRenderWindow')
        cnf={}
        Tkinter.Widget.__init__(self,self.__root,'vtkTkRenderWidget',cnf,kw)


        ###### Initializations from vtkTkRenderWidget
        self._CurrentRenderer = None
        self._CurrentCamera = None
        self._CurrentZoom = 1.0
        self._CurrentLight = None

        self._ViewportCenterX = 0
        self._ViewportCenterY = 0

        # used by the LOD actors
        self._DesiredUpdateRate = 15
        self._StillUpdateRate = 0.0001

        # these record the previous mouse position
        self._LastX = 0
        self._LastY = 0

        # private attributes
        self.__InExpose = 0

        # Create Tk bindings
        self.BindTkRenderWidget()
        ######

        # Adding renderer to the window
        self.GetRenderWindow().AddRenderer(self.GetRenderer())
        self.pack()

###################################################
# __getattr__ taken directly from vtkTkRenderWidget
###################################################    

    def __getattr__(self,attr):
        # because the tk part of vtkTkRenderWidget must have
        # the only remaining reference to the RenderWindow when
        # it is destroyed, we can't actually store the RenderWindow
        # as an attribute but instead have to get it from the tk-side
        if attr == '_RenderWindow':
            return self.GetRenderWindow()
        raise AttributeError, self.__class__.__name__ + \
              " has no attribute named " + attr

    def GetRoot(self):
        """Returns the Tk root."""
        return self.__root

    def DestroyWindow(self):
        """Destroys the Tk window"""
        # First destroy the RenderWindow
        self.destroy()
        # Then the tk root
        self.GetRoot().destroy()

    def BindTkRenderWidget(self):
        """Bind some default actions.
        """
        self.bind("<ButtonPress>",
                  lambda e,s=self: s.StartMotion(e.x,e.y))
        self.bind("<ButtonRelease>",
                  lambda e,s=self: s.EndMotion(e.x,e.y))
        self.bind("<B1-Motion>",
                  lambda e,s=self: s.Rotate(e.x,e.y))
        self.bind("<B2-Motion>",
                  lambda e,s=self: s.Pan(e.x,e.y))
        self.bind("<B3-Motion>",
                  lambda e,s=self: s.Zoom(e.x,e.y))
        self.bind("<Expose>",
                  lambda e,s=self: s.Expose())
        
################################################
# Methods taken directly from vtkTkRenderWidget#
################################################

    def GetZoomFactor(self):
        return self._CurrentZoom

    def SetDesiredUpdateRate(self, rate):
        """Mirrors the method with the same name in
        vtkRenderWindowInteractor."""
        self._DesiredUpdateRate = rate

    def GetDesiredUpdateRate(self):
        """Mirrors the method with the same name in
        vtkRenderWindowInteractor."""
        return self._DesiredUpdateRate 
        
    def SetStillUpdateRate(self, rate):
        """Mirrors the method with the same name in
        vtkRenderWindowInteractor."""
        self._StillUpdateRate = rate

    def GetStillUpdateRate(self):
        """Mirrors the method with the same name in
        vtkRenderWindowInteractor."""
        return self._StillUpdateRate 

    def GetRenderWindow(self):
        addr = self.tk.call(self._w, 'GetRenderWindow')[5:]
        return vtkRenderWindow('_%s_vtkRenderWindow_p' % addr)

    def Render(self):
        if (self._CurrentLight):
            light = self._CurrentLight
            light.SetPosition(self._CurrentCamera.GetPosition())
            light.SetFocalPoint(self._CurrentCamera.GetFocalPoint())

        self._RenderWindow.Render()

    def UpdateRenderer(self,x,y):
        """
        UpdateRenderer will identify the renderer under the mouse and set
        up _CurrentRenderer, _CurrentCamera, and _CurrentLight.
        """
        windowX = self.winfo_width()
        windowY = self.winfo_height()

        renderers = self._RenderWindow.GetRenderers()
        numRenderers = renderers.GetNumberOfItems()

        self._CurrentRenderer = None
        renderers.InitTraversal()
        for i in range(0,numRenderers):
            renderer = renderers.GetNextItem()
            vx,vy = (0,0)
            if (windowX > 1):
                vx = float(x)/(windowX-1)
            if (windowY > 1):
                vy = (windowY-float(y)-1)/(windowY-1)
            (vpxmin,vpymin,vpxmax,vpymax) = renderer.GetViewport()
            
            if (vx >= vpxmin and vx <= vpxmax and
                vy >= vpymin and vy <= vpymax):
                self._CurrentRenderer = renderer
                self._ViewportCenterX = float(windowX)*(vpxmax-vpxmin)/2.0\
                                        +vpxmin
                self._ViewportCenterY = float(windowY)*(vpymax-vpymin)/2.0\
                                        +vpymin
                self._CurrentCamera = self._CurrentRenderer.GetActiveCamera()
                lights = self._CurrentRenderer.GetLights()
                lights.InitTraversal()
                self._CurrentLight = lights.GetNextItem()
                break

        self._LastX = x
        self._LastY = y

    def GetCurrentRenderer(self):
        return self._CurrentRenderer
 
    def StartMotion(self,x,y):
        self.GetRenderWindow().SetDesiredUpdateRate(self._DesiredUpdateRate)
        self.UpdateRenderer(x,y)

    def EndMotion(self,x,y):
        self.GetRenderWindow().SetDesiredUpdateRate(self._StillUpdateRate)
        if self._CurrentRenderer:
            self.Render()

    def Rotate(self,x,y):
        if self._CurrentRenderer:
            
            self._CurrentCamera.Azimuth(self._LastX - x)
            self._CurrentCamera.Elevation(y - self._LastY)
            self._CurrentCamera.OrthogonalizeViewUp()
            
            self._LastX = x
            self._LastY = y
            
            self._CurrentRenderer.ResetCameraClippingRange()
            self.Render()

    def Pan(self,x,y):
        if self._CurrentRenderer:
            
            renderer = self._CurrentRenderer
            camera = self._CurrentCamera
            (pPoint0,pPoint1,pPoint2) = camera.GetPosition()
            (fPoint0,fPoint1,fPoint2) = camera.GetFocalPoint()

            if (camera.GetParallelProjection()):
                renderer.SetWorldPoint(fPoint0,fPoint1,fPoint2,1.0)
                renderer.WorldToDisplay()
                fx,fy,fz = renderer.GetDisplayPoint()
                renderer.SetDisplayPoint(fx-x+self._LastX,
                                         fy+y-self._LastY,
                                         fz)
                renderer.DisplayToWorld()
                fx,fy,fz,fw = renderer.GetWorldPoint()
                camera.SetFocalPoint(fx,fy,fz)

                renderer.SetWorldPoint(pPoint0,pPoint1,pPoint2,1.0)
                renderer.WorldToDisplay()
                fx,fy,fz = renderer.GetDisplayPoint()
                renderer.SetDisplayPoint(fx-x+self._LastX,
                                         fy+y-self._LastY,
                                         fz)
                renderer.DisplayToWorld()
                fx,fy,fz,fw = renderer.GetWorldPoint()
                camera.SetPosition(fx,fy,fz)
                
            else:
                (fPoint0,fPoint1,fPoint2) = camera.GetFocalPoint()
                # Specify a point location in world coordinates
                renderer.SetWorldPoint(fPoint0,fPoint1,fPoint2,1.0)
                renderer.WorldToDisplay()
                # Convert world point coordinates to display coordinates
                dPoint = renderer.GetDisplayPoint()
                focalDepth = dPoint[2]
                
                aPoint0 = self._ViewportCenterX + (x - self._LastX)
                aPoint1 = self._ViewportCenterY - (y - self._LastY)
                
                renderer.SetDisplayPoint(aPoint0,aPoint1,focalDepth)
                renderer.DisplayToWorld()
                
                (rPoint0,rPoint1,rPoint2,rPoint3) = renderer.GetWorldPoint()
                if (rPoint3 != 0.0):
                    rPoint0 = rPoint0/rPoint3
                    rPoint1 = rPoint1/rPoint3
                    rPoint2 = rPoint2/rPoint3

                camera.SetFocalPoint((fPoint0 - rPoint0) + fPoint0, 
                                     (fPoint1 - rPoint1) + fPoint1,
                                     (fPoint2 - rPoint2) + fPoint2) 
                
                camera.SetPosition((fPoint0 - rPoint0) + pPoint0, 
                                   (fPoint1 - rPoint1) + pPoint1,
                                   (fPoint2 - rPoint2) + pPoint2)

            self._LastX = x
            self._LastY = y

            self.Render()

    def Zoom(self,x,y):
        if self._CurrentRenderer:

            renderer = self._CurrentRenderer
            camera = self._CurrentCamera

            zoomFactor = math.pow(1.02,(0.5*(self._LastY - y)))
            self._CurrentZoom = self._CurrentZoom * zoomFactor

            if camera.GetParallelProjection():
                parallelScale = camera.GetParallelScale()/zoomFactor
                camera.SetParallelScale(parallelScale)
            else:
                camera.Dolly(zoomFactor)
                renderer.ResetCameraClippingRange()

            self._LastX = x
            self._LastY = y

            self.Render()

    def Expose(self):
        if (not self.__InExpose):
            self.__InExpose = 1
            self.update()
            self._RenderWindow.Render()
            self.__InExpose = 0


ID_EXIT = 102

