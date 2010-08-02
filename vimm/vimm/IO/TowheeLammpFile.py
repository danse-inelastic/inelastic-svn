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


def load_lammp_file(filedir):
    lammpinputfilename = filedir + "lammps_input"
    file=open(lammpfilename, 'r')
    mixflag = 0
    for line in file:
        if line.rfind("mixing style") != -1:
            mixflag = 1
            if line.rfind("geometric") != -1:
                opts['mixstyle'] = 1
            elif line.rfind("arithmetic") != -1:
                opts['mixstyle'] = 2
            elif line.rfind("sixthpower") != -1:
                opts['mixstyle'] = 3
            else:
                print "wtf?"

        if line.rfind("nonbond style") != -1:
            if line.rfind("class/cutoff") != -1 and mixflag != 1:
                opts['mixstyle'] = 3
            elif line.rfind("lj/charmm") != -1 and mixflag != 1:
                opts['mixstyle'] = 2
            elif mixflag != 1:
                opts['mixstyle'] = 1
            
            nb = line.split()
            opts['nonbondstyle'] = tuple(nb[2:4])                
                     
        if line.rfind("bond style") != -1:
            if line.rfind("harmonic") != -1:
                opts['bondstyle'] = 1
            elif line.rfind("fene/standard") != -1:
                opts['bondstyle'] = 2
            elif line.rfind("fene/shift") != -1:
                opts['bondstyle'] = 3
            elif line.rfind("nonlinear") != -1:
                opts['bondstyle'] = 4
            elif line.rfind("class2") != -1:
                opts['bondstyle'] = 5
            else:
                print "wtf?"

        if line.rfind("angle style") != -1:
            if line.rfind("harmonic") != -1:
                opts['anglestyle'] = 1
            elif line.rfind("class2") != -1:
                opts['angelstyle'] = 2
            elif line.rfind("charmm") != -1:
                opts['anglestyle'] = 3
            else:
                print "wtf?"

        if line.rfind("dihedral style") != -1:
            if line.rfind("multiharmonic") != -1:
                opts['dihedralstyle'] = 3
            elif line.rfind("harmonic") != -1:
                opts['dihedralstyle'] = 1
            elif line.rfind("class2") != -1:
                opts['dihedralstyle'] = 2
            elif line.rfind("charmm") != -1:
                opts['dihedralstyle'] = 4
            else:
                print "wtf?"

        if line.rfind("improper style") != -1:
            if line.rfind("harmonic") != -1:
                opts['improperstyle'] = 1
            elif line.rfind("cvff") != -1:
                opts['improperstyle'] = 2
            elif line.rfind("class2") != -1:
                opts['improperstyle'] = 3
            else:
                print "wtf?"

        if line.rfind("special bonds") != -1:
            if line.rfind("charmm") != -1:
                opts['specialbonds'] = (0.0,0.0,0.0)
            elif line.rfind("amber") != -1:
                opts['specialbonds'] = (0.0,0.0, 1.0/1.2)
            else:
                sb = line.split()
                opts['specialbonds'] = tuple(sb[2:4])

        if line.rfind("temp control") != -1:
            if line.rfind("none") != -1:
                opts['tempcontrol'] = (0.0, 1.0, 0.0)
            elif line.rfind("rescale") != -1:
                b = line.split()
                opts['tempcontrol'] = tuple(b[2:])
            elif line.rfind("replace") != -1:
                b = line.split()
                opts['tempcontrol'] = tuple(b[2:])
            elif line.rfind("langevin") != -1:
                b = line.split()
                opts['tempcontrol'] = tuple(b[2:])
            elif line.rfind("nose/hoover") != -1:
                b = line.split()
                opts['tempcontrol'] = tuple(b[2:])
            else:
                print "wtf?"

     #  if line.rfind("create temp") != -1:
     #  if line.rfind("press control") != -1:
     #  if line.rfind("dielectric") != -1:

    lammpfilename = filedir + "lammps_data"
    file=open(laampfilename, 'r')

    # Read in file header
    line = file.readline()
    line = file.readline()

    # Read in the number of atoms
    line = file.readline()
    natoms,g = line.split()
    opts['natoms'] = int(natoms)

    # Read in the number of bonds
    line = file.readline()
    nbonds,g = line.split()
    opts['nbonds'] = int(nbonds)

    # Read in the number of angles
    line = file.readline()
    nangles,g = line.split()
    opts['nangles'] = int(nangles)

    # Read in the number of dihedrals
    line = file.readline()
    ndihedrals,g = line.split()
    opts['ndihedrals'] = int(ndihedrals)

    # Read in the number of impropers
    line = file.readline()
    nimpropers,g = line.split()
    opts['nimpropers'] = int(nimpropers)

    # Spacer
    line = file.readline()

    # Read in the number of atom types
    line = file.readline()
    natomtypes,g = line.split()
    opts['natomtypes'] = int(natomtypes)

    # Read in the number of bond types
    if opts['nbonds'] > 0:
        line = file.readline()
        nbondtypes,g = line.split()
        opts['nbondtypes'] = int(nbondtypes)

    # Read in the number of angle types
    if opts['nangles'] > 0:
        line = file.readline()
        nangletypes,g = line.split()
        opts['nangletypes'] = int(nangletypes)

    # Read in the number of dihedral types
    if opts['ndihedral'] > 0:
        line = file.readline()
        ndihedraltypes,g = line.split()
        opts['ndihedraltypes'] = int(ndihedraltypes)

    # Read in the number of improper types
    if opts['nimpropers'] > 0:
        line = file.readline()
        nimpropertypes,g = line.split()
        opts['nimpropertypes'] = int(nimpropertypes)

    # Spacer
    line = file.readline()

    # Read in the box dimension
    opts['boxdimension'] = []
    line = file.readline()
    xlo,xhi,g,gg = line.split()
    opts['boxdimension'].append((xlo, xhi))
    line = file.readline()
    ylo,yhi,g,gg = line.split()
    opts['boxdimension'].append((ylo, yhi))
    line = file.readline()
    zlo,zhi,g,gg = line.split()
    opts['boxdimension'].append((zlo, zhi))

    eof = false
    while eof == false:
        # Read identifier string
        line = file.readline()
        id = file.readline()
        line = file.readline()

        if len(line) == 0:
            eof = true
            continue

        if id.strip() == "Masses":
            opts['masses'] = []
            for i in range(opts['natomtypes']):
                line = file.readline()
                num,mass = line.split()
                opts['masses'].append((int(num), masses))

        elif id.strip() == "Atoms":
            opts['atoms'] = []
            for i in range(opts['natoms']):
                line = file.readline()
                atominfo = line.split()
                opts['atoms'].append(tuple(atominfo))
                
        elif id.strip() == "Velocities":
            # Apparently Velocities are not need, so this skips by them
            for i in range(opts['natoms']):
                line = file.readline()
                
        elif id.strip() == "Bonds":
            opts['bonds'] = []
            for i in range(opts['nbonds']):
                line = file.readline()
                bondinfo = int(line.split())
                opts['bonds'].append(tuple(bondinfo))
                
        elif id.strip() == "Angles":
            opts['angles'] = []
            for i in range(opts['nangles']):
                line = file.readline()
                angleinfo = int(line.split())
                opts['bonds'].append(tuple(angleinfo))

        elif id.strip() == "Dihedrals":
            opts['dihedrals'] = []
            for i in range(opts['ndihedrals']):
                line = file.readline()
                dihedralinfo = int(line.split())
                opts['dihedrals'].append(tuple(dihedralinfo))

        elif id.strip() == "Impropers":
            opts['impropers'] = []
            for i in range(opts['nimpropers']):
                line = file.readline()
                improperinfo = int(line.split())
                opts['impropers'].append(tuple(improperinfo))
            
        elif id.strip() == "Nonbond Coeffs":
            opts['nonbondcoeffs'] = []
            for i in range(opts['natomtypes']):
                line = file.readline()
                index,a1,a2 = line.split()
                opts['nonbondcoeffs'].append((int(index), a1, a2))

        elif id.strip() == "Bond Coeffs":
            opts['bondcoeffs'] = []
            for i in range(opts['nbondtypes']):
                line = file.readline()
                bc = line.split()
                opts['bondcoeffs'].append(tuple(bc))

        elif id.strip() == "Angle Coeffs":
            opts['anglecoeffs'] = []
            for i in range(opts['angletypes']):
                line = file.readline()
                ac = line.split()
                opts['anglecoeffs'].append(tuple(ac))

        elif id.strip() == "Dihedral Coeffs":
            opts['dihedralcoeffs'] = []
            for i in range(opts['ndihedraltypes']):
                line = file.readline()
                dc = line.split()
                opts['dihedralcoeffs'].append(tuple(dc))

        elif id.strip() == "Improper Coeffs":
            opts['impropercoeffs'] = []
            for i in range(opts['nimpropertypes']):
                line = file.readline()
                ic = line.split()
                opts['impropercoeffs'].append(tuple(ic))

        elif id.strip() == "BondBond Coeffs":
            opts['bondbondcoeffs'] = []
            for i in range(opts['nangletypes']):
                line = file.readline()
                bbc = line.split()
                opts['bondbondcoeffs'].append(tuple(bbc))

        elif id.strip() == "BondAngle Coeffs":
            opts['bondanglecoeffs'] = []
            for i in range(opts['nangletypes']):
                line = file.readline()
                bac = line.split()
                opts['bondanglecoeffs'].append(tuple(bbc))

        elif id.strip() == "MiddleBondTorsion Coeffs":
            opts['middlebondtorsioncoeffs'] = []
            for i in range(opts['ndihedraltypes']):
                line = file.readline()
                dc = line.split()
                opts['middlebondtorsioncoeffs'].append(tuple(int(dc)))

        elif id.strip() == "EndBondTorsion Coeffs":
            opts['endbondtorsioncoeffs'] = []
            for i in range(opts['ndihedraltypes']):
                line = file.readline()
                dc = line.split()
                opts['endbondtorsioncoeffs'].append(tuple(int(dc)))

        elif id.strip() == "AngleTorsion Coeffs":
            opts['angletorsioncoeffs'] = []
            for i in range(opts['ndihedraltypes']):
                line = file.readline()
                dc = line.split()
                opts['angletorsioncoeffs'].append(tuple(int(dc)))

        elif id.strip() == "AngleAngleTorsion Coeffs":
            opts['angleangletorsioncoeffs'] = []
            for i in range(opts['ndihedraltypes']):
                line = file.readline()
                dc = line.split()
                opts['angleangletorsioncoeffs'].append(tuple(int(dc)))

        elif id.strip() == "BondBond13 Coeffs":
            opts['bondbond13coeffs'] = []
            for i in range(opts['ndihedraltypes']):
                line = file.readline()
                dc = line.split()
                opts['bondbond13coeffs'].append(tuple(int(dc)))

        elif id.strip() == "AngleAngle Coeffs":
            opts['angleanglecoeffs'] = []
            for i in range(opts['nimpropertypes']):
                line = file.readline()
                dc = line.split()
                opts['angleanglecoeffs'].append(tuple(int(dc)))
        else:
            print "wtf?"
    # End of while eof == false:
    return opts

def save_lammp_file(file, opts):
    print "Not yet"
    return
