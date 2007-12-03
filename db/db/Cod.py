
from pyre.components.Component import Component
import MySQLdb
import math

class Cod(Component):
    '''gets db info from cod'''
    class Inventory(Component.Inventory):
        import pyre.inventory as pinv  
#        dbPath = pinv.str('dbPath', default='$HOME'+sep+'danseLocal.db')
#        sample.meta['tip'] = 'piece of material being measured/simulated'
        
    def __init__(self, species=None, symmetry=None, text=None):
        Component.__init__(self, 'Cod', facility='Cod')
        self.atoms=None
        self.species=species
        self.cell=None
        self.spaceGroup=symmetry
        self.text=text
        self.vol=None
        self.numSpecies=0
        self.availableEntries=None
        self.connect()
        
    def volume(self,uc):
        """gives the unit cell volume"""
        conv=math.pi/180.
        (a,b,c,al,be,ga)=uc
        V = a*b*c*(1 - math.cos(conv*al)**2. - math.cos(conv*be)**2. - math.cos(conv*ga)**2. + 2.*math.cos(conv*al)*math.cos(conv*be)*math.cos(conv*ga))**(1/2.)
        return V
        
    def connect(self):
        self.db=MySQLdb.connect(host="fireball.phys.wvu.edu",db='cod')

    def getAvailableEntries(self):
        '''find the available data'''
        if self.availableEntries==None:
            c=self.db.cursor()
            query=self.queryString()
            c.execute(query)
            self.availableEntries=c.fetchall()
        return self.availableEntries
        
    def queryString(self):
        '''get a specific query'''
        query = "SELECT * FROM data WHERE"
        # do this if user entres 
        if self.text!=None:
            words = self.text.split()
            for word in words:
                query += " AND (text LIKE '%" + word + "%')"
        if self.species!=None:
            species = self.species.split()
            self.numSpecies=len(species)
            for specie in species:
                query += " AND (formula LIKE '%"+' '+specie+' '+"%')"
#        if self.species!=None:
#            species = self.species.split()
#            for specie in species:
#                query += " AND (formula NOT LIKE '%" + specie + "%')"      
#        if (!txtVolumeMin.getText().equals("") && !txtVolumeMax.getText().equals("")) {
#            query += " AND (vol BETWEEN " + txtVolumeMin.getText() + " AND " + txtVolumeMax.getText() + ")";
#        }
        if self.numSpecies!=0:
            query += " AND (nel = " + str(self.numSpecies) + ")"
#        if (!txtaMin.getText().equals("") && !txtaMax.getText().equals("")) {
#            query += " AND (a BETWEEN " + txtaMin.getText() + " AND " + txtaMax.getText() + ")";
#        }
#        if (!txtbMin.getText().equals("") && !txtbMax.getText().equals("")) {
#            query += " AND (b BETWEEN " + txtbMin.getText() + " AND " + txtbMax.getText() + ")";
#        }
#        if (!txtcMin.getText().equals("") && !txtcMax.getText().equals("")) {
#            query += " AND (c BETWEEN " + txtcMin.getText() + " AND " + txtcMax.getText() + ")";
#        }
#        if (!txtalphaMin.getText().equals("") && !txtalphaMax.getText().equals("")) {
#            query += " AND (alpha BETWEEN " + txtalphaMin.getText() + " AND " + txtalphaMax.getText() + ")";
#        }
#        if (!txtbetaMin.getText().equals("") && !txtbetaMax.getText().equals("")) {
#            query += " AND (beta BETWEEN " + txtbetaMin.getText() + " AND " + txtbetaMax.getText() + ")";
#        }
#        if (!txtgammaMin.getText().equals("") && !txtgammaMax.getText().equals("")) {
#            query += " AND (gamma BETWEEN " + txtgammaMin.getText() + " AND " + txtgammaMax.getText() + ")";
#        }
        query = query.replace("WHERE AND", "WHERE");
        if query[-6:]==" WHERE":
            query = "SELECT * FROM data";
        query += " ORDER BY entry LIMIT 1000"
        return query