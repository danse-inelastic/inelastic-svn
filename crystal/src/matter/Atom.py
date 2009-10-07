from properties import *
import numpy

# atom property curator

#static part of docstring of Atom class
doc = """Atom class

An object of this Atom class represent an atom in a (crystal) structure.

An atom can be created by its symbol and optionally its position:

>>> Fe57 = Atom( 'Fe', [0,0,0] )
>>> Fe = Atom( 'Fe' )

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
# NOTE: Brandon doesn't like this third one...programmers should be able to set whatever they want...why limit them?
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
Here is a list of properties:

%s

""" % propStr

        AtomClass.__doc__ = doc
        
        #AtomClass._setable = [ state.name for state in states ]
        
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


class CartesianCoordinatesArray(numpy.ndarray):
    """Helper array for accessing Cartesian coordinates.
    Converts and updates related array of corresponding fractional
    coordinates.

    Data members:
        lattice -- instance of Lattice defining fractional coordinates
        xyz     -- instance of numpy.array storing fractional coordinates
    """

    def __new__(self, lattice, xyz):
        return numpy.zeros(3, dtype=float).view(self)

    def __init__(self, lattice, xyz):
        self.lattice = lattice
        self.xyz = xyz
        self[:] = self.lattice.cartesian(self.xyz)
        pass

    def __setitem__(self, idx, value):
        """Set idx-th coordinate and update linked self.xyz

        idx     -- index in xyz array
        value   -- new value of x, y or z
        """
        numpy.ndarray.__setitem__(self, idx, value)
        self.xyz[:] = self.lattice.fractional(self)
        return


# Atom class
class Atom(object):

    def __init__(self, atype=None, xyz=None, Z=None, mass=None, name=None, 
                 occupancy=None, lattice=None):
        """Create atom of a specified type at given lattice coordinates.
        Atom(a) creates a copy of Atom instance a.

        atype       -- element symbol string or Atom instance
        xyz         -- fractional coordinates
        name        -- atom label
        occupancy   -- fractional occupancy
        lattice     -- coordinate system for fractional coordinates
        """
        # declare non-singleton data members
        self.xyz = numpy.zeros(3, dtype=float)
        self.name = ''
        self.occupancy = 1.0
        self.lattice = None

        # assign them as needed
        if isinstance(atype, Atom):
            atype_dup = atype.__copy__()
            self.__dict__.update(atype_dup.__dict__)
        #elif isinstance(atype, str):
        else:
            self.initializeProperties(atype, mass)
        #else:
            # just leave symbol unspecified for now
            #pass
         #   self.__dict__['symbol'] = None
            
        
        
        # take care of remaining arguments
        if xyz is not None:         self.xyz[:] = xyz
        if name is not None:        self.name = name
        if occupancy is not None:   self.occupancy = float(occupancy)
        if lattice is not None:     self.lattice = lattice
        
        return


#    def __setattr__(self, name, value):
#        if name not in Atom._setable:
#            raise AttributeError, "Unknown attribute %s" % name
#        return object.__setattr__(self, name, value)
        
    def initializeProperties(self, atype, mass):
        # if symbol is specified we should check that the symbol passed is a valid chemical element symbol
        self.__dict__['symbol'] = atype
        try:
            Z = self.atomic_number
            self.__dict__['Z'] = Z
            if mass is None: mass = self.average_mass
            self.__dict__['mass'] = mass
        except KeyError:
            #raise AttributeError, 'Invalid chemical element symbol.'
            pass

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
    
    def __repr__(self):
        """simple string representation"""
        xyz = self.xyz
        s = "%-4s %8.6f %8.6f %8.6f %6.4f" % \
                (self.symbol, xyz[0], xyz[1], xyz[2], self.occupancy)
        return s
    
    def __copy__(self):
        """Return a copy of this instance.
        """
        adup = Atom(self.symbol)
        adup.__dict__.update(self.__dict__)
        # create copies for what should be copied
        adup.xyz = numpy.array(self.xyz)
        return adup
    
    ####################################################################
    # property handlers
    ####################################################################

    # xyz_cartn

    def _get_xyz_cartn(self):
        if not self.lattice:
            rv = self.xyz
        else:
            rv = CartesianCoordinatesArray(self.lattice, self.xyz)
        return rv

    def _set_xyz_cartn(self, value):
        if not self.lattice:
            self.xyz[:] = value
        else:
            self.xyz = self.lattice.fractional(value)
        return

    xyz_cartn = property(_get_xyz_cartn, _set_xyz_cartn, doc =
        """absolute Cartesian coordinates of an atom
        """ )
    
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
    
# this class does not really seem to be necessary with lattice
class Site:
    """Representation of a crystallographic site.
    A site corresponds to a position in fractional coordinates.
    It also may have an atom associated with it."""

    def __init__(self, position='', atom=None, occproba=1.0):

        for x in position:
            if (x < 0) or (x > 1):
                raise ValueError, "Site coordinates must be fractional positions."
        self._position = np.array( position )
        self._atom = atom
        self._occproba = occproba
        self.xyz=self._position

    def __str__(self):
        rt = str(self._position) + ":" + str(self._atom)
        return rt

    def setPosition(self, position):
        """Sets the position (in fractional coordinates) of a site.""" 
        for x in position:
            if (x < 0) or (x > 1):
                raise ValueError, "Site coordinates must be fractional positions."
        self._position = np.array(position)
        
    def getPosition(self):
        """Get the position (in fractional coordinates) of a site."""
        return self._position

    def setAtom(self, atom):
        """Set an atom at a site."""
        self._atom = atom

    def getAtom(self):
        """Returns the atom at a site."""
        return self._atom

    def getOccProba(self):
        """Returns the occupation probability for the atom at this site."""
        return self._occproba

    def setOccProba(self,p):
        """Sets the occupation probability for the atom at this site."""
        try:
            proba = float(p)
        except:
            raise ValueError, 'Probability should be a number in [0,1].'
        if proba <= 1.0 and proba >= 0.0:
            self.__occproba = proba
        else:
            raise ValueError, 'Probability should be a number in [0,1].'
            
        
    pass # end of class site




