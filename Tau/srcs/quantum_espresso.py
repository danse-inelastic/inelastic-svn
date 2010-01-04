#! /usr/bin/python

import numpy as np
import pickle

import matter
from  vibrations import Vibrations,DynamicalMatrix, AnharmonicTensor
from  qecalc.qecalc.multiphononcalc import MultiPhononCalc
from  qecalc.qecalc.d3calc import D3Calc

class QuantumEspresso:

    def __init__(self, configfile='config.ini',qgrid=None, \
                issavestructure='False', issavephonon='False', issaved3='False'):

	self.name = 'quantum_espresso'
	self.configfile = configfile
        if qgrid is None:
            return ErrorValue('qpoint sampling is required')
        self.qgrid = qgrid
	self.issavestructure=issavestructure
	self.issavephonon=issavephonon
	self.issaved3=issaved3

    def setup_quantum_espresso(self):
	pass

    def run_quantum_espresso(self):
        '''Generate necessary files and run quantum_espresso'''

        fildrho = "'si.drho'"

        #Running MultiPhonn
        mphon = MultiPhononCalc(self.configfile)
        mphon.ph.input.parse()
        mphon.ph.input.namelist('inputph').remove('fildrho')
        mphon.ph.input.qpoints.setAutomatic(self.qgrid)
        mphon.ph.input.save()
        mphon.launch([mphon.pwph, mphon.q2r])

        grid, qpoints_indep, qpoints_full = mphon.ph.output.property('qpoints')
	print grid
	print qpoints_indep
	print qpoints_full
	# This is a little bit redundant, as diffpy are basically matter
	self.atomicstructure = mphon.pw.input.structure.diffpy()

	if self.issavestructure:
	    output=open('structure.pkl','w')
	    pickle.dump(self.atomicstructure,output)
            output.close()

        mphon.matdyn.input.parse()
        mphon.matdyn.input.qpoints.set(qpoints_full)
        mphon.matdyn.input.save()
        mphon.matdyn.launch()

        pols, freqs, qpoints =  mphon.matdyn.output.property('multi phonon')

        self.phonon = Vibrations(qpoints=qpoints, frequency=freqs, \
                polarization=pols)

        if self.issavephonon:
            output = open('phonon.pkl','w')
            pickle.dump(self.phonon, output)
            output.close()
        
        d3calc = D3Calc('config.ini')
        d3tensor = []
        tasks = [d3calc.ph, d3calc.d3]
        #Gamma point first
        d3calc.ph.input.parse()
        d3calc.d3.input.parse()
        fildrhoG = "'" + fildrho.strip("'") + '_G' + "'"
        d3calc.ph.input.namelist('inputph').add('fildrho', fildrhoG)
        d3calc.d3.input.namelist('inputph').add('fild0rho', fildrhoG)
        d3calc.d3.input.namelist('inputph').add('fildrho', fildrhoG)
        d3calc.ph.input.save()
        d3calc.d3.input.save()
        #I wonder if pw needs to be launched again
        d3calc.pw.launch()
        #Gamma point only
        for task in tasks:
            task.input.parse()
            task.input.qpoints.set([0.0, 0.0, 0.0])
            task.input.save()
            task.launch()            
        d3tensor.append(d3calc.d3.output.property('d3 tensor'))

        # non Gamma points
        d3calc.ph.input.namelist('inputph').add('fildrho', fildrho)
        d3calc.d3.input.namelist('inputph').add('fildrho', fildrho)
        d3calc.ph.input.save()
        d3calc.d3.input.save()
        for qpoint in qpoints_indep[1:]:
            for task in tasks:
                task.input.parse()
                task.input.qpoints.set(qpoint)
                task.input.save()
                task.launch()
            print 'qpoint ', qpoint
            print d3calc.d3.output.property('d3 tensor')
            temp=d3calc.d3.output.property('d3 tensor')
	    print 'len is ', len(temp)
	    
	    for i in range(0,len(temp)):
                d3tensor.append(temp[i])

        self.anharmonictensor = AnharmonicTensor(qpoints=qpoints,anharmonictensor=d3tensor)

        if self.issaved3:
            output = open('d3tensor.pkl','w')
            pickle.dump(self.anharmonictensor, output)
            output.close()

    def get_structure(self):
        return self.atomicstructure

    def get_phonon(self):
        return self.phonon

    def get_anh_dynamical_tensor(self):
        return self.anharmonictensor

def test_myself():
    qe = QuantumEspresso(configfile='config.ini',qgrid=[2,2,2], \
            issavestructure='true', issavephonon='true',issaved3='true')

    qe.run_quantum_espresso()

    print qe.get_structure()
     #qe.get_structure().savetofile()

    qe.get_phonon().savetofile()

    qe.get_anh_dynamical_tensor().savetofile()

if __name__=='__main__':
	print 'Hello World'
	test_myself()	   

__author__="XiaoliTang"
__date__ ="$Oct 26, 2009 12:53:54 AM$"
