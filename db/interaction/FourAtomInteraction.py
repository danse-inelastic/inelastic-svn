DANSEINSTALL='/home/brandon/DANSE' #temporary fix


from pprint import PrettyPrinter
from os import sep
from pyre.components.Component import Component
from sample.globals import shareDir

class FourAtomInteraction(Component):
    '''This is a helper class that looks for atomic properties corresponding
to four atoms such as forcefield parameters'''

    def __init__(self, atom1, atom2, atom3, atom4):
        #eventually will find properties from database
        #for now just get them from files in twoAtom directory
        #files=listdir(DANSEINSTALL+sep+'crystal'+sep+'atomHierarchy'+sep+'twoAtomProperties')
        #            atom1+'-'atom2 in files
        Component.__init__(self, 'FourAtomInteraction', facility=None)
        self.info=None
        self.atom1=atom1
        self.atom2=atom2
        self.atom3=atom3
        self.atom4=atom4
        self.potential=None
        self.name=None
        self.databaseFile=shareDir+sep+'interaction'+sep+'interactionDb'+sep+\
        'fourAtom'+sep+atom1+'-'+atom2+'-'+atom3+'-'+atom4
        try:
            f=file(self.databaseFile, 'r')
            self.info=eval(f.read().strip())
        except IOError, (errno, strerror):
            print "I/O error(%s): %s" % (errno, strerror)
            print 'error reading atom database' 
        else:
            f.close()
    
    def assignInteraction(self, name):
        self.potential=self.info[name]
        self.name=name
    
    def getAssignedInteraction(self):
        return self.potential
        
    def getAvailableInteractions(self, name):
        pp=PrettyPrinter()
        return pp.pprint(self.info)
    
    def setInteraction(self, label, paramsAndValues):
        self.info[label]=paramsAndValues
        f=file(self.databaseFile, 'w')
        pp=PrettyPrinter(stream=f)
        pp.pprint(self.info)
        # print >>f, self.info
        f.close()

    
#    def __getattr__(self, name):
#        if 'info' in self.__dict__.keys():
#            if name in self.info.keys():
#                return self.info[name]
#        else:
#            return self.__getattr__(self, name)
#        
#    def __setattr__(self,label,paramsAndValues):
#        # add a new
#        self.info[label]=paramsAndValues
        
#    def __repr__(self):
#        return '<Two Atom object for '+self.atom1+'-'+self.atom2+'>'

if __name__ == "__main__":
    ta=FourAtomInteraction('O','C','N','N')
    ta.assignInteraction('torsionGulpEx10')
    print ta.getAssignedInteraction()

