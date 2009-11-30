#! /usr/bin/python

import numpy as np

import Vibrations
from qecalc.qecalc import QECalc
from qecalc.qetask.pwtask import PWTask
from qecalc.qetask.phtask import PHTask

class QuantumEspresso:

    def __init__(self, configfile='config.ini')

	self.name = 'quantum_espresso'
	self.configfile = configfile

    def run_quantum_espresso(self)
        '''Generate necessary files and run quantum_espresso'''
	
        #Setup d3 calculator
        d3calc = d3_qecalc(self, self.configfile)
        #Execute quantum_espresso: pw.x, ph.x and d3.x, 
        #this method is imported from qecalc, which is a parentale object of d3_qecalc
        d3calc.launch()
        #Get essential output for Tau module
        self.eigenvec,self.eigenval,self.qpoints =  d3calc.get_phonons()
        self.anh_dynamical_tensor = d3calc.get_d3tensor()

    def write_vibrations(self)
        self.vibedata = Vibrations(self.qpts,self.eigenval,self.eigenvec)
        outputfile = open('phonon.pkl','w')
        pickle.dump(self.vibedata, outputfile)
        outputfile.close()

    def get_anh_dynamical_tensor(self):
        return self.anh_dynamical_tensor

    def get_eigenvec(self):
        return self.eigenvec

    def get_eigenval(self):
        return self.eigenval

    def get_qpoints(self):
        return self.qpoints

class D3Qecalc(QECalc):
    """ Calc for d3 calculations:
    Task list:
      pw     -- PWTask
      ph     -- PHTask
      d3     -- D3Task
      taskList = [ph, pw, d3]
      future taskList will be [phpwd3, q2r,matdyn, d3q2r,d3matdyn]

    Example:
      >>> d3calc = d3_qecalc('config.ini')
      >>> d3calc.launch()
      >>> print d3calc.pw.output.property('total energy')
      >>> polVecs, freqs, qpoints =  d3calc.ph.lookupProperty('multi phonon')
      >>> D3tensor = d3calc.d3.output.property('D3 tensor')

    """

    def __init__(self, filename):
        QECalc.__init__(self, filename)
        self._eigenval = None
        self._eigenvec = None
        self._modes = None
        self._qpts = None
        self._D3tensor = None
        self.pw = PWTask(self.setting)
        self.ph = PHTask(self.setting)
        self.d3 = D3Task(self.setting)
        self.taskList = [self.pw, self.ph, self.d3]

    def get_phonons(self):
        self._eigenvec, self._eigenval, self._qpts = \
		self.ph.out.property('multi phonon')

        return self._eigenvec, self._eigenval, self._qpts

    def get_D3tensor(self):
	self._D3tensor = self.d3.output.property('D3 tensor')
	return self._D3tensor

if __name__=='__main__':
	print 'Hello World'
	   
__author__="XiaoliTang"
__date__ ="$Oct 26, 2009 12:53:54 AM$"
