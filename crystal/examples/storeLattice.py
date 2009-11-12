from dsaw.db import connect
db = connect(db ='postgres:///test')
db.autocommit(True)

# declare tables

from matter.Lattice import Lattice
db.registerTable(Lattice)
db.createAllTables()

l1 = Lattice(a=3.0,b=3.0)
l1.id = 'l1'
db.insertRow(l1)

#t1.myattribute = 'biggercake'
#db.updateRecord(t1)

db.destroyAllTables()