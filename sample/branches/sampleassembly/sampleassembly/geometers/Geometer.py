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


from AbstractGeometer import AbstractGeometer


from numpy import array

class Geometer( AbstractGeometer ):

    import units
    length_unit = units.length.meter
    angle_unit = units.angle.degree

    def __init__(self, target,
                 registry_coordinate_system = None,
                 request_coordinate_system = None):
        """
  - target: system that this geometer will work on
  - registry_coordinate_system: the coordinate system that
    will be used when elements' location are registered.
  - request_coordinate_system: the coordinate system
    that will be used when users of this geometer
    is requesting locations of elements.
    """
        assert isContainer(target), "%s is not a element container" % target
        AbstractGeometer.__init__(self, target)

        if registry_coordinate_system is None:
            from CoordinateSystem import InstrumentScientistCS
            registry_coordinate_system = InstrumentScientistCS
            pass
        
        self._registry_coordinate_system = registry_coordinate_system
        
        from LocationRegistry import LocationRegistry
        self._registry = LocationRegistry( target, registry_coordinate_system )

        from CoordinateSystem import relative2absolute
        self.relative2absolute = relative2absolute[registry_coordinate_system]
        
        self._registration_is_done = False
        # absolute position and orientation of elements
        # in the registry coordinate system
        self._abs_pos_oris = {}#instrument.rootpath: [ (0,0,0), (0,0,0) ] }
        
        if request_coordinate_system is None:
            request_coordinate_system = registry_coordinate_system
            pass

        self.changeRequestCoordinateSystem( request_coordinate_system )
        return


    def changeRequestCoordinateSystem( self, coordinate_system):
        self._request_coordinate_system = coordinate_system
        return


    def finishRegistration(self):
        for element in self.target.elements():
            self._abs_pos_ori_in_registry_coordinate_system( element )
            continue
        self._registration_is_done = True
        return


    def orientation( self, element):
        r = self.pos_ori( element ) [1]
        return array(r) * self.angle_unit

    def position( self, element):
        p = self.pos_ori( element ) [0]
        return array(p) * self.length_unit

    
    def register( self, element, offset, orientation, relative=None):
        if self._registration_is_done:
            msg = "Registration is done. You cannot register more"
            raise RuntimeError , msg
        offset = remove_unit_of_vector( offset, self.length_unit )
        orientation = remove_unit_of_vector( orientation, self.angle_unit )
        self._registry.register(
            element, offset, orientation, relative = relative)
        return


    def request_coordinate_system(self): return self._request_coordinate_system
    def registry_coordinate_system(self): return self._registry_coordinate_system

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
        'abolute position and orientation in the registry coordinate system'
        if element is self.target: return (0,0,0), (0,0,0)
        coords = self._abs_pos_oris.get(element)
        if coords:
            return coords
        self._abs_pos_oris[element] = t = self._calcPos_ori( element )
        return t
    

    def _calcPos_ori( self, element ):
        record = self._registry.location( element )
        if not record:
            msg = "Incomplete registry: %s has not been registered" % (
                element, )
            raise RuntimeError, msg

        #expand registry record
        relative, offset, orientation = record
        
        #absolute position
        if relative is None:
            abspos, absori = offset, orientation
        else:
            target = self.target
            abspos, absori = self.relative2absolute(
                (offset, orientation),
                self._abs_pos_ori_in_registry_coordinate_system( relative ) )
            pass
        return abspos, absori

    pass # end of Geometer


# helpers

def isContainer( e ):
    return hasattr( e, 'elements' )


def remove_unit_of_vector( v, unit ):
    from numpy import array
        
    v = array(v) * 1.0
    try:
        v[0] + unit
        #this means the v has compatible unit
        return v/unit
    except:
        pass

    assert len(v) == 3
    for i in v:
        if not isinstance(i, float):
            raise ValueError , "v should have unit of length: %s" %(
                v, )
        continue
    # this means v already is a unitless vector
    return v


import units
meter = units.length.meter
import unittest

from unittest import TestCase
class Geometer_TestCase(TestCase):

    def test1(self):
        "Geometer: simplest instrument"
        import elements
        instrument = elements.instrument( "instrument" )
        geometer = Geometer( instrument )
        geometer.finishRegistration()
        return


    def test2(self):
        "Geometer: instrument with one moderator given abs position"
        import elements
        instrument = elements.instrument( "instrument" )
        moderator = elements.moderator( 'moderator', 100., 100., 10. ) 
        instrument.addElement( moderator )
        geometer = Geometer( instrument )
        geometer.register( moderator, (0,0,0), (0,0,0) )
        geometer.finishRegistration()
        return


    def test3(self):
        "Geometer: instrument with one moderator and monitors given relative position"
        import elements
        instrument = elements.instrument( "instrument" )
        moderator = elements.moderator( 'moderator', 100., 100., 10. )
        instrument.addElement(moderator)            
        monitor1 = elements.monitor( 'monitor1', 100., 100., 10. ) 
        instrument.addElement( monitor1 )
        monitor2 = elements.monitor( 'monitor2', 100., 100., 10. ) 
        instrument.addElement( monitor2 )
        geometer = Geometer( instrument )
        geometer.register( moderator, (0,0,-5), (0,0,0) )
        geometer.register( monitor1, (0,0,-3), (0,0,0) )
        geometer.register( monitor2, (0,0,2), (0,0,0), relative = monitor1 )
        geometer.finishRegistration()

        monitor1pos = geometer.position( monitor1 ) / meter
        self.assertAlmostEqual( monitor1pos[0], 0 )
        self.assertAlmostEqual( monitor1pos[1], 0 )
        self.assertAlmostEqual( monitor1pos[2], -3 )

        monitor2pos = geometer.position( monitor2 ) / meter
        self.assertAlmostEqual( monitor2pos[0], 0 )
        self.assertAlmostEqual( monitor2pos[1], 0 )
        self.assertAlmostEqual( monitor2pos[2], -1 )
        return

    pass # end of Geometer_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(Geometer_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    unittest.TextTestRunner(verbosity=2).run(pytests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: Geometer.py 1274 2007-10-31 20:23:22Z linjiao $"

# End of file
