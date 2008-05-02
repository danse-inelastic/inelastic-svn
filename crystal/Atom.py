
def atom( *args ):
    """create an atom

    atom( 26, 57 )
    atom( 26 )
    atom( 'Fe' )
    atom( 'Fe', 57 )
    """
    if len(args) == 1:
        Z = args[0]
        A = None
    elif len(args) == 2:
        Z, A = args
    else:
        raise RuntimeError , "Unable to create an atom from %s" % ( args, )
    
    if isinstance( Z, basestring):
        symbol = Z
        Z = None
    else:
        symbol = None
        pass

    return Atom( Z = Z, symbol = symbol, mass = A )
    

from properties import *


# atom property curator

#static part of docstring of Atom class
doc = """Atom class

An object of this Atom class represent an atom in a (crystal) structure.

An atom can be created by its atomic number and optionally its atomic
mass number:

>>> Fe57 = Atom( 26, 57 )
>>> Fe = Atom( 26 )

You can obtain its property (for example, scattering length) in a similar
way one accesses a property of a normal python object:

>>> print Fe.scattering_length
"""        

#meta class for Atom class to collect all properties and set up
#some class constants.
#It establishes:
#  - Atom class's docstring
#  - a list of names of properties
#  - the list of setable attributes, "_setable", (to be used in method __setattr__ of Atom class).
class AtomPropertyCurator(type):
    

    def __init__(AtomClass, name, bases, dict):
        type.__init__(name, bases, dict)

        isotopeNumberProperties, inferredProperties, states = collectProperties( AtomClass )
        properties = isotopeNumberProperties + inferredProperties + states
        AtomClass.propertyNames = [ p.name for p in properties ]
        
        propStr = '\n'.join(
            [ "  %s: %s" % (p.name, p.doc) for p in properties ] )

        global doc
        doc += """
Here is a list of possible properties:

%s

""" % propStr

        AtomClass.__doc__ = doc
        
        AtomClass._setable = [ state.name for state in states ]
        
        pass # end of Atom

    pass #end of AtomPropertyCurator


#helper for atom property curator
def collectProperties( klass ):
    ctorargs = []
    inferred = []
    states = []
    registry = {
        CtorArg: ctorargs,
        InferredProperty: inferred,
        State: states,
        }
    for item in klass.__dict__.values():
        if not isinstance( item, Property ):continue
        registry[ item.__class__ ].append( item )
        continue
    return ctorargs, inferred, states




# Atom class
class Atom(object):

    def __init__(self, Z=None, symbol=None, mass=None):

        if Z is None and symbol is None:
            raise AttributeError, 'Cannot have both Z and symbol undefined for Atom.'
            
        if Z is not None:
            # Should Z be checked for valid value (i.e.  0 <= Z <= 103 or None) ?
            self.__dict__['Z'] = Z
            if symbol is not None and symbol != self.symbol:
                raise AttributeError, 'Incompatible Z number and symbol for Atom.'
            pass
        
        else:
            #Z is not specified, so symbol must be specified
            # We should check that the symbol passed is a valid chemical element symbol
            self.__dict__['symbol'] = symbol
            try:
                Z = self.atomic_number
            except KeyError:
                raise AttributeError, 'Invalid chemical element symbol.'
            self.__dict__['Z'] = Z
            pass 
            
        if mass is None: mass = self.average_mass
        self.__dict__['mass'] = mass
        
        return


    def __setattr__(self, name, value):
        if name not in Atom._setable:
            raise AttributeError, "Unknown attribute %s" % name
        return object.__setattr__(self, name, value)
        

    def __str__(self):
        l = []
        for prop in \
            self.propertyNames:

            value = self.__dict__.get( prop )
            if value is None: continue

            l.append( ( prop, value ) )
            continue

        rt = ','.join( ['%s=%s' % (name, value) for name,value in l ] )
        return "Atom " + rt


    # properties 
    
    # Z and mass
    Z = CtorArg( 'Z', 'atomic number' )
    symbol = CtorArg( 'symbol', 'chemical symbol' )
    mass = CtorArg( 'mass', 'atomic mass number' )


    # read-only, inferred properties
    import atomic_properties
    from utils import getModules
    modules = getModules( atomic_properties )
    del getModules, atomic_properties

    for module in modules:
        name = module.__name__.split( '.' )[-1]
        doc = module.__doc__
        lookup = module.lookup
        #print name, lookup
        cmd = "%s=InferredProperty( name, doc, lookup )" % name
        exec cmd
        del name, doc, lookup, module, cmd
        continue
    del modules


    # states
    velocity = State('velocity', 'velocity of the atom')
    displacement = State('displacement', 'displacement vector of atom')
    force = State('force', 'force on atom (vector)')
    ### should add all possible states here including but
    ### not limit to:
    ###   position( displacement ), pseudopotential, force


    __metaclass__ = AtomPropertyCurator
    
    pass





import unittest

class TestCase( unittest.TestCase ):

    def test_convenient_factory_function(self):
        "atom: convenient factory function"
        Fe57 = atom( 26, 57 )
        Fe57 = atom( "Fe", 57 )
        Fe = atom( "Fe" )
        Fe = atom( 26 )
        self._assertRaises( AttributeError, "Fe = atom( 'hello' )", globals() )

        #shall we check for validity of A?
        #self._assertRaises( Exception, "Fe = atom( 26, 33 )", globals() )

        #shall we check for this too?
        #self._assertRaises( Exception, "Fe = atom( 26.0 )", globals() )
        return
    

    def test_isotope_ctor(self):
        "Atom: isotope ctor"
        Fe57 = Atom( Z=26, mass=57 )
        print "- Z=%s" % Fe57.Z
        print "- mass=%s" % Fe57.mass
        return


    def test_undefined_state(self):
        "Atom: undefined state"
        Fe57 = Atom( Z=26, mass=57 )
        self._assertRaises( AttributeError , "Fe57.velocity", locals() )
        return

    
    def test_setable_state(self):
        "Atom: setable state"
        Fe57 = Atom( Z=26, mass=57 )
        v = (0,0,1)
        print '- Set velocity to %s ... ' % (v,), 
        Fe57.velocity = v
        print ' velocity = %s ' % (Fe57.velocity,)
        print "- velocity's documentation: %s " % Atom.velocity.doc
        return


    def test_arbitrary_prop(self):
        "Atom: set an arbitrary property"
        Fe57 = Atom( Z=26, mass=57 )
        self._assertRaises(
            AttributeError, "Fe57.some_very_very_strange_property = 'hello'",
            locals() )
        return


    def test_del_state(self):
        "Atom: delete state"
        Fe57 = Atom( Z=26, mass=57 )
        Fe57.velocity = (0,0,1)
        del Fe57.velocity
        self._assertRaises( AttributeError, 'Fe57.velocity', locals())
        return


    def test_del_ctorarg(self):
        "Atom: delete ctor arg"
        Fe57 = Atom( Z=26, mass=57 )
        self._assertRaises( AttributeError, "del Fe57.Z" , locals())
        return
        

    def test_str(self):
        "Atom: __str__"
        Fe57 = Atom( Z=26, mass=57 )
        Fe57.velocity = (0,0,1)
        print Fe57
        return


    def test_natural_element(self):
        "Atom: natural element ctor"
        Fe = Atom( 26 )
        print Fe
        return


    def _assertRaises(self, exceptionType, expression, locals):
        try:
            exec expression in locals
        except exceptionType:
            return
        
        raise AssertionError , "%s does not raise exception %s" % (
            expression, exceptionType)

    pass # end of TestCase


def main():
    testsuite = unittest.makeSuite( TestCase )
    unittest.TextTestRunner(verbosity=2).run(testsuite)
    return 

if __name__ == "__main__": main()
