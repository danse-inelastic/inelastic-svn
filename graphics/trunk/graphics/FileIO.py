import wx
from NetcdfFileDialog import NetcdfFileDialog
from VariableSelection import VariableSelection
import wx.wizard as wiz
        
class FileIO:
    
    def __init__(self, parent):
        self.parent = parent
    
    def OnLoadNetcdfFile(self, event):
        # Create the wizard and the pages
        #wizard = wx.PreWizard()
        #wizard.SetExtraStyle(wx.WIZARD_EX_HELPBUTTON)
        #wizard.Create(self, self.ID_wiz, "Simple Wizard",
        #              images.getWizTest1Bitmap())
        wizard = wiz.Wizard(self.parent, -1, "Netcdf import Wizard")

        page1 = NetcdfFileDialog(wizard)
        page2 = VariableSelection(wizard)
        #page3 = TitledPage(wizard, "Page 3")

        wizard.FitToPage(page1)
        
        wiz.WizardPageSimple_Chain(page1, page2)
        #wiz.WizardPageSimple_Chain(page2, page3)

        wizard.GetPageAreaSizer().Add(page1)
        if wizard.RunWizard(page1): # this executes if the wizard does not complete successfully
            self.parent.panel.backendWrap.addLine(x, y)
            
    def OnLoadScatteringFile(self, event):
        # for now assume the scattering file is in netcdf format
        import os
        wildcard = "All files (*)|*"
        dlg = wx.FileDialog(self.parent, 
            message="Choose a file",
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
            for file1 in paths:
                from Scientific.IO.NetCDF import NetCDFFile 
                file = NetCDFFile(file1, 'r')
                vars = file.variables.keys()
                sf=file.variables['sf'].getValue() #Numeric array
                q=file.variables['q'].getValue()
                time=file.variables['time'].getValue()
                for t in range(len(time)):
                    self.parent.backendWrap.addLine(q,sf[:,t])    
        dlg.Destroy()
            
    def OnLoadColumnFile(self, event):
        import os
        wildcard = "All files (*)|*"
        dlg = wx.FileDialog(self.parent, 
            message="Choose a file",
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
                self.parent.backendWrap.addLine(x, y)    
        dlg.Destroy()
        
    def extractColumns(self,filename):
        'gets the columns from a file and returns them as arrays'
        f=file(filename,'r')
        lines=f.readlines()
        x=[];y=[]
        for line in lines:
            if line[0]=="#":continue 
            words=line.split()
            if words==[]: continue
            x.append(float(words[0]))
            y.append(float(words[1]))
#            from decimal import Decimal
#            x.append(float(Decimal(eval(words[0]))))
#            y.append(float(Decimal(eval(words[1]))))
        import numpy as nx
        return nx.array(x),nx.array(y)
    
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
            if self.backend=='matplotlib':
                savefig(path)   
            elif self.backend=='vtk':
                hardcopy(path)
        dlg.Destroy()