# VIMM: Visual Interface for Materials Manipulation
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
import wx

from vimm.Renderers import RenderOptions, SimpleRenderer, LINES, BALLSTICK, \
     BALLS, CYLINDERS
from vimm.Canvas import Canvas
from vimm.CoordEditor import CoordEditor
from vimm.Animation import Animation
from vimm.Measurements import Measurements
from vimm.Sketcher import Sketcher
#from UFF.Cleaner import Cleaner
from vimm.Cartesians import Cartesians
from vimm.CrystalBuilder import CrystalBuilder, CrystalDatabase, Supercell,\
     SlabBuilder, AddUC
from vimm.NanoBuilder import NanoBuilder
from vimm.AlkaneBuilder import AlkaneBuilder
from vimm.OrbitalViewer import OrbitalViewer
from vimm.engines.QuestOptions import QuestOptions
from vimm.BondAdjustor import BondAdjustor
from vimm.ZBuilder import ZBuilder

import FileIO
import vimmLib

class Frame(wx.Frame):
    def __init__(self, parent, id, title, lib=None, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        self.lib = lib
        wx.Frame.__init__(self, parent, id, title, **kwds)
        self.make_widgets()
        self.material = None
        self.surface = None
        self.renderOptions = RenderOptions(CYLINDERS)
        wx.EVT_CLOSE(self, self.closemyself)
        
        try: # Mac doesn't start up in the correct directory
            os.chdir(os.environ["PWD"])
        except:
            pass
        self.Center()
        return

    def closemyself(self, *args):
        if self.lib != None:
            self.lib.camera = self.canvas.camera
            self.lib.material = self.material
            self.lib.render_options = self.renderOptions
        self.Destroy()
        return

    def make_widgets(self):
        self.canvas = Canvas(self, -1)
        self.make_menubar()
        self.statusbar = self.CreateStatusBar(1, 0)
        self.set_properties()
        self.do_layout()
        return

    def make_menubar(self):
        self.make_filemenu()
        self.make_editmenu()
        self.make_viewmenu()
        self.make_toolmenu()
        self.make_appmenu()
        self.make_helpmenu()
        return

    def make_filemenu(self):
        self.menubar = wx.MenuBar()
        self.SetMenuBar(self.menubar)
        self.filemenu = wx.Menu()
        self.filemenu.Append(wx.ID_NEW,
                             "New\tCtrl-n",
                             "Create a new file",
                             wx.ITEM_NORMAL)
        self.filemenu.Append(wx.ID_OPEN,
                             "Open\tCtrl-o",
                             "Open a file containing a new structure",
                             wx.ITEM_NORMAL)
        self.filemenu.Append(wx.ID_SAVE,
                             "Save\tCtrl-s",
                             "Save the current structure",
                             wx.ITEM_NORMAL)
        self.filemenu.Append(wx.ID_SAVEAS,
                             "Save As",
                             "Save structure under a new filename",
                             wx.ITEM_NORMAL)
        ID_POV = wx.NewId()
        self.filemenu.Append(ID_POV,
                             "EXport Povray\tCtrl-x",
                             "Export and render with POVRay",
                             wx.ITEM_NORMAL)
        self.filemenu.Append(wx.ID_CLOSE,
                             "Close\tCtrl-w",
                             "Close the current structure",
                             wx.ITEM_NORMAL)
        self.filemenu.Append(wx.ID_EXIT,
                             "Exit\tCtrl-q",
                             "Quit the program",
                             wx.ITEM_NORMAL)
        self.menubar.Append(self.filemenu, "&File")

        wx.EVT_MENU(self,wx.ID_NEW,self.new_file)
        wx.EVT_MENU(self,wx.ID_OPEN,self.load_file)
        wx.EVT_MENU(self,wx.ID_SAVE,self.save_as)
        wx.EVT_MENU(self,wx.ID_SAVEAS,self.save_as)
        wx.EVT_MENU(self,ID_POV,self.render_povray)
        wx.EVT_MENU(self,wx.ID_EXIT,self.quit)
        
        return

    def make_editmenu(self):
        ID_SCREENSHOT = wx.NewId()
        ID_BGCOLOR = wx.NewId()
        ID_EDIT_COORD = wx.NewId()
        ID_EDIT_CART = wx.NewId()
        ID_EDIT_ZMAT = wx.NewId()
        ID_EDIT_FRAC = wx.NewId()

        self.editmenu = wx.Menu()
        self.editmenu.Append(ID_SCREENSHOT,
                             "Screenshot",
                             "Dump a screenshot to a file",
                             wx.ITEM_NORMAL)
        self.editmenu.Append(ID_BGCOLOR,
                             "Set Background Color",
                             "Set the color of the background",
                             wx.ITEM_NORMAL)
        self.editmenu.AppendSeparator()
        self.editmenu.Append(ID_EDIT_COORD,
                             "Edit Coordinates\tCtrl-e",
                             "Edit the Cartesian or Internal Coordinates",
                             wx.ITEM_NORMAL)
        # This was superceded by the CoordEditor
        #self.editmenu.Append(ID_EDIT_CART,
        #                     "Edit Cartesians",
        #                     "Edit the Cartesian Coordinates",
        #                     wx.ITEM_NORMAL)

        # This was superceded by the CoordEditor
        #self.editmenu.Append(ID_EDIT_ZMAT,
        #                     "Edit Zmatrix",
        #                     "Edit the internal coordinates",
        #                     wx.ITEM_NORMAL)

        # This has never completely worked
        #self.editmenu.Append(ID_EDIT_FRAC,
        #                     "Edit Fractionals",
        #                     "Edit the fractional coordinates",
        #                     wx.ITEM_NORMAL)
        self.menubar.Append(self.editmenu, "&Edit")

        wx.EVT_MENU(self,ID_BGCOLOR,self.set_bg_color)
        wx.EVT_MENU(self,ID_SCREENSHOT,self.dump) 
        wx.EVT_MENU(self,ID_EDIT_COORD, self.edit_coord)
        wx.EVT_MENU(self,ID_EDIT_CART, self.edit_cart)
        return

    def make_viewmenu(self):
        ID_ANIMATE = wx.NewId()
        ID_ANIMATE_NEXT = wx.NewId()
        
        self.ID_UNIT_CELL = wx.NewId()
        self.ID_CELL_LABELS = wx.NewId()
        self.ID_ATOM_LABELS = wx.NewId()
        self.ID_HIDE_H = wx.NewId()

        ID_RENDER_LINES = wx.NewId()
        ID_RENDER_BALLSTICK = wx.NewId()
        ID_RENDER_BALLS = wx.NewId()
        ID_RENDER_CYLINDERS = wx.NewId()

        self.viewmenu = wx.Menu()
        self.viewmenu.Append(ID_ANIMATE,
                             "Animate",
                             "Animate the structures",
                             wx.ITEM_NORMAL)
        self.viewmenu.AppendSeparator()
        self.viewmenu.Append(ID_RENDER_LINES,
                             "Lines",
                             "Render using lines",
                             wx.ITEM_RADIO)
        self.viewmenu.Append(ID_RENDER_BALLSTICK,
                             "Ball and Stick",
                             "Render using balls and sticks",
                             wx.ITEM_RADIO)
        self.viewmenu.Append(ID_RENDER_BALLS,
                             "Balls",
                             "Render using balls",
                             wx.ITEM_RADIO)
        self.viewmenu.Append(ID_RENDER_CYLINDERS,
                             "Cylinders",
                             "Render using cylinders",
                             wx.ITEM_RADIO)
        self.viewmenu.AppendSeparator()
        self.viewmenu.Append(self.ID_UNIT_CELL,
                             "Unit Cell",
                             "Draw the unit cell",
                             wx.ITEM_CHECK)
        self.viewmenu.Append(self.ID_CELL_LABELS,
                             "Cell Labels",
                             "Label the unit cell vectors",
                             wx.ITEM_CHECK)
        self.viewmenu.Append(self.ID_ATOM_LABELS,
                             "Atom Labels",
                             "Label the atoms",
                             wx.ITEM_CHECK)
        self.viewmenu.Append(self.ID_HIDE_H,
                             "Hide Hydrogens",
                             "Hide the hydrogen atoms",
                             wx.ITEM_CHECK)
        self.menubar.Append(self.viewmenu, "&View")

        wx.EVT_MENU(self,ID_ANIMATE,self.animate)

        wx.EVT_MENU(self,ID_RENDER_LINES,self.set_render_lines)
        wx.EVT_MENU(self,ID_RENDER_BALLSTICK,self.set_render_ballstick)
        wx.EVT_MENU(self,ID_RENDER_BALLS,self.set_render_balls)
        wx.EVT_MENU(self,ID_RENDER_CYLINDERS,self.set_render_cylinders)

        wx.EVT_MENU(self, self.ID_UNIT_CELL, self.set_unit_cell)
        wx.EVT_MENU(self, self.ID_CELL_LABELS, self.set_cell_labels)
        wx.EVT_MENU(self, self.ID_ATOM_LABELS, self.set_atom_labels)
        wx.EVT_MENU(self, self.ID_HIDE_H, self.set_hide_h)

        # check defaults manually, unfortunately
        self.viewmenu.Check(ID_RENDER_CYLINDERS,1)
        self.viewmenu.Check(self.ID_UNIT_CELL,1)
        return

    def make_toolmenu(self):
        ID_ADJUST_BONDS = wx.NewId()
        ID_BUILD_XTAL = wx.NewId()
        ID_XTAL_DB = wx.NewId()
        ID_BUILD_SUPER = wx.NewId()
        ID_BUILD_SLAB = wx.NewId()
        ID_ADD_UC = wx.NewId()
        ID_BUILD_NANO = wx.NewId()
        ID_BUILD_ALKA = wx.NewId()
        ID_ZBUILD = wx.NewId()
        ID_SKETCH = wx.NewId()
        ID_CLEAN = wx.NewId()
        ID_VIEW_ORBS = wx.NewId()
        self.ID_MEASURE = wx.NewId()

        self.toolmenu = wx.Menu()
        self.toolmenu.Append(self.ID_MEASURE,
                             "Measure Distances",
                             "Measure Distances",
                             wx.ITEM_NORMAL)
        self.toolmenu.AppendSeparator()
        self.toolmenu.Append(ID_VIEW_ORBS,
                             "View Orbitals",
                             "View Orbitals",
                             wx.ITEM_NORMAL)
        self.toolmenu.AppendSeparator()
        self.toolmenu.Append(ID_ADJUST_BONDS,
                             "Adjust Bonds",
                             "Add/Delete Bonds",
                             wx.ITEM_NORMAL)
        self.toolmenu.Append(ID_BUILD_XTAL,
                             "Crystal Builder",
                             "Build a structure with the crystal builder",
                             wx.ITEM_NORMAL)
        self.toolmenu.Append(ID_XTAL_DB,
                             "Crystal Database",
                             "Build a structure from a crystal database",
                             wx.ITEM_NORMAL)
        self.toolmenu.Append(ID_BUILD_SUPER,
                             "Build Supercell",
                             "Build a supercell of an existing crystal",
                             wx.ITEM_NORMAL)
        self.toolmenu.Append(ID_BUILD_SLAB,
                             "Build Slab",
                             "Build a slab from an existing crystal",
                             wx.ITEM_NORMAL)
        self.toolmenu.Append(ID_ADD_UC,
                             "Add Unit Cell",
                             "Add a unit cell to a molecule",
                             wx.ITEM_NORMAL)
        self.toolmenu.Append(ID_BUILD_NANO,
                             "Build Nanotube",
                             "Build an arbitrary single-walled nanotube",
                             wx.ITEM_NORMAL)
        self.toolmenu.Append(ID_BUILD_ALKA,
                             "Build Alkane",
                             "Build a alkane of arbitrary length",
                             wx.ITEM_NORMAL)
        #self.toolmenu.Append(ID_ZBUILD,
        #                     "Zmatrix Builder",
        #                     "Build a system using zmatrix coordinates",
        #                     wx.ITEM_NORMAL)
        self.toolmenu.AppendSeparator()
        self.toolmenu.Append(ID_SKETCH,
                             "Sketcher",
                             "Draw a molecule with the sketcher",
                             wx.ITEM_NORMAL)
        #self.toolmenu.Append(ID_CLEAN,
        #                     "Cleaner",
        #                     "Clean the current structure using UFF",
        #                     wx.ITEM_NORMAL)

        self.menubar.Append(self.toolmenu, "&Tools")
        
        wx.EVT_MENU(self, ID_VIEW_ORBS, self.view_orbs)
        wx.EVT_MENU(self, ID_ADJUST_BONDS, self.adjust_bonds)
        wx.EVT_MENU(self, self.ID_MEASURE, self.measurements)
        wx.EVT_MENU(self,ID_BUILD_XTAL, self.build_xtal)
        wx.EVT_MENU(self,ID_XTAL_DB, self.xtal_db)
        wx.EVT_MENU(self,ID_BUILD_SUPER, self.build_super)
        wx.EVT_MENU(self,ID_BUILD_SLAB, self.build_slab)
        wx.EVT_MENU(self,ID_ADD_UC, self.add_uc)
        wx.EVT_MENU(self,ID_BUILD_NANO, self.build_nano)
        wx.EVT_MENU(self,ID_BUILD_ALKA, self.build_alka)
        wx.EVT_MENU(self,ID_ZBUILD, self.zbuild)
        wx.EVT_MENU(self,ID_SKETCH, self.sketch)
        wx.EVT_MENU(self,ID_CLEAN, self.clean)
        return

    def make_appmenu(self):
        ID_APP_JAGUAR = wx.NewId()
        ID_APP_QUEST = wx.NewId()
        ID_APP_SOCORRO = wx.NewId()
        ID_APP_TOWHEE = wx.NewId()
        
        self.appmenu = wx.Menu()
        self.appmenu.Append(ID_APP_JAGUAR,
                            "Jaguar",
                            "Options for the Jaguar program",
                            wx.ITEM_NORMAL)
        self.appmenu.Append(ID_APP_QUEST,
                            "Quest",
                            "Options for the Quest program",
                            wx.ITEM_NORMAL)
        self.appmenu.Append(ID_APP_SOCORRO,
                            "Socorro",
                            "Options for the Socorro program",
                            wx.ITEM_NORMAL)
        self.appmenu.Append(ID_APP_TOWHEE,
                            "Towhee",
                            "Options for the Towhee program",
                            wx.ITEM_NORMAL)
        self.menubar.Append(self.appmenu, "&Applications")

        wx.EVT_MENU(self, ID_APP_QUEST, self.Quest)
        wx.EVT_MENU(self, ID_APP_TOWHEE, self.Towhee)
        return

    def make_helpmenu(self):
#        ID_HELP = wx.NewId()
#        ID_LICENSE = wx.NewId()
        
        self.helpmenu = wx.Menu()
        self.helpmenu.Append(wx.ID_ABOUT,
                             "About",
                             "",
                             wx.ITEM_NORMAL)
#        self.helpmenu.Append(ID_HELP,
#                             "Help",
#                             "vimm Helpfile",
#                             wx.ITEM_NORMAL)
#        self.helpmenu.Append(ID_LICENSE,
#                             "License",
#                             "vimm licensing information",
#                             wx.ITEM_NORMAL)
        self.menubar.Append(self.helpmenu, "&Help")

        wx.EVT_MENU(self,wx.ID_ABOUT,self.about)
        #wx.EVT_MENU(self,ID_LICENSE,self.license)
        return

    def do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.canvas, 1, wx.EXPAND, 0)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()
        self.canvas.SetSize((401,401))
        return

    def about(self,*args):
        d = wx.MessageDialog(self,
                             "VIMM\n"
                             "Visual Interface for Materials Manipulation\n",
                             "About VIMM",
                             wx.OK|wx.ICON_INFORMATION)
        d.ShowModal()
        d.Destroy()
        
#    def license(self,*args):
#        d = wx.MessageDialog(self,
#                            "vimm: Visual Interface for Materials Manipulation\n"
#                            "\n"
#                            "Copyright 2010 Caltech.  Copyright 2005 Sandia Corporation.  Under the terms of Contract"
#                            " DE-AC04-94AL85000 with Sandia Corporation, the U.S. Governmenn"
#                            " retains certain rights in this sofware.\n"
#                            "\n"
#                            "This program is free software; you can redistribute it and/or modify"
#                            " it under the terms of the GNU General Public License as published by"
#                            " the Free Software Foundation; either version 2 of the License, or"
#                            " (at your option) any later version.\n"
#                            "\n"
#                            "This program is distributed in the hope that it will be useful,"
#                            " but WITHOUT ANY WARRANTY; without even the implied warranty of"
#                            " MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
#                            " GNU General Public License for more details.\n"
#                            "\n"
#                            "You should have received a copy of the GNU General Public License"
#                            " along with this program; if not, write to the Free Software"
#                            " Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307"
#                            " USA\n",
#                            "vimm License",
#                            wx.OK|wx.ICON_INFORMATION)
#        d.ShowModal()
#        d.Destroy()

    def set_properties(self, title='VIMM', height=400, width=400):
        self.SetTitle(title)
        self.canvas.SetSize((height, width))
        self.statusbar.SetStatusWidths([-1])
        return

#    def Close(self, force):
#        wx.Frame.Close(self, force)
        
#    def Destroy(self):
#        print self.canvas.camera.get_position()
#        wx.Frame.Destroy()

    def dotest(self):
        from Atom import Atom
        from Bond import Bond
        from Cell import Cell
        from NumWrap import array

        pt1 = array((0.,0.,0.))
        pt2 = array((0.5,0.5,0.5))

        atom1 = Atom(8,pt1)
        atom2 = Atom(7,pt2)
        self.material.add_atom(atom1)
        self.material.add_atom(atom2)
        self.material.add_bond(Bond(atom1,atom2))
        self.material.set_cell(Cell(array((1.,0.,0.)),
                                    array((0.,1.,0.)),
                                    array((0.,0.,1.))))
        #the following tests the surface rendering
        self.material.geo.surface.append(((1.,0.,0.),(1.,1.,1.),(0.,0.,0.)))
        return

    def quit(self,*args):
        self.Close(True)

    def addshapes(self,shapes): self.canvas.addshapes(shapes)

    def newshapes(self,shapes,repos_camera=0):
        self.canvas.newshapes(shapes,repos_camera)

    def dump(self,*args): self.canvas.dump()

    def set_bg_color(self,*args):
        d = wx.ColourDialog(self)
        d.GetColourData().SetChooseFull(True)
        if d.ShowModal() == wx.ID_OK:
            data = d.GetColourData()
            r,g,b = data.GetColour().Get()
            color = r/255.,g/255.,b/255.
            self.canvas.OnColor(color)
            fg_r=255-r
            fg_g=255-g
            fg_b=255-b
            fg_color=fg_r/255.,fg_g/255.,fg_b/255.
            self.renderOptions.set_fg_color(fg_color)
            self.render()
        return

    def new_file(self,*args):
        file_types = ['Towhee File', 'Xmol XYZ']
        d = wx.SingleChoiceDialog(self, "Choose file type",
            "Choose file type",
            file_types,
            wx.OK|wx.CANCEL)
        if d.ShowModal() == wx.ID_OK:
            ft = d.GetStringSelection()
            if ft == "Xmol XYZ":
                self.create_xyz_file()
            elif ft == "Towhee File":
                self.create_towhee_file()
            
        return

    def load_file(self,*args):
        fname = None
        d = wx.FileDialog(self,"Open","","","*",wx.OPEN)
        if d.ShowModal() == wx.ID_OK:
            fname = d.GetFilename()
            dir = d.GetDirectory()
            fullfilename = os.path.join(dir,fname)
        d.Destroy()
        self.load_file_nodialog(fullfilename)
        return

    def load_file_nodialog(self,fname=None):
        if fname:
            from vimm.Material import Material
#            from matter.Structure import Structure
            if isinstance(fname, Material):
                self.material = fname
#            elif isinstance(fname, Structure):
#                self.material = vimmLib.loadStructure(fname)
            else:
                #self.setPlottingObject(vimmLib.load_file(fname, "GUI"))
                self.material = vimmLib.load_file(fname, "GUI")
            if self.material:# or self.surface:
                self.SetTitle("Vimm: %s" % self.material.name)
                self.render(1)
        return

#    def setPlottingObject(self, object):
#        from vimm.Material import Material
#        from vimm.Shapes import Triangles
#        if isinstance(object, Material):
#            self.material = object
#        #elif isinstance(object, Surface):
#        elif isinstance(object, Triangles):
#            self.surface = object

#    def load_material_from_file(self,fullfilename):
#        loader = None
#        dir,fname = os.path.split(fullfilename)
#        name,ext = os.path.splitext(fname)
#        ext = ext.replace('.','')
#        if self.loaders.has_key(ext):
#            loaders = self.loaders[ext]
#            load_strings = FileIO.typestrings(loaders)
#            if len(loaders) > 1:
#                d = wx.SingleChoiceDialog(self, "Choose loader",
#                    "Choose loader",
#                    load_strings,
#                    wx.OK|wx.CANCEL)
#                if d.ShowModal() == wx.ID_OK:
#                    lstr = d.GetStringSelection()
#                    i = load_strings.index(lstr)
#                    loader = loaders[i]
#                d.Destroy()
#            else:
#                loader = loaders[0]
#        else:
#            print "No file loader known for extension ",ext
#        if loader:
#            self.material = loader(fullfilename)
#            self.SetTitle("vimm: %s" % self.material.name)
#            self.render(1)
#        return

    def save_as(self,*args):
        fname = None
        d = wx.FileDialog(self,"Save","","","*",wx.SAVE)
        if d.ShowModal() == wx.ID_OK:
            fname = d.GetFilename()
            dir = d.GetDirectory()
            fullfilename = os.path.join(dir,fname)
        d.Destroy()
        if fname:
            vimmLib.save_file(fullfilename, self.material, "GUI")
        return

#    def save_material_to_file(self,fullfilename):
#        saver = None
#        dir,fname = os.path.split(fullfilename)
#        name,ext = os.path.splitext(fname)
#        ext = ext.replace('.','')
#        if self.savers.has_key(ext):
#            savers = self.savers[ext]
#            save_strings = FileIO.typestrings(savers)
#            if len(savers) > 1:
#                d = wx.SingleChoiceDialog(self, "Choose saver",
#                                          "Choose saver",
#                                          save_strings,
#                                          wx.OK|wx.CANCEL)
#                if d.ShowModal() == wx.ID_OK:
#                    lstr = d.GetStringSelection()
#                    i = load_strings.index(lstr)
#                    saver = savers[i]
#                d.Destroy()
#            else:
#                saver = savers[0]
#        else:
#            print "No file saver known for extension ",ext
#        if saver:
#            self.material = saver(fullfilename,self.material)
#        return
        
    def render(self,repos_camera=0):
        if self.material:
            shapes = SimpleRenderer(self.material.geo, self.renderOptions)
            self.newshapes(shapes,repos_camera)
        return

    def render_povray(self,*args):
        povOutput = None
        d = wx.FileDialog(self,"Save","","","*",wx.SAVE)
        if d.ShowModal() == wx.ID_OK:
            povOutput = d.GetFilename()
            dir = d.GetDirectory()
            fullfilename = os.path.join(dir,povOutput)
        d.Destroy()
        if fullfilename:
            # Still to do:
            # - Background color
            # - Is the camera position reversed?
            from POVRay import Scene
            if self.material:
                shapes = SimpleRenderer(self.material.geo,self.renderOptions)
                shapes = shapes.povray()
                r,g,b = self.renderOptions.get_fg_color()
                scene = Scene(self.material.name)
                #scene.set_bgcolor(r/255.,g/255.,b/255.)
                x,y,z = self.canvas.camera.get_position()
                lx,ly,lz = self.canvas.camera.get_look_at()
                scene.set_camera((-x,y,-z),
                                 (lx,ly,lz))
                for shape in shapes:
                    scene.add(shape)
                scene.write_pov(outputFile = fullfilename)
                scene.render(outputFile = fullfilename)
                scene.display()
        return
                          
    def set_render_lines(self, *args):
        self.renderOptions.set_mode(LINES)
        self.render()
        return

    def set_render_ballstick(self, *args):
        self.renderOptions.set_mode(BALLSTICK)
        self.render()
        return

    def set_render_balls(self, *args):
        self.renderOptions.set_mode(BALLS)
        self.render()
        return

    def set_render_cylinders(self, *args):
        self.renderOptions.set_mode(CYLINDERS)
        self.render()
        return

    def set_unit_cell(self, *args):
        self.renderOptions.show_unit_cells(self.viewmenu.IsChecked(self.ID_UNIT_CELL))
        self.render()
        return
        
    def set_cell_labels(self, *args):
        self.renderOptions.show_cell_labels(self.viewmenu.IsChecked(self.ID_CELL_LABELS))
        self.render()
        return
        
    def set_atom_labels(self, *args):
        self.renderOptions.show_atom_labels(self.viewmenu.IsChecked(self.ID_ATOM_LABELS))
        self.render()
        return
        
    def set_hide_h(self, *args):
        self.renderOptions.hide_hydrogens(self.viewmenu.IsChecked(self.ID_HIDE_H))
        self.render()
        return

    def measurements(self, *args):
        self.canvas.set_measure(True)
        self.measurement_window = Measurements(self, -1)
        self.measurement_window.Show()
        return

    def clean(self, *args):
        self.cleaner_window = Cleaner(self,-1)
        self.cleaner_window.Show()
        return

    def animate(self, *args):
        animate_frame = Animation(self, -1)
        animate_frame.Show()
        return

    def advance_frame(self,*args):
        if self.material:
            self.material.advance_frame()
            self.render()
        return

    def create_xyz_file(self):
        import IO.XYZ
        func = getattr(IO.XYZ, 'new')
        self.material = func()
        self.canvas.camera.set_position((0.0, 0.0, 20.0))
        self.canvas.camera.set_look_at((0.0, 0.0, 0.0))
        self.canvas.camera.set_up((0.0, 1.0, 0.0))
        self.canvas.setup_calllist()
        #self.canvas.render()
        #self.dotest()
        self.render()
        return

    def sketch(self, *args):
        self.canvas.set_sketching(True)
        self.sketcher_window = Sketcher(self, -1)
        self.sketcher_window.Show()
        return

    def edit_coord(self, *args):
        coord_editor = CoordEditor(self, -1)
        coord_editor.Show()
        return

    def edit_cart(self, *args):
        cartesian_frame = Cartesians(self, -1, self.material, self.canvas, self.renderOptions)
        cartesian_frame.Show()
        return

    def build_xtal(self, *args):
        xtlb = CrystalBuilder(self,-1)
        xtlb.ShowModal()
        return

    def xtal_db(self, *args):
        xtlb = CrystalDatabase(self,-1)
        xtlb.ShowModal()
        return

    def build_super(self, *args):
        xtlb = Supercell(self,-1)
        xtlb.ShowModal()
        return

    def build_slab(self, *args):
        xtlb = SlabBuilder(self,-1)
        xtlb.ShowModal()
        return

    def add_uc(self, *args):
        xtlb = AddUC(self,-1)
        xtlb.ShowModal()
        return

    def build_nano(self, *args):
        nanob = NanoBuilder(self,-1)
        nanob.ShowModal()
        return

    def build_alka(self, *args):
        alkab = AlkaneBuilder(self,-1)
        alkab.ShowModal()
        return

    def zbuild(self,*args):
        zbuilder = ZBuilder(self,-1)
        zbuilder.Show()
        return

    def adjust_bonds(self, *args):
        bondd = BondAdjustor(self,-1)
        bondd.ShowModal()
        return

    def view_orbs(self, *args):
        if hasattr(self.material.geo, 'orbs'):
            ov = OrbitalViewer(self,-1)
            ov.Show()
        else:
            d = wx.MessageDialog(self,
                "Orbitals do not exist in this file",
                "Cannot View Orbitals",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
        return

# these should be moved

    def Quest(self, *args):
        qopts = QuestOptions(self,-1,self.material)
        qopts.Show()
        return

    def Towhee(self, *args):
        if hasattr(self.material, 'towhee_options'):
            from TowheeEditor import TowheeEditor
            te = TowheeEditor(self, -1, "Towhee Editor", self.material.towhee_options)
            te.Show()
        else:
            d = wx.MessageDialog(self,
                "Can't open Towhee Editor unless it is a Towhee file",
                "Not a Towhee File",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
        return

    def create_towhee_file(self):
        import IO.Towhee
        func = getattr(IO.Towhee, 'new')
        self.material = func()
        self.render()
        return


