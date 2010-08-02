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

import math

import wx
import wx.glcanvas

from vimm import vimmLib

from vimm.Camera import Camera
from vimm.Shapes import WireCube, Line, Label, doglut
from vimm.Atom import Atom
from vimm.Bond import Bond
from vimm.Element import symbol

from vimm.NumWrap import dot, array

from OpenGL.GL import *
from OpenGL.GLU import *
if doglut:
    from OpenGL.GLUT import *

class Canvas(wx.glcanvas.GLCanvas):
    def __init__(self, parent, id, shapes = None, **kwds):
        wx.glcanvas.GLCanvas.__init__(self, parent, id, **kwds)
        self.parent = parent
        self.camera = Camera()
        self.init = False
        self.lastx = self.x = 30
        self.lasty = self.y = 30

        self.create_menu()

        wx.EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_LEFT_DOWN(self, self.OnMouseDown)
        wx.EVT_MIDDLE_DOWN(self, self.OnMouseDown)
        wx.EVT_RIGHT_DOWN(self, self.OnMouseDown)
        wx.EVT_LEFT_UP(self, self.OnMouseUp)
        wx.EVT_MIDDLE_UP(self, self.OnMouseUp)
        wx.EVT_RIGHT_UP(self, self.OnMouseUp)
        wx.EVT_MOTION(self, self.OnMouseMotion)

        self.popup_menu = 0
        self.color = (0.,0.,0.) #black
        #self.color = (1.,1.,1.) #white
        self.dlist = None
        self.measure = False
        self.sketching = False
        self.shapes = shapes

        self.left_button_click = True
        self.middle_button_click = True
        self.right_button_click = True

        self.beginx,self.beginy = 0,0
        return

    def OnSize(self, *arg):
        size = self.GetClientSize()
        old_size = self.camera.get_size()
        self.camera.set_size(size)
        if self.GetContext():
            self.SetCurrent()
            glViewport(0, 0, size.width, size.height)
            if self.dlist:
                self.camera.scaling_motion(size[0], size[1], 
					   old_size[0], old_size[1])
                self.render()
                self.Refresh(True)
        return

    def OnPaint(self, event):
        # A bit of a hack... if we are putting up the popup menu,
        # a wxpaint event occurs. But the problem is that OnDraw gets
        # called and the atoms get moved around and
        # the bonds dissappear.  Kinda makes things weird
        if self.popup_menu:
            return

        dc = wx.PaintDC(self)
        self.SetCurrent()
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()
        return

    def OnEraseBackground(self, event):
        return

    def OnMouseDown(self, evt):
        x,y = evt.GetPosition()
        self.beginx,self.beginy = x,y
        return

    def OnMouseUp(self, evt):
        if not evt: return
        self.beginx,self.beginy = evt.GetPosition()
        if self.measure and evt.LeftUp() and self.left_button_click:
            self.measure_distances(self.beginx, self.beginy)
        elif self.sketching and evt.LeftUp() and self.left_button_click:
            self.place_atom(self.beginx, self.beginy)
        elif self.sketching and evt.RightUp() and self.right_button_click:
            self.show_popup_menu(self.beginx,self.beginy)

        self.left_button_click = True
        self.middle_button_click = True
        self.right_button_click = True
        return

    def OnMouseMotion(self, evt):
        x,y = evt.GetPosition()
        changed = 0
        if evt.Dragging() and evt.LeftIsDown():
            self.left_button_click = False
            self.camera.rotation_motion(x,y,self.beginx,self.beginy)
            changed = 1
        elif evt.Dragging() and evt.MiddleIsDown():
            self.middle_button_click = False
            self.camera.translation_motion(x,y,self.beginx,self.beginy)
            changed = 1
        elif evt.Dragging() and evt.RightIsDown():
            self.right_button_click = False
            self.camera.scaling_motion(x,y,self.beginx,self.beginy)
            changed = 1

        if changed:
            self.render()
            self.Refresh(True)

        self.beginx,self.beginy = x,y
        return

    def OnColor(self, rgb):
        self.color = rgb
        self.render()
        return
        
    def InitGL(self):
        if doglut:
            glutInit(sys.argv)
        self.setup_lights()
        self.setup_antialiasing()
        self.setup_camera()
        self.setup_calllist()
        return

    def setup_antialiasing(self):
        # Original antialiasing code
        #glEnable(GL_BLEND)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        
        # Additional hints from the PyOpenGL list for antialiasing:
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_BLEND)
        glEnable(GL_ALPHA_TEST)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        glHint(GL_LINE_SMOOTH_HINT,GL_DONT_CARE)
        glHint(GL_POLYGON_SMOOTH_HINT,GL_DONT_CARE)
        return


    def OnDraw(self):
        # Attempted to duplicate the clear color code here to make the
        #  antialiasing look better on a white background, but it didn't
        #  make any difference
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glCallList(self.dlist)
        glPopMatrix()

        self.SwapBuffers()
        return

    def setup_calllist(self):
        oldlist = None
        if self.dlist: oldlist = self.dlist
        self.dlist = glGenLists(1)
        glNewList(self.dlist, GL_COMPILE)
        if self.shapes: self.shapes.render()
        glEndList()
        if oldlist and glIsList(oldlist): glDeleteLists(oldlist,1)
        return

    def setup_lights_new(self):
        # Trying another way, but doesn't change anything
        glEnable(GL_LIGHTING)
        lightZeroPosition = [10.,4.,10.,1.]
        lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
        glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
        glEnable(GL_LIGHT0)
        return

    def setup_lights(self):
        glEnable(GL_LIGHTING)
        light_diffuse = [1.0, 1.0, 1.0, 1.0]

        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)

        return

    def setup_camera(self):
        glClearColor(self.color[0], self.color[1], self.color[2], 1.0)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glClearDepth(1.0)

        pos = self.camera.get_position()
        lka = self.camera.get_look_at()
        up = self.camera.get_up()

        rcp = 2*math.sqrt(pos[0]**2+pos[1]**2+pos[2]**2)
        if rcp < 100:
            rcp = 100
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, 1.0, 1.0, rcp)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(pos[0]+lka[0],pos[1]+lka[1],pos[2]+lka[2],
                  lka[0],lka[1],lka[2],
                  up[0],up[1],up[2])
        return

    def addshapes(self,shapes,repos_camera=0):
        self.shapes.extend(shapes)
        self.camera.set_pos_from_bbox(self.shapes.bbox(),repos_camera)
        self.setup_calllist()
        self.render()
        return

    def newshapes(self,shapes,repos_camera=0):
        self.shapes = shapes
        if repos_camera:
            self.camera = Camera()
            self.camera.set_pos_from_bbox(self.shapes.bbox())
        self.setup_calllist()
        self.render()
        return

    def render(self):
        #self.setup_calllist()
        self.setup_camera()
        self.OnDraw()
        return

    def set_measure(self, measure):
        self.measure = measure

        return

    def set_sketching(self, sketching):
        self.sketching = sketching
        return

    def measure_distances(self, x, y):
        atom_index = self.pick_atom(x, y)
        if atom_index == -1:
            return
        atom = self.shapes.atoms[atom_index]
        color = self.parent.measurement_window.color
        weight = self.parent.measurement_window.weight

        if len(self.shapes.selections) == 0:
            if atom.name == "Sphere":
                if atom.rad == 0.1:
                    l = 6*atom.rad
                else:
                    l = 2*atom.rad
            else:
                l = 0.4

            wc = WireCube(atom.get_position(), l, color, weight)
            self.shapes.selections.append(wc)
        else:
            wc1 = self.shapes.selections[0]
            if wc1.get_position() == atom.get_position():
                self.shapes.selections = []
            else:
                self.shapes.selections = []
                
                distance = vimmLib.measure_distance(atom, wc1)
                dis_line = Line(wc1.get_position(), atom.get_position(), color, weight)
                self.shapes.distances.append(dis_line)

                mid_xyz = dis_line.midpoint()
                dis_label = Label("%.3f" % distance, mid_xyz, color)
                self.shapes.distances.append(dis_label)

        self.InitGL()
        self.Refresh()
        return

    def pick_atom(self, x, y):
        hits = list(glSelectWithCallback(x,y,self.find_atoms,10,10))

        min = 2**32
        atom_index = "False"
        for i in range(len(hits)):
            if hits[i][2]:
                if hits[i][0] < min:
                    atom_index = hits[i][2][0] - 1
        
        if atom_index == "False":
            return -1
        else:
            return atom_index

    def find_atoms(self):
        glMatrixMode(GL_MODELVIEW)
        self.shapes.render()

        pos = self.camera.get_position()
        lka = self.camera.get_look_at()
        up = self.camera.get_up()
        glLoadIdentity()
        gluLookAt(pos[0]+lka[0],pos[1]+lka[1],pos[2]+lka[2],
                  lka[0],lka[1],lka[2],
                  up[0],up[1],up[2])
        return

    def place_atom(self, x, y):
        atno = self.parent.sketcher_window.atno
        if atno == -1:
            d = wx.MessageDialog(self,
                "Please select an element before attempting to place one",
                "No element selected",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return

        if self.parent.material.geo.atoms == []:
            size = self.GetClientSize()
            y = size.height - y

            p1 = array(gluUnProject(x, y, 0.0))
            p2 = array(gluUnProject(x, y, 1.0))
            dp = p2 - p1
            u = -p1[2]/dp[2]
            np = p1 + u*dp

            sym = symbol[atno]
            label = sym + str(len(self.parent.material.geo.atoms))
            new_atom = Atom(atno, np, sym, label)
            self.parent.material.add_atom(new_atom)
            self.parent.render()
        else:
            if self.shapes.selections == []:
                atom_index = self.pick_atom(x, y)
                if atom_index == -1:
                    return

                self.placed_atom = self.parent.material.geo.atoms[atom_index]
                atom = self.shapes.atoms[atom_index]

                if atom.name == "Sphere":
                    if atom.rad == 0.1:
                        l = 6*atom.rad
                    else:
                        l = 2*atom.rad
                else:
                    l = 0.4
                color = (1.0, 1.0, 1.0)
                weight = 2
                wc = WireCube(atom.get_position(), l, color, weight)
                self.shapes.selections.append(wc)
                self.InitGL()
                self.Refresh()
            else:
                atom_index = self.pick_atom(x, y)
                if atom_index == -1:
                    size = self.GetClientSize()
                    y = size.height - y

                    p1 = array(gluUnProject(x, y, 0.0))
                    p2 = array(gluUnProject(x, y, 1.0))
                    r = self.camera.get_right()
                    up = self.camera.get_up()
                    
                    Nx = up[1]*r[2] - up[2]*r[1]
                    Ny = up[2]*r[0] - up[0]*r[2]
                    Nz = up[0]*r[1] - up[1]*r[0]
                    N = array((Nx,Ny,Nz))
                    p3 = array(self.placed_atom.get_position())

                    u = dot(N,(p3-p1))/dot(N,(p2-p1))
                    dp = p2 - p1
                    np = p1 + u*dp

                    atno = self.parent.sketcher_window.atno
                    sym = symbol[atno]
                    label = sym + str(len(self.parent.material.geo.atoms))
                    new_atom = Atom(atno, np, sym, label)
                    self.parent.material.add_atom(new_atom)
                    new_bond = Bond(self.placed_atom, new_atom)
                    self.parent.material.add_bond(new_bond)
                else:
                    this_atom = self.parent.material.geo.atoms[atom_index]
                    if this_atom.get_position() != self.placed_atom.get_position():
                        new_bond = Bond(self.placed_atom, this_atom)
                        self.parent.material.add_bond(new_bond)
                self.parent.render()
        return

    def delete_atom(self, *args):
        atom_index = self.current_atom_index
        atom = self.parent.material.geo.atoms[atom_index]
        self.parent.material.geo.atoms.remove(atom)

        bonds_to_eliminate = []
        for i in range(len(self.parent.material.geo.bonds)):
            bond = self.parent.material.geo.bonds[i]
            if bond.atom1 == atom or bond.atom2 == atom:
                bonds_to_eliminate.insert(0, bond)

        for bonds in bonds_to_eliminate:
            self.parent.material.geo.bonds.remove(bonds)
        self.parent.render()
        return

    def delete_bond(self, evt):
        bond_menu_id = evt.GetId()
        bond_id = self.bond_ids.index(bond_menu_id)
        bond = self.current_bonds[bond_id]
        self.parent.material.geo.bonds.remove(bond)
        self.parent.render()
        return

    def change_atom(self, evt):
        change_menu_id = evt.GetId()
        new_atom_no = self.change_ids.index(change_menu_id) + 1
        atom = self.parent.material.geo.atoms[self.current_atom_index]
        atom.atno = new_atom_no
        atom.update_symbol()
        atom.update_label()
        self.parent.material.geo.atoms[self.current_atom_index] = atom
        self.parent.render()
        return

    def show_popup_menu(self, x, y):
        self.popup_menu = 1
        self.current_atom_index = self.pick_atom(x, y)
        if self.current_atom_index == -1:
            return

        for bond_id in self.bond_ids:
            self.bondmenu.Delete(bond_id)

        self.current_bonds = []
        bonded_atoms = []
        for bond in self.parent.material.geo.bonds:
            a1 = self.parent.material.geo.atoms.index(bond.atom1)
            a2 = self.parent.material.geo.atoms.index(bond.atom2)
            if a1 == self.current_atom_index:
                self.current_bonds.append(bond)
                bonded_atoms.append(a2)
            elif a2 == self.current_atom_index:
                self.current_bonds.append(bond)
                bonded_atoms.append(a1)

        self.bond_ids = []
        for ba in bonded_atoms:
            ID_DELETE_BOND = wx.NewId()
            self.bondmenu.Append(ID_DELETE_BOND,
                "Delete bond with " + self.parent.material.geo.atoms[ba].get_label(),
                "",
                wx.ITEM_NORMAL)

            wx.EVT_MENU(self,ID_DELETE_BOND, self.delete_bond)
            self.bond_ids.append(ID_DELETE_BOND)

        self.PopupMenu(self.popupmenu)
        self.render()
        self.popup_menu = 0
        return

    def dump(self):
        try:
            import Image
        except:
            d = wx.MessageDialog(self.parent,
                "PIL module not available, thus screenshot not available",
                "Screenshot Not Available",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return

        filetypes = "PNG (*.png)|*.png|JPEG (*.jpg)|*.jpg|"\
                    "GIF (*.gif)|*.gif|All Files (*.*)|*"

        d = wx.FileDialog(self,"Save Image As",os.getcwd(),"",
                          filetypes,wx.SAVE) 

        if d.ShowModal() == wx.ID_OK:
            fname = d.GetFilename()
            dir = d.GetDirectory()
            fullfilename = os.path.join(dir,fname)
            
            self.dump_to_file(fullfilename)
        d.Destroy()
        return

    def dump_to_file(self, fullfilename):
        import Image
        width,height = self.GetSize()
        pstring = glReadPixels(0,0,width,height,GL_RGBA,
                               GL_UNSIGNED_BYTE)
        snapshot = Image.fromstring("RGBA",(width,height),pstring
                                    ).transpose(Image.FLIP_TOP_BOTTOM)
        from Utilities import assureCorrectFileEnding
        fullfilename = assureCorrectFileEnding(fullfilename,'png')
        snapshot.save(fullfilename)
        return
    #
    # The rest of the file has to do with making that stupid pop up menu.
    #
    def create_menu(self):
        ID_DELETE_ATOM = wx.NewId()
        self.popupmenu = wx.Menu()
        self.popupmenu.Append(ID_DELETE_ATOM,
            "Delete atom",
            "",
            wx.ITEM_NORMAL)
        wx.EVT_MENU(self,ID_DELETE_ATOM, self.delete_atom)
        
        self.bond_ids = []
        self.bondmenu = wx.Menu()
        self.popupmenu.AppendMenu(wx.NewId(),
            "Delete bond",
            self.bondmenu,
            "")

        self.change_ids = []
        self.changemenu = wx.Menu()
        self.create_row1menu()
        self.create_row2menu()
        self.create_row3menu()
        self.create_row4menu()
        self.create_row5menu()
        self.create_row6menu()
        self.create_row7menu()
        self.create_row8menu()
        self.create_row9menu()

        self.changemenu.AppendMenu(wx.NewId(),
            "Row 1",
            self.row1menu,
            "")
        self.changemenu.AppendMenu(wx.NewId(),
            "Row 2",
            self.row2menu,
            "")
        self.changemenu.AppendMenu(wx.NewId(),
            "Row 3",
            self.row3menu,
            "")
        self.changemenu.AppendMenu(wx.NewId(),
            "Row 4",
            self.row4menu,
            "")
        self.changemenu.AppendMenu(wx.NewId(),
            "Row 5",
            self.row5menu,
            "")
        self.changemenu.AppendMenu(wx.NewId(),
            "Row 6",
            self.row6menu,
            "")
        self.changemenu.AppendMenu(wx.NewId(),
            "Row 7",
            self.row7menu,
            "")
        self.changemenu.AppendMenu(wx.NewId(),
            "Row 8",
            self.row8menu,
            "")
        self.changemenu.AppendMenu(wx.NewId(),
            "Row 9",
            self.row9menu,
            "")

        self.popupmenu.AppendMenu(wx.NewId(),
            "Change Element to",
            self.changemenu,
            "")
        return

    def create_row1menu(self):
        self.row1menu = wx.Menu()
        ID_H = wx.NewId()
        ID_He = wx.NewId()

        self.row1menu.Append(ID_H,
            "H",
            "",
            wx.ITEM_NORMAL)
        self.row1menu.Append(ID_He,
            "He",
            "",
            wx.ITEM_NORMAL)

        self.change_ids.append(ID_H)
        self.change_ids.append(ID_He)

        wx.EVT_MENU(self, self.change_ids[0], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[1], self.change_atom)
        return

    def create_row2menu(self):
        self.row2menu = wx.Menu()
        ID_Li = wx.NewId()
        ID_Be = wx.NewId()
        ID_B = wx.NewId()
        ID_C = wx.NewId()
        ID_N = wx.NewId()
        ID_O = wx.NewId()
        ID_F = wx.NewId()
        ID_Ne = wx.NewId()

        self.row2menu.Append(ID_Li,
            "Li",
            "",
            wx.ITEM_NORMAL)
        self.row2menu.Append(ID_Be,
            "Be",
            "",
            wx.ITEM_NORMAL)
        self.row2menu.Append(ID_B,
            "B",
            "",
            wx.ITEM_NORMAL)
        self.row2menu.Append(ID_C,
            "C",
            "",
            wx.ITEM_NORMAL)
        self.row2menu.Append(ID_N,
            "N",
            "",
            wx.ITEM_NORMAL)
        self.row2menu.Append(ID_O,
            "O",
            "",
            wx.ITEM_NORMAL)
        self.row2menu.Append(ID_F,
            "F",
            "",
            wx.ITEM_NORMAL)
        self.row2menu.Append(ID_Ne,
            "Ne",
            "",
            wx.ITEM_NORMAL)

        self.change_ids.append(ID_Li)
        self.change_ids.append(ID_Be)
        self.change_ids.append(ID_B)
        self.change_ids.append(ID_C)
        self.change_ids.append(ID_N)
        self.change_ids.append(ID_O)
        self.change_ids.append(ID_F)
        self.change_ids.append(ID_Ne)

        wx.EVT_MENU(self, self.change_ids[2], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[3], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[4], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[5], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[6], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[7], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[8], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[9], self.change_atom)
        return

    def create_row3menu(self):
        self.row3menu = wx.Menu()
        ID_Na = wx.NewId()
        ID_Mg = wx.NewId()
        ID_Al = wx.NewId()
        ID_Si = wx.NewId()
        ID_P = wx.NewId()
        ID_S = wx.NewId()
        ID_Cl = wx.NewId()
        ID_Ar = wx.NewId()

        self.row3menu.Append(ID_Na,
            "Na",
            "",
            wx.ITEM_NORMAL)
        self.row3menu.Append(ID_Mg,
            "Mg",
            "",
            wx.ITEM_NORMAL)
        self.row3menu.Append(ID_Al,
            "Al",
            "",
            wx.ITEM_NORMAL)
        self.row3menu.Append(ID_Si,
            "Si",
            "",
            wx.ITEM_NORMAL)
        self.row3menu.Append(ID_P,
            "P",
            "",
            wx.ITEM_NORMAL)
        self.row3menu.Append(ID_S,
            "S",
            "",
            wx.ITEM_NORMAL)
        self.row3menu.Append(ID_Cl,
            "Cl",
            "",
            wx.ITEM_NORMAL)
        self.row3menu.Append(ID_Ar,
            "Ar",
            "",
            wx.ITEM_NORMAL)

        self.change_ids.append(ID_Na)
        self.change_ids.append(ID_Mg)
        self.change_ids.append(ID_Al)
        self.change_ids.append(ID_Si)
        self.change_ids.append(ID_P)
        self.change_ids.append(ID_S)
        self.change_ids.append(ID_Cl)
        self.change_ids.append(ID_Ar)

        wx.EVT_MENU(self, self.change_ids[10], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[11], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[12], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[13], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[14], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[15], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[16], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[17], self.change_atom)
        return

    def create_row4menu(self):
        self.row4menu = wx.Menu()
        ID_K = wx.NewId()
        ID_Ca = wx.NewId()
        ID_Sc = wx.NewId()
        ID_Ti = wx.NewId()
        ID_V = wx.NewId()
        ID_Cr = wx.NewId()
        ID_Mn = wx.NewId()
        ID_Fe = wx.NewId()
        ID_Co = wx.NewId()
        ID_Ni = wx.NewId()
        ID_Cu = wx.NewId()
        ID_Zn = wx.NewId()
        ID_Ga = wx.NewId()
        ID_Ge = wx.NewId()
        ID_As = wx.NewId()
        ID_Se = wx.NewId()
        ID_Br = wx.NewId()
        ID_Kr = wx.NewId()

        self.row4menu.Append(ID_K,
            "K",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Ca,
            "Ca",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Sc,
            "Sc",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Ti,
            "Ti",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_V,
            "V",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Cr,
            "Cr",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Mn,
            "Mn",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Fe,
            "Fe",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Co,
            "Co",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Ni,
            "Ni",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Cu,
            "Cu",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Zn,
            "Zn",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Ga,
            "Ga",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Ge,
            "Ge",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_As,
            "As",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Se,
            "Se",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Br,
            "Br",
            "",
            wx.ITEM_NORMAL)
        self.row4menu.Append(ID_Kr,
            "Kr",
            "",
            wx.ITEM_NORMAL)

        self.change_ids.append(ID_K)
        self.change_ids.append(ID_Ca)
        self.change_ids.append(ID_Sc)
        self.change_ids.append(ID_Ti)
        self.change_ids.append(ID_V)
        self.change_ids.append(ID_Cr)
        self.change_ids.append(ID_Mn)
        self.change_ids.append(ID_Fe)
        self.change_ids.append(ID_Co)
        self.change_ids.append(ID_Ni)
        self.change_ids.append(ID_Cu)
        self.change_ids.append(ID_Zn)
        self.change_ids.append(ID_Ga)
        self.change_ids.append(ID_Ge)
        self.change_ids.append(ID_As)
        self.change_ids.append(ID_Se)
        self.change_ids.append(ID_Br)
        self.change_ids.append(ID_Kr)

        wx.EVT_MENU(self, self.change_ids[18], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[19], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[20], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[21], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[22], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[23], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[24], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[25], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[26], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[27], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[28], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[29], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[30], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[31], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[32], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[33], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[34], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[35], self.change_atom)
        return

    def create_row5menu(self):
        self.row5menu = wx.Menu()
        ID_Rb = wx.NewId()
        ID_Sr = wx.NewId()
        ID_Y = wx.NewId()
        ID_Zr = wx.NewId()
        ID_Nb = wx.NewId()
        ID_Mo = wx.NewId()
        ID_Tc = wx.NewId()
        ID_Ru = wx.NewId()
        ID_Rh = wx.NewId()
        ID_Pd = wx.NewId()
        ID_Ag = wx.NewId()
        ID_Cd = wx.NewId()
        ID_In = wx.NewId()
        ID_Sn = wx.NewId()
        ID_Sb = wx.NewId()
        ID_Te = wx.NewId()
        ID_I = wx.NewId()
        ID_Xe = wx.NewId()

        self.row5menu.Append(ID_Rb,
            "Rb",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Sr,
            "Sr",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Y,
            "Y",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Zr,
            "Zr",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Nb,
            "Nb",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Mo,
            "Mo",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Tc,
            "Tc",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Ru,
            "Ru",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Rh,
            "Rh",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Pd,
            "Pd",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Ag,
            "Ag",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Cd,
            "Cd",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_In,
            "In",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Sn,
            "Sn",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Sb,
            "Sb",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Te,
            "Te",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_I,
            "I",
            "",
            wx.ITEM_NORMAL)
        self.row5menu.Append(ID_Xe,
            "Xe",
            "",
            wx.ITEM_NORMAL)

        self.change_ids.append(ID_Rb)
        self.change_ids.append(ID_Sr)
        self.change_ids.append(ID_Y)
        self.change_ids.append(ID_Zr)
        self.change_ids.append(ID_Nb)
        self.change_ids.append(ID_Mo)
        self.change_ids.append(ID_Tc)
        self.change_ids.append(ID_Ru)
        self.change_ids.append(ID_Rh)
        self.change_ids.append(ID_Pd)
        self.change_ids.append(ID_Ag)
        self.change_ids.append(ID_Cd)
        self.change_ids.append(ID_In)
        self.change_ids.append(ID_Sn)
        self.change_ids.append(ID_Sb)
        self.change_ids.append(ID_Te)
        self.change_ids.append(ID_I)
        self.change_ids.append(ID_Xe)

        wx.EVT_MENU(self, self.change_ids[36], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[37], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[38], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[39], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[40], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[41], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[42], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[43], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[44], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[45], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[46], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[47], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[48], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[49], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[50], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[51], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[52], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[53], self.change_atom)
        return

    def create_row6menu(self):
        self.row6menu = wx.Menu()
        ID_Cs = wx.NewId()
        ID_Ba = wx.NewId()
        ID_Lu = wx.NewId()
        ID_Hf = wx.NewId()
        ID_Ta = wx.NewId()
        ID_W = wx.NewId()
        ID_Re = wx.NewId()
        ID_Os = wx.NewId()
        ID_Ir = wx.NewId()
        ID_Pt = wx.NewId()
        ID_Au = wx.NewId()
        ID_Hg = wx.NewId()
        ID_Tl = wx.NewId()
        ID_Pb = wx.NewId()
        ID_Bi = wx.NewId()
        ID_Po = wx.NewId()
        ID_At = wx.NewId()
        ID_Rn = wx.NewId()

        self.row6menu.Append(ID_Cs,
            "Cs",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Ba,
            "Ba",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Lu,
            "Lu",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Hf,
            "Hf",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Ta,
            "Ta",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_W,
            "W",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Re,
            "Re",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Os,
            "Os",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Ir,
            "Ir",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Pt,
            "Pt",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Au,
            "Au",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Hg,
            "Hg",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Tl,
            "Tl",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Pb,
            "Pb",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Bi,
            "Bi",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Po,
            "Po",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_At,
            "At",
            "",
            wx.ITEM_NORMAL)
        self.row6menu.Append(ID_Rn,
            "Rn",
            "",
            wx.ITEM_NORMAL)

        self.change_ids.append(ID_Cs)
        self.change_ids.append(ID_Ba)
        self.change_ids.append(ID_Lu)
        self.change_ids.append(ID_Hf)
        self.change_ids.append(ID_Ta)
        self.change_ids.append(ID_W)
        self.change_ids.append(ID_Re)
        self.change_ids.append(ID_Os)
        self.change_ids.append(ID_Ir)
        self.change_ids.append(ID_Pt)
        self.change_ids.append(ID_Au)
        self.change_ids.append(ID_Hg)
        self.change_ids.append(ID_Tl)
        self.change_ids.append(ID_Pb)
        self.change_ids.append(ID_Bi)
        self.change_ids.append(ID_Po)
        self.change_ids.append(ID_At)
        self.change_ids.append(ID_Rn)

        wx.EVT_MENU(self, self.change_ids[54], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[55], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[56], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[57], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[58], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[59], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[60], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[61], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[62], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[63], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[64], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[65], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[66], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[67], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[68], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[69], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[70], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[71], self.change_atom)
        return

    def create_row7menu(self):
        self.row7menu = wx.Menu()
        ID_Fr = wx.NewId()
        ID_Ra = wx.NewId()
        ID_Lr = wx.NewId()
        ID_Rf = wx.NewId()
        ID_Db = wx.NewId()
        ID_Sg = wx.NewId()
        ID_Bh = wx.NewId()
        ID_Hs = wx.NewId()
        ID_Mt = wx.NewId()
        ID_Ds = wx.NewId()
        ID_Rg = wx.NewId()
        ID_Uub = wx.NewId()
        ID_Uut = wx.NewId()
        ID_Uuq = wx.NewId()
        ID_Uup = wx.NewId()
        ID_Uuh = wx.NewId()
        ID_Uus = wx.NewId()
        ID_Uuo = wx.NewId()

        self.row7menu.Append(ID_Fr,
            "Fr",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Ra,
            "Ra",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Lr,
            "Lr",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Rf,
            "Rf",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Db,
            "Db",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Sg,
            "Sg",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Bh,
            "Bh",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Hs,
            "Hs",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Mt,
            "Mt",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Ds,
            "Ds",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Rg,
            "Rg",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Uub,
            "Uub",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Uut,
            "Uut",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Uuq,
            "Uuq",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Uup,
            "Uup",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Uuh,
            "Uuh",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Uus,
            "Uus",
            "",
            wx.ITEM_NORMAL)
        self.row7menu.Append(ID_Uuo,
            "Uuo",
            "",
            wx.ITEM_NORMAL)

        self.change_ids.append(ID_Fr)
        self.change_ids.append(ID_Ra)
        self.change_ids.append(ID_Lr)
        self.change_ids.append(ID_Rf)
        self.change_ids.append(ID_Db)
        self.change_ids.append(ID_Sg)
        self.change_ids.append(ID_Bh)
        self.change_ids.append(ID_Hs)
        self.change_ids.append(ID_Mt)
        self.change_ids.append(ID_Ds)
        self.change_ids.append(ID_Rg)
        self.change_ids.append(ID_Uub)
        self.change_ids.append(ID_Uut)
        self.change_ids.append(ID_Uuq)
        self.change_ids.append(ID_Uup)
        self.change_ids.append(ID_Uuh)
        self.change_ids.append(ID_Uus)
        self.change_ids.append(ID_Uuo)

        wx.EVT_MENU(self, self.change_ids[72], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[73], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[74], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[75], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[76], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[77], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[78], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[79], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[80], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[81], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[82], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[83], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[84], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[85], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[86], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[87], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[88], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[89], self.change_atom)
        return

    def create_row8menu(self):
        self.row8menu = wx.Menu()
        ID_La = wx.NewId()
        ID_Ce = wx.NewId()
        ID_Pr = wx.NewId()
        ID_Nd = wx.NewId()
        ID_Pm = wx.NewId()
        ID_Sm = wx.NewId()
        ID_Eu = wx.NewId()
        ID_Gd = wx.NewId()
        ID_Tb = wx.NewId()
        ID_Dy = wx.NewId()
        ID_Ho = wx.NewId()
        ID_Er = wx.NewId()
        ID_Tm = wx.NewId()
        ID_Yb = wx.NewId()

        self.row8menu.Append(ID_La,
            "La",
            "",
            wx.ITEM_NORMAL)
        self.row8menu.Append(ID_Ce,
            "Ce",
            "",
            wx.ITEM_NORMAL)
        self.row8menu.Append(ID_Pr,
            "Pr",
            "",
            wx.ITEM_NORMAL)
        self.row8menu.Append(ID_Nd,
            "Nd",
            "",
            wx.ITEM_NORMAL)
        self.row8menu.Append(ID_Pm,
            "Pm",
            "",
            wx.ITEM_NORMAL)
        self.row8menu.Append(ID_Sm,
            "Sm",
            "",
            wx.ITEM_NORMAL)
        self.row8menu.Append(ID_Eu,
            "Eu",
            "",
            wx.ITEM_NORMAL)
        self.row8menu.Append(ID_Gd,
            "Gd",
            "",
            wx.ITEM_NORMAL)
        self.row8menu.Append(ID_Tb,
            "Tb",
            "",
            wx.ITEM_NORMAL)
        self.row8menu.Append(ID_Dy,
            "Dy",
            "",
            wx.ITEM_NORMAL)
        self.row8menu.Append(ID_Ho,
            "Ho",
            "",
            wx.ITEM_NORMAL)
        self.row8menu.Append(ID_Er,
            "Er",
            "",
            wx.ITEM_NORMAL)
        self.row8menu.Append(ID_Tm,
            "Tm",
            "",
            wx.ITEM_NORMAL)
        self.row8menu.Append(ID_Yb,
            "Yb",
            "",
            wx.ITEM_NORMAL)

        self.change_ids.insert(56, ID_La)
        self.change_ids.insert(57, ID_Ce)
        self.change_ids.insert(58, ID_Pr)
        self.change_ids.insert(59, ID_Nd)
        self.change_ids.insert(60, ID_Pm)
        self.change_ids.insert(61, ID_Sm)
        self.change_ids.insert(62, ID_Eu)
        self.change_ids.insert(63, ID_Gd)
        self.change_ids.insert(64, ID_Tb)
        self.change_ids.insert(65, ID_Dy)
        self.change_ids.insert(66, ID_Ho)
        self.change_ids.insert(67, ID_Er)
        self.change_ids.insert(68, ID_Tm)
        self.change_ids.insert(69, ID_Yb)

        wx.EVT_MENU(self, self.change_ids[56], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[57], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[58], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[59], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[60], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[61], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[62], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[63], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[64], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[65], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[66], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[67], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[68], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[69], self.change_atom)
        return

    def create_row9menu(self):
        self.row9menu = wx.Menu()
        ID_Ac = wx.NewId()
        ID_Th = wx.NewId()
        ID_Pa = wx.NewId()
        ID_U = wx.NewId()
        ID_Np = wx.NewId()
        ID_Pu = wx.NewId()
        ID_Am = wx.NewId()
        ID_Cm = wx.NewId()
        ID_Bk = wx.NewId()
        ID_Cf = wx.NewId()
        ID_Es = wx.NewId()
        ID_Fm = wx.NewId()
        ID_Md = wx.NewId()
        ID_No = wx.NewId()

        self.row9menu.Append(ID_Ac,
            "Ac",
            "",
            wx.ITEM_NORMAL)
        self.row9menu.Append(ID_Th,
            "Th",
            "",
            wx.ITEM_NORMAL)
        self.row9menu.Append(ID_Pa,
            "Pa",
            "",
            wx.ITEM_NORMAL)
        self.row9menu.Append(ID_U,
            "U",
            "",
            wx.ITEM_NORMAL)
        self.row9menu.Append(ID_Np,
            "Np",
            "",
            wx.ITEM_NORMAL)
        self.row9menu.Append(ID_Pu,
            "Pu",
            "",
            wx.ITEM_NORMAL)
        self.row9menu.Append(ID_Am,
            "Am",
            "",
            wx.ITEM_NORMAL)
        self.row9menu.Append(ID_Cm,
            "Cm",
            "",
            wx.ITEM_NORMAL)
        self.row9menu.Append(ID_Bk,
            "Bk",
            "",
            wx.ITEM_NORMAL)
        self.row9menu.Append(ID_Cf,
            "Cf",
            "",
            wx.ITEM_NORMAL)
        self.row9menu.Append(ID_Es,
            "Es",
            "",
            wx.ITEM_NORMAL)
        self.row9menu.Append(ID_Fm,
            "Fm",
            "",
            wx.ITEM_NORMAL)
        self.row9menu.Append(ID_Md,
            "Md",
            "",
            wx.ITEM_NORMAL)
        self.row9menu.Append(ID_No,
            "No",
            "",
            wx.ITEM_NORMAL)

        self.change_ids.insert(88, ID_Ac)
        self.change_ids.insert(89, ID_Th)
        self.change_ids.insert(90, ID_Pa)
        self.change_ids.insert(91, ID_U)
        self.change_ids.insert(92, ID_Np)
        self.change_ids.insert(93, ID_Pu)
        self.change_ids.insert(94, ID_Am)
        self.change_ids.insert(95, ID_Cm)
        self.change_ids.insert(96, ID_Bk)
        self.change_ids.insert(97, ID_Cf)
        self.change_ids.insert(98, ID_Es)
        self.change_ids.insert(99, ID_Fm)
        self.change_ids.insert(100, ID_Md)
        self.change_ids.insert(101, ID_No)

        wx.EVT_MENU(self, self.change_ids[88], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[89], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[90], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[91], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[92], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[93], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[94], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[95], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[96], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[97], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[98], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[99], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[100], self.change_atom)
        wx.EVT_MENU(self, self.change_ids[101], self.change_atom)
        return
