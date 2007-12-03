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
from sample.Cod import Cod
from os import linesep

class DbRetrieval(Component):
    '''This is a database retrieval class.'''
    class Inventory(Component.Inventory):
        import pyre.inventory as pinv  
        cod = pinv.facility('cod', default=Cod())
        sqlite = pinv.facility('sqlite', default=Sqlite)
        #pubChem = pinv.facility('pubChem', default=PubChem())
        
    def __init__(self, species=None, symmetry=None, text=None):
        Component.__init__(self, 'DbRetrieval',facility='DbRetrieval')
        self.stats={'crystalStructure':0, 'neutronScatteringData':0, 'abInitioCalcs':0,\
                       'mdCalcs':0, 'atomicProperties':0, 'molecularStructure':0}
        #do query on cod to see if available crystal structures (eventually pubchem,pdb)
        cod = Cod(species,symmetry,text)
        data=cod.getAvailableEntries()
        self.stats['crystalStructure']=len(data)
        #do query on ab initio, md calcs database
        #do query on scattering data database
        
        #atomic property files
        #additional dbs: tuple in format (type, url, path) where type is postgresql, mysql, or sqlite
        additionalDbs=[]
        for db in additionalDbs:
            db=eval(db[0]+'(species,symmetry,text)')

    def availableData(self):
        lines=''
        for k,v in self.stats.iteritems():
            lines+=k+' '+str(v)+linesep
        return lines
        
    def addDbs(self, url, path):
        '''adds additional dbs to db search'''
        
        
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
        
if __name__ == '__main__':
    s = Sample()
    s.atom=Atom3.atom('Ar')
    s.show()
    
    