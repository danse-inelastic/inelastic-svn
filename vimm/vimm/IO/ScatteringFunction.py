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

from vimm.Material import Material
from vimm.Utilities import path_split

extensions=["nc"]
filetype="Scattering Function Netcdf Format"

def load(fullfilename):
    filedir, fileprefix, fileext = path_split(fullfilename)
    material=Material(fileprefix)
    
    from Scientific.IO.NetCDF import NetCDFFile
    file = NetCDFFile(fullfilename, 'r')
    allDimNames = file.dimensions.keys() 
    print 'allDimNames', allDimNames
    vars = file.variables.keys()
    print 'vars', vars
    
    if file.variables.has_key('dsf'):
        sf = file.variables['dsf'].getValue() #numpy array
        zLabel='S(Q,Omega) (a.u.)'
    elif file.variables.has_key('sf'):
        sf = file.variables['sf'].getValue() #numpy array
        zLabel='F(Q,t) (a.u.)'
    print sf
    
    q = file.variables['q'].getValue()
    print 'q',q
    
    if file.variables.has_key('frequency'):
        timeOrFreq = file.variables['frequency'].getValue() #numpy array
        yLabel='Omega (1/ps)'
    elif file.variables.has_key('time'):
        timeOrFreq = file.variables['time'].getValue() #numpy array
        yLabel='Time (ps)'
    print 'timeOrFreq', timeOrFreq
    
    material.new_geo()
    #triangulate and plot the surface
    #from vimm.Shapes import Triangles
    triangleCoords = []#Triangles((1.,0.,1.))
    #start across the first axis as x
    xLen, yLen = sf.shape
#    for i in range(xLen):
#        for j in range(yLen):
#            triangleCoords.append((q[i],timeOrFreq[j],sf[i,j]))
    for i in range(xLen-1):
        for j in [0,1]:#range(yLen-1): 
            #use the spacing given in the q and timeOrFrequency
            #triangulate each of the squares in the grid
            #lower triangle
            #3\
            #| \
            #1--2            
            triangleCoords.append(((q[i],timeOrFreq[j],sf[i,j]),(q[i+1],timeOrFreq[j],sf[i+1,j]),
             (q[i],timeOrFreq[j+1],sf[i,j+1])))
            #upper triangle
            #3--2
            # \ |
            #  \1   
            triangleCoords.append(((q[i+1],timeOrFreq[j],sf[i+1,j]),(q[i+1],timeOrFreq[j+1],sf[i+1,j+1]),
             (q[i],timeOrFreq[j+1],sf[i,j+1])))
    material.geo.surface = triangleCoords
    #add the axes to the plot--assume orthogonal for now
    aLen = q[-1]-q[0]
    bLen = timeOrFreq[-1]-timeOrFreq[0]
    cLen = sf.max()-sf.min()
    a = (aLen, 0, 0)
    b = (0, bLen, 0)
    c = (0, 0, cLen)
        # scale the axes so they are roughly equal
    scaleA = 1/aLen
    scaleB = 1/bLen
    scaleC = 2/cLen #C axis is half as large
    from vimm.Cell import Cell
    cell = Cell(a, b, c, scaleA = scaleA, scaleB = scaleB, 
                scaleC = scaleC)
    cell.aLabel = 'Q (1/Ang)'
    cell.bLabel = yLabel
    cell.cLabel = zLabel
    # add tick mark labels /data point labels to the plot
    cell.tickmarks = {'A':[(qPoint,0,0) for qPoint in q], 
        'B':[(0,timeOrFreqPoint,0) for timeOrFreqPoint in timeOrFreq]}
    material.set_cell(cell)
    return material
    
def save(filename, material):
    pass

#def save(filename, material):
#    file=open(filename, 'w')
#    for geo in material.get_geos():
#        atoms = geo.get_atoms()
#        file.write('%d\nFile written by vimm.xyz\n' % len(atoms))
#        for atom in atoms:
#            x,y,z = atom.get_xyz()
#            atno = atom.get_atno()
#            file.write('%s %f %f %f\n' % (symbol[atno],x,y,z))
#    return

def new():
    material = Material("New Surface")
    return material
