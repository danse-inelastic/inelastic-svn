#! /usr/bin/python

__author__="XiaoliTang"
__date__ ="$Oct 26, 2009 12:53:54 AM$"

import numpy as np
import string
#from idf import Polarizations, Omega2

def read_anh3dyn(fname):
    '''Obtain third order anharmonicity Aqq from QE d3.x'''
    file = open(fname,'r')

#extract the number of atoms in the unit cell out of the output file
    line = file.readline()
    line = file.readline()
    line = file.readline()
    natom = int(line.split()[1])
#    print natom

    AQQ = []
    qP  = []
    val = []
    while True:
        line = file.readline()
#        print line
        if not line:
            break
        if 'q = (' in line:
#            print line
            qP.append([float(f) for f in line.split()[3:6]])
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
                    AQQ.append([temp1,temp2,temp3])

    AQQ = (np.array(AQQ))
    qP = np.array(qP)
    Nq = len(qP)
#    print Nq
#    print qP
    AQQ.resize(Nq,natom,3,natom,natom,3,3)
#    print AQQ

    return (natom,Nq,qP,AQQ)