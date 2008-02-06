#!/usr/bin/env python

from sample.sampleCreation.supercell.Supercell import Supercell

def double():
    sc = Supercell(readFilePath='kc24DomainsH2OneFrame.xyz',coordType='cartesian')#, 1, 1, 1)#, coordType='cartesian')
    sc.i.m=1
    sc.i.n=1
    sc.i.l=2
    sc.create()
    sc.writeSupCellXYZFile('kc24DomainsH2OneFrameStacked.xyz')
#        sc = Supercell(coords, cell, 1, 1, 2)#, coordType='cartesian')
#        sc.writeSupCellXYZFile('MOF74_neutron_4K_a-1x1x2.xyz')
#        sc = Supercell(coords, cell, 2, 2, 2)#, coordType='cartesian')
#        sc.writeSupCellXYZFile('MOF74_neutron_4K_a-2x2x2.xyz')
        #assert coords==[[0.0, 0.0, 0.0], [0.0, 0.0, 0.5], 
#                        [0.33333000000000002, 0.66666999999999998, 0.0], 
#                        [0.66666999999999998, 0.33333999999999997, 0.5]]
    


if __name__ == '__main__': double() 
