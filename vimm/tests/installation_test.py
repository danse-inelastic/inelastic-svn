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

def python_test():
    from sys import version_info
    major = version_info[0]
    minor = version_info[1]
    print "Your python version is %d.%d" % (major,minor)
    if major < 2:
        print "Your version is seriously out of date; Icarus requires you\n",\
              "to upgrade to a modern version (e.g. 2.3.x)"
    elif minor < 3:
        print "Your version is somewhat out of date; you might have trouble\n",\
              "compiling PyOpenGL on versions of python before 2.3"
    else:
        print "Your version of python looks up to date"
    return

def numpy_test():
    try:
        from Numeric import array
        a = array((1.,2.,3.))
        print "NumPy appears to work on your platform"
    except:
        print "Please install Numeric Python from http://numpy.sf.net"
    return

def opengl_test():
    failed = 0
    try:
        from OpenGL.GL import glCallList
        print "GL import succeeded"
    except:
        print "GL import failed"
        failed = 1

    try:
        from OpenGL.GLU import gluCylinder
        print "GLU import succeeded"
    except:
        print "GLU import failed"
        failed = 1

    try:
        from OpenGL.GLUT import glutSolidSphere
        print "GLUT import succeeded"
    except:
        print "GLUT import failed"
        failed = 1

    if failed:
        print "OpenGL appears to be installed incorrectly. Please see\n",\
              "http://pyopengl.sf.net and install a current version"
    else:
        print "OpenGL appears to be installed correctly."
    return

def wx_test():
    try:
        import wx
        app = wx.PySimpleApp()
        frame  = wx.Frame(None,-1,"Hello World")
        print "wxPython appears correctly installed"
    except:
        print "wxPython is not installed correctly. Please see\n",\
              "http://wxpython.org and install this package"
    
    return

def pil_test():
    try:
        import Image
        print "Python Image Library appears correctly installed"
    except:
        print "Python Image Library is not installed correctly.\n",\
            "You will not be able to do screen shots without it.\n",\
            "Please download it from: http://www.pythonware.com/products/pil/"
    return
       
        
def main():
    print "Starting installation tests"
    python_test()
    numpy_test()
    opengl_test()
    wx_test()
    pil_test()
    print "Done with tests"
    return

if __name__ == '__main__': main()

