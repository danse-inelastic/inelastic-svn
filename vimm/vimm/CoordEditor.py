#!/usr/bin/env python

import wx
from math import pi,sin,cos,sqrt,acos
deg2rad = pi/180.
rad2deg = 180./pi

from pprint import pprint
from vimm.Material import Material
from vimm.Atom import Atom
from vimm.Utilities import path_split,cleansym
from vimm.Element import sym2no,symbol
from vimm.NumWrap import array,dot
from vimm.vimmLib import simple_loader

class CoordEditor(wx.Frame):
    def __init__(self, parent, id, **kwds):
        # begin wxGlade: CoordEditor.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, parent,id,"CoordEditor", **kwds)
        self.TextArea = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)

        self.parent = parent
        
        # Menu Bar
        self.MenuBar = wx.MenuBar()
        self.SetMenuBar(self.MenuBar)
        wxglade_tmp_menu = wx.Menu()
        ID_UPDATE = wx.NewId()
        ID_CLOSE = wx.NewId()
        ID_CONVERT_CART = wx.NewId()
        ID_CONVERT_ZMAT = wx.NewId()
        wxglade_tmp_menu.Append(ID_UPDATE,
                                "Save/Update Coordinates\tCtrl-s",
                                "Save the current coordinates and redisplay",
                                wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(ID_CLOSE,
                                "Close\tCtrl-w",
                                "Close the editor window",
                                wx.ITEM_NORMAL)
        self.MenuBar.Append(wxglade_tmp_menu, "File")

        wx.EVT_MENU(self,ID_UPDATE,self.update)
        wx.EVT_MENU(self,ID_CLOSE,self.close)
        
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(ID_CONVERT_CART,
                                "Convert to Cartesians\tCtrl-c",
                                "Convert to Cartesian coordinates",
                                wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(ID_CONVERT_ZMAT,
                                "Convert to ZMatrix\tCtrl-z",
                                "Convert to zmatrix (internal) coordinates",
                                wx.ITEM_NORMAL)
        self.MenuBar.Append(wxglade_tmp_menu, "Coords")

        wx.EVT_MENU(self,ID_CONVERT_CART,self.convert_cart)
        wx.EVT_MENU(self,ID_CONVERT_ZMAT,self.convert_zmat)
        
        # Menu Bar end
        self.__set_properties()
        self.__do_layout()
        self.current_structure()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: CoordEditor.__set_properties
        self.SetTitle("Coordinate Editor")
        self.SetSize((380, 351))
        self.TextArea.SetMinSize((300,300))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: CoordEditor.__do_layout
        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add(self.TextArea, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        self.SetAutoLayout(True)
        self.SetSizer(Sizer)
        self.Layout()
        # end wxGlade

    def current_structure(self):
        lines = material_to_lines(self.parent.material)
        self.load_lines(lines)
        return

    def load_lines(self,lines):
        self.TextArea.Clear()
        self.TextArea.WriteText("\n".join(lines))
        return

    def update(self,*args):
        lines = self.get_lines()

        if is_zmatrix(lines):
            material = parse_zmat(lines)
        else:
            material = parse_cart(lines)

        self.parent.material = material
        self.parent.render(1)
        return

    def close(self,*args): self.Close(True)

    def convert_cart(self,*args):
        lines = self.get_lines()
        if is_zmatrix(lines):
            material = parse_zmat(lines)
            lines = material_to_lines(material)
            self.load_lines(lines)
        return
    
    def convert_zmat(self,*args):
        lines = self.get_lines()
        if not is_zmatrix(lines):
            material = parse_cart(lines)
            zmat = material_to_zmat(material)
            lines = zmat_to_lines(zmat)
            self.load_lines(lines)
        return

    def get_lines(self):
        lines = []
        nlines = self.TextArea.GetNumberOfLines()
        for i in range(nlines):
            val = self.TextArea.GetLineText(i)
            lines.append(val)
        return lines

# end of class CoordEditor

def is_zmatrix(lines): return len(lines[0].split()) == 1

def zmat_to_lines(zmat):
    lines = []
    for atom in zmat:
        lines.append(zatom_string(atom))
    return lines

def material_to_lines(material):
    lines = []
    for atom in material.get_atoms():
        sym = atom.get_symbol()
        xyz = atom.get_xyz()
        lines.append("%s  %15.8f  %15.8f  %15.8f" % (sym,xyz[0],xyz[1],xyz[2]))
    return lines

def catom_string(atom):
    sym,xyz = atom
    return "%s  %15.8f  %15.8f  %15.8f" % (sym,xyz[0],xyz[1],xyz[2])

def zatom_string(atom):
    vals = []
    vals.append("%s" % atom[0])
    if len(atom) > 2:
        j,rij = atom[1:3]
        vals.append("%d %15.8f" % (j+1,rij))
    if len(atom) > 4:
        k,aijk = atom[3:5]
        vals.append("%d %15.8f" % (k+1,aijk))
    if len(atom) > 6:
        l,tijkl = atom[5:7]
        vals.append("%d %15.8f" % (l+1,tijkl))
    return " ".join(vals)

def parse_cart(lines):
    material = Material("vimm")
    for line in lines:
        words = line.split()
        if not words: continue
        sym = str(words[0])
        atno = sym2no[sym]
        xyz = array(map(float,words[1:4]))
        material.add_atom(Atom(atno,xyz,sym,sym))
    material.bonds_from_distance()
    return material        

def parse_zmat(lines):
    material = Material("vimm")
    for line in lines:
        words = line.split()
        if len(words) == 0:
            continue
        sym = words[0]
        if len(words) == 1:
            # Atom at origin
            x=y=z=0
        elif len(words) == 3:
            # Atom along z-axis
            x=y=0
            iat = int(words[1])-1
            assert iat == 0
            r = float(words[2])
            z = r
        elif len(words) == 4:
            # This line contains a simple list of cartesian coordinates
            x,y,z = map(float,words[1:])
        elif len(words) == 5:
            # Atom in xy-plane
            y=0
            iat = int(words[1])-1
            r = float(words[2])
            jat = int(words[3])-1
            theta = float(words[4])*deg2rad
            # Change this to simply use the numpy object:
            x0,y0,z0 = material.get_atom(iat).get_xyz()
            x = x0+r*sin(theta)
            if iat == 0:
                z = z0 + r*cos(theta)
            else:
                z = z0 - r*cos(theta)
        else:
            # General case
            iat = int(words[1])-1
            r = float(words[2])
            jat = int(words[3])-1
            theta = float(words[4])*deg2rad
            kat = int(words[5])-1
            phi = float(words[6])*deg2rad
            # Change these to simply use the numpy object:
            xi,yi,zi = material.get_atom(iat).get_xyz()
            xj,yj,zj = material.get_atom(jat).get_xyz()
            xk,yk,zk = material.get_atom(kat).get_xyz()

            # Change these to use numpy math:
            # Vector from iat -> jat
            xx = xj-xi
            yy = yj-yi
            zz = zj-zi
            rinv = 1/sqrt(xx*xx+yy*yy+zz*zz)
            xa = xx*rinv
            ya = yy*rinv
            za = zz*rinv

            # Vector from iat -> kat
            xb = xk-xi
            yb = yk-yi
            zb = zk-zi

            # Unit vector from iat -> kat
            xc = ya*zb - za*yb
            yc = za*xb - xa*zb
            zc = xa*yb - ya*xb
            rinv = 1/sqrt(xc*xc+yc*yc+zc*zc)
            xc *= rinv
            yc *= rinv
            zc *= rinv

            xb = yc*za - zc*ya
            yb = zc*xa - xc*za
            zb = xc*ya - yc*xa

            zz = r*cos(theta)
            xx = r*sin(theta)*cos(phi)
            yy = r*sin(theta)*sin(phi)

            x = xi + xa*zz + xb*xx + xc*yy
            y = yi + ya*zz + yb*xx + yc*yy
            z = zi + za*zz + zb*xx + zc*yy
        atno = sym2no[sym]
        xyz = array([x,y,z])
        material.add_atom(Atom(atno,xyz,sym,sym))
    material.bonds_from_distance()
    return material

def material_to_zmat(material):
    zarray = build_zarray(material)
    zvals = zarray_values(material,zarray)
    zmat = build_zmat(material,zarray,zvals)
    # check for linear geometries and try to correct, if possible
    return zmat

def build_zarray(material):
    zarray = []
    nat = material.get_nat()
    for i in range(nat):
        atomi = material.get_atom(i)
        if i == 0:
            zi = []
        elif i == 1:
            zi = [0]
        elif i == 2:
            atom0 = material.get_atom(0)
            atom1 = material.get_atom(1)
            if atomi.distance(atom1) < atomi.distance(atom0):
                zi = [1,0]
            else:
                zi = [0,1]
        else:
            rmin = 1e10
            jref = 0
            for j in range(i):
                atomj = material.get_atom(j)
                rij = atomi.distance(atomj)
                if rij < rmin:
                    rmin = rij
                    jref = j

            if jref == 0:
                kref = 1
                lref = 2
            elif jref == 1:
                kref = 0
                lref = 2
            else:
                kref = zarray[jref][0]
                lref = zarray[jref][1]
            zi = [jref,kref,lref]
        zarray.append(zi)
    return zarray

def zarray_values(material,zarray):
    zvals = []
    nat = material.get_nat()
    for i in range(nat):
        atomi = material.get_atom(i)
        zarrayi = zarray[i]
        zval = []
        zlen = len(zarrayi)
        if zlen > 0:
            j = zarrayi[0]
            atomj = material.get_atom(j)
            rij = atomi.distance(atomj)
            zval.append(rij)
        if zlen > 1:
            k = zarrayi[1]
            atomk = material.get_atom(k)
            aijk = angle(atomi.xyz,atomj.xyz,atomk.xyz)
            zval.append(aijk)
        if zlen > 2:
            l = zarrayi[2]
            atoml = material.get_atom(l)
            tijkl = torsion2(atomi.xyz,atomj.xyz,atomk.xyz,atoml.xyz)
            zval.append(tijkl)
        zvals.append(zval)
    return zvals

def build_zmat(material,zarray,zvals):
    zmat = []
    nat = material.get_nat()
    for i in range(nat):
        atomi = material.get_atom(i)
        sym = atomi.get_symbol()
        zat = [sym]
        if i > 0:
            zat.extend([zarray[i][0],zvals[i][0]])
        if i > 1:
            zat.extend([zarray[i][1],zvals[i][1]])
        if i > 2:
            zat.extend([zarray[i][2],zvals[i][2]])
        zmat.append(zat)
    return zmat

def angle(vi,vj,vk): return vangle(vi-vj,vk-vj)
def length(v):
    return sqrt(dot(v,v))

def vangle(v1,v2):
    r1 = length(v1)
    r2 = length(v2)
    mag = r1*r2
    dp = dot(v1,v2)/mag
    dp = max(-0.999999,dp)
    dp = min(0.999999,dp)
    return rad2deg*acos(dp)

def torsion2(a,b,c,d):
    b1 = a-b
    b2 = b-c
    b3 = c-d

    c1 = cross(b1,b2)
    c2 = cross(b2,b3)
    c3 = cross(c1,c2)

    if length(c1)*length(c2) < 0.001:
        tijkl = 0
    else:
        tijkl = vangle(c1,c2)
        if dot(b2,c3) > 0:
            tijkl *= -1
    return tijkl

def cross((a,b,c),(d,e,f)): return b*f-e*c,c*d-a*f,a*e-b*d
