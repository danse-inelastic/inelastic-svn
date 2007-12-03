#!/usr/bin/env python
# Jiao Lin Copyright (c) 2007 All rights reserved


## \namespace sampleassembly::geometers
## This subpackage collects geometers
##

def geometer(
    target, local_geometers,
    registry_coordinate_system = "InstrumentScientist",
    **kwds ):
    
    cs = coordinateSystem( registry_coordinate_system )
    from GloabalGeometer import GloabalGeometer
    return GloabalGeometer(
        target, local_geometers, registry_coordinate_system = cs, **kwds )


def local_geometer( target, registry_coordinate_system = 'InstrumentScientist',
              **kwds ):
    cs = coordinateSystem( registry_coordinate_system )
    from Geometer import Geometer
    return Geometer( target, registry_coordinate_system = cs, **kwds )


def coordinateSystem( name ):
    '''coordinateSystem(name) --> prebuilt coordinate system of given name
    '''
    from CoordinateSystem import coordinateSystem
    return coordinateSystem( name )


from _journal import debug

# version
__id__ = "$Id: __init__.py 1257 2007-09-30 22:55:39Z linjiao $"

# End of file

