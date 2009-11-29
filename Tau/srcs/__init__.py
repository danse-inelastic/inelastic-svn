#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="XiaoliTang"
__date__ ="$Nov 10, 2009 11:02:11 AM$"

if __name__ == "__main__":
    print "Hello World";
    welcome()

def welcome():
    print 'Welcome to Tau package'
    print 'Supported by DANSE project'
    print 'It is currently under development!'
                                  

import numpy as np
from taupy.symmetry import Symmetry
from taupy.cells import get_supercell, Primitive, print_cell
from taupy.displacement import get_least_displacements, print_displacements
from taupy.anh_dynamicaltensor import get_anh_dynamical_tensor
from taupy.har_dynamicalmatrix import get_har_dynamical_matrix
from taupy.forces import Forces

class Taupy:
    def __init__(self, unitcell, supercell_matrix, displacement=0.01, symprec=1e-5):
        self.supercell_matrix = supercell_matrix
        self.symprec = symprec
        self.unitcell = unitcell
        self.displacement = displacement
        self.set_supercell()
        self.set_symmetry()
        self.set_displacements()
        self.set_supercells_with_displacements()
        
    def set_supercell(self):
        self.supercell = get_supercell(self.unitcell,
                                       self.supercell_matrix,
                                       self.symprec)

# This function should do symmetry analysis, figuring out irreducible 
# pair moves and also the map to reconstruction

    def set_symmetry(self):
	pass.
#        self.symmetry = Symmetry(self.supercell,
#                                 self.symprec)
#        print "Spacegroup: ", self.symmetry.get_international_table()

    def get_symmetry(self):
        return self.symmetry


# displace these pair atoms with the user-specified displacement
    def set_displacements(self):
        lattice = self.supercell.get_cell()
        self.displacements = []
        for disp in get_least_displacements(self.symmetry):
            atom_num = disp[0]
            disp_cartesian = np.dot(disp[1:], lattice)
            disp_cartesian = disp_cartesian / np.linalg.norm(disp_cartesian) * self.distance
            self.displacements.append({'number': atom_num, 'disp': disp_cartesian})


##Maybe here we can add mpi portion to split the jobs for vasp calculation

# generate the distorted supercell
    def set_supercells_with_displacements(self):
        supercells = []
        for disp in self.displacements:
            positions = self.supercell.get_positions()
            positions[disp['number']] += disp['disp']
            supercells.append( ase.Atoms( 
                    numbers = self.supercell.get_atomic_numbers(),
                    masses = self.supercell.get_masses(),
                    positions = positions,
                    cell = self.supercell.get_cell(),
                    pbc = True ) )

        self.supercells_with_displacements = supercells
                        
    def get_supercells_with_displacements(self):
        return self.supercells_with_displacements

    def set_post_process(self, primitive_matrix, set_of_forces):
        # Forces
        forces = []
        for i, disp in enumerate(self.displacements):
            forces.append(Forces(disp['number'], disp['disp'], set_of_forces[i]))
            
        # Primitive cell
        self.primitive = Primitive(self.supercell, primitive_matrix, self.symprec)

        # Force constants

        har_force_constant, anh_force_constants = get_force_constant(forces,
                                             self.symmetry,
                                             self.supercell,
                                             self.primitive.get_primitive_to_supercell_map())

        # Dynamical Matrix
        har_dynamical_matrix = DynamicalMatrix(self.suprcell,
                                            self.primitive,
                                            har_force_constant,
                                            self.symprec)
        anh_dynamical_tensor = Anh_DynamicalMatrix(self.supercell,
                                           self.primitive,
                                           force_constants,
                                           self.symprec)

        self.har_dynamical_matrix = har_dynamical_matrix
        self.anh_dynamical_tensor = anh_dynamical_tensor

    def get_frequencies(self, q):
        self.dynamical_matrix.set_dynamical_matrix(q)
        dm = self.dynamical_matrix.get_dynamical_matrix()
        frequencies = []
        for eig in np.linalg.eigvalsh(dm):
            if eig < 0:
                frequencies.append(-np.sqrt(-eig))
            else:
                frequencies.append(np.sqrt(eig))
            
        return np.array(frequencies)

    def get_tau(self,q):
        pass
        ruturn n.array(tau)

    def band_plot(self, bands):
        print "Paths in reciprocal reduced coordinates:"
        for band in bands:
            print "[%5.2f %5.2f %5.2f] --> [%5.2f %5.2f %5.2f]" % \
                (tuple(band[0]) + tuple(band[-1]))
        plot = BandStructure(bands, self.dynamical_matrix, self.primitive)
        plot.plot_band().show()
