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

from math import pi,sqrt,acos
from vimm.NumWrap import array,dot
from vimm.Utilities import isapprox

rt32 = sqrt(3)/2.

class Cell:
    def __init__(self,axyz,bxyz,cxyz,**opts):
        self.scaleA = opts.get('scaleA',1.0)
        self.scaleB = opts.get('scaleB',1.0)
        self.scaleC = opts.get('scaleC',1.0)
        verbose = opts.get('verbose',False)
        if verbose:
            print "Forming Cell"
            print axyz
            print bxyz
            print cxyz
            print self.scaleA
            print self.scaleB
            print self.scaleC
        self.axyz = array(axyz)*self.scaleA
        self.bxyz = array(bxyz)*self.scaleB
        self.cxyz = array(cxyz)*self.scaleC
        self.origin = array([0,0,0])
        self.aLabel = opts.get('aLabel','A')
        self.bLabel = opts.get('bLabel','B')
        self.cLabel = opts.get('cLabel','C')
        self.originLabel = opts.get('originLabel','O')
        return

    def abcabg(self): return uc2abcabg(self.axyz,self.bxyz,self.cxyz)
    def abc(self): return self.axyz,self.bxyz,self.cxyz

    def lat2cart_factory(self):
        """Factory: returns a fuction that does the transformation
           from lattice to cartesian coordinates"""
        def func(x,y,z):
            from math import floor
            x -= floor(x) # Transform to [0,1)
            y -= floor(y)
            z -= floor(z)
            return x*self.axyz + y*self.bxyz + z*self.cxyz
        return func

    def cart2lat_factory(self):
        """Factory: returns a fuction that does the transformation
           from cartesian to lattice coordinates"""
        print "Warning: cart2lat_conv haven't tested this extensively"
        def func(x,y,z):
            xyz = array((x,y,z))
            #xyzl = sqrt(dot(xyz,xyz))
            #xyz = xyz/xyzl
            al = dot(self.axyz,self.axyz)
            bl = dot(self.bxyz,self.bxyz)
            cl = dot(self.cxyz,self.cxyz)
            return dot(xyz,self.axyz)/al,dot(xyz,self.bxyz)/bl,dot(xyz,self.cxyz)/cl
        return func


# General utilities for lattice vectors
def abcabg2abc(a,b,c,alpha,beta,gamma):
    if isapprox(alpha,90) and isapprox(beta,90) and isapprox(gamma,90):
        return [a,0,0],[0,b,0],[0,0,c]
    elif isapprox(alpha,90) and isapprox(beta,90) and isapprox(gamma,120):
        return [a,0,0],[-b/2.,rt32*b,0],[0,0,c]
    raise "abcabg2abc: general lattice symmetries not implemented yet"
    return
    
def uc2abcabg((ax,ay,az),(bx,by,bz),(cx,cy,cz)):
    "Convert Cartesian cell vectors to A,B,C,alpha,beta,gamma values"
    todeg = 180./pi
    a = sqrt(ax*ax+ay*ay+az*az)
    b = sqrt(bx*bx+by*by+bz*bz)
    c = sqrt(cx*cx+cy*cy+cz*cz)
    bdotc = (bx*cx+by*cy+bz*cz)/b/c
    adotc = (ax*cx+ay*cy+az*cz)/a/c
    adotb = (ax*bx+ay*by+az*bz)/a/b
    alpha = acos((bx*cx+by*cy+bz*cz)/b/c)*todeg
    beta = acos((ax*cx+ay*cy+az*cz)/a/c)*todeg
    gamma= acos((ax*bx+ay*by+az*bz)/a/b)*todeg
    return a,b,c,alpha,beta,gamma

