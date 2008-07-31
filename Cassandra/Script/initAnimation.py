import time
from vtk import *
from java.util import ArrayList
from java.io import File
from com.artenum.cassandra.plugin.isolevel import *

#
# Get the main objects
#

path_sat = "./Data/Sat-Plasma/spacecraft.vtk"
path_plasma = "./Data/Sat-Plasma/plasma.vtk"
outputImageBasePath = "./Data/sat-images/"


pipeLineManager = cassandra.getPipeLineManager()

view = pipeLineManager.getCassandraView()
pipeLineManager.addVtkFile(File(path_sat))
pipeLineManager.addVtkFile(File(path_plasma))
cassandra.getDefaultUI().hidePipeLine()
cassandra.getDefaultUI().hideConsole()

sat_dataset = pipeLineManager.getDataSetList().getElementAt(0).getVtkObject()
plasma_dataset = pipeLineManager.getDataSetList().getElementAt(1).getVtkObject()

plasma_actor = pipeLineManager.getActorList().getElementAt(1).getVtkObject()

level_start = -0.1529
scaleFactor = 1.0

step = 0.001 / scaleFactor
nbStep = 140 * scaleFactor


isoLevel = IsoLevelPlugin(pipeLineManager, cassandra.getPluginManager(), None)
isoLevel.updateIsoLevel(plasma_dataset, level_start, 1, 0,level_start, 0) 
isoLevelActor = isoLevel.getActor().getVtkObject()
isoLevelActor.GetProperty().SetOpacity(0.5)

pipeLineManager.setActorVisible(pipeLineManager.getActorList().getElementAt(0),1)
pipeLineManager.setActorVisible(pipeLineManager.getActorList().getElementAt(1),0)
pipeLineManager.setActorVisible(pipeLineManager.getActorList().getElementAt(2),1)
pipeLineManager.setActorVisible(pipeLineManager.getScalarBarList().getElementAt(0),0)
pipeLineManager.setActorVisible(pipeLineManager.getScalarBarList().getElementAt(1),0)
pipeLineManager.setActorVisible(pipeLineManager.getScalarBarList().getElementAt(2),0)

view.rotate(90,0);
view.rotate(0,90);
view.rotate(75,0);
view.rotate(0,15);
view.zoom(4.5)
