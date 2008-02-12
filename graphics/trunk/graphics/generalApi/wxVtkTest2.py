import vtk
from vtk.wx.wxVTKRenderWindow import *
import wx
from pylab import *

def Intensity(x=[],y=[],z=[],Ex = []):

    #here i input the points in x,y,z form an Ex is the intensity of each point
    # every wx app needs an app
    app = wxPySimpleApp()

    # create the widget
    frame = wxFrame(None, -1, "First plot ", size=wxSize(400,400))
    widget = wxVTKRenderWindow(frame, -1)

    ren = vtk.vtkRenderer()
    widget.GetRenderWindow().AddRenderer(ren)
    numberOfOutputPoints = len(x)
    # Create a float array which represents the points.
    pcoords = vtk.vtkFloatArray()
    # Note that by default, an array has 1 component.
    # We have to change it to 3 for points
    pcoords.SetNumberOfComponents(3)
    # We ask pcoords to allocate room for at least 4 tuples
    # and set the number of tuples to 4. now 6
    pcoords.SetNumberOfTuples(numberOfOutputPoints)
    # Assign each tuple. There are 5 specialized versions of SetTuple:
    # SetTuple1 SetTuple2 SetTuple3 SetTuple4 SetTuple9
    # These take 1, 2, 3, 4 and 9 components respectively.
    x1 =0
    y1 =0
    z1 =0
    for i in range(0,numberOfOutputPoints):
        x1= x[i]; y1 = y[i]; z1 = z[i]
        pcoords.SetTuple3(i, x1, y1, z1)
        #print i,x1,y1,z1

    # Create vtkPoints and assign pcoords as the internal data array.
    points = vtk.vtkPoints()
    points.SetData(pcoords)
    #points.SetRadius(0.5)

    # Create the cells. In this case, a triangle strip with 2 triangles
    # (which can be represented by 4 points)

    strips = vtk.vtkCellArray()
    strips.InsertNextCell(numberOfOutputPoints)
    for i in range(0, numberOfOutputPoints):
        strips.InsertCellPoint(i)

    # Create an integer array with 4 tuples. Note that when using
    # InsertNextValue (or InsertNextTuple1 which is equivalent in
    # this situation), the array will expand automatically
     
    temperature = vtk.vtkDoubleArray()
    temperature.SetName("Temperature")
    #temp = arange(1,60,10)
    temp =Ex
    for i in temp :
        temperature.InsertNextValue(i)

    # Create the dataset. In this case, we create a vtkPolyData
    polydata = vtk.vtkPolyData()
    # Assign points and cells
    polydata.SetPoints(points)
    polydata.SetStrips(strips)
    # Assign scalars

    polydata.GetPointData().SetScalars(temperature)

    # Create the mapper and set the appropriate scalar range
    # (default is (0,1)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInput(polydata)
    mapper.SetScalarRange(0, max(temp))

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    #########################################################

    #########################################################

    ren.AddActor(actor)
    ren.SetBackground( 1.0, 1.0, 1.0 )

    frame.Show(1)

    app.MainLoop()
    
if __name__=='__main__':
    x=[1,2]
    y=[1,2]
    z=[1,2]
    ex=[1,2]
    Intensity(x,y,z,ex)
