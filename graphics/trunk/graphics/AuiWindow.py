import wx
#print dir(wx)
import wx.aui
from graphics.SizeReportCtrl import SizeReportCtrl
from graphics.SettingsPanel import SettingsPanel
from graphics.MatplotlibWrap import MatplotlibWrap
from graphics.GnuplotWrap import GnuplotWrap
from graphics.VtkWrap import VtkWrap
from graphics.PlotBrowser import PlotBrowser
from graphics.PropertyEditor import PropertyEditor
from graphics.FileIO import FileIO
from pylab import *
 
ID_CreateWorkspaceBrowser = wx.NewId()
ID_CreatePropertyEditor = wx.NewId()
ID_CreatePlotBrowser = wx.NewId()
ID_CreateSizeReport = wx.NewId()
ID_CreateMatplotlib = wx.NewId()
ID_CreateGnuplot = wx.NewId()
ID_CreateVTK = wx.NewId()
ID_CreatePerspective = wx.NewId()
ID_CopyPerspective = wx.NewId()

ID_Settings = wx.NewId()
ID_About = wx.NewId()
ID_ColumnFile = wx.NewId()
ID_SavePlot = wx.NewId()
ID_FirstPerspective = ID_CreatePerspective+1000

#----------------------------------------------------------------------
#def GetMondrianData():
#    return \
#'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
#\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
#ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
#o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
#\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
#\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
#\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82' 
#
#def GetMondrianBitmap():
#    return wx.BitmapFromImage(GetMondrianImage())
#
#def GetMondrianImage():
#    stream = cStringIO.StringIO(GetMondrianData())
#    return wx.ImageFromStream(stream)
#
#def GetMondrianIcon():
#    icon = wx.EmptyIcon()
#    icon.CopyFromBitmap(GetMondrianBitmap())
#    return icon

class MainPlotWindow(wx.Frame):
    
    #currentItem=None
    
    def __init__(self, parent, id=-1, title="", pos=wx.DefaultPosition,
                size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE |
                wx.SUNKEN_BORDER | wx.CLIP_CHILDREN):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        # tell FrameManager to manage this frame        
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        self._perspectives = []
        self.n = 0
        self.x = 0
#        self.backend='vtk'
        #self.SetIcon(GetMondrianIcon())
        self.plotItems={}
        #self.currentItem=None

        # create menu
        mb = wx.MenuBar()
        file_menu = wx.Menu()
        file_menu.Append(ID_ColumnFile, "Load File: Column Data")
        file_menu.Append(ID_SavePlot, "Save Plot")
        file_menu.Append(wx.ID_EXIT, "Exit")
        view_menu = wx.Menu()
        view_menu.Append(ID_CreateWorkspaceBrowser, "Show Workspace Browser")
        view_menu.Append(ID_CreatePropertyEditor, "Show Property Editor")
        view_menu.Append(ID_CreatePlotBrowser, "Show Plot Browser")
        view_menu.Append(ID_CreateSizeReport, "Show Size Reporter")
        view_menu.Append(ID_CreateMatplotlib, "Show Matplotlib")
        #view_menu.Append(ID_CreateGnuplot, "Show Gnuplot")
        view_menu.Append(ID_CreateVTK, "Show VTK")        
        options_menu = wx.Menu()
        options_menu.Append(ID_Settings, "Settings Pane")
        self._perspectives_menu = wx.Menu()
        self._perspectives_menu.Append(ID_CreatePerspective, "Create Perspective")
        self._perspectives_menu.Append(ID_CopyPerspective, "Copy Perspective Data To Clipboard")
        self._perspectives_menu.AppendSeparator()
        self._perspectives_menu.Append(ID_FirstPerspective+0, "Default Startup")
        help_menu = wx.Menu()
        help_menu.Append(ID_About, "About...")
        mb.Append(file_menu, "File")
        mb.Append(view_menu, "View")
        mb.Append(self._perspectives_menu, "Perspectives")
        mb.Append(options_menu, "Options")
        mb.Append(help_menu, "Help")
        self.SetMenuBar(mb)
        
#        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
#        self.statusbar.SetStatusWidths([-2, -3])
#        self.statusbar.SetStatusText("Ready", 0)
#        self.statusbar.SetStatusText("", 1)
        # min size for the frame itself isn't completely done.
        # see the end up FrameManager::Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))

        # create a practice toolbar
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb1.SetToolBitmapSize(wx.Size(48,48))
        tb1.AddLabelTool(101, "Test", wx.ArtProvider_GetBitmap(wx.ART_ERROR))
        tb1.AddSeparator()
        tb1.AddLabelTool(102, "Test", wx.ArtProvider_GetBitmap(wx.ART_QUESTION))
        tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_INFORMATION))
        tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_WARNING))
        tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_MISSING_IMAGE))
        tb1.Realize()
        
        self.io=FileIO(self)

        # add a bunch of panes
#        self._mgr.AddPane(self.CreateWorkspaceBrowser(), wx.aui.AuiPaneInfo().
#                          Name("workspace").Caption("Workspace").
#                          Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))
        self._mgr.AddPane(SettingsPanel(self, self), wx.aui.AuiPaneInfo().
                          Name("settings").Caption("Dock Manager Settings").
                          Dockable(False).Float().Hide().CloseButton(True).MaximizeButton(True))
#        self._mgr.AddPane(self.CreatePlotBrowser(), wx.LEFT)
#        self._mgr.AddPane(self.CreatePropertyEditor(), wx.RIGHT)
#        # create default center pane
#        self._mgr.AddPane(self.matplotlibController.CreateMatplotlib(), wx.CENTER)
        
        #Center
        self._mgr.AddPane(self.CreateVtk(), wx.aui.AuiPaneInfo().
                          Name("Matplotlib").Caption("Matplotlib").Center().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))
        #self._mgr.AddPane(self.CreateMatplotlib(), wx.aui.AuiPaneInfo().
        #                   Name("Matplotlib").Caption("Matplotlib").Center().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))
        #Left Pane
        self._mgr.AddPane(self.CreatePlotBrowser(), wx.aui.AuiPaneInfo().
                           Name("Plot Browser").Caption("Plot Browser").Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))
        #Right Pane
        self._mgr.AddPane(self.CreatePropertyEditor(), wx.aui.AuiPaneInfo().
                           Name("Property Editor").Caption("Property Editor").Right().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))
                                
        # add the toolbar to the manager
#        self._mgr.AddPane(tb1, wx.aui.AuiPaneInfo().
#                          Name("tb1").Caption("Big Toolbar").
#                          ToolbarPane().Top().
#                          LeftDockable(False).RightDockable(False))

        # make the default perspective
        perspective_default = self._mgr.SavePerspective()
        self._perspectives.append(perspective_default)

        # "commit" all changes made to FrameManager   
        self._mgr.Update()

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
      
        self.Bind(wx.EVT_MENU, self.OnCreateWorkspaceBrowser, id=ID_CreateWorkspaceBrowser)
        self.Bind(wx.EVT_MENU, self.OnCreatePropertyEditor, id=ID_CreatePropertyEditor)  
        self.Bind(wx.EVT_MENU, self.OnCreatePlotBrowser, id=ID_CreatePlotBrowser)
        self.Bind(wx.EVT_MENU, self.OnCreateMatplotlib, id=ID_CreateMatplotlib)
        self.Bind(wx.EVT_MENU, self.OnCreateGnuplot, id=ID_CreateGnuplot)
        self.Bind(wx.EVT_MENU, self.OnCreateVTK, id=ID_CreateVTK)
        self.Bind(wx.EVT_MENU, self.OnCreateSizeReport, id=ID_CreateSizeReport)
        self.Bind(wx.EVT_MENU, self.OnCreatePerspective, id=ID_CreatePerspective)
        self.Bind(wx.EVT_MENU, self.OnCopyPerspective, id=ID_CopyPerspective)

        self.Bind(wx.EVT_MENU, self.OnSettings, id=ID_Settings)
        self.Bind(wx.EVT_MENU, self.io.OnLoadColumnFile, id=ID_ColumnFile)
        self.Bind(wx.EVT_MENU, self.OnSavePlot, id=ID_SavePlot)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_About)

        self.Bind(wx.EVT_MENU_RANGE, self.OnRestorePerspective, id=ID_FirstPerspective,
                  id2=ID_FirstPerspective+1000)
        
        self.testLine()
        
    def testLine(self):
        x,y=self.io.extractColumns('/home/jbk/DANSE/graphics/trunk/tests2/api/DOS_Al6x6x6-300.plot')
        self.backendWrap.addLine(x, y)
        
        # last minute testing initialization
        #self.loadPlottable()
#        import numpy as nx
#        x = nx.array([1,2,3,4,5,6])
#        y = nx.array([4,5,6,5,4,5])
#        self.loadLine(x,y)
        
    def loadLine(self,x,y):
        self.backendWrap.addLine(x, y)
        # worry abt events happening in the subpanels
        #self.Bind(wx.EVT_MENU, self.OnCreateWorkspaceBrowser, id=ID_CreateWorkspaceBrowser)

    def CreatePlotBrowser(self): 
        self.plotBrowser = PlotBrowser(self,-1, size=(100,546))    
        return self.plotBrowser
    
    def CreateMatplotlib(self):
        self.backendWrap = MatplotlibWrap(self,-1)
        setBackend(None, 'matplotlib')
        return self.backendWrap
    
    def CreateGnuplot(self): 
        self.backendWrap = GnuplotWrap(self,-1)  
        setBackend(None, 'gnuplot')  
        return self.backendWrap

    def CreateVtk(self): 
        self.backendWrap = VtkWrap(self,-1)    
        setBackend(None, 'vtk')
        return self.backendWrap

    def CreatePropertyEditor(self):
        #xmin,xmax=xlim()
        #ymin,ymax=ylim()
        #options=[('x min',str(xmin)),('x max',str(xmax))]
        #ctrl = Options(self,options)
        self.propertyEditor = PropertyEditor(self)
        return self.propertyEditor#eval(editorChoices[self.focusedPlotItem])
        
    def OnCreateWorkspaceBrowser(self, event):
        self._mgr.AddPane(self.CreateWorkspaceBrowser(), wx.aui.AuiPaneInfo().Caption("Workspace Browser Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(150, 300)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()

    def OnCreatePropertyEditor(self, event):
        self._mgr.AddPane(self.CreatePropertyEditor(), wx.aui.AuiPaneInfo().
                          Caption("Property Editor").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 300)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()
        
    def OnCreatePlotBrowser(self, event):
        self._mgr.AddPane(self.CreatePlotBrowser(), wx.aui.AuiPaneInfo().
                          Caption("Plot Browser").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()

    def OnCreateMatplotlib(self, event):
        self._mgr.AddPane(self.CreateMatplotlib(), wx.aui.AuiPaneInfo().
                          Caption("Matplotlib").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()

    def OnCreateGnuplot(self, event):
        self._mgr.AddPane(self.CreateGnuplot(), wx.aui.AuiPaneInfo().
                          Caption("Gnuplot").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()

    def OnCreateVTK(self, event):
        self._mgr.AddPane(self.CreateVtk(), wx.aui.AuiPaneInfo().
                          Caption("VTK").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()
        
    def OnCreateSizeReport(self, event):
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Caption("Client Size Reporter").
                          Float().FloatingPosition(self.GetStartPosition()).
                          CloseButton(True).MaximizeButton(True))
        self._mgr.Update()

#    def OnChangeContentPane(self, event):
#        self._mgr.GetPane("matplotlib_content").Show(event.GetId() == ID_MatplotlibContent)
#        self._mgr.GetPane("tree_content").Show(event.GetId() == ID_WorkspaceBrowserContent)
#        self._mgr.GetPane("sizereport_content").Show(event.GetId() == ID_SizeReportContent)
#        self._mgr.GetPane("propertyeditor_content").Show(event.GetId() == ID_PropertyEditorContent)
#        self._mgr.GetPane("plotbrowser_content").Show(event.GetId() == ID_PlotBrowserContent)
#        self._mgr.Update()
        
    def CreateWorkspaceBrowser(self):
        tree = wx.TreeCtrl(self, -1, wx.Point(0, 0), wx.Size(160, 250),
                           wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        root = tree.AddRoot("AUI Project")
        items = []
        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16,16)))
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16,16)))
        tree.AssignImageList(imglist)
        items.append(tree.AppendItem(root, "Item 1", 0))
        items.append(tree.AppendItem(root, "Item 2", 0))
        for ii in xrange(len(items)):
            id = items[ii]
            tree.AppendItem(id, "Subitem 1", 1)
            tree.AppendItem(id, "Subitem 2", 1)
        tree.Expand(root)
        return tree

    def CreateSizeReportCtrl(self, width=80, height=80):
        return SizeReportCtrl(self, -1, wx.DefaultPosition, wx.Size(width, height), self._mgr)
    
    def OnLoadColumnFile(self, event):
        import os
        wildcard = "All files (*)|*"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
        
        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()
            #parse the files
            for file in paths:
                x,y=self.extractColumns(file)
                self.backendWrap.addLine(x, y)    
        dlg.Destroy()
            
    def extractColumns(self,filename):
        'gets the columns from a file and returns them as arrays'
        f=file(filename,'r')
        lines=f.readlines()
        x=[];y=[]
        for line in lines:
            if line[0]=="#":continue 
            words=line.split()
            x.append(float(words[0]))
            y.append(float(words[1]))
#            from decimal import Decimal
#            x.append(float(Decimal(eval(words[0]))))
#            y.append(float(Decimal(eval(words[1]))))
        import numpy as nx
        return nx.array(x),nx.array(y)
            
  
# more stock-type controls -----------------------------------------------    

    def OnClose(self, event):
        self._mgr.UnInit()
        del self._mgr
        self.Destroy()
        
    def OnSavePlot(self, event):
        import os
        wildcard = "All files (*)|*"
        dlg = wx.FileDialog(
            self, message="Save plot as",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.CHANGE_DIR)
        
        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if backend=='matplotlib':
                savefig(path)   
            elif backend=='vtk':
                hardcopy(path)
        dlg.Destroy()

    def OnExit(self, event):
        self.Close()

    def OnAbout(self, event):
        msg = "Graphics\n" + \
              "Brandon Keith\n" + \
              "jbrkeith@gmail.com"
        dlg = wx.MessageDialog(self, msg, "About Graphics",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()        

    def GetDockArt(self):
        return self._mgr.GetArtProvider()

    def DoUpdate(self):
        self._mgr.Update()

    def OnEraseBackground(self, event):
        event.Skip()

    def OnSize(self, event):
        event.Skip()

    def OnSettings(self, event):
        # show the settings pane, and float it
        floating_pane = self._mgr.GetPane("settings").Float().Show()
        if floating_pane.floating_pos == wx.DefaultPosition:
            floating_pane.FloatingPosition(self.GetStartPosition())
        self._mgr.Update()
                
    def OnCreatePerspective(self, event):
        dlg = wx.TextEntryDialog(self, "Enter a name for the new perspective:", "AUI Test")
        dlg.SetValue(("Perspective %d")%(len(self._perspectives)+1))
        if dlg.ShowModal() != wx.ID_OK:
            return
        if len(self._perspectives) == 0:
            self._perspectives_menu.AppendSeparator()
        self._perspectives_menu.Append(ID_FirstPerspective + len(self._perspectives), dlg.GetValue())
        self._perspectives.append(self._mgr.SavePerspective())

    def OnCopyPerspective(self, event):
        s = self._mgr.SavePerspective()
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(s))
            wx.TheClipboard.Close()
        
    def OnRestorePerspective(self, event):
        self._mgr.LoadPerspective(self._perspectives[event.GetId() - ID_FirstPerspective])

    def GetStartPosition(self):
        self.x = self.x + 20
        x = self.x
        pt = self.ClientToScreen(wx.Point(0, 0))
        return wx.Point(pt.x + x, pt.y + x)

# testing---------------------------------------------------------------

def runGraphics():
    # Make a frame to show it
    app = wx.PySimpleApp()
    frame = MainPlotWindow(None, wx.ID_ANY, "Graphics", size=(1110, 590))
    #frame = wx.Frame(None,-1,'Plottables')
    #plotter = Plotter(frame)
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    runGraphics()
