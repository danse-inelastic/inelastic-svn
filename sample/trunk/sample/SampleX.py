#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.components.Component import Component
from sample.DbRetrieval import DbRetrieval

class Sample(Component):
    '''This is a container class which "holds" atoms, external conditions, 
unit cells, or anything else pertaining to the sample.  Ideas are given below.'''
    class Inventory(Component.Inventory):
        import pyre.inventory as inv  
#        id = pinv.str('id',default='0')
    
        
    def __init__(self, species=None, symmetry=None, text=None):
        Component.__init__(self, 'Sample',facility='Sample')
        self.species=species
        self.symmetry=symmetry
        self.text=text
        self.availableData=None
        self.crystalStructureQuery=None

    def getAvailableData(self):
        '''displays available data'''
        if self.availableData==None:
            dbs=DbRetrieval(self.species, self.symmetry, self.text)
            self.availableData=dbs.availableData()
            del dbs
        return self.availableData
    
    def getCrystalStructures(self):
        '''displays short form of crystal structures'''
        if self.crystalStructureQuery==None:
            from sample.Cod import Cod
            cod=Cod(self.species, self.symmetry, self.text)
            self.crystalStructureQuery=cod.getAvailableEntries()
            del cod
        return self.crystalStructureQuery
        
    def _defaults(self):
        Component._defaults(self)

    def _configure(self):
        Component._configure(self)

    def _init(self):
        Component._init(self)
        
#    def __getattr__(self,name):
#        try:
#            attr=self.name
#        except:
#            raise AttributeError, 'Unknown attribute!'
#        return attr

#    def __setattr__(self,name,value):
#        if name in self.__dict__.keys():
#            self.__dict__[name] = value
#            return
#        self.__dict__[name]=value
#        return

    def show(self):
        for k,v in self.__dict__.iteritems():
            print k,v
        