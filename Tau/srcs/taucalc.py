#! /usr/bin/python

import numpy as np
import math

from qe import QuantumEspresso
from vasp import VASP
from matter.UnitCell import getNumAtoms


class TauCalc:
    def __init__(self, unitcell, mesh, qpoint, mode, \
                 SIGMA=1.0, NFINE=32, calculator=None):

        self.pcell = unitcell
        self.pnatom = self.pcell.getNumAtoms
        self.qpoint = qpoint
        self.mode = mode
        self.NFINE = NFINE
        self.SIGMA = SIGMA
        self.mesh = mesh

        if calculator is 'vasp':
            self.scell = VASP.get_supercell
            self.eigenVal = VASP.get_eigenVal
            self.eigenVec = VASP.get_eigenVec
            self.qpoints = VASP.get_qpoints
            self.anh_dynamical_matrix = vasp.get_anh_dynamical_matrix
        elif calculator is 'quantum_espresso':
            self.eigenVal = QuantumEspresso.get_eigenVal
            self.eigenVec = QuantumEspresso.get_eigenVec
            self.qpoints = QuantumEspresso.get_qpoints
            self.anh_dynamical_matrix = QuantumEspresso.get_anh_dynamical_matrix
        else:
            raise ValueError('calculator other than vasp and \
		            quantum_espresso is currently not supported')

        self.nmode = 3 * self.pnatom

    def get_tau(self):

        iq = self.qpoint
        imode = self.mode
        q1 = self.qpoints[iq]
        ivec = get_eigenV[iq][imode]
        fofq = np.zeros(self)
        
        for jq , q2 in enumerate(self.qpoints):
            kq = self.get_kq(self,iq,jq)
            q3 = self.qpoints[kq]
            D3 = get_anh_dynamical_tensor(q1,q2,q3)
            SS1, SS2 = average_cube(self, imode,iq,jq,kq)
            Phi3 = np.zeros((self.nmode,self.nmode))

            for jmode in range(0,nmode):
                jvec = get_eigenV[jq][jmode]

                for kmode in range(0,nmode):
                    kvec = get_eigenV[kq][kmode]
                    Phi3[jmode][kmode] = dot(dot(dot(D3,ivec),jvec),kvec)
                    # Phi3 = np.dot(np.dot(np.dot(D3,ivec),jvec),kvec)
                    # _sum = _sum + np.dot(Phi3, Phi3.conj().transpose()) * \
                    #         (S1[jmode][kmode] + S2[jmode][kmode])
            fofq[jq] = np.dot(np.dot(Phi3, Phi3.conj().transpose())), (SS1 + SS2))

        self.tau = fofq.sum() / (len(self.qpoints) + 1) / self.nmode / self.nmode

        return self.tau

    def get_kq(self,iq,jq):
        i1,i2,i3 = find_indexofq(self,iq)
        j1,j2,j3 = find_indexofq(self,jq)
        for n in range(0,3):
            if 0 < (n * self.mesh[0] - i1 - j1) < self.mesh[0]:
                k1 = n * self.mesh[0] - i1 - j1
            if 0 < (n * self.mesh[1] - i2 - j2) <  self.mesh[1]:
                k2 = n * self.mesh[3] - i2 - j2
            if 0 < (n * self.mesh[2] - i3 - j3) < self.mesh[2]:
                k3 = n * self.mesh[2] - i3 - j3
        kq = (k1 - 1) * self.mesh[1] * self.mesh[2] + \
             (k2 - 1) * self.mesh[2] + k3 - 1

        return kq

    def average_cube(self,imode, iq, jq, kq):

        ojlist = sample_cubejq(self,jq)
        oklist = sample_cubekq(self,kq)
        _S1 = np.zeros((self.nmode,self,nmode))
        _S2 = np.zeros((self.nmode,self,nmode))
        oi = self.omega[iq][imode]

        for i in range(0,nfine):
            for j in range(0,nfine):
                for k in range(0,nfine):
                    olist[1.0, \
                          float(i) / nfine, \
                          float(j) / nfine, \
                          float(k) / nfine, \
                          float(i * j) / nfine / nfine, \
                          float(i * k) / nfine / nfine, \
                          float(j * k) / nfine / nfine, \
                          float(i * j * k) / nfine / nfine / nfine]
		    oj = np.dot(np.array(ojlist), np.array(olist))
		    ok = np.dot(np.array(oklist), np.array(olist))
		    nj = np.array([get_occupationnumber(temperature,frequency) \
                          for frequency in oj.tolist()])
		    nk = np.array([get_occupationnumber(temperature,frequency) \
                          for frequency in ok.tolist()])

		    while m1 in rang(0,self.nmode):
		        while m2 in rang(0,self.nmode):
		            deltaS1 = get_delta(self.SIGMA,oi - oj[m1] - ok[m2])
		            _S1[m1][m2] = _S1[m1][m2] + \
                            (nj[m1] + nk[m2] + 1) * deltaS1 / oi / oj[m1] / ok[m2]
		            deltaS2 = get_delta(self.SIGMA,oi + oj[m1] - ok[m2])
                            _S2 = _S2 + 2 * (nj[m1] - nk[m2]) * \
                                 deltaS2 / oi / oj[m1] / ok[m2]

        _S1 = _S1 / nfine / nfine / nfine
        _S2 = _S2 / nfine / nfine / nfine

        return _S1,_S2

    def sample_cubejq(self,jq):

        i, j, k = find_indexofq(self,jq)
        temp = self.omega.reshape[self.mesh[0],self.mesh[1],\
                                   self.mesh[2],self.nmode]
        oj1=temp[i, j, k]
        oj2=temp[i + 1, j, k]
        oj3=temp[i, j + 1, k]
        oj4=temp[i, j, k + 1]
        oj5=temp[i + 1, j + 1, k]
        oj6=temp[i + 1, j, k + 1]
        oj7=temp[i, j + 1, k + 1]
        oj8=temp[i + 1, j + 1, k + 1]
        ojlist=[oj1, oj2 - oj1, oj3 - oj1, oj4 - oj1, oj1 - oj2 - oj3 + oj5, \
                oj1 - oj2 - oj4 + oj6, oj1 - oj3 - oj4 + oj7, \
                -oj1 + oj2 + oj3 + oj4 - oj5 - oj6 - oj7 + oj8]

        return ojlist

    def sample_cubekq(self,kq):
        i, j, k = find_indexofq(self,kq)
        temp = self.omega.reshape[self.mesh[0],self.mesh[1], \
                                  self.mesh[2],self.nmode]
        ok1=temp[i, j, k]
        ok2=temp[i - 1, j, k]
        ok3=temp[i, j - 1, k]
        ok4=temp[i, j, k - 1]
        ok5=temp[i - 1, j - 1, k]
        ok6=temp[i - 1, j, k - 1]
        ok7=temp[i, j - 1, k - 1]
        ok8=temp[i - 1, j - 1, k - 1]
        oklist=[ok1, ok2 - ok1, ok3 - ok1, ok4 - ok1, ok1 - ok2 - ok3 + ok5,\
                ok1 - ok2 - ok4 + ok6, ok1 - ok3 - ok4 + ok7, \
                -ok1 + ok2 + ok3 + ok4 - ok5 - ok6 - ok7 + ok8]

        return oklist

    def find_indexofq(self,nq):
        i = (nq + 1) / (self.mesh[1] * self.mesh[2])
        j = (nq - i * self.mesh[1] * self.mesh[2]) / self.mesh[2]
        k = nq - i * self.mesh[1] * self.mesh[2] - j * self.mesh[2]
  
        return i,j,k

    def get_occupation_number(self, temperature, frequency)
	    
        # frequency unit: cm-1 and T unit K 
        n = max(math.exp(1.43882513 * frequency / temperature) - 1) , 1.0e-8]

        return (1.0 / n)

class Tau(object):
    '''Data Object for Phonon Lifetime
       It could be merged to vibrations data oject later on

       '''
    def __init__(self):
        self.qpoint = []
        self.tau = []

    def fetch_qpoint(self, iq):
        return self.qpoint[iq]


    def fetch_tau(self, iq, imode):
        unit = 'ps'
        return self.tau[iq][imode-1], unit
    
__author__="XiaoliTang"
