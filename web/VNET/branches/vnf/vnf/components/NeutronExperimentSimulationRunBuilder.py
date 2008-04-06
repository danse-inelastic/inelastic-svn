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


class Builder:


    pyscriptname = 'simapp.py'
    shscriptname = 'run.sh'
    

    def render(self, experiment):
        return self.dispatch(experiment)


    def dispatch(self, something):
        func = 'on%s' % something.__class__.__name__
        f = getattr( self, func )
        return f( something )


    def onNeutronExperiment(self, experiment):
        instrument = experiment.instrument
        pyscriptconents, options = self.dispatch( instrument )

        sampleassembly = experiment.sampleassembly
        if sampleassembly:
            sampleassembly_files = self.dispatch( sampleassembly )
            pass
        
        parameters = [ 'ncount' ]
        for parameter in parameters:
            options[ parameter ] = getattr(experiment, parameter )
            continue

        pyscriptname = self.pyscriptname
        command = '%s %s' % (pyscriptname, ' '.join(
            ['--%s=%r' % (item, options.get(item))
             for item in options ] ) )

        shscriptname = self.shscriptname
        files = [ (pyscriptname, pyscriptconents),
                  (shscriptname, [command] ),
                  ]
        return files + sampleassembly_files

    
    def onInstrument(self, instrument):
        from InstrumentSimulationAppBuilder import Builder
        return Builder().render( instrument )


    def onSampleAssembly(self, sampleassembly):
        if sampleassembly.__class__.__name__ == 'SampleAssembly':
            from McvineSampleAssemblyBuilder import Builder
        else:
            from McstasSampleBuilder import Builder
            pass
        return Builder().render( sampleassembly )


    pass # end of Builder


# version
__id__ = "$Id$"

# End of file 
