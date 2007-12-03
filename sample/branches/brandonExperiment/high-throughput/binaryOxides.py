from sampleCreation.cluster.Culster import Cluster
from sampleCreation.supercell.Supercell import Supercell
from pycifrw.CifParser
from os import listdir

structures=listdir('./binaryOxides')
structures=structures[:2]

for structure in structures:
    #open file
    f = file(structure,'r')
    contents = f.readlines()
    
    #make unit cell
    
    #make cluster
    
    #feed cluster to UFF simulator
    
    
    

#get energies/structures and rank according to top 100
    
for structure in structures:
    
    #calculate with cpmd