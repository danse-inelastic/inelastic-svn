import wx
import wx.wizard as wiz

[wxID_FRAME1, wxID_FRAME1LISTVIEW1, wxID_FRAME1LISTVIEW2, 
 wxID_FRAME1LISTVIEW3, wxID_FRAME1XAXIS, wxID_FRAME1YAXES, 
] = [wx.NewId() for _init_ctrls in range(6)]

ID_StartDrag = wx.NewId()

class VariableSelection(wiz.WizardPageSimple):
    
    def __init__(self, parent):
        wiz.WizardPageSimple.__init__(self, parent)
        self.variablesList = VariablesList(self)
        self.xAxisBin = XAxisBin(self)
        self.yAxisBin = YAxisBin(self)
        self.xAxis = wx.StaticText(id=wxID_FRAME1XAXIS, label=u'x axis',
              name=u'xAxis', parent=self, pos=wx.Point(248, 24), size=wx.Size(72, 17), style=0)
        self.yAxes = wx.StaticText(id=wxID_FRAME1YAXES, label=u'y axes',
              name=u'yAxes', parent=self, pos=wx.Point(248, 160), size=wx.Size(72, 24), style=0)
        #EVT_RIGHT_DOWN(self.variablesList, self.OnDragInit)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnDragInit, id=ID_StartDrag)
        
    def insertItems(self, netcdfFile):
        self.netcdfVariables = self.getNetcdfVariables(netcdfFile)
        self.variablesList.InsertItems(self.netcdfVariables, 0)
        
    def getNetcdfVariables(self,filename):
        from Scientific.IO.NetCDF import NetCDFFile 
        file = NetCDFFile(filename, 'r')
        #allDimNames = file.dimensions.keys() 
        #print allDimNames
        vars = file.variables.keys()
        return vars
    
    def OnDragInit(self, event):
        """ Begin a Drag Operation """
        # Create a Text Data Object, which holds the text that is to be dragged
        tdo = wx.TextDataObject(str(self.variableList.GetSelections()))
        # Create a Drop Source Object, which enables the Drag operation
        tds = wx.DropSource(self.variablesList)
        # Associate the Data to be dragged with the Drop Source Object
        tds.SetData(tdo)
        # Intiate the Drag Operation
        tds.DoDragDrop(True)
    
class YAxisBin(wx.ListBox):
    def __init__(self, parent):
        wx.ListBox.__init__(self, id=wxID_FRAME1LISTVIEW3, name=u'yAxisList',
              parent=parent, pos=wx.Point(248, 192), size=wx.Size(200, 136))
        dt = ListBoxDropTarget(self)
        self.SetDropTarget(dt)

class XAxisBin(wx.ListBox):
    def __init__(self, parent):
        wx.ListBox.__init__(self, id=wxID_FRAME1LISTVIEW2, name=u'xAxisList',
              parent=parent, pos=wx.Point(248, 48), size=wx.Size(200, 100))
        dt = ListBoxDropTarget(self)
        self.SetDropTarget(dt)
        
        
class ListBoxDropTarget(wx.TextDropTarget):
    def __init__(self, obj):
        wx.DropTarget.__init__(self)
        self.obj = obj

    def OnDropText(self, x, y, data):
        #self.log.WriteText("OnDrop: %d %d\n" % (x, y))
        self.obj.AppendAndEnsureVisible(data)

class VariablesList(wx.ListBox):
    
    def __init__(self, parent):
        wx.ListBox.__init__(self, id=wxID_FRAME1LISTVIEW1, name='variablesList',
              parent=parent, pos=wx.Point(8, 24), size=wx.Size(208, 304))
