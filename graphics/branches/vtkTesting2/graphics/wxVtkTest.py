import wx

import vtk
from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow

class Viewer(wxVTKRenderWindow):

    def __init__(self, parent):

        wxVTKRenderWindow.__init__(self, parent, -1)

        self.ren = vtk.vtkRenderer()
        self.GetRenderWindow().AddRenderer(self.ren)
        
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName("VTKExample.vtk")
        reader.SetScalarsName("_I_PORV")

        surfaceMapper = vtk.vtkDataSetMapper()
        surfaceMapper.SetInputConnection(reader.GetOutputPort())
        surfaceMapper.SetScalarRange((1e3, 2e6))

        surfaceActor = vtk.vtkActor()
        surfaceActor.SetMapper(surfaceMapper)

        self.ren.AddActor(surfaceActor)
            
        self.ren.ResetCamera()
        self.ren.BackingStoreOn()


class MainFrame(wx.Frame):

    def __init__(self, parent, id, title, size):

        wx.Frame.__init__(self, parent, id, title, size=size)
        notebook = wx.Notebook(self, -1)

        for ii in xrange(2):
            page = Viewer(notebook)
            notebook.AddPage(page, "Viewer No %d"%(ii+1))

        self.CenterOnScreen()
        self.Show()

app = wx.PySimpleApp()
frame = MainFrame(None, -1, "VTK Example", (400, 400))
app.MainLoop()
