#! /usr/bin/python

import numpy as np

from atoms import Atoms
from vibrations import Vibrations

def parse_scf(outputfile):
    'Obtain material system information'
    unit_lvs = []
    unit_rlvs = []
    mass = []
    symbol = []
    position = []
    file = open(outputfile, 'r')
    lines = file.readlines()
    for index, line in enumerate(lines):
        if 'bravais-lattice index' in line:
            ibrav = int(line.split()[3])
        if 'lattice parameter' in line:
            lattice_constant = float(line.split()[4])
        if 'number of atoms/cell' in line:
            natom = int(line.split()[4])
        if 'number of atomic types' in line:
            ntype = int(line.split()[5])
        if 'crystal axes' in line:
            for i in range(0,3):
                unit_lvs.append([float(f) for f in lines[index+1+i].split()[3:6]])
        #unit_lvs = unit_lvs * lattice_constant
        if 'reciprocal axes:' in line:
            for i in range(0,3):
                unit_rlvs.append([float(f) for f in lines[index+1+i].split()[3:6]])
        #unit_rlvs = unit_rlvs * 2 * math.pi / lattice_constant
        if 'mass' in line:
            for i in range(0,ntype):
                symbol.append(lines[index+1+i].split()[0])
                mass.append(float(lines[index+1+i].split()[2]))
        if 'positions' in line:
            for i in range(0,natom):
                position.append([float(f) for f in lines[index+1+i].split()[6:9]])

    unitcell = Atoms(ntype, symbol, mass, natom, position, unit_lvs)
    unitcell.print_info()
    return unitcell
    

def parse_qpoints_from_dyn(dynfile):
    """parse qpoints from dyn file
    for example: si.dyn is specified in ph.input
    then ph output will have si.dyn0, si.dyn1...etc
    this parser reads in si.dyn0 first getting irreducible qpoints
    and then proceed to read all the other files getting full list of qpoints

    """
    file = open(dynfile+'0','r')
    lines = file.readlines()
    file.close()
    [nq1,nq2,nq3]=[int(f) for f in lines[0].split()]
    Nq_indep = int(lines[1].split()[0])
    qpoints_indep = []
    qpoints_full = []
    for i in range(0,Nq_indep):
        qpoints_indep.append([float(f) for f in lines[i+2].split()])
    for i in range(0,Nq_indep):
        file = open(dynfile+str(i+1),'r')
        lines = file.readlines()
        file.close()
        for index, line in enumerate(lines):
            if 'axes' in line:
                qpoints_full.append([float(f) for f in lines[index+2].split()[3:6]])

    print [nq1,nq2,nq3]
    print qpoints_indep
    print len(qpoints_full)
    return [nq1,nq2,nq3], qpoints_indep, qpoints_full
        
def parse_dyn(dynfile):
    
    file = open(dynfile,'r')
    lines = file.readlines()
    ntype = int(lines[2].split()[0])
    natom = int(lines[2].split()[1])
    qpoints = []
    dynmatrix = []
    eigenval = []
    eigenvec = []
    #numberq = lines.count('Dynamical  Matrix in cartesian axes')
    numberq = 0
    for index, line in enumerate(lines):
        if 'Dynamical Matrix in cartesian axes' in line:
            numberq = numberq + 1
            qpoints.append([float(f) for f in lines[index+2].split()[3:6]])
            for i in range(0,natom):
                for j in range(0,natom):
                    for idir in range(0,3):
                        _itemp = index+3+i*natom*3+j*3+idir+(i+1)*natom+j
                        _val = [float(f) for f in lines[_itemp].split() ]
                        dynmatrix.append(complex(_val[0],_val[1]))
                        dynmatrix.append(complex(_val[2],_val[3]))
                        dynmatrix.append(complex(_val[4],_val[5]))
        if 'omega' in line:
            eigenval.append(float(lines[index].split()[6]))
            for i in range(0,natom):
                print index+1+i
                _val = [float(f) for f in lines[index+1+i].split()[1:7]]
                eigenvec.append(complex(_val[0],_val[1]))
                eigenvec.append(complex(_val[2],_val[3]))
                eigenvec.append(complex(_val[4],_val[5]))

    #phonon = Vibrations(numberq, qpoints, eigenval, eigenvec)
    
    return phonon

def parse_d3(d3file):
    'Obtain third order anharmonic tensor from QE d3.x'

    file = open(d3file, 'r')
    lines = file.readlines()
    ntype = int(lines[2].split()[0])
    natom = int(lines[2].split()[1])
    d3tensor = []
    qpoints = []
    numberq = 0
    for index, line in enumerate(lines):
        if 'q = (' in line:
            numberq = numberq + 1
            qpoints.append([float(f) for f in lines[index].split()[3:6]])
            for mode in range(0,3*natom):
                for i in range(0,natom):
                    for j in range(0,natom):
                        for idir in range(0,3):
                            _itemp = index+mode*(natom*natom*7 + 3)+\
                                     (i*natom+j)*7 + 6 + idir*natom
                            temp = lines[_itemp]+lines[_itemp + 1]
                            _val = [float(f) for f in temp.split()]
                            d3tensor.append(complex(_val[0],_val[1]))
                            d3tensor.append(complex(_val[2],_val[3]))
                            d3tensor.append(complex(_val[4],_val[5]))

    return np.array(qpoints), \
    np.rollaxis(np.array(d3tensor).reshape(numberq,natom,3,natom,natom,3,3),2,5)

    #return np.array(qpoints), \
    #np.rollaxis(np.array(d3tensor).reshape(numberq,natom,3,natom,natom,3,3),2,5)


def parse_dyn_old(dynfile, outputfile):
    'Obtain dynamical matrix'

    file = open(outputfile, 'r')
    for line in file.readlines():
        if 'Number of q in the star =' in line:
            numberq = int(line.split()[7])
    file.close()

    file = open(dynfile,'r')
    line = file.readline()
    line = file.readline()
    line = file.readline()
    ntype = int(line.split()[0])
    natom = int(line.split()[1])
    ibrav = int(line.split()[2])
    celldm = line.split()[3:]
    symbol = [0] * ntype
    mass = [0] * ntype
    type = [0] * natom
    position = [[0] * 3] * natom
    qpoints = []
    eigenval = []
    eigenvec = []
    dynmatrix = []

    for i in range(0,ntype):
        line = file.readline()
        symbol[i] = (line.split()[1])
        mass[i] = line.split()[2]
    for i in range(0,natom):
        line = file.readline()
        type[i] = line.split()[1]
        position[i] = line.split()[2:]

    for q in range(0,numberq):
        line = file.readline()
        line = file.readline()
        line = file.readline()
        line = file.readline()
        qpoints.append([float(f) for f in line.split()[3:6]])
        line = file.readline()
        for ii in range(0, natom):
            for jj in range(0,natom):
                i1,j1 = file.readline().split()
                if int(i1) is not ii+1: raise ValueError('wrong') 
                if int(i1) is not ii+1: raise ValueError('wrong')
                for idir in range(0,3):
	            line = file.readline()
                    _val = [float(f) for f in line.split()]
                    dynmatrix.append(complex(_val[0],_val[1]))
                    dynmatrix.append(complex(_val[2],_val[3]))
                    dynmatrix.append(complex(_val[4],_val[5]))
    line = file.readline()
    line = file.readline()
    line = file.readline()
    line = file.readline()
    line = file.readline()
    line = file.readline()
    for ii in range(0,3 * natom):
        eigenval.append(float(file.readline().split()[6]))
        for jj in range(0,natom):
            line = file.readline()
            eigenvec.append(line.split()[1:7])
    line = file.readline()

    file.close()


    phonon = Vibrations(qpoints, eigenval, eigenvec, dynmatrix)

    return np.array(qpoints), \
           np.array(omega).reshape(3 * natom), \
           np.array(eigenV), \
           np.array(dynmatrix).reshape(numberq,natom,natom,3,3)


def parse_d3_old(d3file,outputfile):
    'Obtain third order anharmonic tensor from QE d3.x'

    file = open(outputfile, 'r')
    for line in file.readlines():
        if 'Number of q in the star =' in line:
            numberq = int(line.split()[7])
    file.close()

    file = open(dynfile,'r')
    line = file.readline()
    line = file.readline()
    line = file.readline()
    ntype = int(line.split()[0])
    natom = int(line.split()[1])
    ibrav = int(line.split()[2])
    celldm = line.split()[3:]
    symbol = [0] * ntype
    mass = [0] * ntype
    type = [0] * natom
    position = [[0] * 3] * natom
    qpoints = []
    dynmatrix = []

    for i in range(0,ntype):
        line = file.readline()
        symbol[i] = (line.split()[1])
        mass[i] = line.split()[2]
    for i in range(0,natom):
        line = file.readline()
        type[i] = line.split()[1]
        position[i] = line.split()[2:]

    for q in range(0,numberq):
        line = file.readline()
        line = file.readline()
        line = file.readline()
        line = file.readline()
        qpoints.append([float(f) for f in line.split()[3:6]])
        line = file.readline()
        for ii in range(0,3 * natom):
            line = file.readline()
            line = file.readline()
            if ii is not int(line.split()[1]) - 1:
               return SyntaxError('wrong match')
            line = file.readline()

            for j in range(0,natom):
                for k in range(0,natom):
                    line = file.readline()
                    for jdir in range(0,3):
                        jj = (j - 1) * 3 + jdir
                        kk = (k - 1) * 3
                        line = file.readline() + file.readline()
                        _val = [float(f) for f in line.split()]
                        d3tensor.append(complex(_val[0],_val[1]))
                        d3tensor.append(complex(_val[2],_val[3]))
                        d3tensor.append(complex(_val[4],_val[5]))

    file.close()
    #print 'qpoints are',qpoints
    #print 'ntype is ', ntype
    #print 'natom is ', natom
    #print 'd3 tensor is ', d3tensor
    return np.array(qpoints), \
    np.rollaxis(np.array(d3tensor).reshape(numberq,natom,3,natom,natom,3,3),2,5)

if __name__ == "__main__":
    print "Hello World";
    #qpoints, d3tensor = parse_d3('si.anh_X','si.d3X.out')
    parse_qpoints_from_dyn('si.dyn')

__author__="Xiaoli Tang"
__date__ ="$Nov 28, 2009 4:57:29 PM$"
