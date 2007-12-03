from vtk.wx.wxVTKRenderWindow import *

class wxVTKRenderWindowWrapper(wxVTKRenderWindow):
    
    # this __init__ is identical to that of the base class minus the annoying show frame part (commented out)
    def __init__(self, parent, ID, *args, **kw):

        # miscellaneous protected variables
        self._CurrentRenderer = None
        self._CurrentCamera = None
        self._CurrentZoom = 1.0
        self._CurrentLight = None

        self._ViewportCenterX = 0
        self._ViewportCenterY = 0
        
        self._Picker = vtk.vtkCellPicker()
        self._PickedActor = None
        self._PickedProperty = vtk.vtkProperty()
        self._PickedProperty.SetColor(1,0,0)
        self._PrePickedProperty = None
        
        # these record the previous mouse position
        self._LastX = 0
        self._LastY = 0

        # the current interaction mode (Rotate, Pan, Zoom, etc)
        self._Mode = None
        self._ActiveButton = None

        # private attributes
        self.__OldFocus = None

        # used by the LOD actors
        self._DesiredUpdateRate = 15
        self._StillUpdateRate = 0.0001

        # First do special handling of some keywords:
        # stereo, position, size, width, height, style
        
        stereo = 0
        
        if kw.has_key('stereo'):
            if kw['stereo']:
                stereo = 1
            del kw['stereo']

        position = wxDefaultPosition

        if kw.has_key('position'):
            position = kw['position']
            del kw['position']

        try:
            size = parent.GetSize()
        except AttributeError:
            size = wxDefaultSize

        if kw.has_key('size'):
            size = kw['size']
            del kw['size']
        
        if kw.has_key('width') and kw.has_key('height'):
            size = (kw['width'], kw['height'])
            del kw['width']
            del kw['height']

        # wxWANTS_CHARS says to give us e.g. TAB
        # wxNO_FULL_REPAINT_ON_RESIZE cuts down resize flicker under GTK
        style = wxWANTS_CHARS | wxNO_FULL_REPAINT_ON_RESIZE

        if kw.has_key('style'):
            style = style | kw['style']
            del kw['style']

        # the enclosing frame must be shown under GTK or the windows
        #  don't connect together properly
#        l = []
#        p = parent
#        while p: # make a list of all parents
#            l.append(p)
#            p = p.GetParent()
#        l.reverse() # sort list into descending order
#        for p in l:
#            p.Show(1)

        # initialize the wxWindow
        baseClassRef=super(wxVTKRenderWindow,self)
        baseClassRef.__init__(parent, ID, position, size, style)

        # create the RenderWindow and initialize it
        self._RenderWindow = vtk.vtkRenderWindow()
        try:
            self._RenderWindow.SetSize(size.width, size.height)
        except AttributeError:
            self._RenderWindow.SetSize(size[0], size[1])
        if stereo:
            self._RenderWindow.StereoCapableWindowOn()
            self._RenderWindow.SetStereoTypeToCrystalEyes()

        self.__handle = None

        # refresh window by doing a Render
        EVT_PAINT(self, self.OnPaint)
        # turn off background erase to reduce flicker
        EVT_ERASE_BACKGROUND(self, lambda e: None)
        
        # Bind the events to the event converters
        EVT_RIGHT_DOWN(self, self._OnButtonDown)
        EVT_LEFT_DOWN(self, self._OnButtonDown)
        EVT_MIDDLE_DOWN(self, self._OnButtonDown)
        EVT_RIGHT_UP(self, self._OnButtonUp)
        EVT_LEFT_UP(self, self._OnButtonUp)
        EVT_MIDDLE_UP(self, self._OnButtonUp)
        EVT_MOTION(self, self.OnMotion)

        EVT_ENTER_WINDOW(self, self._OnEnterWindow)
        EVT_LEAVE_WINDOW(self, self._OnLeaveWindow)

        EVT_CHAR(self, self.OnChar)

        # If we use EVT_KEY_DOWN instead of EVT_CHAR, capital versions
        # of all characters are always returned.  EVT_CHAR also performs
        # other necessary keyboard-dependent translations.
        EVT_CHAR(self, self.OnKeyDown)
        EVT_KEY_UP(self, self.OnKeyUp)
        
        EVT_SIZE(self, self._OnSize)
        EVT_MOVE(self, self.OnMove)
        
        EVT_SET_FOCUS(self, self.OnSetFocus)
        EVT_KILL_FOCUS(self, self.OnKillFocus)