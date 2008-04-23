#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Collector:


    def __init__(self, path):
        '''
        path: the run directory where all files about the run should be placed.
        '''
        self.path = path
        return
    

    def render(self, sampleassembly):
        self.dispatch(sampleassembly)
        return
    

    def dispatch(self, something):
        func = 'on%s' % something.__class__.__name__
        f = getattr( self, func )
        return f( something )


    def onSampleAssembly(self, sampleassembly):
        for scatterer in sampleassembly.scatterers:
            self.dispatch( scatterer )
            continue
        return 


    def onScatterer(self, scatterer):
        realscatterer = scatterer.realscatterer
        return self.dispatch( realscatterer )


    def onShape(self, shape):
        realshape = shape.realshape
        #self.dispatch( realshape )
        return


    def onCrystal(self, crystal):
        datafile = crystal.datafile
        datapath = os.path.join( self._datadir( crystal ), datafile )
        link = os.path.join( self.path, datafile )
        self._link( datapath, link )
        return


    def onPolyXtalScatterer(self, scatterer):
        self.dispatch(scatterer.shape)
        self.dispatch( scatterer.crystal )
        for kernel in scatterer.kernels:
            self.dispatch( kernel )
            continue
        return


    def onScatteringKernel(self, kernel):
        realscatteringkernel = kernel.realscatteringkernel
        self.dispatch( realscatteringkernel )
        return


    def onPolyXtalCoherentPhononScatteringKernel(self, kernel):
        dispersion = kernel.dispersion
        self.dispatch( dispersion )
        return 


    def onPhononDispersion(self, dispersion):
        realphonondispersion = dispersion.realphonondispersion
        self.dispatch( realphonondispersion )
        return
    

    def onIDFPhononDispersion(self, dispersion):
        idfdispersion_dir = self._datadir( dispersion )
        #make a symbolic link in the run directory to the dispersion
        link = os.path.join( self.path, dispersion.id )
        self._link( idfdispersion_dir, link )
        return
    

    def _link(self, linked, link):
        cmd = 'ln -s %s %s' % (linked, link )
        from spawn import spawn
        spawn( cmd )
        return


    def _datadir(self, obj):
        from misc import datadir
        datadir = os.path.abspath( datadir() )
        path = os.path.join(
            datadir,
            obj.__class__.__name__.lower(),
            obj.id,
            )
        return path

    pass # end of Builder


import os

# version
__id__ = "$Id$"

# End of file 
