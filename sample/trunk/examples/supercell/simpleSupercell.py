"""
do graphite 2x1x1 supercell from fractional xyz coordinates
"""
from ccp1gui.Supercell import Supercell

lattice=[[2.456, 0.0, 0.0],[-1.228, 2.1269583916945813, 0.0]
         ,[0.0, 0.0, 6.696]]
fracUnitCell=[['C', 0.0, 0.0, 0.0], ['C', 0.0, 0.0, 0.5], 
                ['C', 0.33333000000000002, 0.66666999999999998, 0.0], 
                ['C', 0.66666999999999998, 0.33333999999999997, 0.5]]
supercellFromFrac = Supercell(fracUnitCell,lattice,2,2,1)
coords = supercellFromFrac.getSupercellFractionalCoordinates()
#print coords
supercellFromFrac.writeSupCellXYZFile('221graphite.xyz')
print supercellFromFrac.getSupercellLatticeVectors()


