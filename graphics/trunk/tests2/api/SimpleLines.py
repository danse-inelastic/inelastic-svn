import wx
from graphics.MainPlotWindow import MainPlotWindow
from graphics.plottables import Data1D, Theory1D

# instantiate plotter window
app = wx.PySimpleApp()
frame = MainPlotWindow(None, wx.ID_ANY, "DANSE 2D Plotter", size=(805, 590))
frame.Show()

#This bypasses the property editor widget for now and interacts directly with the api

import numpy as nx

# Construct a simple graph--typically this data will be loaded
if False:
    x = nx.array([1,2,3,4,5,6],'d')
    y = nx.array([4,5,6,5,4,5],'d')
    dy = nx.array([0.2, 0.3, 0.1, 0.2, 0.9, 0.3])
else:
    x = nx.linspace(0,1.,10000)
    y = nx.sin(2*nx.pi*x*2.8)
    dy = nx.sqrt(100*nx.abs(y))/100
#put data in container--this will typically be done by gui widget
data1 = Data1D(x,y,dy=dy)
data1.xaxis('distance', 'm')
data1.yaxis('time', 's')
data2 = Theory1D(x,y,dy=dy)
#put the data in the graph container
graph=frame.matplotlibController.graph
graph.title('Walking Results')
graph.add(data1)
graph.add(data2)

# render the data onto the plot
frame.matplotlibController.replot()


#send it on its main loop
app.MainLoop()