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
# Taken from PyQuante

from math import sqrt,exp,pow,pi,floor

class CGBF:
    "Class for a contracted Gaussian basis function"
    def __init__(self,origin,powers=(0,0,0)):
        self._origin = origin
        self._powers = powers
        self._normalization = 1
        self._prims = []
        self._pnorms = []
        self._pexps = []
        self._pcoefs = []
        return

    def __repr__(self):
        s = "<cgbf origin=\"(%f,%f,%f)\" powers=\"(%d,%d,%d)\">\n" % \
            (self._origin[0],self._origin[1],self._origin[2],
             self._powers[0],self._powers[1],self._powers[2])
        for prim in self._prims:
            s = s + prim.prim_str(self.norm())
        s = s + "</cgbf>\n"
        return s

    def norm(self): return self._normalization
    def origin(self): return self._origin
    def powers(self): return self._powers
    def prims(self): return self._prims

    def exps(self): return self._pexps
    def coefs(self): return self._pcoefs
    def pnorms(self): return self._pnorms

    def center(self,other):
        # Crude estimate to where the center is. The correct form
        #  would use gaussian_product_center, but this has multiple
        #  values for each pair of primitives
        xa,ya,za = self._origin
        xb,yb,zb = other.origin()
        return 0.5*(xa+xb),0.5*(ya+yb),0.5*(za+zb)


    def add_primitive(self,exponent,coefficient):
        "Add a primitive BF to this contracted set"
        pbf = PGBF(exponent,self._origin,self._powers)
        pbf._coefficient = coefficient # move into PGBF constructor
        self._prims.append(pbf)
        self._pexps.append(exponent)
        self._pcoefs.append(coefficient)
        return

    def reset_powers(self,px,py,pz):
        self._powers = (px,py,pz)
        for prim in self.prims():
            prim.reset_powers(px,py,pz)
        return

    def normalize(self):
        "Normalize the current CGBF"
        olap = self.overlap(self)
        self._normalization = 1./sqrt(olap)
        for prim in self._prims: self._pnorms.append(prim.norm())

    def overlap(self,other):
        "Overlap matrix element with another CGBF"
        Sij = 0.
        for ipbf in self._prims:
            for jpbf in other._prims:
                Sij = Sij + ipbf.coef()*jpbf.coef()*ipbf.overlap(jpbf)
        return self.norm()*other.norm()*Sij

    def kinetic(self,other):
        "KE matrix element with another CGBF"
        Tij = 0.
        for ipbf in self._prims:
            for jpbf in other._prims:
                Tij = Tij + ipbf.coef()*jpbf.coef()*ipbf.kinetic(jpbf)
        return self.norm()*other.norm()*Tij

    def nuclear(self,other,C):
        "Nuclear matrix element with another CGBF and a center C"
        Vij = 0.
        for ipbf in self._prims:
            for jpbf in other._prims:
                Vij = Vij + ipbf.coef()*jpbf.coef()*ipbf.nuclear(jpbf,C)
        return self.norm()*other.norm()*Vij

    def amp(self,x,y,z):
        "Compute the amplitude of the CGBF at point x,y,z"
        val = 0.
        for prim in self._prims: val+= prim.amp(x,y,z)
        return self._normalization*val

    def laplacian(self,pos):
        "Evaluate the laplacian of the function at pos=x,y,z"
        val = 0.
        for prim in self._prims: val += prim.laplacian(pos)
        return self._normalization*val

    def grad(self,pos):
        "Evaluate the grad of the function at pos=x,y,z"
        val = zeros(3,Float)
        for prim in self._prims:
            val += prim.grad(pos)
        return self._normalization*val

class PGBF:
    "Class for Primitive Gaussian Basis Functions."

    # Constructor
    def __init__(self,exponent,origin,powers=(0,0,0),norm=1.):
        self._exponent = exponent
        self._origin = origin
        self._powers= powers
        self._normalization = norm
        self.normalize()
        self._coefficient = 1
        return

    # Public
    def exp(self): return self._exponent
    def origin(self): return self._origin
    def powers(self): return self._powers
    def norm(self): return self._normalization
    def coef(self): return self._coefficient

    def reset_powers(self,px,py,pz):
        self._powers = (px,py,pz)
        return

    def overlap(self,other):
        "Compute overlap element with another PGBF"
        return self._normalization*other._normalization*\
               overlap(self._exponent,self._powers,self._origin,
                       other._exponent,other._powers,other._origin)

    def kinetic(self,other):
        "Overlap between two gaussians. THO eq. 2.14."
        return self._normalization*other._normalization*\
               kinetic(self._exponent,self._powers,self._origin,
                       other._exponent,other._powers,other._origin)


    def nuclear(self,other,C):
        "THO eq. 2.17 and 3.1"
        return nuclear_attraction(self._origin,self._normalization,
                                  self._powers,self._exponent,
                                  other._origin,other._normalization,
                                  other._powers,other._exponent,
                                  C)

    def amp(self,x,y,z):
        "Compute the amplitude of the PGBF at point x,y,z"
        i,j,k = self._powers
        x0,y0,z0 = self._origin
        return self._normalization*self._coefficient*\
               pow(x-x0,i)*pow(y-y0,j)*pow(z-z0,k)*\
               exp(-self._exponent*dist2((x,y,z),(x0,y0,z0)) )

    # Private
    def normalize(self):
        "Normalize basis function. From THO eq. 2.2"
        l,m,n = self._powers
        alpha = self._exponent
        self._normalization = sqrt(pow(2,2*(l+m+n)+1.5)*
                                   pow(alpha,l+m+n+1.5)/
                                   fact2(2*l-1)/fact2(2*m-1)/
                                   fact2(2*n-1)/pow(pi,1.5))
        return


    # Other overloads
    def __str__(self):
	    return "PGBF(%.2f," % self._exponent +\
               "(%.2f,%.2f,%.2f)," % self._origin +\
               "(%d,%d,%d)," % self._powers +\
               "%.2f)" % self._normalization

    def prim_str(self,topnorm=1):
        return "    <prim exp=\"%6.4f\" coeff=\"%6.4f\" ncoeff=\"%6.4f\"/>\n" \
               % (self.exp(),self.coef(),topnorm*self.norm()*self.coef())

    def laplacian(self,pos):
        amp = self.amp(pos[0],pos[1],pos[2])
        alpha = self._exponent
        x = pos[0]-self._origin[0]
        y = pos[1]-self._origin[1]
        z = pos[2]-self._origin[2]
        x2 = x*x
        y2 = y*y
        z2 = z*z
        r2 = x2+y2+z2
        L,M,N = self._powers
        term = (L*(L-1)/x2 + M*(M-1)/y2 + N*(N-1)/z2) +\
                4*alpha*alpha*r2 - 2*alpha*(2*(L+M+N)+3)
        return self._normalization*self._coefficient*amp*term

    def grad(self,pos):
        amp = self.amp(pos[0],pos[1],pos[2])
        alpha = self._exponent
        L,M,N = self._powers
        x = pos[0]-self._origin[0]
        y = pos[1]-self._origin[1]
        z = pos[2]-self._origin[2]
        val = array([L/x - 2*x*alpha,M/y - 2*y*alpha,N/z-2*z*alpha])
        return self._normalization*self._coefficient*val*amp

def overlap(alpha1,(l1,m1,n1),A,alpha2,(l2,m2,n2),B):
    "Taken from THO eq. 2.12"
    rab2 = dist2(A,B)
    gamma = alpha1+alpha2
    P = gaussian_product_center(alpha1,A,alpha2,B)

    pre = pow(pi/gamma,1.5)*exp(-alpha1*alpha2*rab2/gamma)

    wx = overlap_1D(l1,l2,P[0]-A[0],P[0]-B[0],gamma)
    wy = overlap_1D(m1,m2,P[1]-A[1],P[1]-B[1],gamma)
    wz = overlap_1D(n1,n2,P[2]-A[2],P[2]-B[2],gamma)
    return pre*wx*wy*wz

def overlap_1D(l1,l2,PAx,PBx,gamma):
    "Taken from THO eq. 2.12"
    sum = 0
    for i in range(1+int(floor(0.5*(l1+l2)))):
        sum = sum + binomial_prefactor(2*i,l1,l2,PAx,PBx)* \
              fact2(2*i-1)/pow(2*gamma,i)
    return sum

    
def gaussian_product_center(alpha1,A,alpha2,B):
    gamma = alpha1+alpha2
    return (alpha1*A[0]+alpha2*B[0])/gamma,\
           (alpha1*A[1]+alpha2*B[1])/gamma,\
           (alpha1*A[2]+alpha2*B[2])/gamma

def binomial_prefactor(s,ia,ib,xpa,xpb):
    "From Augspurger and Dykstra"
    sum = 0
    for t in range(s+1):
        if s-ia <= t <= ib:
            sum = sum + binomial(ia,s-t)*binomial(ib,t)* \
                  pow(xpa,ia-s+t)*pow(xpb,ib-t)
    return sum

def binomial(a,b):
    "Binomial coefficient"
    return fact(a)/fact(b)/fact(a-b)

def fact(i):
    "Normal factorial"
    val = 1
    while (i>1):
        val = i*val
        i = i-1
    return val

def fact2(i):
    "Double factorial (!!) function = 1*3*5*...*i"
    val = 1
    while (i>0):
        val = i*val
        i = i-2
    return val

def dist2(A,B):
    dx,dy,dz = A[0]-B[0],A[1]-B[1],A[2]-B[2]
    return dx*dx+dy*dy+dz*dz


sym2powerlist = {
    'S' : [(0,0,0)],
    'P' : [(1,0,0),(0,1,0),(0,0,1)],
    'D' : [(2,0,0),(0,2,0),(0,0,2),(1,1,0),(0,1,1),(1,0,1)],
    'F' : [(3,0,0),(2,1,0),(2,0,1),(1,2,0),(1,1,1),(1,0,2),
           (0,3,0),(0,2,1),(0,1,2), (0,0,3)]
    }

