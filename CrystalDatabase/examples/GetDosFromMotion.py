_id = 0
def guid():
    global _id
    _id += 1
    return str(_id)

#get motion from trajectory
###########################
base = 'graphiteShort'

rawTraject = base+'.his'

ncFile = base+'.nc'

cmd = 'postProcessGulp.py --historyFile='+rawTraject+' --ncFile='+ncFile
#temp sub for job submission
import os
os.system(cmd)

import os
curDir = os.path.abspath('.')
ncFilePath = os.path.join(curDir,ncFile)
from vsat.Motion import Motion
motion = Motion(ncFilePath)

#insert Motion in db
####################
# needs to be a function that takes no argument and returns a unique ID every time called
#guid = 'graphiteShort' 

from dsaw.db import connect
#db = connect(db ='postgres://linjiao:4OdACm#@localhost/vnfa2b')
db = connect(db ='postgres:///test')
db.autocommit(True)
from dsaw.model.visitors.OrmManager import OrmManager
orm = OrmManager(db, guid)
orm.save(motion)

# retrieve the d.o.
###################
motion2 = orm.load(Motion, id=orm(motion).id)
db.destroyAllTables()

# use dos calculator
########################
from vsat.trajectory.MotionDosCalc import MotionDosCalc
c = MotionDosCalc(motion2)
print c.getInputFile()