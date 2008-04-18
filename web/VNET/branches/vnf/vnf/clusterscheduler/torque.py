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


import journal
debug = journal.debug( 'torque' )



class Scheduler:

    
    def __init__(self, launcher, prefix = None):
        self.prefix = prefix
        self.launcher = launcher
        return
    
    
    def submit( self, cmd ):
        cmds = [ r'echo \"%s\" | qsub' % (cmd,) ]
        return self._launch( cmds ).strip()
    

    def status( self, jobid ):
        cmds = [ 'qstat -f %s' % (jobid,) ]
        try:
            ret = self._launch( cmds )
        except:
            import traceback
            debug.log( traceback.format_exc() )
            return self.statusByTracejob( jobid )
        
        ret = ret.split( '\n' )
        ret = ret[1:] # first line removed
        if len(ret) == 0: return self.statusByTracejob( jobid )
        d = {}
        for line in ret:
            try:
                k,v = line.split( '=' )
            except:
                continue
            d[ k.strip() ] = v.strip()
            continue
        return d


    def statusByTracejob( self, jobid ):
        tag = 'Exit_status'
        cmds = [ 'tracejob %s | grep %s' % (jobid, tag) ]
        output = self._launch( cmds )

        words = output.split( )
        debug.log( 'words: %s' % words )
        status = words[3]
        
        key, value = status.split( '=' )
        assert key.lower() == 'exit_status'

        return { 'exit_status': value }
    

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
