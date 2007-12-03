import wx.grid as gridlib
from graphics.PlotBrowser import PlotBrowser
# changes these imports so only those for which the backend is appropriate are imported
# or better yet completely delete the entire table and load the other one
from pylab import getp, gca
#from graphics.VtkBackend import VtkBackend
from graphics.VtkPropertyModel import VtkPropertyModel
#from graphics.common import use

#plt = VtkBackend() # Create backend instance
#use(plt, globals()) # Export public namespace of plt to globals()

class VtkPropertyTable(gridlib.PyGridTableBase):
    
    def __init__(self, parent):#, log, tableType):
        gridlib.PyGridTableBase.__init__(self)
        self.parent=parent
        self.plotItems=parent.plotItems
        self.backend=parent.backend
        self.properties=None
        self.colLabels=['property','value']
#        self.dataTypes = [gridlib.GRID_VALUE_STRING]
        self.data = [[]]
        self.vtkPropertyModel = VtkPropertyModel(self)
        self.loadModel(PlotBrowser.currentItem)

        
    def loadModel(self,model):
        # first clear the grid
        self.Clear()
        # now load the new data
        if model.find('axes')!=-1:
            #from graphics.VtkPropertyModel import axesProps as properties, axesPropDataTypes as dataTypes
            properties = self.vtkPropertyModel.axesProps
            dataTypes = self.vtkPropertyModel.axesPropDataTypes
        elif model.find('line')!=-1:
            #from graphics.VtkPropertyModel import linePropDataTypes as dataTypes
            #properties = self.vtkPropertyModel.lineProps
            dataTypes = self.vtkPropertyModel.linePropDataTypes
            
            plotItem = self.plotItems[PlotBrowser.currentItem]
            #plotItem = gca()._prop['plotitems'][0]
            properties = lineProps = plotItem._prop.items()
            properties = lineProps
        elif model.find('figure')!=-1:
            #from graphics.VtkPropertyModel import figureProps as properties, figurePropDataTypes as dataTypes
            properties = self.vtkPropertyModel.figureProps
            dataTypes = self.vtkPropertyModel.figurePropDataTypes            
        else:
            raise 'cannot find model properties'  
        properties.sort()
        dataTypes=dataTypes.items()
        dataTypes.sort()
         
        self.properties = [list(i) for i in properties]
        self.dataTypes = [i[1] for i in dataTypes]
        # turn everything into a string
        for i in range(len(self.properties)):
            self.properties[i][1] = str(self.properties[i][1])
        self.data = self.properties
            

        # now insert the data--two columns for property value and
        # as many rows as it takes
        self.InsertCols(0,2)
        self.InsertRows(len(self.data))
#        for i in range(len(properties)):
#            self.InsertRows()

    def getCurrentValue(self, row):
        objectReference = self.plotItems[PlotBrowser.currentItem]
        eval(objectReference+'.get('++')')
        return value

    def roundNChopNString(self,num):
        '''This rounds everything to three decimal places and eventually chops off trailing stuff'''
        if type(num)==type(1.0):# or type(num)==type(1):
            return round(num,3)
        elif type(num)==type([1.0]):
            newNum=[]
            for i in range(len(num)):
                newNum.append(round(num[i],3))
            return num
        elif type(num)==type((1.0,)):
            newNum=[]
            for i in range(len(num)):
                newNum.append(round(num[i],3))
            return tuple(num)
        
    # required methods for the wxPyGridTableBase interface

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data[0])

    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    # Get/Set values in the table.  The Python version of these
    # methods can handle any data-type, (as long as the Editor and
    # Renderer understand the type too,) not just strings as in the
    # C++ version.
    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''

    def SetValue(self, row, col, value):
        
        try:
            self.data[row][col] = value
        except IndexError:
            # add a new row
            self.data.append([''] * self.GetNumberCols())
            self.SetValue(row, col, value)

            # tell the grid we've added a row
            msg = gridlib.GridTableMessage(self,            # The table
                    gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
                    1                                       # how many
                    )

            self.GetView().ProcessTableMessage(msg)

    #--------------------------------------------------
    # Some optional methods

    # Called when the grid needs to display labels
    def GetColLabelValue(self, col):
        return self.colLabels[col]

    # Called to determine the kind of editor/renderer to use by
    # default, doesn't necessarily have to be the same type used
    # natively by the editor/renderer if they know how to convert.
    def GetTypeName(self, row, col):
        if col==0:
            return gridlib.GRID_VALUE_STRING
        else:
            return self.dataTypes[row]

    # Called to determine how the data can be fetched and stored by the
    # editor and renderer.  This allows you to enforce some type-safety
    # in the grid.
    def CanGetValueAs(self, row, col, typeName):
        #can't change the first column
        if col==0:
            return False
        # everything in second column depends on the row
        entryType = self.dataTypes[row].split(':')[0]
        if typeName == entryType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)
    
#    def GetAttr(self,row,col):
#        if col
    
