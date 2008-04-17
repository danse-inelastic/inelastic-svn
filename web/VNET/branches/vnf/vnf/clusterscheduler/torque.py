# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Scheduler:

    
    def __init__(self, launcher, prefix = None):
        self.prefix = prefix
        self.launcher = launcher
        return
    
    
    def submit( self, cmd ):
        cmds = [ r'echo \"%s\" | qsub' % (cmd,) ]
        return self._launch( cmds )
    

    def status( self, jobid ):
        cmds = [ 'qstat -f %s' % (jobid,) ]
        ret = self._launch( cmds )
        
        ret = ret.split( '\n' )
        ret = ret[1:] # first line removed
        d = {}
        for line in ret:
            k,v = line.split( '=' )
            d[ k.strip() ] = v.strip()
            continue
        return d


    def _launch(self, cmds):
        if self.prefix: cmds = [ self.prefix ] + cmds
        return self.launcher( ' && '.join( cmds ) )

    pass # end of Scheduler


def test():
    import os
    s = Scheduler( os.system )
    print s.submit( 'ls' )
    return


def main():
    test()
    return


if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
