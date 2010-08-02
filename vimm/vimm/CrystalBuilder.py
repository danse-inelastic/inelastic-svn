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


#!/usr/bin/env python

import wx
from math import sqrt
from vimm.Material import Material
from vimm.Cell import Cell
from vimm.Atom import Atom
from vimm.Element import sym2no
from vimm.Utilities import entry_float, entry_string, entry_int, bbox_atoms
from vimm.NumWrap import array,dot

rt3 = sqrt(3.)

do_destroy = 1 # destroy Frame after build

class CrystalDatabase(wx.Dialog):
    def __init__(self, parent, id, title="Crystal Database", **kwds):
        self.parent = parent
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Dialog.__init__(self, parent,id, title, **kwds)

        self.make_widgets()
        return

    def make_widgets(self):
        self.lblSpecies = wx.StaticText(self, -1, "Species")
        self.cboSpecies = wx.ComboBox(self, -1,
                                      choices=[
            "He", "Li", "Be", "Diamond", "Graphite", "Ne", "Na", "Mg","Al", 
            "Si", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Fe", "Co", "Ni", "Cu",
            "Zn", "Ge", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh",
            "Pd", "Ag", "Cd", "Xe", "Cs", "Ba", "Ce", "Eu", "Gd", "Tb", "Dy", "Ho",
            "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au",
            "Tl", "Pb", "Po", "Ac", "Th", "LiH","MgO", "MnO", "NaCl", "AgBr", "PbS",
            "KCl", "KBr", "BeCu", "AlNi", "CuZn", "CuPd", "AgMg", "LiHg", "TlBr",
            "CsCl", "TlI", "CuF", "SiC", "CuCl", "ZnS", "AlP", "GaP"],
                                      style=wx.CB_DROPDOWN)
        self.btnBuildDB = wx.Button(self, -1, "Build")
        self.btnBuildDB.SetDefault()
        self.btnCancel = wx.Button(self, -1, "Cancel")

        szrDatabase = wx.BoxSizer(wx.VERTICAL)
        szrSpecies = wx.BoxSizer(wx.HORIZONTAL)
        szrSpecies.Add(self.lblSpecies, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrSpecies.Add(self.cboSpecies, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        szrButton = wx.BoxSizer(wx.HORIZONTAL)
        szrButton.Add(self.btnBuildDB, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrButton.Add(self.btnCancel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        szrDatabase.Add(szrSpecies, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        szrDatabase.Add(szrButton, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.SetAutoLayout(1)
        self.SetSizer(szrDatabase)
        szrDatabase.Fit(self)
        szrDatabase.SetSizeHints(self)
        self.cboSpecies.SetSelection(0)

        wx.EVT_BUTTON(self, self.btnBuildDB.GetId(), self.do_db_build)
        wx.EVT_BUTTON(self, self.btnCancel.GetId(), self.cancel)
        return

    def do_db_build(self,*args):
        crystal_type = self.cboSpecies.GetStringSelection()
        self.parent.material = build_the_crystal_from_db(crystal_type)
        self.parent.render(1)
        if do_destroy: self.Destroy()
        return

    def cancel(self, *args):
        self.Destroy()
        return

class Supercell(wx.Dialog):
    def __init__(self, parent, id, title="Supercell Builder", **kwds):
        self.parent = parent
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Dialog.__init__(self, parent, id, title, **kwds)

        self.make_widgets()
        return

    def make_widgets(self):
        self.lblSCdim = wx.StaticText(self, -1, "Dimensions")
        self.txtSCaentry = wx.TextCtrl(self, -1, "")
        self.txtSCbentry = wx.TextCtrl(self, -1, "")
        self.txtSCcentry = wx.TextCtrl(self, -1, "")
        self.btnCancel = wx.Button(self, -1, "Cancel")
        self.btnBuild = wx.Button(self, -1, "Build")
        self.btnBuild.SetDefault()
        
        szrSupercell = wx.BoxSizer(wx.VERTICAL)
        szrDimensions = wx.BoxSizer(wx.HORIZONTAL)
        szrButton = wx.BoxSizer(wx.HORIZONTAL)

        szrDimensions.Add(self.lblSCdim, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrDimensions.Add(self.txtSCaentry, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrDimensions.Add(self.txtSCbentry, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrDimensions.Add(self.txtSCcentry, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrButton.Add(self.btnBuild, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrButton.Add(self.btnCancel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrSupercell.Add(szrDimensions, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        szrSupercell.Add(szrButton, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.SetAutoLayout(1)
        self.SetSizer(szrSupercell)
        szrSupercell.Fit(self)
        szrSupercell.SetSizeHints(self)
        wx.EVT_BUTTON(self, self.btnBuild.GetId(), self.do_sc_build)
        wx.EVT_BUTTON(self, self.btnCancel.GetId(), self.cancel)
        return

    def do_sc_build(self,*args):
        material = self.parent.material

        ass = entry_int(self.txtSCaentry,1)
        bss = entry_int(self.txtSCbentry,1)
        css = entry_int(self.txtSCcentry,1)

        self.parent.material = build_the_supercell(material, ass, bss, css)
        self.parent.render(1)
        if do_destroy: self.Destroy()
        return

    def cancel(self, *args):
        self.Destroy()
        return

class SlabBuilder(wx.Dialog):
    def __init__(self, parent, id, title="Slab Builder", **kwds):
        self.parent = parent
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Dialog.__init__(self, parent, id, title, **kwds)

        self.make_widgets()
        return

    def make_widgets(self):
        self.lblCleavage = wx.StaticText(self, -1, "Cleavage Direction", size=(110,-1))
        self.cboCleavage = wx.ComboBox(self, -1,
                                       choices=["C", "B", "A"],
                                       style=wx.CB_DROPDOWN)
        self.lblSlabDepth = wx.StaticText(self, -1, "Slab Depth", size=(110,-1))
        self.txtSlabDepth = wx.TextCtrl(self, -1, "")
        self.lblVacuum = wx.StaticText(self, -1, "Vacuum Amount", size=(110,-1))
        self.txtVacuum = wx.TextCtrl(self, -1, "")

        self.btnCancel = wx.Button(self, -1, "Cancel")
        self.btnBuildSlab = wx.Button(self, -1, "Build")
        self.btnBuildSlab.SetDefault()

        szrSlab = wx.BoxSizer(wx.VERTICAL)
        szrCleavage = wx.BoxSizer(wx.HORIZONTAL)
        szrSlabDepth = wx.BoxSizer(wx.HORIZONTAL)
        szrVacuum = wx.BoxSizer(wx.HORIZONTAL)
        szrButton = wx.BoxSizer(wx.HORIZONTAL)
        szrCleavage.Add(self.lblCleavage, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrCleavage.Add(self.cboCleavage, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrSlabDepth.Add(self.lblSlabDepth, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrSlabDepth.Add(self.txtSlabDepth, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrVacuum.Add(self.lblVacuum, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrVacuum.Add(self.txtVacuum, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrButton.Add(self.btnBuildSlab, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrButton.Add(self.btnCancel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrSlab.Add(szrCleavage, 0, 0, 0)
        szrSlab.Add(szrSlabDepth, 0, 0, 0)
        szrSlab.Add(szrVacuum, 0, 0, 0)
        szrSlab.Add(szrButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetAutoLayout(1)
        self.SetSizer(szrSlab)
        szrSlab.Fit(self)
        szrSlab.SetSizeHints(self)
        self.cboCleavage.SetSelection(0)
        wx.EVT_BUTTON(self, self.btnBuildSlab.GetId(), self.do_slab_build)
        wx.EVT_BUTTON(self, self.btnCancel.GetId(), self.cancel)
        return

    def cancel(self,*args):
        self.Destroy()
        return

    def do_slab_build(self,*args):
        material = self.parent.material
        cleave_dir = self.cboCleavage.GetStringSelection()
        depth = entry_int(self.txtSlabDepth,1)
        vacuum = entry_float(self.txtVacuum,0)
        
        self.parent.material = build_the_slab(material, cleave_dir, depth, vacuum)
        self.parent.render(1)
        if do_destroy: self.Destroy()
        return

class AddUC(wx.Dialog):
    def __init__(self, parent, id, title="Add Unit Cell", **kwds):
        self.parent = parent
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Dialog.__init__(self, parent,id, title, **kwds)

        self.make_widgets()
        return

    def make_widgets(self):
        self.lblBuffer = wx.StaticText(self, -1, "Buffer amount", size=(90,-1))
        self.txtBuffer = wx.TextCtrl(self, -1, "")
        self.lblUnitCell = wx.StaticText(self, -1, "Unit Cell", size=(90,-1))
        self.txtEntryA = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        self.txtEntryB = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        self.txtEntryC = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        self.btnComputeAddUC = wx.Button(self, -1, "Compute")
        self.btnBuildAddUC = wx.Button(self, -1, "Build")
        self.btnCancel = wx.Button(self, -1, "Cancel")
        szrAddUC = wx.BoxSizer(wx.VERTICAL)
        szrBuffer = wx.BoxSizer(wx.HORIZONTAL)
        szrUnitCell = wx.BoxSizer(wx.HORIZONTAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrBuffer.Add(self.lblBuffer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrBuffer.Add(self.txtBuffer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrUnitCell.Add(self.lblUnitCell, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrUnitCell.Add(self.txtEntryA, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrUnitCell.Add(self.txtEntryB, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrUnitCell.Add(self.txtEntryC, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrButtons.Add(self.btnComputeAddUC, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrButtons.Add(self.btnBuildAddUC, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrButtons.Add(self.btnCancel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        szrAddUC.Add(szrBuffer, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        szrAddUC.Add(szrUnitCell, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        szrAddUC.Add(szrButtons, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 0)

        wx.EVT_BUTTON(self, self.btnComputeAddUC.GetId(), self.do_adduc_compute)
        wx.EVT_BUTTON(self, self.btnBuildAddUC.GetId(), self.do_adduc_build)
        wx.EVT_BUTTON(self, self.btnCancel.GetId(), self.cancel)

        self.SetAutoLayout(1)
        self.SetSizer(szrAddUC)
        szrAddUC.Fit(self)
        szrAddUC.SetSizeHints(self)
        return
        
    def do_adduc_compute(self,*args):
        material = self.parent.material
        buffer = entry_float(self.txtBuffer)
        
        unit_cell_data = compute_the_unit_cell(material, buffer)
        self.txtBuffer.SetValue(str(unit_cell_data[0]))
        self.txtEntryA.SetValue(str(unit_cell_data[1]))
        self.txtEntryB.SetValue(str(unit_cell_data[2]))
        self.txtEntryC.SetValue(str(unit_cell_data[3]))
        return

    def do_adduc_build(self,*args):
        material = self.parent.material
        buffer = entry_float(self.txtBuffer)
        
        self.parent.material = add_the_unit_cell(material, buffer)
        self.parent.render(1)
        if do_destroy: self.Destroy()
        return

    def cancel(self, *args):
        self.Destroy()
        return

class CrystalBuilder(wx.Dialog):
    def __init__(self, parent, id, title="Crystal Builder", **kwds):
        self.parent = parent
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Dialog.__init__(self, parent,id, title, **kwds)

        self.make_widgets()
        return

    def make_widgets(self):
        self.lblLattice = wx.StaticText(self, -1, "Lattice", size=(80,-1))
        self.cboUCtype = wx.ComboBox(self, -1,
                                      choices=["SC", "FCC", "BCC", "HCP",
                                               "Diamond", "bTin", "Graphite",
                                               "Hexag", "NaCl", "CsCl", "Cubic ZnS",
                                               "Hex Zns"],
                                      style=wx.CB_DROPDOWN)
        
        self.lblAtomtype = wx.StaticText(self, -1, "Atom Types", size=(80,-1))
        self.txtAtomType1 = wx.TextCtrl(self, -1, "")
        self.txtAtomType2 = wx.TextCtrl(self, -1, "")
        
        self.lblACA = wx.StaticText(self, -1, "A, C/A", size=(80,-1))
        self.txtAentry = wx.TextCtrl(self, -1, "")
        self.txtCAentry = wx.TextCtrl(self, -1, "")

        self.btnCancel = wx.Button(self, -1, "Cancel")
        self.btnBuild = wx.Button(self, -1, "Build")
        self.btnBuild.SetDefault()

        szrCrystalBuilder = wx.BoxSizer(wx.VERTICAL)
        szrLattice = wx.BoxSizer(wx.HORIZONTAL)
        szrAtomTypes = wx.BoxSizer(wx.HORIZONTAL)
        szrACA = wx.BoxSizer(wx.HORIZONTAL)
        szrButton = wx.BoxSizer(wx.HORIZONTAL)
        szrLattice.Add(self.lblLattice, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrLattice.Add(self.cboUCtype, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrAtomTypes.Add(self.lblAtomtype, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrAtomTypes.Add(self.txtAtomType1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrAtomTypes.Add(self.txtAtomType2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrACA.Add(self.lblACA, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrACA.Add(self.txtAentry, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrACA.Add(self.txtCAentry, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrButton.Add(self.btnBuild, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrButton.Add(self.btnCancel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrCrystalBuilder.Add(szrLattice, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0)
        szrCrystalBuilder.Add(szrAtomTypes, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0)
        szrCrystalBuilder.Add(szrACA, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0)
        szrCrystalBuilder.Add(szrButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(szrCrystalBuilder)
        szrCrystalBuilder.Fit(self)
        szrCrystalBuilder.SetSizeHints(self)
        self.cboUCtype.SetSelection(0)
        wx.EVT_BUTTON(self, self.btnBuild.GetId(), self.do_build)
        wx.EVT_BUTTON(self, self.btnCancel.GetId(), self.cancel)
        return

    def do_build(self, *args):
        crystal_type = self.cboUCtype.GetStringSelection()
        sym1 = entry_string(self.txtAtomType1)
        sym2 = entry_string(self.txtAtomType2)
        a = entry_float(self.txtAentry)
        c_a = entry_float(self.txtCAentry)
        self.parent.material = build_the_crystal(crystal_type,sym1,sym2,a,c_a)
        self.parent.render(1)
        if do_destroy: self.Destroy()

    def cancel(self, *args):
        self.Destroy()
        return

def build_the_crystal(crystal_type, sym1, sym2, a, c_a):
    uc,atoms = builders[crystal_type](a,c_a,sym1,sym2)
    material = Material(crystal_type.replace(' ','_'))
    for sym,(x,y,z) in atoms:
        atno = sym2no[sym]
        material.add_atom(Atom(atno,array((x,y,z))))
    cell = Cell(uc[0],uc[1],uc[2])
    material.set_cell(cell)
    material.bonds_from_distance()
    return material

def build_the_crystal_from_db(crystal_type):
    uc,atoms = crystal_type_dict[crystal_type]
    material = Material(crystal_type.replace(' ','_'))
    for sym,(x,y,z) in atoms:
        atno = sym2no[sym]
        material.add_atom(Atom(atno,array((x,y,z)),sym))
    cell = Cell(uc[0],uc[1],uc[2])
    material.set_cell(cell)
    material.bonds_from_distance()
    return material

def compute_the_unit_cell(material, buffer):
    name = material.get_name()
    cell = material.get_cell()
    atoms = material.get_atom_list()

    if cell: return None # Don't do anything for now
    if not buffer: buffer = 2. # Can still set to a small value like 0.01

    xmin,xmax,ymin,ymax,zmin,zmax = bbox_atoms(atoms,buffer)
    return (buffer, xmax-xmin, ymax-ymin, zmax-zmin)

def add_the_unit_cell(material, buffer):
    name = material.get_name()
    cell = material.get_cell()
    atoms = material.get_atom_list()

    if cell: return material # Don't do anything for now

    newname = "%s_cell" % name
    newmaterial = Material(newname)

    if not buffer: buffer = 2. # Can still set to a small value like 0.01
    xmin,xmax,ymin,ymax,zmin,zmax = bbox_atoms(atoms,buffer)

    for atom in atoms:
        atno = atom.get_atno()
        xyz = atom.get_position()
        xyznew = array((xyz[0]-xmin,xyz[1]-ymin,xyz[2]-zmin))
        newmaterial.add_atom(Atom(atno,xyznew))

    newmaterial.set_cell(Cell((xmax-xmin,0,0),
                              (0,ymax-ymin,0),
                              (0,0,zmax-zmin)))

    opts = getattr(material,"seqquest_options",{})
    if opts: newmaterial.seqquest_options = opts.copy()
    
    opts = getattr(material,"socorro_options",{})
    if opts: newmaterial.socorro_options = opts.copy()
    
    newmaterial.bonds_from_distance()
    return newmaterial

def build_the_supercell(material, ass, bss, css):
    if ass == 1 and bss == 1 and css == 1:
        return material

    name = material.get_name()
    cell = material.get_cell()
    atomlist = material.get_atom_list()

    axyz = cell.axyz
    bxyz = cell.bxyz
    cxyz = cell.cxyz


    newname = "%s%d%d%d" % (name,ass,bss,css)
    newmaterial = Material(newname)
    naxyz = ass*axyz
    nbxyz = bss*bxyz
    ncxyz = css*cxyz

    for atom in atomlist:
        atno = atom.get_atno()
        sym = atom.get_symbol()
        xyz = atom.get_position()
        for i in range(ass):
            for j in range(bss):
                for k in range(css):
                    xyznew = xyz + i*axyz + j*bxyz + k*cxyz
                    newmaterial.add_atom(Atom(atno,xyznew,sym))

    newmaterial.set_cell(Cell(naxyz,nbxyz,ncxyz))
    
    opts = getattr(material,"seqquest_options",{})
    if opts: newmaterial.seqquest_options = opts.copy()
    
    opts = getattr(material,"socorro_options",{})
    if opts: newmaterial.socorro_options = opts.copy()
    
    newmaterial.bonds_from_distance()
    return newmaterial

def build_the_slab(material, cleave_dir, depth, vacuum):
    name = material.get_name()
    cell = material.get_cell()
    atomlist = material.get_atom_list()
    if not cleave_dir: cleave_dir = 'C'

    axyz = cell.axyz
    bxyz = cell.bxyz
    cxyz = cell.cxyz

    if depth == 1 and vacuum == 0:
        return material# do nothing

    newname = "%s_slab" % name
    newmaterial = Material(newname)
    #
    # Replace abc -> uvw (w is the cleave direction) so we can
    # cleave in more general ways:
    #
    if cleave_dir == "C":
        uxyz = axyz
        vxyz = bxyz
        wxyz = cxyz
        idir = 2
    elif cleave_dir == "B":
        uxyz = cxyz
        vxyz = axyz
        wxyz = bxyz
        idir = 1
    elif cleave_dir == "A":
        uxyz = bxyz
        vxyz = cxyz
        wxyz = axyz
        idir = 0

    wlength = sqrt(dot(wxyz,wxyz))
    wscale = (wlength*depth+vacuum)/wlength
    nwxyz = wxyz*wscale

    for atom in atomlist:
        atno = atom.get_atno()
        xyz = atom.get_position()
        for k in range(depth):
            xyznew = xyz + k*wxyz
            xyznew[idir] += vacuum/2.
            newmaterial.add_atom(Atom(atno,xyznew))
        if abs(xyz[idir]) < 1e-2: # Periodic image of bottom:
            xyznew = xyz + depth*wxyz
            xyznew[idir] += vacuum/2.
            newmaterial.add_atom(Atom(atno,xyznew))

    # I can't tell whether I have to do the cyclic permutations here
    #  i.e. output w,u,v in some cases.
    newmaterial.set_cell(Cell(uxyz,vxyz,nwxyz))

    opts = getattr(material,"seqquest_options",{})
    if opts: newmaterial.seqquest_options = opts.copy()
    
    opts = getattr(material,"socorro_options",{})
    if opts: newmaterial.socorro_options = opts.copy()
    
    newmaterial.center()
    newmaterial.bonds_from_distance()
    return newmaterial

def sc_builder(a,c_a,sym1,sym2):
    fracs = [(sym1,(0,0,0))]
    uc = [(a,0,0),(0,a,0),(0,0,a)]
    return uc,frac2cart(fracs,uc)

def fcc_builder(a,c_a,sym1,sym2):
    fracs = [(sym1,(0,0,0)),(sym1,(0.5,0.5,0)),
             (sym1,(0.5,0,0.5)),(sym1,(0,0.5,0.5))]
    uc = [(a,0,0),(0,a,0),(0,0,a)]
    return uc,frac2cart(fracs,uc)

def bcc_builder(a,c_a,sym1,sym2):
    fracs = [(sym1,(0,0,0)),(sym1,(0.5,0.5,0.5))]
    uc = [(a,0,0),(0,a,0),(0,0,a)]
    return uc,frac2cart(fracs,uc)

def hcp_builder(a,c_a,sym1,sym2):
    fracs = [(sym1,(0,0,0)),(sym1,(1./3.,1./3.,0.5))]
    uc = [(a,0,0),
          (a/2,rt3*a/2,0),
          (0,0,c_a*a)]
    return uc,frac2cart(fracs,uc)

def diamond_builder(a,c_a,sym1,sym2):
    fracs = [(sym1,(0,0,0)),(sym1,(0.5,0.5,0)),
             (sym1,(0.5,0,0.5)),(sym1,(0,0.5,0.5)),
             (sym1,(0.25,0.25,0.25)),(sym1,(0.75,0.75,0.25)),
             (sym1,(0.75,0.25,0.75)),(sym1,(0.25,0.75,0.75))]
    uc = [(a,0,0),(0,a,0),(0,0,a)]
    return uc,frac2cart(fracs,uc)

def btin_builder(a,c_a,sym1,sym2):
    fracs = [(sym1,(-0.125,-0.375,0.25)),(sym1,(0.125,0.375,-0.25))]
    uc = [(a,0,0),(0,a,0),(0.5,0.5,c_a*a)]
    return uc,frac2cart(fracs,uc)

def graphite_builder(a,c_a,sym1,sym2):
    fracs=[(sym1,(0,0,0)),
           (sym1,(0,0,0.5)),
           (sym1,(1./3.,2./3.,0)),
           (sym1,(2./3.,1./3.,0.5))]
    uc = [(a/2,-rt3*a/2.,0),
          (a/2,rt3*a/2.,0),
          (0,0,a*c_a)]
    return uc,frac2cart(fracs,uc)

def hexagonal_builder(a,c_a,sym1,sym2):
    fracs = [(sym1,(0,0,0))]
    uc = [(a/2,-rt3*a/2,0),
          (a/2,rt3*a/2,0),
          (0,0,c_a*a)]
    return uc,frac2cart(fracs,uc)

def nacl_builder(a,c_a,sym1,sym2):
    uc = [(a,0,0),(0,a,0),(0,0,a)]
    fracs = [(sym1,(0,0,0)),(sym1,(0.5,0.5,0)),
             (sym1,(0.5,0,0.5)),(sym1,(0,0.5,0.5)),
             (sym2,(0.5,0.5,0.5)),(sym2,(0,0,0.5)),
             (sym2,(0,0.5,0)),(sym2,(0.5,0,0))]
    return uc,frac2cart(fracs,uc)

def cscl_builder(a,c_a,sym1,sym2):
    uc = [(a,0,0),(0,a,0),(0,0,a)]
    fracs = [(sym1,(0,0,0)),(sym2,(0.5,0.5,0.5))]
    return uc,frac2cart(fracs,uc)

def cubiczns_builder(a,c_a,sym1,sym2):
    uc = [(a,0,0),(0,a,0),(0,0,a)]
    fracs = [(sym1,(0,0,0)),(sym1,(0.5,0.5,0)),
             (sym1,(0.5,0,0.5)),(sym1,(0,0.5,0.5)),
             (sym2,(0.25,0.25,0.25)),(sym2,(0.75,0.75,0.25)),
             (sym2,(0.75,0.25,0.75)),(sym2,(0.25,0.75,0.75))]
    return uc,frac2cart(fracs,uc)

def hexzns_builder(a,c_a,sym1,sym2):
    raise "Not supported yet"
    return uc,frac2cart(fracs,uc)

def frac2cart(fracs,uc):
    (ax,ay,az),(bx,by,bz),(cx,cy,cz) = uc
    atoms = []
    for i in range(len(fracs)):
        sym,(fa,fb,fc) = fracs[i]
        x = fa*ax + fb*bx + fc*cx
        y = fa*ay + fb*by + fc*cy
        z = fa*az + fb*bz + fc*cz
        atoms.append((sym,(x,y,z)))
    return atoms

builders = {
    "SC" : sc_builder, "FCC" : fcc_builder , "BCC" : bcc_builder,
    "HCP" : hcp_builder, "Diamond" : diamond_builder,
    "bTin" : btin_builder, "Graphite" : graphite_builder,
    "Hex" : hexagonal_builder, "NaCl" : nacl_builder,
    "CsCl" : cscl_builder, "Cubic ZnS" : cubiczns_builder,
    "Hex ZnS" : hexzns_builder}

crystal_type_dict = {
    #el, builder(a,c_a,sym1,sym2)
    "He" : hcp_builder(3.57,1.633,"He",None),
    "Li" : bcc_builder(3.491,0,"Li",None),
    "Be" : hcp_builder(2.27,1.58,"Be",None),
    "Diamond" : diamond_builder(3.567,0,"C",None),
    "Graphite" : graphite_builder(0,0,"C",None),
    "Ne" : fcc_builder(4.46,0,"Ne",None),
    "Na" : bcc_builder(4.225,0,"Na",None),
    "Mg" : hcp_builder(3.21,1.623,"Mg",None),
    "Al" : fcc_builder(4.05,0,"Al",None),
    "Si" : diamond_builder(5.43,0,"Si",None),
    "Ar" : fcc_builder(5.31,0,"Ar",None),
    "K" : bcc_builder(5.225,0,"K",None),
    "Ca" : fcc_builder(5.58,0,"Ca",None),
    "Sc" : hcp_builder(3.31,1.592,"Sc",None),
    "Ti" : hcp_builder(2.95,1.586,"Ti",None),
    "V" : bcc_builder(3.03,0,"V",None),
    "Cr" : bcc_builder(2.88,0,"Cr",None),
    "Fe" : bcc_builder(2.87,0,"Fe",None),
    "Co" : hcp_builder(2.51,1.62,"Co",None),
    "Ni" : fcc_builder(3.52,0,"Ni",None),
    "Cu" : fcc_builder(3.61,0,"Cu",None),
    "Zn" : hcp_builder(2.66,1.86,"Zn",None),
    "Ge" : diamond_builder(5.658,0,"Ge",None),
    "Kr" : fcc_builder(5.64,0,"Kr",None),
    "Rb" : bcc_builder(5.585,0,"Rb",None),
    "Sr" : fcc_builder(6.08,0,"Sr",None),
    "Y"  : hcp_builder(3.65,1.57,"Y",None),
    "Zr" : hcp_builder(3.23,1.59,"Zr",None),
    "Nb" : bcc_builder(3.30,0,"Nb",None),
    "Mo" : bcc_builder(3.15,0,"Mo",None),
    "Tc" : hcp_builder(2.74,1.606,"Tc",None),
    "Ru" : hcp_builder(2.71,1.579,"Ru",None),
    "Rh" : fcc_builder(3.80,0,"Rh",None),
    "Pd" : fcc_builder(3.89,0,"Pd",None),
    "Ag" : fcc_builder(4.09,0,"Ag",None),
    "Cd" : hcp_builder(2.98,1.886,"Cd",None),
    "Xe" : fcc_builder(6.13,0,"Xe",None),
    "Cs" : bcc_builder(6.045,0,"Cs",None),
    "Ba" : bcc_builder(5.02,0,"Ba",None),
    "Ce" : fcc_builder(5.16,0,"Ce",None),
    "Eu" : bcc_builder(4.58,0,"Eu",None),
    "Gd" : hcp_builder(3.63,1.592,"Gd",None),
    "Tb" : hcp_builder(3.60,1.583,"Tb",None),
    "Dy" : hcp_builder(3.59,1.574,"Dy",None),
    "Ho" : hcp_builder(3.58,1.570,"Ho",None),
    "Er" : hcp_builder(3.56,1.570,"Er",None),
    "Tm" : hcp_builder(3.54,1.571,"Tm",None),
    "Yb" : fcc_builder(5.48,0,"Yb",None),
    "Lu" : hcp_builder(3.50,1.586,"Lu",None),
    "Hf" : hcp_builder(3.19,1.583,"Hf",None),
    "Ta" : bcc_builder(3.30,0,"Ta",None),
    "W"  : bcc_builder(3.16,0,"W",None),
    "Re" : hcp_builder(2.76,1.616,"Re",None),
    "Os" : hcp_builder(2.74,1.577,"Os",None),
    "Ir" : fcc_builder(3.84,0,"Ir",None),
    "Pt" : fcc_builder(3.92,0,"Pt",None),
    "Au" : fcc_builder(4.08,0,"Au",None),
    "Tl" : hcp_builder(3.46,1.595,"Tl",None),
    "Pb" : fcc_builder(4.95,0,"Pb",None),
    "Po" : sc_builder(3.34,0,"Po",None),
    "Ac" : fcc_builder(5.31,0,"Ac",None),
    "Th" : fcc_builder(5.08,0,"Th",None),
    "LiH" : nacl_builder(4.08,0,"Li","H"),
    "MgO" : nacl_builder(4.20,0,"Mg","O"),
    "MnO" : nacl_builder(4.43,0,"Mn","O"),
    "NaCl" : nacl_builder(5.63,0,"Na","Cl"),
    "AgBr" : nacl_builder(5.77,0,"Ag","Br"),
    "PbS" : nacl_builder(5.92,0,"Pb","S"),
    "KCl" : nacl_builder(6.29,0,"K","Cl"),
    "KBr" : nacl_builder(6.59,0,"K","Br"),
    "BeCu" : cscl_builder(2.70,0,"Be","Cu"),
    "AlNi" : cscl_builder(2.88,0,"Al","Ni"),
    "CuZn" : cscl_builder(2.94,0,"Cu","Zn"),
    "CuPd" : cscl_builder(2.99,0,"Cu","Pd"),
    "AgMg" : cscl_builder(3.28,0,"Ag","Mg"),
    "LiHg" : cscl_builder(3.29,0,"Li","Hg"),
    "TlBr" : cscl_builder(3.97,0,"Tl","Br"),
    "CsCl" : cscl_builder(4.11,0,"Cs","Cl"),
    "TlI" : cscl_builder(4.20,0,"Tl","I"),
    "CuF" : cubiczns_builder(4.26,0,"Cu","F"),
    "SiC" : cubiczns_builder(4.35,0,"Si","C"),
    "CuCl" : cubiczns_builder(5.41,0,"Cu","Cl"),
    "ZnS" : cubiczns_builder(5.41,0,"Zn","S"),
    "AlP" : cubiczns_builder(5.45,0,"Al","P"),
    "GaP" : cubiczns_builder(5.45,0,"Ga","P"),
    "ZnSe" : cubiczns_builder(5.65,0,"Zn","Se"),
    "GaAs" : cubiczns_builder(5.65,0,"Ga","As"),
    "AlAs" : cubiczns_builder(5.66,0,"Al","As"),
    "CdS" : cubiczns_builder(5.82,0,"Cd","S"),
    "InSb" : cubiczns_builder(6.46,0,"In","Sb"),
    "AgI" : cubiczns_builder(6.47,0,"Ag","I")
    }


