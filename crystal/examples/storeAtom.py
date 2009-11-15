import sys
print sys.path

from dsaw.db import connect
db = connect(db ='postgres:///test')
db.autocommit(True)

# declare tables

from matter.Atom import Atom
#db.registerTable(Lattice)
#db.createAllTables()

db.createTable(Atom)

a1 = Atom()
a1.id = 'a1'
db.insertRow(a1)

#t1.myattribute = 'biggercake'
#db.updateRecord(t1)

#db.destroyAllTables()
