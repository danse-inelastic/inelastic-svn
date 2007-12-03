#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from _journal import debug


from numpy import array


from AbstractGlobalGeometer import AbstractGlobalGeometer

class GlobalGeometer( AbstractGlobalGeometer ):

    
    import units
    length_unit = units.length.meter
    angle_unit = units.angle.degree


    def __init__(self, target, local_geometers = None,
                 registry_coordinate_system = None,
                 request_coordinate_system = None):
        '''GlobalGeometer

  - registry_coordinate_system: the coordinate system that
    will be used when elements\' location are registered.
  - request_coordinate_system: the coordinate system
    that will be used when users of this geometer
    is requesting locations of elements.
    '''
        if registry_coordinate_system is None:
            from CoordinateSystem import InstrumentScientistCS
            registry_coordinate_system = InstrumentScientistCS
            pass

        if local_geometers == None: local_geometers = []
        self._local_geometers = {}
        for lg in local_geometers:
            assert lg.registry_coordinate_system() == registry_coordinate_system
            assert lg.length_unit == self.length_unit
            assert lg.angle_unit == self.angle_unit
            lg.changeRequestCoordinateSystem( registry_coordinate_system )
            self._local_geometers[lg.target] = lg
            continue
        self._registry_coordinate_system = registry_coordinate_system

        import CoordinateSystem
        self.relative2absolute = CoordinateSystem.relative2absolute[
            registry_coordinate_system ]
        
        AbstractGlobalGeometer.__init__(self, target)

        #cache of coordinates of elements
        #the coordinate system used is the registry_coordinate_system
        self._cache = {}

        if request_coordinate_system is None:
            request_coordinate_system = registry_coordinate_system
            pass

        self.changeRequestCoordinateSystem( request_coordinate_system )
        return


    def createDefaultLocalGeometer( self, container ):
        from Geometer import Geometer
        lg = Geometer(container, self._registry_coordinate_system )
        self._addLocalGeometer( container, lg )
        return lg


    def register( self, element, offset, orientation, relative=None):
        if relative is None:
            try: parent = element.parent()
            except: parent = self.target
            relative = parent
        local_geometer = self._getLocalGeometer( relative )
        local_geometer.register( element, offset, orientation, relative )
        return


    def finishRegistration( self ):
        for geometer in self._local_geometers.values():
            geometer.finishRegistration()
            continue
        return


    def request_coordinate_system(self): return self._request_coordinate_system
    def registry_coordinate_system(self): return self._registry_coordinate_system


    def changeRequestCoordinateSystem( self, coordinate_system):
        self._request_coordinate_system = coordinate_system
        return


    def displacement( self, element1, element2):
        from utils import displacement
        return displacement( self.position(element1), self.position(element2) )


    def distance(self, element1, element2 ):
        from utils import length
        return length( self.displacement( element1, element2 ))


    def orientation( self, element): 
        r = self.pos_ori( element ) [1]
        return array(r) * self.angle_unit
        

    def position( self, element):
        p = self.pos_ori( element ) [0]
        return array(p) * self.length_unit


    def pos_ori(self, element):
        'absolute position and orientation in the request coordinate system'
        offset, orientation = self._abs_pos_ori_in_registry_coordinate_system( element )
        #convert to the request coordinate system
        from CoordinateSystem import fitCoordinateSystem
        offset, orientation = fitCoordinateSystem(
            (offset, orientation),
            self._registry_coordinate_system,
            self._request_coordinate_system,
            )
        return offset, orientation


    def _abs_pos_ori_in_registry_coordinate_system( self, element):
        t = self._cache.get(element)
        if t is None: self._cache[element] = t = self._calcPos_ori( element )
        return t


    def _calcPos_ori1(self, indexTuple):
        if len(indexTuple) == 0:
            return (0,0,0), (0,0,0)
        if len(indexTuple) == 1:
            e  = self.target.elementFromId( indexTuple[0] )
            return self._getLocalPos_ori( self.target, e )
        
        parent =  indexTuple[:-1] 
        parentPos_ori = self._abs_pos_ori_in_registry_coordinate_system(
            parent )
        
        parentElement = self.target._getDescendentFromIndexTuple( parent )
        try:
            e = parentElement.elementFromId( indexTuple[-1] )
        except AttributeError:
            msg = "'%s': no a container. But got a request "\
                  " for its child '%s'" % (
                parentElement.name, indexTuple[-1] )
            raise RuntimeError ,  msg
        
        localPos_ori = self._getLocalPos_ori( parentElement, e )
        
        return self.relative2absolute( localPos_ori, parentPos_ori )
    

    def _calcPos_ori(self, element):
        if isIndexTuple( element ): return self._calcPos_ori1(element)
        
        if element is self.target or element == '' :
            return (0,0,0), (0,0,0)
        
        if isIdentifier( element ):
            element = element.strip('/')
            path = element.split('/')
            pass
        else:
            #if it is not an identifier, I have to assume
            #it is a direct child of instrument
            msg = "element %s is not a child of instrument %s" % (
                element.name, self.target.name )
            assert element in self.target.elements(), msg
            path = [element.name]
            pass
        
        if len(path) == 1:
            #direct child of instrument
            e = self.target.elementFromName( path[0] )
            return self._getLocalPos_ori( self.target, e )
        
        parent = '/'.join( path[:-1] )
        parentPos_ori = self._abs_pos_ori_in_registry_coordinate_system(
            parent )
        
        parentElement = self.target._getDescendent( parent )
        try:
            e = parentElement.elementFromName( path[-1] )
        except AttributeError, err:
            msg = "%s: %s\n'%s': no a container. But got a request "\
                  " for its child '%s'" % (
                err.__class__.__name__, err,
                parentElement.name, path[-1] )
            raise RuntimeError ,  msg
        
        localPos_ori = self._getLocalPos_ori( parentElement, e )
        
        return self.relative2absolute( localPos_ori, parentPos_ori )
    

    def _getLocalPos_ori( self, container, element):
        lg  = self._getLocalGeometer( container )
        return lg.pos_ori( element )


    def _getLocalGeometer( self, container):
        lg = self._local_geometers.get( container )
        if lg is None:
            lg = self.createDefaultLocalGeometer( container )
        return lg


    def _addLocalGeometer( self, container, lg ):
        self._local_geometers[ container ] = lg
        return
    

    pass # end of GlobalGeometer


# helpers
def isIdentifier( e ): return isinstance(e, basestring)

def isIndexTuple( candidate ):
    if not isinstance( candidate, tuple ): return False
    for i in candidate:
        if not isinstance( i, int ): return False
        continue
    return True

    
import unittest

from unittest import TestCase
class GlobalGeometer_TestCase(TestCase):

    def test1(self):
        "GlobalGeometer: simplest instrument"
        import elements
        from Geometer import Geometer
        instrument = elements.instrument( "instrument" )
        instrument_geometer = Geometer( instrument )
        instrument_geometer.finishRegistration()
        local_geometers = [ instrument_geometer ]
        global_geometer = GlobalGeometer( instrument, local_geometers )
        return


    def test2(self):
        "GlobalGeometer: instrument with one moderator given abs position"
        import elements
        from Geometer import Geometer
        instrument = elements.ElementContainer( "instrument" )
        moderator = elements.moderator( "moderator", 100., 100., 10. ) 
        instrument.addElement( moderator )
            
        instrument_geometer = Geometer( instrument )
        instrument_geometer.register( moderator, (0,0,-5), (0,0,0) )
        instrument_geometer.finishRegistration()
        
        local_geometers = [ instrument_geometer ]
        global_geometer = GlobalGeometer( instrument, local_geometers )
        
        mod_pos = global_geometer.position( moderator ) / meter
        self.assertAlmostEqual( mod_pos[0], 0 )
        self.assertAlmostEqual( mod_pos[1], 0 )
        self.assertAlmostEqual( mod_pos[2], -5 )
        return


    def test3(self):
        "GlobalGeometer: instrument with one moderator and monitors given relative position"
        import elements
        from Geometer import Geometer
        instrument = elements.ElementContainer( "instrument" )
        moderator = elements.moderator( "moderator", 100., 100., 10. ) 
        instrument.addElement( moderator )
                             
        monitor1 = elements.monitor( "monitor1", 100., 100., 10. ) 
        instrument.addElement( monitor1 )
        monitor2 = elements.monitor( "monitor2", 100., 100., 10. ) 
        instrument.addElement( monitor2 )
        
        instrument_geometer = Geometer( instrument )
        instrument_geometer.register( moderator, (0,0,-5), (0,0,0))
        instrument_geometer.register( monitor1, (0,0,-3), (0,0,0))
        instrument_geometer.register( monitor2, (0,0,2), (0,0,0), relative = monitor1 )
        instrument_geometer.finishRegistration()

        local_geometers = [ instrument_geometer ]

        global_geometer = GlobalGeometer( instrument, local_geometers )
        
        moderator_pos = global_geometer.position( moderator ) / meter
        self.assertAlmostEqual( moderator_pos[0], 0 )
        self.assertAlmostEqual( moderator_pos[1], 0 )
        self.assertAlmostEqual( moderator_pos[2], -5 )
        
        monitor1_pos = global_geometer.position( monitor1 )  / meter
        self.assertAlmostEqual( monitor1_pos[0], 0 )
        self.assertAlmostEqual( monitor1_pos[1], 0 )
        self.assertAlmostEqual( monitor1_pos[2], -3 )
        
        monitor2_pos = global_geometer.position( monitor2 ) / meter
        self.assertAlmostEqual( monitor2_pos[0], 0 )
        self.assertAlmostEqual( monitor2_pos[1], 0 )
        self.assertAlmostEqual( monitor2_pos[2], -1 )
        return


    def test4(self):
        "GlobalGeometer: instrument with layers"
        import elements
        from Geometer import Geometer
        
        instrument = elements.instrument( "instrument" )
        
        moderator = elements.moderator( "moderator", 100., 100., 10. ) 
        instrument.addElement( moderator ) 
        
        monitor1 = elements.monitor( "monitor1", 100., 100., 10. ) 
        instrument.addElement( monitor1 )
        
        sample = elements.sample( "sample" )
        instrument.addElement( sample)
        
        detectorSystem = elements.detectorSystem( "detectorSystem" )
        instrument.addElement( detectorSystem )

        local_geometers = []
        
        detectorSystem_geometer = Geometer( detectorSystem )
        local_geometers.append( detectorSystem_geometer )
        
        #add 8X10 detectors by brute force
        for i in range(10):
            
            detpack = elements.detectorPack( "detpack%s" % i )
            detpack_geometer = Geometer( detpack )

            for j in range(8):
                name = "det%s"%j
                det = elements.detector(name)
                exec 'det_%s_%s = det' % (i,j)
                detpack.addElement( det )
                detpack_geometer.register( det, (j-3.5, 0, 0 ), (0,0,0) )
                continue
            
            detpack_geometer.finishRegistration()
            
            detectorSystem.addElement( detpack)
            local_geometers.append( detpack_geometer )
            
            detectorSystem_geometer.register( detpack, (10*i, 0, 0), (0,0,0) )
            continue

        detectorSystem_geometer.finishRegistration()

        instrument_geometer = Geometer( instrument )
        instrument_geometer.register( moderator, (0,0,-5), (0,0,0) )
        instrument_geometer.register( sample, (0,0,0), (0,0,0) )
        instrument_geometer.register( detectorSystem, (0,0,0), (0,0,0) )
        instrument_geometer.register( monitor1, (0,0,-3), (0,0,0) )
        instrument_geometer.finishRegistration()

        local_geometers.append( instrument_geometer )

        global_geometer = GlobalGeometer( instrument, local_geometers )
        
        moderator_pos = global_geometer.position( moderator ) / meter
        self.assertAlmostEqual( moderator_pos[0], 0 )
        self.assertAlmostEqual( moderator_pos[1], 0 )
        self.assertAlmostEqual( moderator_pos[2], -5 )

        detector00_pos = global_geometer.position(
            'detectorSystem/detpack0/det0') / meter
        self.assertAlmostEqual( detector00_pos[0], -3.5 )
        self.assertAlmostEqual( detector00_pos[1], 0 )
        self.assertAlmostEqual( detector00_pos[2], 0 )

        moderator2detector00 = global_geometer.displacement(
            moderator, 'detectorSystem/detpack0/det0' ) / meter
        self.assertAlmostEqual( moderator2detector00[0], -3.5 )
        self.assertAlmostEqual( moderator2detector00[1], 0 )
        self.assertAlmostEqual( moderator2detector00[2], 5 )
        
        return


    def test4a(self):
        '''GlobalGeometer: instrument with very simple layers.
        local geometers are created automatically.
        '''
        import elements
        
        instrument = elements.instrument( "instrument" )
        
        moderator = elements.moderator( "moderator", 100., 100., 10. ) 
        instrument.addElement( moderator ) 

        detectorSystem = elements.detectorSystem( 'detectorSystem' )
        instrument.addElement( detectorSystem )
        
        detpack = elements.detectorPack( 'detpack', )
        detectorSystem.addElement( detpack )

        detector = elements.detector( 'detector', )
        detpack.addElement( detector )

        instrumentGeomter = GlobalGeometer( instrument )

        instrumentGeomter.register( moderator, (0,0,0), (0,0,0) )
        instrumentGeomter.register( detectorSystem, (0,0,10), (0,0,0) )
        instrumentGeomter.register(
            detpack, (0,0,0), (0,0,0), relative = detectorSystem )
        instrumentGeomter.register(
            detector, (0,0,0), (0,0,0), relative = detpack )
        instrumentGeomter.finishRegistration()

        detposition = instrumentGeomter.position(
            'detectorSystem/detpack/detector' ) / meter
        
        self.assertAlmostEqual( detposition[0], 0 )
        self.assertAlmostEqual( detposition[1], 0 )
        self.assertAlmostEqual( detposition[2], 10 )
        return


    def test4b(self):
        '''GlobalGeometer: use elment identifier instead of element
        itself.
        local geometers are created automatically.
        '''
        import elements
        
        instrument = elements.instrument( "instrument" )
        
        moderator = elements.moderator( "moderator", 100., 100., 10. ) 
        instrument.addElement( moderator ) 

        detectorSystem = elements.detectorSystem( 'detectorSystem' )
        instrument.addElement( detectorSystem )
        
        detpack = elements.detectorPack( 'detpack', )
        detectorSystem.addElement( detpack )

        detector = elements.detector( 'detector', )
        detpack.addElement( detector )

        detpack2 = elements.Copy( 'detpack2', detpack )
        detectorSystem.addElement( detpack2 )

        instrumentGeomter = GlobalGeometer( instrument )

        instrumentGeomter.register( moderator, (0,0,0), (0,0,0) )
        instrumentGeomter.register( detectorSystem, (0,0,10), (0,0,0) )
        instrumentGeomter.register(
            detpack, (0,0,0), (0,0,0), relative = detectorSystem )
        instrumentGeomter.register(
            detector, (0,0,0), (0,0,0), relative = detpack )
        instrumentGeomter.register(
            detpack2, (0,0,1), (0,0,0), relative = detectorSystem )
        instrumentGeomter.finishRegistration()

        detposition = instrumentGeomter.position(
            'detectorSystem/detpack/detector' ) / meter
        
        self.assertAlmostEqual( detposition[0], 0 )
        self.assertAlmostEqual( detposition[1], 0 )
        self.assertAlmostEqual( detposition[2], 10 )
        
        self.assertRaises(
            Exception, instrumentGeomter.position, 
            'detectorSystem/detpack/detector/abc' )

        detposition = instrumentGeomter.position(
            'detectorSystem/detpack2/detector' ) / meter
        self.assertAlmostEqual( detposition[0], 0 )
        self.assertAlmostEqual( detposition[1], 0 )
        self.assertAlmostEqual( detposition[2], 11 )
        
        detposition = instrumentGeomter.position(
            (1,1,0) ) / meter
        self.assertAlmostEqual( detposition[0], 0 )
        self.assertAlmostEqual( detposition[1], 0 )
        self.assertAlmostEqual( detposition[2], 11 )
        
        return


    def test5(self):
        ''' GlobalGeometer: request_coordinate_system
        '''
        import elements
        
        instrument = elements.ElementContainer( "instrument" )
        
        moderator = elements.moderator( "moderator", 100., 100., 10. ) 
        instrument.addElement( moderator )

        from CoordinateSystem import McStasCS, InstrumentScientistCS
        instrumentGeomter = GlobalGeometer(
            instrument,
            registry_coordinate_system = InstrumentScientistCS,
            request_coordinate_system = McStasCS )

        instrumentGeomter.register( moderator, (1,2,3), (0,0,0) )

        instrumentGeomter.finishRegistration()
        
        pos = instrumentGeomter.position( moderator ) / meter
        
        self.assertAlmostEqual( pos[0], 2 )
        self.assertAlmostEqual( pos[1], 3 )
        self.assertAlmostEqual( pos[2], 1 )
        
        return


    pass # end of GlobalGeometer_TestCase

import units
meter = units.length.meter
    
def pysuite():
    suite1 = unittest.makeSuite(GlobalGeometer_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    unittest.TextTestRunner(verbosity=2).run(pytests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: GlobalGeometer.py 1274 2007-10-31 20:23:22Z linjiao $"

# End of file
