#!/usr/bin/env python
"Taken from the Icarus Camera module"

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


from vimm.NumWrap import array,dot,matrixmultiply,reshape,identity
from math import tan,sqrt,cos,tan,sin

from OpenGL.GLU import gluProject, gluUnProject

DEBUG = 0

class Camera:
    def __init__(self, position=[0.0,0.0,1.0], look_at=[0.0,0.0,0.0], 
                 up=[0.0,1.0,0.0], right=[1.0,0.0,0.0]):
        self._pos_init = 0
        self._position=position[:]
        self._look_at=look_at[:]
        self._up=up[:]
        self._right=right[:]
        self.size = (400,400)
        self.rotate_scale = 0.01
        return

    def set_position(self, position): self._position=position[:]
    def set_look_at(self, look_at): self._look_at=look_at[:]
    def set_up(self, up): self._up=up[:]
    def set_right(self, right): self._right=right[:]
    def get_position(self): return self._position
    def get_look_at(self): return self._look_at
    def get_up(self): return self._up
    def get_right(self): return self._right
    def set_size(self,size): 
	#print "Resetting camera size: ",self.size,size
	self.size = size
    def get_size(self): return self.size

    def get_view_height(self):
        if self.size: return self.size[1]
        return 400

    def get_view_width(self):
        if self.size: return self.size[0]
        return 400

    def set_pos_from_bbox(self,(xmin,xmax,ymin,ymax,zmin,zmax),
                          view_angle=40.):
        if self._pos_init: return # Don't do if pos already set
        self._pos_init = 1
        min_vector = array((xmin,ymin,zmin))
        max_vector = array((xmax,ymax,zmax))

        center = 0.5*(min_vector+max_vector)
        buffer = 1.2
        l = buffer*(max_vector-min_vector)
        max_length = max(l)
        z_distance=((max_length/(2.0*tan(0.017453293*view_angle/2.0)))
                +max_vector[2])
        self.set_position([0.0, 0.0, z_distance])
        self.set_look_at(list(center))
        return
        

    def translation_motion(self,x,y,xold,yold):
        newpos = array((x,y))
        oldpos = array((xold,yold))
        oldpos_model = self.model_coords(oldpos[0],oldpos[1])
        newpos_model = self.model_coords(newpos[0],newpos[1])
        dp = oldpos_model - newpos_model
        up=array(self.get_up())  
        right=array(self.get_right())
        t_up=(dot(dp,up))*up;
        t_right=(dot(dp,right))*right;
        self.set_look_at(self.get_look_at()+t_up+t_right);
        return

    def scaling_motion(self,x,y,xold,yold):
        newpos = array((x,y))
        oldpos = array((xold,yold))
        (dx,dy)=newpos-oldpos
        scale = 1 + float(dy)/self.get_view_height()
        self.set_position(scale*array(self.get_position()))
        return

    def rotation_motion(self,x,y,xold,yold):
        newpos = array((x,y))
        oldpos = array((xold,yold))
        diff_pos=newpos-oldpos
        r=sqrt(dot(diff_pos,diff_pos))
        if r==0: return
        diff_pos=diff_pos/r
        angle=r*self.rotate_scale
        rot_mat=self.rotation_matrix(diff_pos,angle);
        self.set_up(matrixmultiply(rot_mat,array(self.get_up()))[:])
        self.set_right(matrixmultiply(rot_mat,array(self.get_right()))[:])
        self.set_position(matrixmultiply(rot_mat, array(self.get_position()))[:])
        return

    def rotation_matrix(self,diffpos,alpha):
        # diffpos given in model coords
        #r=dot(diffpos,diffpos);
        dx,dy=diffpos;
        up=array(self.get_up());
        right=array(self.get_right());
        u=-(dy*right)-(dx*up);
        u=u/sqrt(dot(u,u));  # normalize the vector
        (a,b,c)=u
        #
        # construct the S and M matrices, see
        # OpenGL Programming Guide, p. 672
        #
        # The M matrix is the rotation matrix
        #
        S=array((( 0, -c,  b),
                 ( c,  0, -a),
                 (-b,  a,  0)));
        #
        # u_uT is u times its transpose (to give a 3x3 matrix)
        #
        u_uT=matrixmultiply(reshape(u,(3,1)),reshape(u,(1,3)));
        M=u_uT+cos(alpha)*(identity(3)-u_uT)+sin(alpha)*S
        return M;

    def model_coords(self,x,y):
        """given an (x,y) coordinate pair on the viewport, returns the
        coordinates in model space"""
        tz = gluProject(self._look_at[0],self._look_at[1],
                        self._look_at[2])[2] # retrieve the depth coordinate
        return array(gluUnProject(x,self.get_view_height()-y,tz))

