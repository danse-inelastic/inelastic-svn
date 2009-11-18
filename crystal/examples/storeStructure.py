import sys
print sys.path

from dsaw.db import connect
db = connect(db ='postgres:///test', echo = True)
db.autocommit(True)

from matter.Atom import Atom
from matter.Lattice import Lattice
from matter.Structure import Structure
#db.registerTable(Lattice)
#db.createAllTables()
db.createTable(Atom)
db.createTable(Lattice)
db.createTable(Structure)


at1 = Atom('C', [0.333333333333333, 0.666666666666667, 0])
at1.id = 'at1'
db.insertRow(at1)
at2 = Atom('C', [0.666666666666667, 0.333333333333333, 0])
at2.id = 'at2'
db.insertRow(at2)
hexag = Lattice(1, 1, 1, 90, 90, 120)
hexag.id = 'hexag'
db.insertRow(hexag)
graphite = Structure( [ at1, at2], lattice = hexag)
graphite.id = 'graphite'
db.insertRow(graphite)
    
db.dropTable(Structure)
db.dropTable(Lattice)
db.dropTable(Atom)



    


