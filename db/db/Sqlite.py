
from pyre.components.Component import Component
from pysqlite2 import dbapi2 as sqlite

class Sqlite(Component):
    '''gets db info from cod'''
    class Inventory(Component.Inventory):
        import pyre.inventory as pinv  
        dbPath = pinv.str('dbPath', default='$HOME'+sep+'danseLocal.db')
#        sample.meta['tip'] = 'piece of material being measured/simulated'
        
    def __init__(self, name='Sqlite'):
        Component.__init__(self, name, facility=None)
        
    def connect(self):
        con = sqlite.connect(dbPath)
        self.cur = con.cursor()

    def insert(self):
        cur.execute("Create table picture_table(images)")
        
    def SQL(self,statement):
        '''execute a low-level sql statement'''
        cur.execute(statement)
        
        
    
    