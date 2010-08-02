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

from vimm.NumWrap import array
from vimm.Utilities import entry_int
from vimm.Material import Material
from vimm.Atom import Atom

do_destroy = 1 # destroy Frame after build

# Parameters obtained by B3LYP/6-31G** calculations 
xh = 0.6
yh = 0.65
yh2 = 0.6
zh = 0.88
xc = 1.3
yc = 1.0

class AlkaneBuilder(wx.Dialog):
    def __init__(self, parent, id, **kwds):
        self.parent = parent
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Dialog.__init__(self, parent, id, 'Alkane Builder', **kwds)
        self.SetTitle("Alkane Builder")

        self.lblNunits = wx.StaticText(self, -1, "N Units")
        self.txtNunits = wx.TextCtrl(self, -1, "")
        self.btnBuildAlkane = wx.Button(self, -1, "Build")
        self.btnCancel = wx.Button(self, -1, "Cancel")
        self.btnBuildAlkane.SetDefault()

        szrAlkane = wx.BoxSizer(wx.VERTICAL)
        szrNunits = wx.BoxSizer(wx.HORIZONTAL)
        szrButton = wx.BoxSizer(wx.HORIZONTAL)
        szrNunits.Add(self.lblNunits, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
        szrNunits.Add(self.txtNunits, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
        szrButton.Add(self.btnBuildAlkane, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
        szrButton.Add(self.btnCancel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
        szrAlkane.Add(szrNunits, 1, wx.ALL, 10)
        szrAlkane.Add(szrButton, 1, wx.ALL, 10)

        self.SetAutoLayout(1)
        self.SetSizer(szrAlkane)
        szrAlkane.Fit(self)
        szrAlkane.SetSizeHints(self)

        wx.EVT_BUTTON(self, self.btnBuildAlkane.GetId(), self.do_build)
        wx.EVT_BUTTON(self, self.btnCancel.GetId(), self.cancel)
        return

    def cancel(self, *args):
        self.Destroy()
        return

    def do_build(self, *args):
        n = entry_int(self.txtNunits)

        self.parent.material = build_the_alkane(n)
        self.parent.render(1)
        
        if do_destroy: self.Destroy()
        return

def build_the_alkane(n):
    atoms = alkanebuilder(n)
    if not n: n=1
    nc=2*n+2
    nh = 2*nc+2
    material = Material("C%dH%d" % (nc,nh))
    for atno,xyz in atoms:
        material.add_atom(Atom(atno,xyz))
    material.bonds_from_distance()
    return material

def C(x,y,z): return (6,array((x,y,z)))
def H(x,y,z): return (1,array((x,y,z)))
def methyl_start(x):
    return [C(x,0,0),H(x-xh,yh2,0),H(x,-yh,zh),H(x,-yh,-zh)]

def methyl_end(x):
    return [C(x,yc,0),H(x+xh,yc-yh2,0),H(x,yc+yh,zh),H(x,yc+yh,-zh)]

def ethyl(x):
    return [C(x,yc,0),H(x,yc+yh,zh),H(x,yc+yh,-zh),
            C(x+xc,0,0),H(x+xc,-yh,zh),H(x+xc,-yh,-zh)]

def alkanebuilder(nunits):
    x0 = 0 # Starting point for insertion
    atoms = methyl_start(x0)
    x0 = x0 + xc
    for i in range(nunits):
        atoms.extend(ethyl(x0))
        x0 = x0 + 2*xc
    atoms.extend(methyl_end(x0))
    return atoms


if __name__ == '__main__':
    print alkanebuilder(3)
