#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                              Brandon Keith
#                      California Institute of Technology
#              (C) 2007 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from kernelGenerator.mdSqe.nMoldynBase import nMoldynBase
from kernelGenerator.mdSqe.ModifiedCommand import ModifiedCommand


class CoherentScatteringFunction(nMoldynBase):
    '''given input parameters and coordinates of a trajectory, returns the coherent
    scattering function'''
    
    class Inventory(nMoldynBase.Inventory):   
        import pyre.inventory as inv 
        QValues= inv.str('Q Values',default='0.:0.1:10')
        QValues.meta['tip'] = 'range of Q of instrument used'
        QValues.meta['importance'] = 9
        QShellWidth = inv.float('Q Shell Width', default = 1.)
        QShellWidth.meta['tip'] = 'width of the shell'
        QShellWidth.meta['importance'] = 8
        VectorsPerShell = inv.int('Vectors per Shell',default = 50)
        VectorsPerShell.meta['tip'] = 'vectors in each Q shell'
        VectorsPerShell.meta['importance'] = 7
        QDirection = inv.str('Q Projection',default = '')
        QDirection.meta['tip'] = 'direction in which the Q vector is projected'
        QDirection.meta['importance'] = 6
        weights=inv.str('weights', default='coherent')
        weights.meta['tip'] = 'type of weight for each atom'
        weights.validator=inv.choice(['none','mass','incoherent','coherent'])
        units_q=inv.str('units_q', default='1/nm')
        units_q.meta['tip'] = 'the units to use for q vector'
        units_q.validator = inv.choice(['1/nm','1/Ang'])
        time_steps=inv.str('time_steps', default='2000')
        time_steps.meta['tip'] = 'the number of time steps'
        frequency_points=inv.str('frequency_points', default='2000')
        frequency_points.meta['tip'] = 'the number of frequency points to use'
        ft_window=inv.str('ft_window', default='10')
        ft_window.meta['tip'] = 'the fourier transform window'
        outputFilenameOmega = inv.str('S(Q,omega) filename', default='CSF_SPECT')
        outputFilenameOmega.meta['tip'] = 'output filename'
        outputFilenameTime = inv.str('S(Q,t) filename', default='CSF')
        outputFilenameTime.meta['tip'] = 'output filename'

    def __init__(self, name='CoherentScatteringFunction'):
        nMoldynBase.__init__(self, name, 'mdPostprocessing')
        self.i=self.inventory
        
    def compute(self):
        qTuple=str((str(self.i.QValues),str(self.i.QShellWidth),str(self.i.VectorsPerShell),str(self.i.QDirection)))
        self.pyreArgs={'trajectoryFilenames':[self.i.trajectoryFilename], 
            'title':self.i.title, 'q_vector_set':qTuple, 'weights':self.i.weights, 
            'units_q':self.i.units_q, 'time_steps':self.i.time_steps, 
            'frequency_points':self.i.frequency_points, 'ft_window':self.i.ft_window,
            'output_files':(self.i.outputFilenameTime,self.i.outputFilenameOmega)} 
        #this tuple was cut and paste from xMoldyn except for the last entry. 
        # it contains parameters (6th arg) that have new defaults specific to 
        # CoherentScatteringFunction  
        self.commandArgs=('Coherent Scattering Function', 
            'Scattering', 5, 'Coherent Scattering Function', 
            ['coordinates'], 
            ['q_vector_set', ('weights', 'coherent'), 'units_q', 
             'time_steps', 'frequency_points', 'ft_window'], 
            ['atom', 'deuter'], 
            [('nc', 'CSF.nc', 'csf', ''), 
             ('nc', 'CSF_SPECT.nc', 'fft', 
              'Output file for Dynamic Structure Factor')], 
            'csf', self.pyreArgs)
        self.modifiedCommand = ModifiedCommand(*self.commandArgs)
        if self.i.trajectoryFilename!="":
            self.modifiedCommand.run()
            # read back in
        else:
            print 'please load a trajectory first'
        
        
    
    
    

    