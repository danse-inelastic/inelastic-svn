#! /usr/bin/python

class Atoms(object):
    'data object for crystal'
    def __init__(self, ntype=None, symbol=None, mass=None, natom=None, positions=None, \
                 lvs=None):
        #integer
        self.ntype = ntype
        #list of strings
	self.symbol = symbol
        #list of float numbers
        self.mass = mass
        self.natom = natom
        self.positions = positions
        self.lvs = lvs 
    
    def get_rlvs(self):
	return self.rlvs

    def calc_rlvs(self,lvs):
        pass
       
    def print_info(self):
        print '# of atom types is', self.ntype
        print 'their symbols are', self.symbol
        print 'their masses are', self.mass
        print '# of atoms in the unit cell is', self.natom
        print 'the unitcell lattice vectors are', self.lvs
        print 'the relative atomic positions are', self.positions
        return