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
# Converted by R Muller from the code that Steve Lustig put into Towhee

import wx

from math import sqrt,atan,sin,cos,pi
from vimm.NumWrap import array
from vimm.Utilities import entry_int
from vimm.Material import Material
from vimm.Atom import Atom
from vimm.Cell import Cell

do_destroy = 1 # destroy Frame after build

class NanoBuilder(wx.Dialog):
    def __init__(self, parent, id, **kwds):
        self.parent = parent
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Dialog.__init__(self, parent, id, 'Build Nanotube',**kwds)

        self.make_widgets()
        self.Center()
        return

    def make_widgets(self):
        self.lblUnits = wx.StaticText(self, -1, "Units")
        self.txtUnits = wx.TextCtrl(self, -1, "")
        self.lblN = wx.StaticText(self, -1, "N")
        self.txtN = wx.TextCtrl(self, -1, "")
        self.lblM = wx.StaticText(self, -1, "M")
        self.txtM = wx.TextCtrl(self, -1, "")
        self.btnBuild = wx.Button(self, -1, "Build")
        self.btnCancel = wx.Button(self, -1, "Cancel")
        self.btnBuild.SetDefault()

        self.SetTitle("Build Nanotube")
        szrNano = wx.BoxSizer(wx.VERTICAL)
        szrButton = wx.BoxSizer(wx.HORIZONTAL)
        szrUnits = wx.BoxSizer(wx.HORIZONTAL)
        szrUnits.Add(self.lblUnits, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrUnits.Add(self.txtUnits, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrUnits.Add(self.lblN, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrUnits.Add(self.txtN, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrUnits.Add(self.lblM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrUnits.Add(self.txtM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrButton.Add(self.btnBuild, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        szrButton.Add(self.btnCancel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        szrNano.Add(szrUnits, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        szrNano.Add(szrButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
 
        wx.EVT_BUTTON(self, self.btnBuild.GetId(), self.do_build)
        wx.EVT_BUTTON(self, self.btnCancel.GetId(), self.cancel)

        self.SetAutoLayout(1)
        self.SetSizer(szrNano)
        szrNano.Fit(self)
        szrNano.SetSizeHints(self)
        return

    def cancel(self, *args):
        self.Destroy()
        return

    def do_build(self,*args):
        n = entry_int(self.txtN, 1)
        m = entry_int(self.txtM, 1)
        ncells = entry_int(self.txtUnits, 1)
        material = create_nanotube_material(n, m, ncells)
        self.update_parent(material)
        return

    def update_parent(self, material):
        self.parent.material = material
        self.parent.render(1)
        
        if do_destroy: self.Destroy()
        return

def create_nanotube_material(n, m, ncells):
    bondlength = 1.35 # Angstroms
    buffer = 2 # Angstroms to pack around nt in uc

    np,nq,ndr = gen11(n,m)

    rt3 = sqrt(3)

    a = rt3*bondlength
    r = a*sqrt(np*np+nq*nq+np*nq)
    c = a*sqrt(n*n+m*m+n*m)
    t = rt3*c/ndr
    rs = c/2/pi
    nn = 2*(n*n+m*m+n*m)/ndr # hexagons in unit cell N

    #print 'Nanotube unit cell length ',t
    #print 'Nanotube radius ',rs
    #print 'Nanotube unit cell atoms ',nn*2

    q1 = atan( (rt3*m)/(2*n+m) )    # Chiral angle for C_h
    q2 = atan( (rt3*nq)/(2*np+nq) ) # Chiral angle for R
    q3 = q1-q2                      # Angle btw C_h and R
    q4 = 2*pi/nn                    # Period of angle for A atom
    q5 = bondlength*cos(pi/6-q1)/c*2*pi
    #   diff of the angle btw A and B atoms
    h1 = abs(t)/abs(sin(q3))
    h2 = bondlength*sin(pi/6-q1) # dz btw A and B atoms

    xyz = []
    for i in range(nn):
        # A atom
        k = int(i*abs(r)/h1)
        x1 = rs*cos(i*q4)
        y1 = rs*sin(i*q4)
        z1 = (i*abs(r)-k*h1)*sin(q3)
        kk2 = abs(int(z1/t))+1

        # Insure A in unit cell
        if z1 > t-0.02: z1 -= t*kk2
        if z1 < -0.02: z1 += t*kk2

        xyz.append((x1,y1,z1))

        # B atom
        # Insure B in unit cell
        z3 = (i*abs(r)-k*h1)*sin(q3)-h2
        if z3 > -0.02 and z3 < t-0.02:
            x2 = rs*cos(i*q4+q5)
            y2 = rs*sin(i*q4+q5)
            z2 = (i*abs(r)-k*h1)*sin(q3)-h2
            xyz.append((x2,y2,z2))
        else:
            x2 = rs*cos(i*q4+q5)
            y2 = rs*sin(i*q4+q5)
            z2 = (i*abs(r)-(k+1)*h1)*sin(q3)-h2
            kk = abs(int(z2/t))+1
            if z2 > t-0.01: z2 -= t*kk
            if z2 < -0.01: z2 += t*kk
            xyz.append((x2,y2,z2))

    xyznew = []
    ii = 0
    dxy = rs+buffer
    for j in range(ncells):
        dz = j*t
        for i in range(2*nn):
            x,y,z = xyz[i]
            xyznew.append((x+dxy,y+dxy,z+dz))

    #for x,y,z in xyznew: print " C %10.4f %10.4f %10.4f" % (x,y,z)

    material = Material('nanotube%d%d%d' % (ncells,n,m))
    for xyz in xyznew:
        material.add_atom(Atom(6,array(xyz)))

    material.bonds_from_distance()
    material.set_cell(Cell((2*dxy,0,0),(0,2*dxy,0),(0,0,ncells*t)))
    return material

def gen11(n,m):
    nnp = [0]*100
    nnq = [0]*100

    nd = igcm(n,m)

    if (n-m)%(3*nd) == 0:
        ndr = 3*nd
    else:
        ndr = nd

    a = sqrt(3)*1.421

    l2 = n*n+m*m+n*m
    if l2 <= 0: raise 'l2 <= 0'
    l = int(sqrt(l2))

    dt = a*sqrt(l2)/pi

    nr = (2*m+n)/ndr
    ns = -(2*n+m)/ndr
    nt2 = 3*l2/ndr/ndr
    nt = int(sqrt(nt2))

    nn = 2*l2/ndr

    ichk = 0
    if nr == 0:
        n60 = 1
    else:
        n60 = nr

    for np in range(-abs(n60),abs(n60)+1):
        for nq in range(-abs(ns),abs(ns)+1):
            j2 = nr*nq - ns*np
            if j2 == 1:
                j1 = m*np - n*nq
                if j1 > 0 and j1 < nn:
                    nnp[ichk] = np
                    nnq[ichk] = nq
                    ichk += 1

    if ichk == 0: raise 'Not found p,q strange!!'

    if ichk > 2: raise 'More than 1 pair of p,q strange !!'

    return nnp[0],nnq[0],ndr

def igcm(ii,jj): # Greatest common devisor
    MAXIT=1000
    i = abs(ii)
    j = abs(jj)
    if j > i: i,j = j,i
    if j == 0: return i
    for k in range(MAXIT):
        ir = i%j
        if ir == 0: return j
        i,j = j,ir
    else:
        raise "igcm: Maximum iterations exceeded! %d %d" % (ii,jj)
    return None


if __name__ == '__main__':
    print igcm(1,10),igcm(2,20),igcm(412,770)
