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


import wx
from vimm.Utilities import entry_float

class BondAdjustor(wx.Dialog):
    def __init__(self, parent,id,title="Adjust Bonds", **kwds):
        self.parent = parent
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Dialog.__init__(self, parent, id, title, **kwds)
        self.lblScale = wx.StaticText(self, -1, "Scale", size=(40,-1))
        self.txtScale = wx.TextCtrl(self, -1, "")
        self.lblScope = wx.StaticText(self, -1, "Scope", size=(40,-1))
        self.chkScope = wx.CheckBox(self, -1, "All Geos")
        self.btnAddBonds = wx.Button(self, -1, "Add Bonds")
        self.btnCancel = wx.Button(self, -1, "Close")
        self.btnDeleteBonds = wx.Button(self, -1, "Delete All")

        wx.EVT_BUTTON(self, self.btnDeleteBonds.GetId(), self.delete_bonds)
        wx.EVT_BUTTON(self, self.btnAddBonds.GetId(), self.add_bonds)
        wx.EVT_BUTTON(self, self.btnCancel.GetId(), self.cancel)

        self.SetTitle("Adjust Bonds")
        self.btnAddBonds.SetDefault()
        self.__do_layout()
        return

    def __do_layout(self):
        szrBondAdjustor = wx.BoxSizer(wx.VERTICAL)
        szrScale = wx.BoxSizer(wx.HORIZONTAL)
        szrScope = wx.BoxSizer(wx.HORIZONTAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)

        szrScale.Add(self.lblScale, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrScale.Add(self.txtScale, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrScope.Add(self.lblScope, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrScope.Add(self.chkScope, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrButtons.Add(self.btnAddBonds, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnDeleteBonds, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrBondAdjustor.Add(szrScale, 0, 0, 0)
        szrBondAdjustor.Add(szrScope, 0, 0, 0)
        szrBondAdjustor.Add(szrButtons, 0, wx.EXPAND, 0)

        self.SetAutoLayout(1)
        self.SetSizer(szrBondAdjustor)
        szrBondAdjustor.Fit(self)
        szrBondAdjustor.SetSizeHints(self)
        return

    def delete_bonds(self,*args):
        material = self.parent.material
        if self.chkScope.IsChecked():
            scope = True
        else:
            scope = False
        self.parent.material = delete_the_bonds(material, scope)
        self.parent.render(1)
        return

    def add_bonds(self,*args):
        material = self.parent.material
        scopeval = entry_float(self.txtScale,1.2)
        if self.chkScope.IsChecked():
            scope = True
        else:
            scope = False

        self.parent.material = add_the_bonds(material, scope, scopeval)
        self.parent.render(1)
        return

    def cancel(self,*args):
        self.Destroy()
        return
# end of class BondAdjustor

def delete_the_bonds(material, scope):
    if scope:
        material.delete_all_bonds()
    else:
        material.delete_current_bonds()
    return material

def add_the_bonds(material, scope, scopeval):
    if scope:
        material.bonds_from_distance(scopeval,force_bonds=1)
    else:
        material.current_bonds_from_distance(scopeval,force_bonds=1)
    return material
