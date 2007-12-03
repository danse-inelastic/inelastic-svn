import sys
# importing the VTK modules
# Trying first to load from vtkpython then from the modules 
# libVTK*Python.
try:
	#from vtkpython import *
	from vtk import *
except ImportError:
	try: 
		from libVTKGraphicsPython import *
		from libVTKContribPython import *
		from libVTKCommonPython import *
		from libVTKImagingPython import *
	except: 
		pass



