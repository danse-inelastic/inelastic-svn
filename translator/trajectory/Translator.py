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

from pyre.components.Component import Component
from pyregui.inventory.extensions.OutputDir import OutputDir
from pyregui.inventory.extensions.InputFile import InputFile

class Translator(Component):
    '''given input parameters and coordinates of a trajectory, returns the coherent
    scattering function'''
    
    class Inventory(Component.Inventory):   
        import pyre.inventory as inv 
        historyFile = InputFile( ".his Filename", default = "")
        historyFile.meta['tip'] = "the trajectory file of the MD run (NetCDF format)"
        historyFile.meta['importance'] = 10

    def __init__(self, name = 'Translator', facility=None):
        Component.__init__(self, name, facility)
        self.i=self.inventory
        
    def translate(self):
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
        
        
    
    
    

    