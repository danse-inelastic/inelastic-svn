import wx
import  wx.wizard as wiz
        
[wxID_BrowseButton, wxID_NetcdfFile, 
] = [wx.NewId() for _init_ctrls in range(2)]
        
class NetcdfFileDialog(wiz.WizardPageSimple):
    
#    def _init_sizers(self):
#        # generated method, don't edit
#        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        self.FilenameTextCtrl = wx.TextCtrl(id=wxID_NetcdfFile,
              name=u'NetcdfFile', parent=self, pos=wx.Point(96, 104),
              size=wx.Size(208, 27), style=0, value=u'')
        self.BrowseButton = wx.Button(id=wxID_BrowseButton,
              label=u'Browse', name=u'BrowseButton', parent=self,
              pos=wx.Point(320, 104), size=wx.Size(85, 32), style=0)
        self.BrowseButton.Bind(wx.EVT_BUTTON, self.OnBrowse, id=wxID_BrowseButton)
        #self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
        #self.boxSizer1.Add(self.cb, 0, wx.ALL, 5)
#        self._init_sizers()

    def __init__(self, parent):
        wiz.WizardPageSimple.__init__(self, parent)
        self._init_ctrls(parent)
        
    def OnBrowse(self,event):
        import os
        wildcard = "Netcdf (*.nc)|*.nc"
        dlg = wx.FileDialog(self,
            message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
        
        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            self.paths = dlg.GetPaths()
            self.FilenameTextCtrl.SetValue(self.paths[0])
            nextPage=self.GetNext()
            nextPage.insertItems(self.paths[0])
            #parse the files
            #for file in paths:
            #    self.x,self.y=self.chooseVariables(file)    
        dlg.Destroy()
        