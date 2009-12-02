# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



# Dummy is a very simple data object with attributes of simple
# types such as int, str, float, etc.
# It does not have references or reference sets.
class CodQuery:

    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)
        return

    a = 'aa'
    x = 3.0
    i = 1
    b = True
    vec = [1.,2.,3.]
    mat = [ [1.,0.,0,2],
            [0,1,0,0],
            [0,0,1,0],]



# computation and job are two data objects that are associated.
# This example demonstrates how you establish a has-a association.
class Computation:

    about = ''

    def __init__(self, about):
        self.about = about
        return

class Job:

    def __init__(self, server, computation):
        self.server = server
        self.computation = computation

    server = 'octopod.danse.us'
    computation = Computation('') # This establish the has-a association between job and computation, meaning each job owns a computation.
    


# This example demonstrates
#  1. polymorphic reference
#  2. reference set
class AbstractShape(object): pass
class Box(AbstractShape):
    def __init__(self, x,y,z): self.x=x; self.y=y; self.z=z
    x = 1.
    y = 2.
    z = 3.
class Cylinder(AbstractShape):
    def __init__(self, r,h): self.r=r; self.h=h
    r = 1.
    h = 2.

class Atom:
    def __init__(self, symbol=None): self.symbol = symbol or self.__class__.symbol
    symbol = 'H'

class Structure:
    def __init__(self, shape, atoms):
        self.shape = shape
        self.atoms = atoms
        return
    shape = AbstractShape() # This establishes a polymorphic reference, because the type of the instance is an abstract class (its name starts with 'Abstract')
    atoms = [Atom()] # This establishes a reference set.
    


# class without ctor
class Sample:

    shape = AbstractShape()
    

# This example demonstrates __establishInventory__ and __restoreFromInventory__
class Position:
    def __init__(self): self._x = self._y = self._z = 0
    def setX(self, x): self._x = x
    def setY(self, y): self._y = y
    def setZ(self, z): self._z = z
    def getX(self): return self._x
    def getY(self): return self._y
    def getZ(self): return self._z

    x = y = z = 0.
    def __establishInventory__(self, inventory):
        inventory.x =  self._x
        inventory.y =  self._y
        inventory.z =  self._z
    def __restoreFromInventory__(self, inventory):
        self.setX(inventory.x)
        self.setY(inventory.y)
        self.setZ(inventory.z)
    
        

# version
__id__ = "$Id$"

