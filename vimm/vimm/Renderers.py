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



from vimm.Element import color1, rvdw
from vimm.Shapes import Sphere, Cylinder, Line, Point, ShapeList, Label,\
     Triangles, Triangle, CylRad

#modes
LINES = 0
BALLSTICK = 1
BALLS = 2
CYLINDERS = 3

SPHERE_SCALE_BS = 0.25
SPHERE_SCALE_B = 0.7

class RenderOptions:
    def __init__(self, mode=BALLSTICK, unit_cell = 1, cell_label=0,
                 atom_label=0, hydrogen=0, fg_color=(1,1,1)):
        self.mode = mode
        self.unit_cell = unit_cell
        self.cell_label = cell_label
        self.atom_label = atom_label
        self.hydrogen = hydrogen
        self.fg_color = fg_color
        return

    def set_lines(self):
        self.mode = LINES

    def set_ballstick(self):
        self.mode = BALLSTICK

    def set_balls(self):
        self.mode = BALLS

    def set_lines(self):
        self.mode = CYLINDERS

    def set_mode(self, mode):
        self.mode = mode
        return

    def show_unit_cells(self, unit_cell):
        self.unit_cell = unit_cell
        return

    def show_cell_labels(self, cell_label):
        self.cell_label = cell_label
        return

    def show_atom_labels(self, atom_label):
        self.atom_label = atom_label
        return

    def hide_hydrogens(self, hydrogen):
        self.hydrogen = hydrogen
        return

    def set_fg_color(self, fg_color):
        self.fg_color = fg_color
        return
        
    def get_mode(self):
        return self.mode

    def get_unit_cells(self):
        return self.unit_cell

    def get_cell_labels(self):
        return self.cell_label

    def get_atom_labels(self):
        return self.atom_label

    def get_hydrogens(self):
        return self.hydrogen

    def get_fg_color(self):
        return self.fg_color

def SimpleRenderer(geo,options):
    shapes = ShapeList()
    atoms_images = geo.atoms + geo.images
    nat = len(atoms_images)

    # Commenting out the code to fall back to lines
    #if nat > 600:
    #    options.set_mode(LINES)
    #    print "Setting mode to lines"
    #    print options.get_mode()
    ##Never did figure out a way to set the menu item back to lines
    
    for atom in atoms_images:
        atno = atom.atno
        rgb = color1[atno]
        rad = rvdw[atno]
        if atno == 1 and options.get_hydrogens():
            pass
        else:
            if options.get_mode() == BALLSTICK:
                shapes.append_atom(Sphere(atom.xyz,SPHERE_SCALE_BS*rad,rgb))
                distance = 0.5
            elif options.get_mode() == BALLS:
                shapes.append_atom(Sphere(atom.xyz,SPHERE_SCALE_B*rad,rgb))
                distance = 0.7
            elif options.get_mode() == CYLINDERS:
                shapes.append_atom(Sphere(atom.xyz,CylRad,rgb))
                distance = 0.4
            elif options.get_mode() == LINES:
                shapes.append_atom(Point(atom.xyz,rgb,2))
                distance = 0.1
            if options.get_atom_labels():
                shapes.append_label(Label(atom.get_label(), atom.xyz,
                                          options.get_fg_color(), distance))
        #endif loop around get_hydrogens
    for bond in geo.bonds:
        atom1 = bond.atom1
        atom2 = bond.atom2
        rgb1 = color1[atom1.atno]
        rgb2 = color1[atom2.atno]
        midpoint = (atom1.xyz + atom2.xyz)/2
        if (atom1.atno == 1 or atom2.atno == 1) and options.get_hydrogens():
            pass
        else:
            if options.get_mode() == CYLINDERS \
                   or options.get_mode() == BALLSTICK:
                shapes.append_bond(Cylinder(atom1.xyz,midpoint,rgb1))
                shapes.append_bond(Cylinder(midpoint,atom2.xyz,rgb2))
            elif options.get_mode() == LINES:
                shapes.append_bond(Line(atom1.xyz,midpoint,rgb1,2))
                shapes.append_bond(Line(atom2.xyz,midpoint,rgb2,2))
        #endif loop around get_hydrogens
    if geo.cell and options.get_unit_cells():
        axyz = geo.cell.axyz
        bxyz = geo.cell.bxyz
        cxyz = geo.cell.cxyz
        origin = geo.cell.origin

        black = (0,0,0)
        white = (1,1,1)
        color = options.get_fg_color()

        shapes.append_label(Line(origin,axyz,color))
        shapes.append_label(Line(origin,bxyz,color))
        shapes.append_label(Line(origin,cxyz,color))
        shapes.append_label(Line(axyz,axyz+bxyz,color))
        shapes.append_label(Line(axyz,axyz+cxyz,color))
        shapes.append_label(Line(bxyz,bxyz+cxyz,color))
        shapes.append_label(Line(bxyz,bxyz+axyz,color))
        shapes.append_label(Line(cxyz,axyz+cxyz,color))
        shapes.append_label(Line(cxyz,bxyz+cxyz,color))
        shapes.append_label(Line(bxyz+axyz,bxyz+axyz+cxyz,color))
        shapes.append_label(Line(axyz+cxyz,axyz+cxyz+bxyz,color))
        shapes.append_label(Line(bxyz+cxyz,axyz+bxyz+cxyz,color))
        
        if hasattr(geo.cell, 'tickmarks'):
            # add label tick marks along a and b axes
            # one for each data point is default
            for position in geo.cell.tickmarks['A']:
                shapes.append_label(Label('%.1f' % position[0], position, color,-0.4))
            for position in geo.cell.tickmarks['B']:
                shapes.append_label(Label('%.1f' % position[1], position, color,-0.4))

        if options.get_cell_labels():
            shapes.append_label(Label(geo.cell.originLabel, origin,color,-0.4))
            shapes.append_label(Label(geo.cell.aLabel, axyz,color,-0.4))
            shapes.append_label(Label(geo.cell.bLabel, bxyz,color,-0.4))
            shapes.append_label(Label(geo.cell.cLabel, cxyz,color,-0.4))

    if geo.surface: #isosurface rendering
        tris = Triangles((1.,0.,1.))
        shapes.append_surface(tris)
        for xyz1,xyz2,xyz3 in geo.surface:
            tris.append(xyz1,xyz2,xyz3)
    if geo.nsurface:
        ntris = Triangles((0,1.,1.))
        shapes.append_surface(ntris)
        for xyz1,xyz2,xyz3 in geo.nsurface:
            ntris.append(xyz1,xyz2,xyz3)
    return shapes
