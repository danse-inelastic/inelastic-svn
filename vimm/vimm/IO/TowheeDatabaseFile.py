# Vimm: Visual Interface to Materials Manipulation
#
# Copyright 2010 Caltech.  Copyright 2005 Sandia Corporation.  Under the terms of Contract
# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government
# retains certain rights in this sofware.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  
# USA


def load_database_file(file, filedir):
    line = file.readline()
    line = file.readline()
    opts['minvectorlength'] = line.strip()

    line = file.readline()
    line = file.readline()
    opts['potentype'] = int(line.strip())

    # mixrule section
    if opts['potentype'] == 0 or opts['potentype'] == 5:
        line = file.readline()
        line = file.readline()
        opts['mixrule'] = int(line.strip())
    elif opts['potentype'] == 6:
        opts['mixrule'] = 4
        line = file.readline()
        line = file.readline()
        opts['interpolatestyle'] = int(line.strip())
    else:
        print "wtf?"

    # rcut section
    if opts['potentype'] == 0 or opts['potentype'] == 6:
        line = file.readline()
        line = file.readline()
        opts['rcut'] = line.strip()

    line = file.readline()
    line = file.readline()
    opts['energystyle'] = line.strip()

    # loptimize section
    if opts['potentype'] == 5 or opts['potentype'] == 6:
        line = file.readline()
        line = file.readline()
        opts['loptimize'] = line.strip()

    # Read in the print logical
    line = file.readline()
    line = file.readline()
    opts['lprint'] = line.strip()

    # Read in the number of forcefields
    line = file.readline()
    line = file.readline()
    opts['ffnumber'] = int(line.strip())

    # Read in the forcefield file names
    line = file.readline()
    opts['ff_filename'] = []
    for i in range(opts['ffnumber']):
        line = file.readline()
        opts['ff_filename'].append(line.strip())

    #
    # The call to rwforcefield happens here
    #

    # Read in the number of data points
    line = file.readline()
    line = file.readline()
    opts['datapoints'] = int(line.strip())

    # Read in the scanstyle
    line = file.readline()
    line = file.readline()
    opts['scanstyle'] = line.strip()

    file.close()

    if scanstyle == "'dakota'":
        dakotainputfilename = filedir + "dakota_input"
        file=open(dakotainputfilename, 'r')
        line = file.readline()
        opts['nvariable'] = int(line.strip())

        if opts['potentype'] == 5:
            opts['dakota_data'] = []
            for i in range(opts['nvariable']):
                line = file.readline()
                opts['dakota_data'].append(tuple(line.split()))
            
        elif opts['potentype'] == 6:
            opts['dakota_data'] = []
            for i in range(opts['nvariable']):
                line = file.readline()
                opts['dakota_data'].append(tuple(line.split()))
        else:
            print "wtf?"

    file.close()
        
    # Open database input
    databseinputfilename = filedir + "database_input"
    file=open(databaseinputfilename, 'r')

    opts['datastyle'] = []
    opts['datastart'] = []
    opts['datasetname'] = []
    opts['notes'] = []
    opts['distance'] = []
    opts['dimension'] = []
    opts['cellvectors'] = []
    opts['dbnatoms'] = []
    opts['eatomize'] = []
    opts['ebinding'] = []
    opts['etotal'] = []

    for i in range(opts['datapoints']):
        line = file.readline()
        opts['datastyle'].append(line.strip())
        if opts['datastyle'] == "@structure":
            iline = 0

            while 1:
                line = file.readline()
                iline+=1
                if iline == 1:
                    if line[0] == "@":
                        iline = 0
                        continue

                    if line[0] == "$":
                        if line.rfind("start") != -1:
                            if line.rfind("structur") != -1:
                                opts['datastart'].append(line.strip())
                                line = file.readline()
                                opts['datasetname'].append(line.strip())
                                continue

                    print "Something bad happened"
                        
                if line[0] == "@":
                    print "Unsupported!"
                elif line[0] == "$":
                    if line.rfind("end") != -1:
                        break
                    elif line.rfind("notes") != -1:
                        stripped_line = line.strip()
                        nnotes = int(stripped_line[-1])
                        temp_notes = []
                        for j in range(nnotes):
                            line = file.readline()
                            temp_notes.append(line.strip())

                        opts['notes'].append(temp_notes)
                    elif line.rfind("distance") != -1:
                        line = file.readline()
                        opts['distance'].append(line.strip())
                    elif line.rfind("dimensio") != -1:
                        line = file.readline()
                        opts['dimension'].append(line.strip())
                    elif line.rfind("cell") != -1:
                        temp_cell_vectors = []
                        for j in range(3):
                            line = file.readline()
                            cv = line.split()
                            temp_cell_vectors.append(tuple(cv))
                        opts['cellvectors'].append(temp_cell_vectors)
                    elif line.rfind("number") != -1:
                        line = file.readline()
                        opts['dbnatoms'].append(int(line.strip()))
                    elif line.rfind("atom type") != -1:
                        temp_atomtypedata = []
                        for j in range(opts['dbnatoms'][i]):
                            line = file.readline()
                            atd = line.split()
                            temp_atomtypedata.append(int(atd[0]))
                            temp_atomtypedata.append(atd[1])
                            temp_atomtypedata.append(tuple(atd[2:]))
                        opts['atomtypedata'].append(temp_atomtypedata)
                    elif line.rfind("Eatomize") != -1:
                        line = file.readline()
                        opts['eatomize'].append(line.strip())
                    elif line.rfind("Ebinding") != -1:
                        line = file.readline()
                        opts['ebinding'].append(line.strip())
                    elif line.rfind("Etotal") != -1:
                        line = file.readline()
                        opts['etotal'].append(line.strip())
    return opts

def save_database_file(file, opts):
    print "Not yet"
    return
