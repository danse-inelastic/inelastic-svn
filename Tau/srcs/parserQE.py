#! /usr/bin/python

__author__="XiaoliTang"
__date__ ="$Oct 26, 2009 12:53:54 AM$"

# QE parser for AQQ

import numpy as np
import string
import AQQ as AQQ

def read_anh3dyn(fname):
    '''Obtain third order anharmonicity Aqq from QE d3.x'''
    file = open(fname,'r')

#extract the number of atoms in the unit cell out of the output file
    line = file.readline()
    line = file.readline()
    line = file.readline()
    natom = int(line.split()[1])
#    print natom

    A = []
    q = []
    val = []
    while True:
        line = file.readline()
#        print line
        if not line:
            break
        if 'q = (' in line:
#            print line
            q.append([float(f) for f in line.split()[3:6]])
        if 'modo:' in line:
            print line
            line =file.readline()
            i=0
            while  i < natom*natom:
                line = file.readline()
#                print line
                i=i+1
                j=0
                while j < 3:
                    j=j+1
                    line1 = file.readline()
                    line2 = file.readline()
                    line = line1+line2
                    val = line.split()
                    temp1=complex(float(val[0]),float(val[1]))
                    temp2=complex(float(val[2]),float(val[3]))
                    temp3=complex(float(val[4]),float(val[5]))
                    A.append([temp1,temp2,temp3])

    AQQ.kpoints = (np.array(q))
  
#    print Nq
#    print qP
    A.resize(natom,3,natom,natom,3,3)

    AQQ.AQQ = np.rollaxis(np.array(A),1,4)

    print AQQ.AQQ.shape

    return (AQQ)