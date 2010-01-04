#! /usr/bin/python

import numpy as np
import math

from matter import Atom, Lattice, Structure
from vibrations import Vibrations

class TauCalc:
    def __init__(self, unitcell=None, qgrid=None, vibrations=None, \
                 anhTensor=None, SIGMA=1.0, NFINE=32):
	"""Phonon frequency : cm-1
           Temeperature: T
	   self.factor will be the factor of the whole equation given the standard unit
        """

        self.unitcell = unitcell
        self.qgrid = qgrid
        self.phonon = vibrations
        self.anh_tensor = anhTensor
        self.NFINE = NFINE
        self.SIGMA = SIGMA
	""" input          unit
            omega	   eV, wavenumbr  was converted to eV in the code by multiplying by h'
            Temperture     eV, K was converted to eV in the code by multiplying by kB'
            mass           atomic unit mass
            Aijk tensor	   eV/Amstrong^3
            Based on these, the self.factor is the following 
        """
	self.factor = 0.03395789 #in the unit of THz , Tau in the unit of ps
	
	#self.factor = 1.13272257 #in the unit of wavenumber
 
	if self.unitcell is None:
            pass
	else:
	    self.pnatom = len(self.unitcell.atoms)
            self.nmode = 3 * self.pnatom
	    self.numberqpt = self.qgrid[0]*self.qgrid[1]*self.qgrid[2]

	if self.phonon is None:
            pass
        else:
	    #paser output omega is in the unnit of wavenumber, now changed it to eV (h)
            cm2eV = 1.23979e-4
            self.eigenVal = self.phonon.frequency * cm2eV
            self.eigenVec = self.phonon.polarization
	    self.qpoints = self.phonon.qpoints

	# The qe parse should return a D3 tensor of pnatom*pnatom*pnatom*3*3*3
	#print np.array(self.anh_d3).shape
	if self.anh_tensor is None:
	    pass
	else:
            self.anh_d3 = [[[[[[[1+1j]*3]*3]*3]*self.pnatom]*self.pnatom]*self.pnatom]*self.numberqpt
	    print np.array(self.anh_d3).shape

    def get_number_of_atoms(self):
        self.pnatom = len(self.unitcell.atoms)+1
	return self.pnatom
    
    def get_Nmode(self):
	self.nmode = 3 * self.pnatom
	return self.nmode

    def get_tau(self, qpoint=None, mode=None, temperature= 300):
        """ Get modetau of given qpoint and mode,
        e.g.:
            mytauc = TauCalC(...)
            mytauc.get_tau(1,4)
            getting mode tau of 4th mode at firt qpoint
	    
        """
	'convert temperature K to eV T2eV = T*kB = 8.617343e-5'
	T2eV = 8.617343e-5
        temperature = temperature * T2eV
	iq = qpoint-1
	imode = mode-1
        q1 = self.qpoints[iq]
        ivec = np.array(self.eigenVec[iq][imode]).reshape(self.nmode)
        
	#loop over q2
        for jq , q2 in enumerate(self.qpoints):
            fofq = np.zeros(self.qgrid[0] * self.qgrid[1] * self.qgrid[2])
	    #sample fo the cube where q2 is the corner of the cube
	    jqlist = self.sample_cubejq(jq)
            #find q3
            kq = self.get_kq(iq,jq)
            q3 = self.qpoints[kq]
	    #sample fo the cube where q2 is the corner of the cube
	    kqlist = self.sample_cubekq(kq)
            # getting Nmode*Nmode*Nmode anharmonic tensor at (iq,jq,kq)
            D3 = np.array(self.anh_d3[jq]).reshape(self.nmode,self.nmode,self.nmode)
	    print '######################'
	    print '--------'
	    print jq,q2,kq,q3
            print jqlist
            print kqlist
	    print 'D3 shape', D3.shape
	    print '--------'
	    print ' '

            for jmode in range(0,self.nmode):
                jvec = np.array(self.eigenVec[jq][jmode]).reshape(self.nmode)
	        jval = self.eigenVal[jq][jmode]
	        ojlist = [self.eigenVal[jqlist[i]][jmode] for i in range(0,8)]
                for kmode in range(0,self.nmode):
                    kvec = np.array(self.eigenVec[kq][kmode]).reshape(self.nmode)
	            #print 'kvec shape',kvec.shape
	            kval = self.eigenVal[kq][kmode]
	            oklist = [self.eigenVal[kqlist[i]][kmode] for i in range(0,8)]
		    #V(q1,q2,q3,j1,j2,j33)
		    # Check if it is D3 * kvec.transpose()
	            a = np.tensordot(D3,kvec,axes=([2],[0]))
	            print a.shape	
	            b = np.tensordot(a,jvec,axes=([1],[0]))
	            print b.shape	
                    print ivec.shape
	            Phi3 = np.dot(b,ivec.transpose())
		    #MASS ISSUE ---------Resolve it in the QE parser
	            oj = [0]*8
	            ok = [0]*8
	            print '--------'
	            print jmode,kmode
                    print jval,jvec.shape
                    print kval,kvec.shape
	            print '--------'

	            for i in range(0,8):
                        oj[i] = self.eigenVal[jq][imode]
                        ok[i] = self.eigenVal[kq][imode]
  
                    ojlist=[oj[0], oj[1] - oj[0], oj[2] - oj[0], oj[3] - oj[0], oj[0] - oj[1] - oj[2] + oj[4], \
                            oj[0] - oj[1] - oj[3] + oj[5], oj[0] - oj[2] - oj[3] + oj[6], \
                           -oj[0] + oj[1] + oj[2] + oj[3] - oj[4] - oj[5] - oj[6] + oj[7]]

                    oklist=[ok[0], ok[1] - ok[0], ok[2] - ok[0], ok[3] - ok[0], ok[0] - ok[1] - ok[2] + ok[4], \
                            ok[0] - ok[1] - ok[3] + ok[5], ok[0] - ok[2] - ok[3] + ok[6], \
                           -ok[0] + ok[1] + ok[2] + ok[3] - ok[4] - ok[5] - ok[6] + ok[7]]

                    SS1, SS2 = self.average_cube(iq,imode,ojlist,oklist,temperature)
	            fofq[jq-1] = fofq[jq-1] + self.factor * Phi3*Phi3.conjugate() * \
	                       (SS1 + SS2)

        tau = fofq.sum() / len(self.qpoints) / self.nmode / self.nmode

        return tau

    def get_kq(self,iq,jq):
        'Momentum Conservation'

        i1,i2,i3 = self.get_q_component(iq)
        #print 'i1,i2,i3 for iq is ', i1,i2,i3,iq
        j1,j2,j3 = self.get_q_component(jq)
	#print 'j1,j2,j3 for jq is',j1,j2,j3,jq
	k1 = self.get_kq_component(1,i1,j1)
	#print 'k1',k1
	k2 = self.get_kq_component(2,i2,j2)
	#print 'k2',k2
	k3 = self.get_kq_component(3,i3,j3)
	#print 'k3',k3
	kq = self.get_q_index(k1,k2,k3)
	#print i1,i2,i3
        #print j1,j2,j3
        #print k1,k2,k3
        return kq

    def get_q_component(self, nq):
        'get indexes along b1, b2 and b3'
        i = int(nq) / self.qgrid[1] / self.qgrid[2]
        j = (int(nq) - i * self.qgrid[1] * self.qgrid[2]) / self.qgrid[2]
        k = int(nq) - i * self.qgrid[1] * self.qgrid[2] - j * self.qgrid[2]
        return i,j,k

    def get_q_index(self,i,j,k):
	qindex = i * self.qgrid[1] * self.qgrid[2] + j * self.qgrid[2] + k
	return qindex

    def get_kq_component(self,component,i,j):

	try:
            for n in range(0,3):
                #print int(self.qgrid[component-1])-i-j
                if (0 <= (n * self.qgrid[component-1]-i-j) < self.qgrid[component-1]):
                    k = n * int(self.qgrid[component-1]) - i - j
                    return k
                else:
                    continue
	except ValueError:
            print 'Could not find the proper component'

    def average_cube(self,iq,imode,ojlist,oklist,temperature):

        #_S1 = np.zeros((self.nmode,self.nmode))
        #_S2 = np.zeros((self.nmode,self.nmode))
	_S1 = 0.0
	_S2 = 0.0
        oi = self.eigenVal[iq-1][imode-1]

        for i in range(0,self.NFINE):
            for j in range(0,self.NFINE):
                for k in range(0,self.NFINE):
                    olist=[1.0, \
                          float(i) / self.NFINE, \
                          float(j) / self.NFINE, \
                          float(k) / self.NFINE, \
                          float(i * j) / self.NFINE / self.NFINE, \
                          float(i * k) / self.NFINE / self.NFINE, \
                          float(j * k) / self.NFINE / self.NFINE, \
                          float(i * j * k) / self.NFINE / self.NFINE / self.NFINE]
                    #oj and ok shall be 1D list with Nmode elements
		    oj = np.dot(np.array(ojlist), np.array(olist))
		    ok = np.dot(np.array(oklist), np.array(olist))
		    nj = self.get_occupation_number(temperature,oj)
		    nk = self.get_occupation_number(temperature,ok)
                    if oi * oj * ok > 0.0000001:

		        deltaS11 = self.get_delta(self.SIGMA, oi + oj - ok)
		        deltaS12 = self.get_delta(self.SIGMA, oj - ok - oi)
	                _S1 = _S1 + (nk - nj) * (deltaS12 - deltaS11) / \
				              (oi * oj * ok)

                        deltaS21 = self.get_delta(self.SIGMA, oj + oj - oi)
                        deltaS22 = self.get_delta(self.SIGMA, oj + oj + oi)
	                _S2 = _S2 + (nk + nj + 1 ) * \
                                              (deltaS21 - deltaS22) / (oi * oj * ok)
	  
        _S1 = _S1 / self.NFINE / self.NFINE / self.NFINE
        _S2 = _S2 / self.NFINE / self.NFINE / self.NFINE

        return _S1,_S2

    def sample_cubejq(self, jq):

        j1,j2,j3 = self.get_q_component(jq)
        jj1 = j1 - (j1 + 1) / self.qgrid[0] * self.qgrid[0] + 1
        jj2 = j2 - (j2 + 1) / self.qgrid[1] * self.qgrid[1] + 1
        jj3 = j3 - (j3 + 1) / self.qgrid[2] * self.qgrid[2] + 1
	#print j1,j2,j3
	#print jj1,j2,j3
	#print j1,jj2,j3
	#print j1,j2,jj3
	#print jj1,jj2,j3
	#print jj1,j2,jj3
	#print j1,jj2,jj3
	#print jj1,jj2,jj3
        q1 = jq
	q2 = self.get_q_index(jj1,j2,j3)
	q3 = self.get_q_index(j1,jj2,j3)
	q4 = self.get_q_index(j1,j2,jj3)
	q5 = self.get_q_index(jj1,jj2,j3)
	q6 = self.get_q_index(jj1,j2,jj3)
	q7 = self.get_q_index(j1,jj2,jj3)
	q8 = self.get_q_index(jj1,jj2,jj3)
        jqlist = [q1,q2,q3,q4,q5,q6,q7,q8]

	return jqlist

    def sample_cubekq(self, kq):

        k1, k2, k3 = self.get_q_component(kq)
	kk1 = k1 + self.qgrid[0] - 1 - (k1 + self.qgrid[0] -1) / self.qgrid[0] * self.qgrid[0]
	kk2 = k2 + self.qgrid[1] - 1 - (k2 + self.qgrid[1] -1) / self.qgrid[1] * self.qgrid[1]
	kk3 = k3 + self.qgrid[2] - 1 - (k3 + self.qgrid[2] -1) / self.qgrid[2] * self.qgrid[2]
	#print k1,k2,k3
	#print kk1,k2,k3
	#print k1,kk2,k3
	#print k1,k2,kk3
	#print kk1,kk2,k3
	#print kk1,k2,kk3
	#print k1,kk2,kk3
	#print kk1,kk2,kk3
        q1 = kq
        q2 = self.get_q_index(kk1,k2,k3)
        q3 = self.get_q_index(k1,kk2,k3)
        q4 = self.get_q_index(k1,k2,kk3)
        q5 = self.get_q_index(kk1,kk2,k3)
        q6 = self.get_q_index(kk1,k2,kk3)
        q7 = self.get_q_index(k1,kk2,kk3)
        q8 = self.get_q_index(kk1,kk2,kk3)
        kqlist = [q1,q2,q3,q4,q5,q6,q7,q8]

        return kqlist

    def get_occupation_number(self, temperature, omega):
	    
        # frequency unit: cm-1 and T unit K 
	#Here omega in unit of eV (factor h), and T in unit of eV (factor kB) 
        n = max(math.exp(omega / (temperature * 2 * math.pi)) - 1 , 1.0e-8)

        return (1.0 / n)

    def get_delta(self,sigma,x):
        y = 0.75 * (1 - x * x / sigma / sigma) / sigma
	if y<0:
            y=0   
	return y


if __name__ == '__main__':
    print "Hello World";
    
__author__="XiaoliTang"
