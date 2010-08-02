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

# This is the only place I'm using GLUT, and I'm trying to break my habit:

import math
from vimm import POVRay
from vimm.NumWrap import array,dot

doglut = True
#doglut = False

from OpenGL.GL import *
from OpenGL.GLU import *
if doglut:
    from OpenGL.GLUT import *

rad2deg=180.0/math.pi

CylRad = 0.1 # default radius for cylinder
        
class ShapeList:
    def __init__(self):
        self.atoms = []
        self.bonds = []
        self.surfaces = []
        self.labels = []
        self.selections = []
        self.distances = []

    def append_atom(self,shape): self.atoms.append(shape)
    def extend_atom(self,shapes): self.atoms.extend(shapes)
    def append_bond(self,bond): self.bonds.append(bond)
    def extend_bond(self,bonds): self.bonds.extend(bonds)
    def append_label(self,label): self.labels.append(label)
    def extend_label(self,labels): self.labels.extend(labels)
    def append_surface(self,surface): self.surfaces.append(surface)
    def extend_surface(self,surfaces): self.surfaces.extend(surfaces)

    def clear(self):
        self.atoms = []
        self.bonds = []
        self.surfaces = []
        self.labels = []
        self.selections = []
        self.distances = []
        return

    def povray(self):
        return [atom.povray() for atom in self.atoms] +\
               [bond.povray() for bond in self.bonds] +\
               [label.povray() for label in self.labels]

    def render(self):
        i = 1
        for atom in self.atoms:
            glPushName(i)
            atom.render()
            glPopName()
            i+=1

        for bond in self.bonds:
            bond.render()

        for surface in self.surfaces:
            surface.render()

        for label in self.labels:
            label.render()

        for selection in self.selections:
            selection.render()

        for distance in self.distances:
            distance.render()
        return

    def bbox(self):
        BIG = 1000.
        xmin = ymin = zmin = BIG
        xmax = ymax = zmax = -BIG
        for features in self.atoms, self.bonds, self.surfaces:
            for shape in features:
                sxmin,sxmax,symin,symax,szmin,szmax = shape.bbox()
                xmin = min(xmin,sxmin)
                xmax = max(xmax,sxmax)
                ymin = min(ymin,symin)
                ymax = max(ymax,symax)
                zmin = min(zmin,szmin)
                zmax = max(zmax,szmax)
        return xmin,xmax,ymin,ymax,zmin,zmax

    def center(self):
        xmin,xmax,ymin,ymax,zmin,zmax = self.bbox()
        xc, yc, zc = 0.5*(xmin+xmax), 0.5*(ymin+ymax), 0.5*(zmin+zmax)
        for shape in self.shapes: shape.shift(-xc,-yc,-zc)
        return

    def names(self):
        n = []
        for shape in self.shapes: n.append(shape.name)
        return ' '.join(n)

class Sphere:
    name = 'Sphere'
    def __init__(self,(x,y,z),rad=1,(red,green,blue)=(0.5,0.5,0.5),
                 nslices=20,nstacks=20):
        self.x = x
        self.y = y
        self.z = z
        self.rad = rad
        self.red = red
        self.green = green
        self.blue = blue
        self.nslices = nslices
        self.nstacks = nstacks
        return

    def render(self):
        glPushMatrix();
        glTranslatef(self.x,self.y,self.z,)
        color = [self.red,self.green,self.blue,1.]
        glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,color) # add color
        glMaterialfv(GL_FRONT, GL_SHININESS, [25.0]) # add material light
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0,1.0,1.0,1.0]) # add specular light
        if doglut:
            glutSolidSphere(self.rad,self.nslices,self.nstacks)
        else:
            q = gluNewQuadric()
            gluSphere(q,self.rad,self.nslices,self.nstacks)
        glPopMatrix()
        return

    def toString(self):
        return "Sphere (%.2f,%.2f,%.2f), (%.2f,%.2f,%.2f)" %\
               (self.x,self.y,self.z,self.red,self.green,self.blue)

    def bbox(self):
        return self.x-self.rad,self.x+self.rad,\
               self.y-self.rad,self.y+self.rad,\
               self.z-self.rad,self.z+self.rad

    def shift(self,x,y,z):
        self.x += x
        self.y += y
        self.z += z
        return

    def get_position(self):
        return (self.x,self.y,self.z)

    def povray(self):
        return POVRay.Sphere((self.x,self.y,self.z),self.rad,
                             (self.red,self.green,self.blue))
    

class Cylinder:
    name = 'Cylinder'
    def __init__(self,xyz1,xyz2,
                 (red,green,blue)=(0.5,0.5,0.5),rad=CylRad, nsides=20):
        self.xyz1 = array(xyz1,'d')
        self.xyz2 = array(xyz2,'d')
        self.dxyz = self.xyz2-self.xyz1
        self.length = math.sqrt(dot(self.dxyz,self.dxyz))
        xd,yd,zd = self.dxyz/self.length
        self.rot = (-yd,xd,0)
        self.theta = math.acos(zd)*rad2deg
        self.rad = rad
        self.nsides = nsides
        self.red = red
        self.green = green
        self.blue = blue
        return

    def povray(self):
        return POVRay.Cylinder(tuple(self.xyz1),tuple(self.xyz2),self.rad,
                             (self.red,self.green,self.blue))
    def render(self):
        "Code that uses GLU"
        glPushMatrix()
        glTranslatef(self.xyz1[0],self.xyz1[1],self.xyz1[2])
        glRotatef(self.theta,self.rot[0],self.rot[1],self.rot[2])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (self.red,self.green,self.blue,1.0))
        glMaterialfv(GL_FRONT, GL_SHININESS, [25.0]) # add material light
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0,1.0,1.0,1.0]) # add specular light
        self.obj = gluNewQuadric()
        gluCylinder(self.obj,self.rad,self.rad,self.length,self.nsides,self.nsides)
        glPopMatrix()
        return

    def renderold(self):
        "This is Ryan's cylinder from Icarus, slightly slower than GLU"
        ax,ay,az = self.xyz1
        bx,by,bz = self.xyz2
        dx,dy,dz = self.dxyz

        L = self.length

        theta=-math.atan2(dz,dx)*rad2deg
        phi=math.asin(dy/L)*rad2deg
  
        glPushMatrix()
        glTranslatef(ax,ay,az)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (self.red,self.green,self.blue,1))
        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(phi, 0.0, 0.0, 1.0)
        dphi=math.pi/self.nsides
        glBegin(GL_TRIANGLE_STRIP)        
        for i in range(0, self.nsides*2+1):
            angle=i*dphi
            sinangle=math.sin(angle)
            cosangle=math.cos(angle)
            sar=sinangle*self.rad
            car=cosangle*self.rad
            glNormal3f(0.0, sinangle, cosangle)
            glVertex3f(0.0, sar, car)
            glVertex3f(L, sar, car)
        glEnd()
        glPopMatrix()
        return
        
    def toString(self):
        return "Cylinder (%.2f,%.2f,%.2f), (%.2f,%.2f,%.2f)" %\
               tuple(list(self.xyz1)+list(self.xyz2))

    def bbox(self):
        mx = min(self.xyz1[0],self.xyz2[0])
        my = min(self.xyz1[1],self.xyz2[1])
        mz = min(self.xyz1[2],self.xyz2[2])
        Mx = max(self.xyz1[0],self.xyz2[0])
        My = max(self.xyz1[1],self.xyz2[1])
        Mz = max(self.xyz1[2],self.xyz2[2])
        return mx,Mx,my,My,mz,Mz

    def shift(self,x,y,z):
        d = array((x,y,z))
        self.xyz1 += d
        self.xyz2 += d
        return

class Line:
    name = 'Line'
    def __init__(self,(x1,y1,z1),(x2,y2,z2),
                 (red,green,blue)=(0.9,0.9,0.9),weight=1):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.red = red
        self.green = green
        self.blue = blue
        self.weight = weight
        return

    def povray(self):
        return POVRay.Line((self.x1,self.y1,self.z1),(self.x2,self.y2,self.z2),
                           (self.red,self.green,self.blue))

    def render(self): 
        glDisable(GL_LIGHTING)
        glEnable(GL_LINE_SMOOTH)
        glLineWidth(self.weight)
        glColor3f(self.red,self.green,self.blue)
        glBegin(GL_LINES)
        glVertex3f(self.x1,self.y1,self.z1)
        glVertex3f(self.x2,self.y2,self.z2)
        glEnd()
        glDisable(GL_LINE_SMOOTH)
        glEnable(GL_LIGHTING)
        return

    def toString(self):
        return "Line (%.2f,%.2f,%.2f), (%.2f,%.2f,%.2f)" %\
               (self.x1,self.y1,self.z1,self.x2,self.y2,self.z2)
    
    def bbox(self): return min(self.x1,self.x2),max(self.x1,self.x2),\
        min(self.y1,self.y2),max(self.y1,self.y2),\
        min(self.z1,self.z2),max(self.z1,self.z2),
               
    def shift(self,x,y,z):
        self.x1 += x
        self.y1 += y
        self.z1 += z
        self.x2 += x
        self.y2 += y
        self.z2 += z
        return

    def midpoint(self):
        mx = (self.x1+self.x2)/2
        my = (self.y1+self.y2)/2
        mz = (self.z1+self.z2)/2
        return (mx,my,mz)


class Triangles:
    name = 'Triangles'
    def __init__(self,(red,green,blue)=(1.,0.,1.),opac=1.0):
        self.triangles = []
        self.red = red
        self.green = green
        self.blue = blue
        self.opac = opac
        return

    def povray(self): return None

    def append(self,xyz1,xyz2,xyz3):
        self.triangles.append(Triangle(xyz1,xyz2,xyz3))

    def render(self):
        self.renorm_mesh()
        glPushMatrix()
        glBegin(GL_TRIANGLES)
        side = GL_FRONT_AND_BACK
        #side = GL_FRONT
        glMaterialfv(side, GL_DIFFUSE,
                     (self.red,self.green,self.blue,self.opac))
        #glMaterialfv(side, GL_SHININESS, [25.0]) # add material light
        #glMaterialfv(side, GL_SPECULAR, [1.0,1.0,1.0,1.0]) # add specular light
        for tri in self.triangles: tri.render()
        glEnd()
        glPopMatrix()
        
        #for now, do it twice so can see below
        glPushMatrix()
        glBegin(GL_TRIANGLES)
        side = GL_BACK
        #side = GL_FRONT
        glMaterialfv(side, GL_DIFFUSE,
                     (self.red,self.green,self.blue,self.opac))
        #glMaterialfv(side, GL_SHININESS, [25.0]) # add material light
        #glMaterialfv(side, GL_SPECULAR, [1.0,1.0,1.0,1.0]) # add specular light
        for tri in self.triangles: tri.render()
        glEnd()
        glPopMatrix()
        return

    def bbox(self):
        BIG = 1000.
        xmin = ymin = zmin = BIG
        xmax = ymax = zmax = -BIG
        for tri in self.triangles:
            mx,Mx,my,My,mz,Mz = tri.bbox()
            xmin = min(xmin,mx)
            xmax = max(xmax,Mx)
            ymin = min(ymin,my)
            ymax = max(ymax,My)
            zmin = min(zmin,mz)
            zmax = max(zmax,Mz)
        return xmin,xmax,ymin,ymax,zmin,zmax

    def renorm_mesh(self):
        vertex_norms = {}
        for tri in self.triangles:
            xyz1 = tuple(tri.xyz1)
            xyz2 = tuple(tri.xyz2)
            xyz3 = tuple(tri.xyz3)
            if vertex_norms.has_key(xyz1):
                vertex_norms[xyz1].append(tri.norm1)
            else:
                vertex_norms[xyz1] = [tri.norm1]
            if vertex_norms.has_key(xyz2):
                vertex_norms[xyz2].append(tri.norm2)
            else:
                vertex_norms[xyz2] = [tri.norm2]
            if vertex_norms.has_key(xyz3):
                vertex_norms[xyz3].append(tri.norm3)
            else:
                vertex_norms[xyz3] = [tri.norm3]
        for vertex in vertex_norms:
            vertex_norms[vertex] = norm(avg(vertex_norms[vertex]))
        for tri in self.triangles:
            xyz1 = tuple(tri.xyz1)
            xyz2 = tuple(tri.xyz2)
            xyz3 = tuple(tri.xyz3)
            tri.norm1 = vertex_norms[xyz1]
            tri.norm2 = vertex_norms[xyz2]
            tri.norm3 = vertex_norms[xyz3]
        return

class Triangle:
    def __init__(self,xyz1,xyz2,xyz3):
        self.xyz1 = array(xyz1)
        self.xyz2 = array(xyz2)
        self.xyz3 = array(xyz3)
        v12 = self.xyz2-self.xyz1
        v13 = self.xyz3-self.xyz1
        self.simplenorm = norm(cross(v12,v13))
        self.norm1 = self.simplenorm
        self.norm2 = self.simplenorm
        self.norm3 = self.simplenorm
        return

    def povray(self):
        return POVRay.Polygon([self.xyz1,self.xyz2,self.xyz3],
                              (128,128,128))

#    def bbox(self):
#        mx,my,mz = min(self.xyz1,self.xyz2,self.xyz3)
#        Mx,My,Mz = max(self.xyz1,self.xyz2,self.xyz3)
#        return mx,Mx,my,My,mz,Mz
    
    def bbox(self):
        mx = min(self.xyz1[0],self.xyz2[0],self.xyz3[0])
        my = min(self.xyz1[1],self.xyz2[1],self.xyz3[1])
        mz = min(self.xyz1[2],self.xyz2[2],self.xyz3[2])
        Mx = max(self.xyz1[0],self.xyz2[0],self.xyz3[0])
        My = max(self.xyz1[1],self.xyz2[1],self.xyz3[1])
        Mz = max(self.xyz1[2],self.xyz2[2],self.xyz3[2])
        return mx,Mx,my,My,mz,Mz

    def render(self):
        #if self.norm1: glNormal3fv(self.norm1)
        glNormal3fv(self.norm1)
        glVertex3fv(self.xyz1)
        glNormal3fv(self.norm2)
        glVertex3fv(self.xyz2)
        glNormal3fv(self.norm3)
        glVertex3fv(self.xyz3)
        return
    
class Point:
    name = 'Point'
    def __init__(self,(x,y,z),(red,green,blue)=(0.9,0.9,0.9),weight=1):
        self.x = x
        self.y = y
        self.z = z
        self.red = red
        self.green = green
        self.blue = blue
        self.weight = weight
        return

    def render(self):
        glDisable(GL_LIGHTING)
        glColor3f(self.red,self.green,self.blue)
        glPointSize(self.weight)
        glBegin(GL_POINTS)
        glVertex3f(self.x,self.y,self.z)
        glEnd()
        glEnable(GL_LIGHTING)
        return

    def toString(self):
        return "Point (%.2f,%.2f,%.2f)" % (self.x,self.y,self.z)
    
    def bbox(self): return self.x,self.x,self.y,self.y,self.z,self.z

    def shift(self,x,y,z):
        self.x += x
        self.y += y
        self.z += z
        return

    def get_position(self):
        return (self.x,self.y,self.z)

class Label:
    def __init__(self,label,xyz,rgb,dis=0.4):
        self.label = label
        self.x,self.y,self.z = xyz
        self.red, self.green, self.blue = rgb
        self.dis = dis
        return

    def povray(self):
        return POVRay.Text(self.label,(self.x,self.y,self.z))
    
    def toString(self):
        return "Label (%s, %.2f,%.2f,%.2f)" % (self.label,self.x,self.y,self.z)
    
    def bbox(self): return self.x,self.x,self.y,self.y,self.z,self.z

    def render(self):
        if not doglut: return
        glDisable(GL_LIGHTING)
        glColor3f(self.red, self.green, self.blue)
        glRasterPos3f(self.x+self.dis, self.y+self.dis, self.z+self.dis)
        for char in list(self.label):
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13,ord(char))
        glEnable(GL_LIGHTING)
        return
    

class WireCube:
    name = 'WireCube'
    def __init__(self,(x,y,z),len=0,(red,green,blue)=(1.0,1.0,1.0),weight=2):
        self.x = x
        self.y = y
        self.z = z
        self.weight = weight
        self.len = len
        self.red = red
        self.green = green
        self.blue = blue
        return

    def render(self):
        if not doglut: return
        glPushMatrix();
        glDisable(GL_LIGHTING)
        glEnable(GL_LINE_SMOOTH)
        glLineWidth(self.weight)
        glTranslatef(self.x,self.y,self.z,)
        color = [self.red,self.green,self.blue,1.]
        glColor3fv(color)
        glutWireCube(self.len)
        glDisable(GL_LINE_SMOOTH)
        glEnable(GL_LIGHTING)
        glPopMatrix()
        return

    def toString(self):
        return "Sphere (%.2f,%.2f,%.2f), (%.2f,%.2f,%.2f)" %\
               (self.x,self.y,self.z,self.red,self.green,self.blue)

    def bbox(self):
        return self.x-self.len/2, self.x+self.len/2,\
            self.y-self.len/2, self.y+self.len/2,\
            self.z-self.len/2, self.z+self.len/2

    def shift(self,x,y,z):
        self.x += x
        self.y += y
        self.z += z
        return

    def get_position(self):
        return (self.x,self.y,self.z)

def cross(a,b): return array((a[1]*b[2]-a[2]*b[1],
                              a[2]*b[0]-a[0]*b[2],
                              a[0]*b[1]-a[1]*b[0]))
def norm(a): return a/math.sqrt(dot(a,a))
def avg(vals): return sum(vals)/float(len(vals))
