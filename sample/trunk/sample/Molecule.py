import numpy
import  Matrix 
import  copy
import  LinearAlgebra
#import arrayfns
#from math import cos,sin
import math
import os

class Molecule:  
    """Representation of a molecule"""

    def __init__(
        self,
        atomList=None, 
        name=None,
        formula='H2'
        ):
      
        self.atomList = atomList
        self.name  = name
        self.formula = formula
        
#        self.atomlist=[]
#        for i in range(0, len(AtomNames)):
#            for j in range(0, len(PositionsList[i])):
#                self.atomlist.append( (AtomNames[i],j ) )

#    def __deepcopy__(self):
#        res = CrystalStructure()
#        res.cellvectors = numpy.array(self.cellvectors, copy=1)
#        res.AtomNames  = copy.copy(self.AtomNames)
#        res.PositionsList = copy.copy(self.PositionsList)
#        for i in range(0, len(res.PositionsList)):
#            res.PositionsList[i] = numpy.array(res.PositionsList[i],  copy=1 )
#        return res

    def getListOfAtoms(self):
        return

    def getFormula(self):
        return 
    
    def getConnectivity(self):
        return 

  
