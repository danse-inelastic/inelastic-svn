import sys
print sys.path

from dsaw.db import connect
db = connect(db ='postgres:///test')
db.autocommit(True)

# we have to create system tables because we're using a reference
db.createSystemTables()

#create Lattice
from matter.Lattice import Lattice
db.createTable(Lattice)
l1 = Lattice()
l1.id = 'l1'
db.insertRow(l1)

# create Atom that weakly references it
from matter.Atom import Atom
#db.registerTable(Lattice)
#db.createAllTables()
db.createTable(Atom)
a1 = Atom()
a1.id = 'a1'
a1.lattice = l1
try:
    db.insertRow(a1)
    
#    db.dropTable(Atom)
#    db.dropTable(Lattice)
#    db.destroyAllTables()
finally:
    db.dropTable(Atom)
    db.dropTable(Lattice)
    db.destroySystemTables()
    


