

from pprint import PrettyPrinter
from os import sep
from pyre.components.Component import Component
from sample.globals import shareDir

class TwoAtomInteraction(Component):
    '''This is a helper class that looks for atomic properties corresponding
to two atoms such as forcefield or Born von Karman interaction parameters'''

#    class Inventory(Component.Inventory):
#        import pyre.inventory as inv  
#        #print TwoAtomInteraction.potentialChoices
#        availableInteractions = inv.str('Available Interactions', default=None)#,\
#                        #validator=inv.choice(TwoAtomInteraction.potentialChoices))
#        availableInteractions.meta['tip'] = '''what interactions are available for this 
#atom combination'''

    def __init__(self, atom1, atom2):
        #eventually will find properties from database
        #for now just get them from files in twoAtom directory
        #files=listdir(DANSEINSTALL+sep+'crystal'+sep+'atomHierarchy'+sep+'twoAtomProperties')
        #            atom1+'-'atom2 in files
        Component.__init__(self, 'TwoAtomInteraction', facility=None)
        #self.i=self.inventory
        self.info = {}
        self.atom1 = atom1
        self.atom2 = atom2
        self.potential = None
        self.name = None
        
        self.databaseFile = shareDir + sep + 'interaction'+sep+'interactionDb'+sep+\
        'twoAtom'+sep+atom1+'-'+atom2
        try:
            f=file(self.databaseFile, 'r')
            #get strings of potential choices here
            self.info=eval(f.read().strip())
            self.potentialChoices=self.info.keys()
        except IOError, (errno, strerror):
            print "I/O error(%s): %s" % (errno, strerror)
            print 'error reading atom database for ' +atom1+'-'+atom2
        else:
            f.close()
        # the stuff below could be done if a general type of forcefield were needed where 
        # users can set which atoms they want interactions between and then choose which
        # interactions they'd like to set
#        self.i.availableInteractions=self.potentialChoices[0]
#        self.i.availableInteractions=self.potentialChoices

    def getAvailableInteractions(self):
        #turn the dictionary into a list of pyre components whose parameters 
        #can be set by the user
#        potentialComponents=[]
#        for entry in self.info:
#            #get the local variables in namespace
#            exec(entry)
#            #assign them to a data structure
#            potentialNameAndForm=entry.split('=')
#            potentialName=eval(potentialNameAndForm[0])
#            potentialComponents.append(potentialName)
#        print potentialComponents
        return self.info        

    def printAvailableInteractions(self):
        pp=PrettyPrinter()
        return pp.pprint(self.info)
    
    def addInteraction(self, label, paramsAndValues):
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
    ta=TwoAtomInteraction('Ar','Ar')
    print ta.getAvailableInteractions()
#    ta.assignInteraction('lennardJonesMmtk')
#    print ta.getAssignedInteraction()
#    key='myLJPotential'
#    val={'sigma':3.4, 'epsilon':121, 
#    'cutoff':15.0, 'note':'from Brandon"s head'}
#    ta.addInteraction(key, val)
