import sys
print sys.path

from dsaw.db import connect
db = connect(db ='postgres:///test', echo = True)
db.autocommit(True)

from matter.orm.Atom import Atom
from matter.orm.Lattice import Lattice
from matter.orm.Structure import Structure

from dsaw.model.visitors.OrmManager import OrmManager
orm = OrmManager(db)
at1 = Atom('C', [0.333333333333333, 0.666666666666667, 0])
at1.id = 'at1'
#orm.save(at1)

at2 = Atom('C', [0.666666666666667, 0.333333333333333, 0])
at2.id = 'at2'
#orm.save(at2)

hexag = Lattice(1, 1, 1, 90, 90, 120)
hexag.id = 'hexag'
#orm.save(hexag)

graphite = Structure( [ at1, at2], lattice = hexag)
graphite.id = 'graphite'
orm.save(graphite)

    
#db.destroyAllTables()
    



    


