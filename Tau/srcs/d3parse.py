#! /usr/bin/python

import numpy as np

def parse_dyn(dynfile, outputfile):
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
    omega = []
    eigenV = []
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
        omega.append(file.readline().split()[6])
        for jj in range(0,natom):
            line = file.readline()
            eigenV.append(line.split()[1:7])
    line = file.readline()

    file.close()
    return np.array(qpoints), \
           np.array(omega).reshape(3 * natom), \
           np.array(eigenV), \
           np.array(dynmatrix).reshape(numberq,natom,natom,3,3)


def parse_d3(d3file,outputfile):
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
    qpoints, omega, eigenV, dynmatrix = parse_dyn('si.dyn2','si.ph.out2')
    print 'qpoints are', qpoints
    print 'frequencies are',omega
    print 'eigenV are', eigenV
    for q in range(0,len(qpoints)):
          print 'd2 at qpoint', qpoints[q], 'is:'
          print dynmatrix[q]
          print ' '

__author__="Xiaoli Tang"
__date__ ="$Nov 28, 2009 4:57:29 PM$"
