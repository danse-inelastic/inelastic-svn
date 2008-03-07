#!/usr/bin/env python

# user-settable items-----------------------------------

# In species set the name, the number, the atoms involved, and any constraints.  
# If no constraints, put [].


#-------------------------------------------------------

# Conversion of a DLPOLY trajectory to MMTK's trajectory format.
#
# Usage: dlpoly_to_nc dlpoly_directory nc_file
#

from MMTK import *
from MMTK.Trajectory import Trajectory, SnapshotGenerator, TrajectoryOutput
from Scientific.IO.FortranFormat import FortranLine, FortranFormat
import Numeric, getopt, os, string, sys



_elements2 = ['cl', 'as', 'in', 'tb', 'tl', 'he', 'ar', 'se', 'sn',
'dy', 'pb', 'li', 'br', 'sb', 'ho', 'bi', 'be', 'ca', 'kr', 'te',
'er', 'po', 'sc', 'rb', 'tm', 'at', 'ti', 'sr', 'xe', 'yb', 'rn',
'cs', 'lu', 'fr', 'cr', 'zr', 'ba', 'hf', 'ra', 'mn', 'nb', 'la',
'ta', 'ac', 'ne', 'fe', 'mo', 'ce', 'th', 'na', 'co', 'tc', 'pr',
're', 'pa', 'mg', 'ni', 'ru', 'nd', 'os', 'al', 'cu', 'rh', 'pm',
'ir', 'np', 'si', 'zn', 'pd', 'sm', 'pt', 'pu', 'ga', 'ag', 'eu',
'au', 'am', 'ge', 'cd', 'gd', 'hg', 'cm', 'cf']

field_atom_line = FortranFormat('A8,2F12,3I5')
history_timestep_line = FortranFormat('A8,4I10,F12.6')
history_pbc_line = FortranFormat('3G12.4')

class DLPOLYData:

    def __init__(self,species,historyFile):
        #self.directory = directory
        self.history = open(historyFile)
        self.title = string.strip(self.history.readline())
        info = FortranLine(self.history.readline(), '2I10')
        if info[1] > 3:
            raise ValueError, "box shape not implemented"
        nvectors = info[0]+1
        self.makeUniverse(info[1], species)
        if nvectors > 1:
            self.universe.initializeVelocitiesToTemperature(0.)

    def checkDirective(self, line, directive):
        return string.upper(line[:len(directive)]) == directive

    def makeUniverse(self, pbc, molecules):
        if pbc == 0:
            self.universe = InfiniteUniverse()
        else:
            self.universe = OrthorhombicPeriodicUniverse((0., 0., 0.))
        number = 0
        for mol_name, mol_count, atoms, constraints in molecules:
            for i in range(mol_count):
                atom_objects = []
                for element, name in atoms:
                    a = Atom(element, name = name)
                    a.number = number
                    number = number + 1
                    atom_objects.append(a)
                if len(atom_objects) == 1:
                    self.universe.addObject(atom_objects[0])
                else:
                    ac = AtomCluster(atom_objects, name = mol_name)
                    for i1, i2, d in constraints:
                        ac.addDistanceConstraint(atom_objects[i1],
                                                 atom_objects[i2],
                                                 d)
                    self.universe.addObject(ac)
        self.universe.configuration()

    def writeTrajectory(self, trajectory_name, block_size=1):
        trajectory = Trajectory(self.universe, trajectory_name, 'w',
                                self.title, block_size=block_size)
        actions = [TrajectoryOutput(trajectory, ["all"], 0, None, 1)]
        snapshot = SnapshotGenerator(self.universe, actions=actions)
        conf = self.universe.configuration()
        vel = self.universe.velocities()
        grad = ParticleVector(self.universe)
        try:
            while 1:
                line = self.history.readline()
                if not line:
                    break
                data = FortranLine(line, history_timestep_line)
                step = data[1]
                natoms = data[2]
                nvectors = data[3]+1
                pbc = data[4]
                dt = data[5]
                step_data = {'time': step*dt}
                if nvectors > 2:
                    step_data['gradients'] = grad
                if pbc:
                    data = FortranLine(self.history.readline(), history_pbc_line)
                    box_x = data[0]*Units.Ang
                    #if data[1] != 0. or data[2] != 0.:
                    #    raise ValueError, "box shape not supported"
                    data = FortranLine(self.history.readline(), history_pbc_line)
                    box_y = data[1]*Units.Ang
                    #if data[0] != 0. or data[2] != 0.:
                    #    raise ValueError, "box shape not supported"
                    data = FortranLine(self.history.readline(), history_pbc_line)
                    box_z = data[2]*Units.Ang
                    #if data[0] != 0. or data[1] != 0.:
                    #    raise ValueError, "box shape not supported"
                    self.universe.setSize((box_x, box_y, box_z))
                for i in range(natoms):
                    self.history.readline()
                    conf.array[i] = map(float,
                                        string.split(self.history.readline()))
                    if nvectors > 1:
                        vel.array[i] = map(float,
                                           string.split(self.history.readline()))
                        if nvectors > 2:
                            grad.array[i] = map(float,
                                             string.split(self.history.readline()))
                Numeric.multiply(conf.array, Units.Ang, conf.array)
                if nvectors > 1:
                    Numeric.multiply(vel.array, Units.Ang/Units.ps, vel.array)
                if nvectors > 2:
                    Numeric.multiply(grad.array, -Units.amu*Units.Ang/Units.ps**2,
                                     grad.array)

                snapshot(data=step_data)
        finally:
            trajectory.close()






def hisToNc(speciesNumbers,historyFile,blockSize=1):
    '''convert a .his file in dlpoly history format to netcdf format
    
speciesNumbers--give a list of species tuples--the species itself and its 
total number (i.e. speciesNumbers=[('C',6),('H',6)] for benzene)
historyFile--name of .his file
blockSize--the block structure of the netCDF trajectory. The
         default value of 1 optimizes the trajectory for step-by-step access
         to conformations. Larger values favour atom-by-atom access to
         one-particle trajectories for all times, which is required for the
         calculation of dynamic quantities. The highest sensible value is
         the number of steps in the trajectory.
    
'''
    

    #convert species to internal format.  This is still experimental.  Examples follow
    #species = [['Al',864,[('al','Al')],[]]]
    #species = [['topGraphiteLayer',504,[('c','C')],[]],['bottomGraphiteLayer',504,[('c','C')],[]],['potassiums',36,[('k','K')],[]],['hydrogens',72,[('h','H')],[]]]
    #species = [['Nickel',256,['Ni'],[]]]
    species=[]
    for specAndNum in speciesNumbers:
        label=specAndNum[0]
        num=specAndNum[1]
        species.append([label,num,[(label.lower(),label)],[]])
        
    nc_file = os.path.splitext(historyFile)[0] + '.nc'

#    try:
#        options, file_args = getopt.getopt(sys.argv[1:], '', ['block-size='])
#    except getopt.GetoptError:
#        sys.stderr.write(usage)
#        raise SystemExit
    
    block_size = blockSize
        
    #if len(file_args) != 2:
    #    sys.stderr.write(usage)
    #    raise SystemExit
    #directory = file_args[0]
    #nc_file = file_args[1]
    
    #if not os.path.exists(os.path.join(directory, 'FIELD')):
    #    sys.stderr.write("No FIELD file in " + directory + ".\n")
    #    raise SystemExit
    #if not os.path.exists(os.path.join(directory, 'HISTORY')):
    #    sys.stderr.write("No HISTORY file in " + directory + ".\n")
    #    raise SystemExit
    
    
    #if os.path.exists(nc_file):
    #    sys.stderr.write('File %s already exists. ' % nc_file)
    #    while 1:
    #        answer = raw_input('Overwrite? [y/n] ')
    #        if answer == 'n':
    #            raise SystemExit
    #        if answer == 'y':
    #            break
    
    data = DLPOLYData(species,historyFile)
    data.writeTrajectory(nc_file, block_size)
    
if __name__=='__main__':
    speciesNumbers=[('K',36),('H',72),('C',1008)]
    historyFile='../useCases/kc24HisToNc/kc24-70K.his'
    hisToNc(speciesNumbers,historyFile)
