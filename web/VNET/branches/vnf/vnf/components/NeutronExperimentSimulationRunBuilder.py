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

    def render(self, experiment):
        return self.dispatch(experiment)


    def dispatch(self, something):
        func = 'on%s' % something.__class__.__name__
        f = getattr( self, func )
        return f( something )


    def onNeutronExperiment(self, experiment):
        self.commandline_arguments = {}
        parameters = [ 'ncount' ]
        for parameter in parameter:
            self.commandline_arguments[ parameter ] = getattr(
                experiment, parameter )
            continue
        
        instrument = experiment.instrument
        simuapp = self.dispatch( instrument )

        sampleassembly = experiment.sampleassembly
        sampleassembly = self.dispatch( sampleassembly )
        
        return simuapp, commandline_arguments, sampleassembly

    
    def onInstrument(self, instrument):
        from InstrumentSimulationAppBuilder import Builder
        return Builder().render( instrument )


    def onSampleAssembly(self, sampleassembly):
        return


    pass # end of Builder


# version
__id__ = "$Id$"

# End of file 
