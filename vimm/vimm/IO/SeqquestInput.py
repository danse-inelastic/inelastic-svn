# vimm: Visual Interface for Materials Manipulation
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



from vimm.Material import Material
from vimm.Atom import Atom
from vimm.Cell import Cell
from vimm.Utilities import path_split,cleansym
from vimm.Element import sym2no
from vimm.NumWrap import array
from vimm.Constants import bohr2ang

from math import sqrt

extensions = ["tape5","in"]
filetype = "Seqquest Input"

def load(fullfilename):
    filedir, fileprefix, fileext = path_split(fullfilename)
    file=open(fullfilename, 'r')
    
    # Initialize atom data
    material = Material(fileprefix)
    opts = {}
    material.seqquest_options = opts

    line = file.readline() # start reading

    # Read in the run options
    while 1:
        if line[:8] == 'output l':
            line = file.readline()
            opts['lvlout'] = int(line.strip())
            line = file.readline()
        elif line[:8] == 'do setup':
            opts['dosetup'] = True
            line = file.readline()
        elif line[:8] == 'no setup':
            opts['dosetup'] = False
            line = file.readline()
        elif line[:8] == 'do iters':
            opts['doiters'] = True
            line = file.readline()
        elif line[:8] == 'no iters':
            opts['doiters'] = False
            line = file.readline()
        elif line[:8] == 'do force':
            opts['doforce'] = True
            line = file.readline()
        elif line[:8] == 'no force':
            opts['doforce'] = False
            line = file.readline()
        elif line[:8] == 'do relax':
            opts['dorelax'] = True
            line = file.readline()
        elif line[:8] == 'no relax':
            opts['dorelax'] = False
            line = file.readline()
        elif line[:7] == 'do cell':
            opts['docell'] = True
            line = file.readline()
        elif line[:7] == 'no cell':
            opts['docell'] = False
            line = file.readline()
        elif line[:6] == 'do neb':
            opts['doneb'] = True
            line = file.readline()
        elif line[:6] == 'no neb':
            opts['doneb'] = False
            line = file.readline()
        elif line[:5] == 'do md':
            opts['domd'] = True
            line = file.readline()
        elif line[:5] == 'no md':
            opts['domd'] = False
            line = file.readline()
        elif line[:7] == 'do post':
            opts['dopost'] = True
            line = file.readline()
        elif line[:7] == 'no post':
            opts['dopost'] = False
            line = file.readline()

        elif line[:7] == 'do blas':
            opts['doblas3'] = True
            line = file.readline()
        elif line[:7] == 'no blas':
            opts['doblas3'] = False
            line = file.readline()
        else:
            # Comment this out when debugged:
            print "Unknown line from command section"
            print line,
            print "Assuming end of Input Options Section"
            break
    # end of run options

    # Beginning of setup info
    if line[:6] == 'input ':
        line = file.readline() # skip line
    # Title
    if line[:5] == 'title':
        opts['title'] = []
        try:
            ntitl = int(line[5])
        except:
            ntitl = 1
        for i in range(ntitl):
            line = file.readline()
            opts['title'].append(line.strip())
        line = file.readline()

    if line[:5] == 'scale':
        line = file.readline()
        opts['scalep'] = float(line.strip())
        line = file.readline()

    # DFT fcnal
    if line[:6] == 'functi':
        line = file.readline()
        opts['dft_func'] = line.strip()
        line = file.readline()

    # Spin polarization
    if line[:6] == 'spin p':
        line = file.readline()
        opts['spinpol'] = int(line.strip())
    #should put an error condition here if dft requires
    # spin and no spinpol input
        line = file.readline()

    # External electric field
    if line[:6] == 'efield':
        line = file.readline()
        ex,ey,ez = map(float,line.split())
        opts['efield'] = (ex,ey,ez) # in Ry/au
        line = file.readline()

    # External dielectric constant
    if line[:6] == 'dielec':
        line = file.readline()
        opts['dielec'] = float(line.split())
        line = file.readline()

    # Problem dimension
    if line[:6] == 'dimens' or line[:6] == 'lattic':
        line = file.readline()
        opts['ndim'] = int(line.strip())
        line = file.readline()
    else:
        print line
        raise "Dimension must be specified in Quest input"

    # Coordinates (lattice or cartesian)
    if line[:6] == 'coordi':
        line = file.readline()
        opts['coordi'] = line.strip()
        line = file.readline()

    # Problem scaling
    # RPM: Need to do a better job of this:
    #if line[:6] == 'scalep' or (line[:5] == 'scale' and len(line) == 5):
    if line[:6] == 'scalep' or line[:6] == 'scale\n':
        line = file.readline()
        opts['scalep'] = float(line.strip())
        line = file.readline()

    if line[:6] == 'scaleu':
        line = file.readline()
        opts['scaleu'] = float(line.strip())
        line = file.readline()

    if line[:6] == 'scalex':
        line = file.readline()
        opts['scalex'] = float(line.strip())
        line = file.readline()

    if line[:6] == 'scaley':
        line = file.readline()
        opts['scaley'] = float(line.strip())
        line = file.readline()

    if line[:6] == 'scalez':
        line = file.readline()
        opts['scalez'] = float(line.strip())
        line = file.readline()

    # Strain
    if line[:6] == 'strain':
        line = file.readline()
        xx,xy,xz = map(float,line.split())
        line = file.readline()
        yx,yy,yz = map(float,line.split())
        line = file.readline()
        zx,zy,zz = map(float,line.split())
        opts['strain'] = (xx,xy,xz,yx,yy,yz,zx,zy,zz)
        line = file.readline()
    if line[:6] == 'strfac':
        line = file.readline()
        opts['strfac'] = float(line.strip())
        line = file.readline()

    # Lattice vectors:
    if line[:6] == 'primit':
        line = file.readline()
        ax,ay,az = map(float,line.split())
        axyz = ax*bohr2ang,ay*bohr2ang,az*bohr2ang
        line = file.readline()
        bx,by,bz = map(float,line.split())
        bxyz = bx*bohr2ang,by*bohr2ang,bz*bohr2ang
        line = file.readline()
        cx,cy,cz = map(float,line.split())
        cxyz = cx*bohr2ang,cy*bohr2ang,cz*bohr2ang
        cell = Cell(axyz,bxyz,cxyz)
        line = file.readline()

    # grid dimensions
    if line[:6] == 'grid d' or line[:6] == 'points':
        line = file.readline()
        opts['griddim'] = map(int,line.split())
        line = file.readline()

    # nearby function
    if line[:6] == 'nearby':
        line = file.readline()
        opts['nearby'] = int(line.strip())
        line = file.readline()

    # number of atom types
    if line[:6] == 'atom t':
        line = file.readline()
        opts['ntyp'] = int(line.strip())
        opts['types'] = []
        line = file.readline()
    else:
        print line,len(line)
        raise "Number of atom types must be specified"
    
    # atom types:
    for i in range(opts['ntyp']):
        if line[:6] == 'atom f':
            line = file.readline()
            opts['types'].append(line.strip())
            line = file.readline()
        else:
            raise "Error: expecting another atom file"


    # number of atoms
    if line[:6] == 'number':
        line = file.readline()
        opts['nat'] = int(line.strip())
        line = file.readline()

    if line[:6] == 'atom, ':
        for i in range(opts['nat']):
            line = file.readline()
            words = line.split()
            inum = int(words[0])
            ityp = int(words[1])
            x,y,z = map(float,words[2:5])
            xyz = x*bohr2ang,y*bohr2ang,z*bohr2ang
            xyz = array(xyz)
            sym = cleansym(opts['types'][ityp-1])
            atno = sym2no[sym]
            material.add_atom(Atom(atno,xyz))
        line = file.readline()
        material.set_cell(cell)
        material.bonds_from_distance()
    else:
        raise "Error: expected atom listing here"

    # to lattice/to cartesian
    if line[:6] == 'to_lat': 
        opts['to_lat'] = True
        line = file.readline()
    elif line[:6] == 'to_car':
        opts['to_car'] = True
        line = file.readline()

    # origin offset
    if line[:6] == 'origin':
        line = file.readline()
        opts['dorig'] = map(float,line.split())
        line = file.readline()

    # wigner-seitz origin
    if line[:6] == 'wigner':
        line = file.readline()
        opts['rchrg'] = map(float,line.split())
        line = file.readline()

    # center of symmetry
    if line[:6] == 'symmet':
        line = file.readline()
        opts['rsym'] = map(float,line.split())
        line = file.readline()

    # bloch info
    if line[:5] == 'kgrid':
        line = file.readline()
        opts['kgrid'] = map(int,line.split())
        line = file.readline()
    elif line[:4] == 'khex':
        line = file.readline()
        opts['khex'] = map(int,line.split())
        line = file.readline()

    # skipping more detailed bloch info for now
    if line[:6] == 'n bloc':
        line = file.readline()
        opts['nk'] = int(line.strip())
        line = file.readline()

    if line[:6] == 'scalin':
        line = file.readline()
        opts['scalin'] = map(float,line.split())
        line = file.readline()

    if line[:6] == 'lattic':
        line = file.readline()
        opts['bloch_lattic'] = map(float,line.split())
        line = file.readline()
    elif line[:6] == 'cartes':
        line = file.readline()
        opts['bloch_cartes'] = map(float,line.split())
        line = file.readline()

    if line[:6] == 'bloch ':
        opts['bloch_vecs'] = []
        for i in range(opts['nk']):
            line = file.readline()
            opts['bloch_vecs'].append(map(float,line.split()))
        line = file.readline()

    # symmetry info
    if line[:6] == 'symops':
        line = file.readline()
        opts['nsymi'] = int(line.strip())
        line = file.readline()

    if line[:6] == 'defini':
        opts['symvecs'] = []
        for i in range(opts['nsymi']):
            line = file.readline()
            words = line.split()
            type = int(words[0])
            s1,s2,s3,s4,s5,s6 = map(float,words[1:])
            opts['symvecs'].append((type,s1,s2,s3,s4,s5,s6))
        line = file.readline()

    if line[:6] == 'end se':
        line = file.readline()
    else:
        raise "Expected end setup phase tag"
    # End of setup info

    # Beginning of Run Data
    if line[:6] == 'run ph':
        while 1:
            line = file.readline()
            if not line: break
            if line[:6] == 'end ru' or line[:6] == 'end of':
                break
            elif line[:6] == 'do fla':
                opts['doflag'] = True
            elif line[:6] == 'no fla':
                opts['doflag'] = False
            elif line[:6] == 'first ':
                line = file.readline()
                opts['itstart'] = int(line.strip())
            elif line[:6] == 'last i':
                line = file.readline()
                opts['itstop'] = int(line.strip())
            elif line[:6] == 'histor':
                line = file.readline()
                opts['nhiste'] = int(line.strip())
            elif line[:6] == 'restar':
                line = file.readline()
                opts['itrst'] = int(line.strip())
            elif line[:6] == 'states':
                line = file.readline()
                opts['nstate'] = int(line.strip())
            elif line[:6] == 'temper':
                line = file.readline()
                opts['etemp'] = float(line.strip())
            elif line[:6] == 'blend ' or line[:6] == 'percen':
                line = file.readline()
                opts['scfblnd'] = float(line.strip())
            elif line[:6] == 'scfbl2':
                line = file.readline()
                opts['scfbl2'] = float(line.strip())
            elif line[:6] == 'conver':
                line = file.readline()
                opts['scfconv'] = float(line.strip())
            elif line[:6] == 'alfast':
                line = file.readline()
                opts['alfast'] = float(line.strip())
            elif line[:6] == 'cutii ':
                line = file.readline()
                opts['convii'] = float(line.strip())
            elif line[:6] == 'cutslo':
                line = file.readline()
                opts['convsl'] = float(line.strip())
            elif line[:6] == 'cut2s ':
                line = file.readline()
                opts['conv2s'] = float(line.strip())
            elif line[:6] == 'cutset':
                line = file.readline()
                opts['cutset'] = float(line.strip())
            elif line[:6] == 'cutfrc':
                line = file.readline()
                opts['cutfrc'] = float(line.strip())
            elif line[:6] == 'cutgrd':
                line = file.readline()
                opts['convgr'] = float(line.strip())
            elif line[:6] == 'cut1c ':
                line = file.readline()
                opts['conv1c'] = float(line.strip())
            elif line[:6] == 'geomet':
                # Jump into Geometry Data
                opts['write_geo_sect'] = True
                while 1:
                    line = file.readline()
                    if line[:4] == 'stop' or line[:3] == 'end':
                        break
                    elif line[:6] == 'relax ':
                        opts['dorelax'] = True
                        opts['geo_dorelax'] = True
                    elif line[:6] == 'grelax':
                        line = file.readline()
                        opts['relax_range'] = map(int,line.split())
                    elif line[:6] == 'gfixed':
                        line = file.readline()
                        opts['fixed_range'] = map(int,line.split())
                    elif line[:6] == 'only r':
                        line = file.readline()
                        opts['only_relax']= int(line.strip())
                    elif line[:6] == 'frame ':
                        line = file.readline()
                        opts['relax_frame'] = map(int,line.split())
                    elif line[:6] == 'defect':
                        line = file.readline()
                        opts['defect'] = int(line.strip())
                    elif line[:6] == 'gblend':
                        line = file.readline()
                        opts['gblend'] = float(line.strip())
                    elif line[:5] == 'gconv':
                        line = file.readline()
                        opts['gconv'] = float(line.strip())
                    elif line[:6] == 'gstart':
                        line = file.readline()
                        opts['gstart'] = int(line.strip())
                    elif line[:6] == 'gsteps':
                        line = file.readline()
                        opts['gsteps'] = int(line.strip())
                    elif line[:6] == 'ghisto':
                        line = file.readline()
                        opts['nhistg'] = int(line.strip())
                    elif line[:6] == 'no ges':
                        opts['igges'] = 0
                    elif line[:6] == 'guess ':
                        line = file.readline()
                        opts['igges'] = int(line.strip())
                    elif line[:6] == 'gmetho':
                        line = file.readline()
                        opts['gmethod'] = line.strip()
                    elif line[:6] == 'timest':
                        line = file.readline()
                        opts['gtstep'] = float(line.strip())
                    else:
                        print "Unknown geomdata line:"
                        print line
                # End of Geometry Data
            elif line[:5] == 'cell ':
                # Jump into Cell Data
                opts['write_cell_sect'] = True
                while 1:
                    line = file.readline()
                    if line[:6] == 'end ce':
                        break
                    elif line[:6] == 'ucstep':
                        line = file.readline()
                        opts['maxucsteps'] = int(line.strip())
                    elif line[:6] == 'ucconv':
                        line = file.readline()
                        opts['ucconv'] = float(line.strip())
                    elif line[:6] == 'pressu':
                        line = file.readline()
                        opts['pressure'] = float(line.strip())
                    elif line[:6] == 'uniaxi':
                        line = file.readline()
                        opts['uniaxial'] = map(float,line.split())
                    elif line[:6] == 'stress':
                        opts['stress'] = []
                        for i in range(opts['ndim']):
                            line = file.readline()
                            opts['stress'].append(map(float,line.split()))
                    elif line[:6] == 'uchist':
                        line = file.readline()
                        opts['nhistuc'] = int(line.strip())
                    elif line[:6] == 'ucmeth':
                        line = file.readline()
                        opts['ucmeth'] = line.strip()
                    elif line[:6] == 'str_br':
                        line = file.readline()
                        opts['strsbroy'] = float(line.strip())
                    elif line[:6] == 'max_st':
                        line = file.readline()
                        opts['strnmax'] = float(line.strip())
                    elif line[:6] == 'cell_f':
                        line = file.readline()
                        opts['cell_f'] = float(line.strip())
                    elif line[:6] == 'bulk_m':
                        line = file.readline()
                        opts['bmod'] = float(line.strip())
                    elif line[:6] == 'uc_ble':
                        line = file.readline()
                        opts['ucblend'] = float(line.strip())
                    else:
                        print "Unknown celldata line:"
                        print line
                # End of Cell Data
            else:
                print "Unknown rundata line:"
                print line
    # End of Run Data

    # Start of MD Data
    line = file.readline()
    if line[:6] == 'md dat':
        while 1:
            line = file.readline()
            if line[:3] == 'end':
                break
            elif line[:6] == 'temper':
                line = file.readline()
                opts['mdtemp'] = float(line.strip())
            elif line[:6] == 'time s':
                line = file.readline()
                opts['ntstep'] = int(line.strip())
            elif line[:6] == 'equil ':
                line = file.readline()
                opts['neqsteps'] = int(line.strip())
            elif line[:6] == 'step s':
                line = file.readline()
                opts['md_dt'] = float(line.strip())
            elif line[:6] == 'md typ':
                line = file.readline()
                opts['mdtype'] = line.strip()
            else:
                print "Unknown md flag"
                print line
    return material

def save(fullfilename,material):
    filedir, fileprefix, fileext = path_split(fullfilename)
    file=open(fullfilename, 'w')
    
    opts = getattr(material,'seqquest_options',{})
    cell = material.get_cell()

    if opts.has_key('lvlout'):
        file.write('output level\n%d\n' % opts['lvlout'])

    if opts.has_key('dosetup'):
        if not opts['dosetup']: file.write('no setup\n')
    else: file.write('do setup\n')

    if opts.has_key('doiters'):
        if not opts['doiters']: file.write('no iters\n')
    else: file.write('do iters\n')

    if opts.has_key('doforce'):
        if opts['doforce']: file.write('do force\n')
    else: file.write('no force\n')

    if opts.has_key('dorelax'):
        if opts['dorelax']: file.write('do relax\n')
    else: file.write('no relax\n')
    
    if opts.has_key('docell'):
        if opts['docell']: file.write('do cell\n')
    else: file.write('no cell\n')

    if opts.has_key('doneb'):
        if opts['doneb']: file.write('do neb\n')
	else: file.write('no neb\n')

    if opts.has_key('domd'):
        if opts['domd']: file.write('do md\n')
        else: file.write('no md\n')

    if opts.has_key('dopost'):
        if opts['dopost']: file.write('do post\n')
        else: file.write('no post\n')

    if opts.has_key('doblas3'):
        if opts['doblas3']: file.write('do blas3\n')
        else: file.write('no blas3\n')

    file.write('setup data\n')

    if opts.has_key('title'):
        lines = opts['title']
        file.write('title%d\n' % len(lines))
        for line in lines: file.write('%s\n' % line)
    else:
        file.write('title\nSeqquest input file generated by Icarus\n')

    if opts.has_key('dft_func'):
        file.write('functional\n%s\n' % opts['dft_func'])

    if opts.has_key('spinpol'):
        file.write('spin polarization\n%d\n' % opts['spinpol'])

    if opts.has_key('efield'):
        file.write('efield\n%f %f %f\n' % opts['efield'])

    if opts.has_key('dielec'):
        file.write('dielectric constant\n%f\n' % opts['dielec'])

    ndim = opts.get('ndim',3)
    file.write('dimensions of system (0=cluster ... 3=bulk)\n%d\n' % ndim)

    if opts.has_key('coords'):
        file.write('coordinates\n%s\n' % opts['coords'])

    if opts.has_key('scalep'):
        file.write('scalep\n%f\n' % opts['scalep'])
    if opts.has_key('scaleu'):
        file.write('scaleu\n%f\n' % opts['scaleu'])
    if opts.has_key('scalex'):
        file.write('scalex\n%f\n' % opts['scalex'])
    if opts.has_key('scaley'):
        file.write('scaley\n%f\n' % opts['scaley'])
    if opts.has_key('scalez'):
        file.write('scalez\n%f\n' % opts['scalez'])

    if opts.has_key('strain'):
        file.write('strain\n%f %f %f\n%f %f %f\n%f %f %f\n' % opts['strain'])
    if opts.has_key('strfac'):
        file.write('strfac\n%f\n' % opts['strfac'])

    ax,ay,az = cell.axyz
    ax,ay,az = ax/bohr2ang,ay/bohr2ang,az/bohr2ang
    bx,by,bz = cell.bxyz
    bx,by,bz = bx/bohr2ang,by/bohr2ang,bz/bohr2ang
    cx,cy,cz = cell.cxyz
    cx,cy,cz = cx/bohr2ang,cy/bohr2ang,cz/bohr2ang
    file.write('primitive lattice vectors\n%f %f %f\n%f %f %f\n%f %f %f\n' %
               (ax,ay,az,bx,by,bz,cx,cy,cz))

    grid = opts.get('griddim',None)
    if not grid:
	a = sqrt(ax*ax+ay*ay+az*az)
	b = sqrt(bx*bx+by*by+bz*bz)
	c = sqrt(cx*cx+cy*cy+cz*cz)
	grid = (int(a/0.3),int(b/0.3),int(c/0.3))
    file.write('grid dimensions\n%d %d %d\n' % tuple(grid))

    if opts.has_key('nearby'):
        file.write('nearby\n%d\n' % opts['nearby'])

    atoms = material.get_atom_list()
    nat = len(atoms)

    if opts.has_key('types'):
        types = opts['types']
    else:
        # Using a list for types here; replace this with a dict
        # if this becomes slow, since a dict is faster for
        # membership testing. Maybe even a set?
        types = []
        opts['types'] = types 
        for i in range(nat): 
            sym = atoms[i].get_symbol()
            if sym not in types: types.append(sym)

    ntypes = len(types)
    file.write('atom types\n%d\n' % ntypes)
    typeindex = {}
    for i in range(ntypes):
        fname = types[i]
        sym = cleansym(fname)
        typeindex[sym] = i+1
        if fname[:-4] != '.atm': fname = fname + '.atm'
        file.write('atom file\n%s\n' % fname)

    file.write('number of atoms in unit cell\n%d\n' % nat)
    file.write('atom, type, position vector\n')
    for i in range(nat):
        atom = atoms[i]
        sym = atom.get_symbol()
        x,y,z = atom.get_position()
        x,y,z = x/bohr2ang,y/bohr2ang,z/bohr2ang
        file.write('%d %d %14.10f %14.10f %14.10f\n' % (i+1,typeindex[sym],x,y,z))

    if opts.has_key('to_lat'):
        file.write('to_lattice\n')
    elif opts.has_key('to_car'):
        file.write('to_cartesian\n')

    if opts.has_key('dorig'):
        file.write('origin\n%f %f %f\n' % opts['dorig'])

    if opts.has_key('rchrg'):
        file.write('wigner seitz origin\n%f %f %f\n' % opts['rchrg'])

    if opts.has_key('rsym'):
        file.write('symmetry origin\n%f %f %f\n' % opts['rsym'])

    if opts.has_key('kgrid'):
        file.write('kgrid\n%d %d %d\n' % tuple(opts['kgrid']))
    elif opts.has_key('khex'):
        file.write('kgrid\n%d %d\n' % tuple(opts['khex']))
    else:
        ndim = opts.get('ndim',3)
        if ndim == 3: file.write('kgrid\n%d %d %d\n' % (1,1,1))
        elif ndim == 2: file.write('kgrid\n%d %d %d\n' % (1,1,0))
        elif ndim == 1: file.write('kgrid\n%d %d %d\n' % (1,0,0))

    if opts.has_key('nk'):
        file.write('n bloch vectors\n%d\n' % opts['nk'])
        # skipping scalin, lattic, cartes
    if opts.has_key('bloch vectors\n'):
        bvecs = opts['bloch_vecs']
        for bvec in bvecs:
            file.write('%f %f %f\n' % bvec)

    if opts.has_key('nsymi'):
        file.write('symops\n%d\n' % opts['nsymi'])
        file.write('definition of symmetry operations\n')
        symvecs = opts['symvecs']
        for symvec in symvecs:
            file.write('%4d %10.5f %10.5f %10.5f  %10.5f %10.5f %10.5f\n'
                       % symvec)

    file.write('end setup phase data\n')

    file.write('run phase input data\n')
    
    if opts.has_key('doflag'):
        if opts['doflag']: file.write('do flag\n')
        else: file.write('no flag\n')

    if opts.has_key('itstart'):file.write('first iteration\n%d\n' % opts['itstart'])
    if opts.has_key('itstop'): file.write('last iteration\n%d\n' % opts['itstop'])
    if opts.has_key('nhiste'): file.write('history\n%d\n' % opts['nhiste'])
    if opts.has_key('itrst'): file.write('restart\n%d\n' % opts['itrst'])
    if opts.has_key('nstate'): file.write('states\n%d\n' % opts['nstate'])
    if opts.has_key('etemp'): file.write('temperature\n%f\n' % opts['etemp'])
    if opts.has_key('scfblnd'): file.write('blend percent\n%f\n' % opts['scfblnd'])
    if opts.has_key('scfbl2'): file.write('scfbl2\n%f\n' % opts['scfbl2'])
    if opts.has_key('scfconv'):
        file.write('convergence criteria\n%f\n' % opts['scfconv'])
    if opts.has_key('alfast'): file.write('alfast\n%f\n' % opts['alfast'])

    if opts.has_key('convii'): file.write('cutii \n%f\n' % opts['convii'])
    if opts.has_key('convsl'): file.write('cutslo\n%f\n' % opts['convsl'])
    if opts.has_key('conv2s'): file.write('cut2s \n%f\n' % opts['conv2s'])
    if opts.has_key('cutset'): file.write('cutset\n%f\n' % opts['cutset'])
    if opts.has_key('cutfrc'): file.write('cutfrc\n%f\n' % opts['cutfrc'])
    if opts.has_key('convgr'): file.write('cutgrd\n%f\n' % opts['convgr'])
    if opts.has_key('conv1c'): file.write('cut1c \n%f\n' % opts['conv1c'])

    dowritegeo = opts.get('write_geo_sect',False)
    if dowritegeo:
        file.write('geometry parameters\n')
        if opts.has_key('geo_dorelax'): file.write('relax\n')

        if opts.has_key('relax_range'):
            file.write('grelax\n%d %d\n' % opts['relax_range'])
        if opts.has_key('fixed_range'):
            file.write('gfixed\n%d %d\n' % opts['fixed_range'])
        if opts.has_key('only_relax'):
            file.write('only relax\n%d\n' % opts['only_relax'])
        if opts.has_key('relax_frame'):
            file.write('frame for relaxation\n%d %d %d\n' % opts['relax_frame'])
        if opts.has_key('defect'):
            file.write('defect\n%d\n' % opts['defect'])
        if opts.has_key('gblend'):
            file.write('gblend\n%f\n' % opts['gblend'])
        if opts.has_key('gconv'):
            file.write('gconv \n%f\n' % opts['gconv'])
        if opts.has_key('gstart'):
            file.write('gstart\n%d\n' % opts['gstart'])
        if opts.has_key('gsteps'):
            file.write('gsteps\n%d\n' % opts['gsteps'])
        if opts.has_key('nhistg'):
            file.write('ghistory\n%d\n' % opts['nhistg'])
        if opts.has_key('igges'):
            igges = opts['igges']
            if igges == 0:
                file.write('no ges\n')
            else:
                file.write('guess \n%d\n' % igges)
        if opts.has_key('gmethod'):
            file.write('gmethod\n%s\n' % opts['gmethod'])
        if opts.has_key('gtstep'):
            file.write('timestep\n%f\n' % opts['gtstep'])
        file.write('end geometry parameters\n')

    dowritecell = opts.get('write_cell_sect',False)
    if dowritecell:
        file.write('cell paramters\n')
        if opts.has_key('maxucsteps'):
            file.write('ucstep\n%d\n' % opts['maxucsteps'])
        if opts.has_key('ucconv'):
            file.write('uc_convergence\n%f\n' % opts['ucconv'])
        if opts.has_key('pressure'):
            file.write('pressure\n%f\n' % opts['pressure'])
        if opts.has_key('uniaxial'):
            file.write('uniaxial pressure\n%f %f %f\n' % opts['uniaxial'])
        if opts.has_key('stress'):
            file.write('stress\n')
            stress = opts['stress']
            for vec in stress:
                file.write('%f %f %f\n' % vec)
        if opts.has_key('nhistuc'):
            file.write('uchistory\n%d\n' % opts['nhistuc'])
        if opts.has_key('ucmeth'):
            file.write('ucmethod\n%s\n' % opts['ucmeth'])
        if opts.has_key('strsbroy'):
            file.write('str_br\n%f\n' % opts['strsbroy'])
        if opts.has_key('strnmax'):
            file.write('max_strain\n%f\n' % opts['strnmax'])
        if opts.has_key('cell_f'):
            file.write('cell_f\n%f\n' % opts['cell_f'])
        if opts.has_key('bmod'):
            file.write('bulk_modulus\n%f\n' % opts['bmod'])
        if opts.has_key('ucblend'):
            file.write('uc_blend\n%f\n' % opts['ucblend'])
        file.write('end cell parameters\n')
    file.write('end of run phase data\n')

    if opts.has_key('domd') and opts['domd']:
        file.write('md data\n')
        if opts.has_key('mdtemp'):
            file.write('temperature\n%f\n' % opts['mdtemp'])
        if opts.has_key('ntstep'):
            file.write('time steps\n%d\n' % opts['ntstep'])
        if opts.has_key('neqsteps'):
            file.write('equil steps\n%d\n' % opts['neqsteps'])
        if opts.has_key('md_dt'):
            file.write('step size\n%f\n' % opts['md_dt'])
        if opts.has_key('mdtype'):
            file.write('md type\n%s\n' % opts['mdtype'])
        file.write('end md data\n')
    # done!
    return 
