# Vimm: Visual Interface for Materials Manipulation
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


import os
from vimm import FileIO
#from OpenGL.GL import *
#from OpenGL.GLU import *

# this should load serialized Structure objects as well (where it can get unit cell info)
def load_file(filename, filetype = "DEFAULT"):
    all_loaders = FileIO.loaders()
    dir,fname = os.path.split(filename)
    name,ext = os.path.splitext(fname)
    ext = ext.replace('.','')
    if all_loaders.has_key(ext):
        possible_loaders = all_loaders[ext]
        load_strings = FileIO.typestrings(possible_loaders)
        load_index = 0
        if len(possible_loaders) > 1:
            if filetype == "GUI":
                from wx import SingleChoiceDialog, OK, CANCEL, ID_OK
                d = SingleChoiceDialog(None, "Choose loader",
                    "Choose loader",
                    load_strings,
                    OK|CANCEL)
                if d.ShowModal() == ID_OK:
                    lstr = d.GetStringSelection()
                    load_index = load_strings.index(lstr)
                d.Destroy()
            else:
                for load_string in load_strings:
                    if filetype == load_string:
                        load_index = load_strings.index(filetype)
        loader = possible_loaders[load_index]
    else:
        print "No file loader known for extension ", ext
        return False

    material = loader(filename)
    return material

def simple_loader(geo):
    from Material import Material
    from Atom import Atom
    from Utilities import path_split,cleansym
    from Element import sym2no,symbol
    from NumWrap import array
    material = Material("vimm")
    for sym,xyz in geo:
        sym = sym
        atno = sym2no[sym]
        xyz = array(xyz)
        material.add_atom(Atom(atno,xyz,sym,sym))
    material.bonds_from_distance()
    return material
    

def save_file(filename, material, filetype = "DEFAULT"):
    all_savers = FileIO.savers()
    dir,fname = os.path.split(filename)
    name,ext = os.path.splitext(fname)
    if ext is None: ext = material.format
    ext = ext.replace('.','')
    if all_savers.has_key(ext):
        possible_savers = all_savers[ext]
        save_strings = FileIO.typestrings(possible_savers)
        save_index = 0
        if len(possible_savers) > 1:
            if filetype == "GUI":
                from wx import SingleChoiceDialog, OK, CANCEL, ID_OK
                d = SingleChoiceDialog(None, "Choose saver",
                    "Choose saver",
                    load_strings,
                    OK|CANCEL)
                if d.ShowModal() == ID_OK:
                    sstr = d.GetStringSelection()
                    save_index = save_strings.index(sstr)
                d.Destroy()
            else:
                for save_string in save_strings:
                    if filetype == save_string:
                        save_index = save_strings.index(filetype)
        saver = possible_savers[save_index]
    else:
        print "No file saver known for extension ", ext
        return False

    saver(filename, material)
    return True

def measure_distance(object1, object2):
    from math import sqrt
    x1,y1,z1 = object1.get_position()
    x2,y2,z2 = object2.get_position()
    distance = sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
    return distance

def create_nanotube(n, m, ncells):
    from NanoBuilder import create_nanotube_material
    newmaterial = create_nanotube_material(n, m, ncells)
    return newmaterial

def compute_unit_cell(material, buffer):
    from CrystalBuilder import compute_the_unit_cell
    unit_cell_data = compute_the_unit_cell(material, buffer)
    return unit_cell_data

def add_unit_cell(material, buffer):
    from CrystalBuilder import add_the_unit_cell
    newmaterial = add_the_unit_cell(material, buffer)
    return newmaterial

def build_crystal(crystal_type, sym1, sym2, a, c_a):
    from CrystalBuilder import build_the_crystal
    newmaterial = build_the_crystal(crystal_type, sym1, sym2, a, c_a)
    return newmaterial

def build_crystal_from_db(crystal_type):
    from CrystalBuilder import build_the_crystal_from_db
    newmaterial = build_the_crystal_from_db(crystal_type)
    return newmaterial

def build_supercell(material, a, b, c):
    from CrystalBuilder import build_the_supercell
    newmaterial = build_the_supercell(material, a, b, c)
    return newmaterial

def build_slab(material, cleave_dir, depth, vacuum):
    from CrystalBuilder import build_the_slab
    newmaterial = build_the_slab(material, cleave_dir, depth, vacuum)
    return newmaterial

def build_alkane(n):
    from AlkaneBuilder import build_the_alkane
    newmaterial = build_the_alkane(n)
    return newmaterial

def delete_bonds(material, scope):
    from BondAdjuster import delete_the_bonds
    newmaterial = delete_the_bonds(material, scope)
    return newmaterial

def add_bonds(material, scope, scopeval):
    from BondAdjuster import add_the_bonds
    newmaterial = add_the_bonds(material, scope, scopeval)
    return newmaterial

def create_render_options():
    from Renderers import RenderOptions
    ro = RenderOptions()
    return ro

def dump_movie(material, fname, camera=None, render_options=None, start=0, end=-1, step=1):
    if(start < 1 or start > material.length):
        start_frame = 0
    else:
        start_frame-=1

    if end <= start_frame or end > material.length:
        end_frame = material.length
    else:
        end_frame = end+1
        
    for fn in range(start_frame, end_frame, step):
        frame_number = fn + 1
        file_name = "frame_" + str(frame_number) + "_" + fname
        material.set_frame(fn)
        screen_capture(material, file_name, camera, render_options)
        
def screen_capture(material, fname, camera=None, render_options=None):
    from Renderers import RenderOptions, SimpleRenderer
    from Canvas import Canvas
    from wx import PySimpleApp, Frame
    
    if render_options:
        options = render_options
    else:
        options = RenderOptions()
    shapes = SimpleRenderer(material.geo, options)

    app = PySimpleApp()
    if camera:
        win = Frame(None, -1, "empty", size=camera.get_size())
        glc = Canvas(win, -1)
        glc.SetClientSize(camera.get_size())
        glc.OnSize()
    else:
        win = Frame(None, -1, "empty", size=(400,400))
        glc = Canvas(win, -1)
    win.Show()
    glc.Hide()
    win.Hide()
    glc.setup_lights()
    if camera:
        glc.camera = camera
        glc.newshapes(shapes, 0)
    else:
        glc.newshapes(shapes, 1)
    glc.setup_camera()
    glc.OnDraw()
    glc.dump_to_file(fname)
    return

class Viewer:
    def __init__(self, filename=None):
        from wx import PySimpleApp
        from Frame import Frame
        app = PySimpleApp()
        self.frame = Frame(None, -1, "vimm")#, filename, self)
        self.frame.Show()
        if filename:
            self.frame.load_file_nodialog(filename)
        app.MainLoop()
        return

    def get_camera(self):
        return self.camera

    def get_camera_position(self):
        return self.camera.get_position()

    def get_material(self):
        return self.material

    def get_render_options(self):
        return self.render_options
