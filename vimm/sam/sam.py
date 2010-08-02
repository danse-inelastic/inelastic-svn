#!/usr/bin/env python

# Defaults for kwarg-passed options
defaults = {
    'mat_draw'    : True,     # Use materials/lighting to draw
    'wire_draw'   : False,    # Use open wires to draw
    'swire_draw'  : False,    # Use smoothed wires to draw
    'fwire_draw'  : False,    # Use filled wires to draw
    'specular'    : True,     # Use specular highlights
    'sslices'     : 32,       # Number of slices in a sphere
    'sstacks'     : 32,       # Number of stacks in a sphere
    'cslices'     : 12,       # Number of slices in a cylinder
    'cstacks'     : 12,       # Number of stacks in a cylinder
    'lweight'     : 1,        # Line weight
    'width'       : 600,      # Window width
    'height'      : 600,      # Window height
    }

from pyglet.gl import *
from pyglet import window
from trackball_camera import TrackballCamera
import math

def draw_sphere(x,y,z,red,green,blue,rad,**kwargs):
    mat_draw = kwargs.get('mat_draw',defaults['mat_draw'])
    fwire_draw = kwargs.get('fwire_draw',defaults['fwire_draw'])
    sslices = kwargs.get('sslices',defaults['sslices'])
    sstacks = kwargs.get('sstacks',defaults['sstacks'])
    specular = kwargs.get('specular',defaults['specular'])
    glColor3f(red, green, blue)
    q = gluNewQuadric()
    if mat_draw:
        glMaterialfv(GL_FRONT, GL_DIFFUSE, glf((red,green,blue,1.0)))
        if specular:
            glMaterialfv(GL_FRONT, GL_SHININESS, glf([25.0]))
            glMaterialfv(GL_FRONT, GL_SPECULAR, glf([1.0,1.0,1.0,1.0])) 
    elif fwire_draw:
        gluQuadricDrawStyle(q,GLU_FILL)
    else:
        gluQuadricDrawStyle(q,GLU_LINE)
    glPushMatrix()
    glTranslatef(x, y, z)
    gluSphere(q,rad,sslices,sstacks)
    glPopMatrix()
    return

def draw_grid():
    # Either remove hardwires or delete
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    for i in range(10):
        glVertex3f(i*10.0,-100., 0.)
        glVertex3f(i*10.0, 100., 0.)
        
        glVertex3f(-i*10.0,-100., 0.)
        glVertex3f(-i*10.0, 100., 0.)

        glVertex3f(-100., i*10.0, 0.)
        glVertex3f( 100., i*10.0, 0.)

        glVertex3f(-100.,-i*10.0, 0.)
        glVertex3f( 100.,-i*10.0, 0.)
    glEnd()
    return

def draw_cylinder(x1,y1,z1,x2,y2,z2,red,green,blue,rad,**kwargs):
    mat_draw = kwargs.get('mat_draw',defaults['mat_draw'])
    fwire_draw = kwargs.get('fwire_draw',defaults['fwire_draw'])
    cslices = kwargs.get('cslices',defaults['cslices'])
    cstacks = kwargs.get('cstacks',defaults['cstacks'])
    specular = kwargs.get('specular',defaults['specular'])

    rad2deg=180.0/math.pi
    dx,dy,dz = x2-x1,y2-y1,z2-z1
    length = math.sqrt(dx*dx+dy*dy+dz*dz)
    dxn,dyn,dzn = dx/length,dy/length,dz/length
    rx,ry,rz = -dyn,dxn,0
    theta = math.acos(dzn)*rad2deg

    glPushMatrix()
    glColor3f(red, green, blue)
    q = gluNewQuadric()
    if mat_draw:
        glMaterialfv(GL_FRONT, GL_DIFFUSE, glf((red,green,blue,1.0)))
        if specular:
            glMaterialfv(GL_FRONT, GL_SHININESS, glf([25.0]))
            glMaterialfv(GL_FRONT, GL_SPECULAR, glf([1.0,1.0,1.0,1.0])) 
    elif fwire_draw:
        gluQuadricDrawStyle(q,GLU_FILL)
    else:
        gluQuadricDrawStyle(q,GLU_LINE)
    glTranslatef(x1,y1,z1)

    glRotatef(theta,rx,ry,rz)
    gluCylinder(q,rad,rad,length,cslices,cstacks)
    glPopMatrix()
    return

def draw_line(x1,y1,z1,x2,y2,z2,red,green,blue,**kwargs):
    lweight = kwargs.get('lweight',defaults['lweight'])
    glDisable(GL_LIGHTING)
    glEnable(GL_LINE_SMOOTH)
    glLineWidth(lweight)
    glColor3f(red,green,blue)
    glBegin(GL_LINES)
    glVertex3f(x1,y1,z1)
    glVertex3f(x2,y2,z2)
    glEnd()
    glDisable(GL_LINE_SMOOTH)
    glEnable(GL_LIGHTING)
    return

def glf(x): return (GLfloat * len(x))(*x)

def norm1(x,maxx):
    """given x within [0,maxx], scale to a range [-1,1]."""
    return (2.0 * x - float(maxx)) / float(maxx)

class TBWindow:
    def __init__(self,width=defaults['width'],height=defaults['height']):
        self.width = width
        self.height = height
        self.config = Config(double_buffer=True, depth_size=24)
        self.win = window.Window(visible=True,resizable=True,
                                 config=self.config, caption='Sam')

        # set callbacks
        self.win.on_resize = self.on_resize
        self.win.on_draw = self.on_draw
        self.win.on_mouse_press = self.on_mouse_press
        self.win.on_mouse_drag = self.on_mouse_drag

        self.win.set_size(self.width,self.height)

        self.init_gl()
        
        self.tb = TrackballCamera(20.0)
        self.clnum = 1
        return

    def init_gl(self,**kwargs):
        swire_draw = kwargs.get('swire_draw',defaults['swire_draw'])
        mat_draw = kwargs.get('mat_draw',defaults['mat_draw'])
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        if swire_draw:
            glEnable(GL_LINE_SMOOTH)
        elif mat_draw:
            glEnable(GL_LIGHTING)
            lightZeroPosition = glf([10.,4.,10.,1.])
            lightZeroColor = glf([0.8,1.0,0.8,1.0]) #green tinged
            glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
            glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
            glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
            glEnable(GL_LIGHT0)
        return

    def run(self): pyglet.app.run()

    def calllist(self, spheres=[], cyls=[], lines=[]):
        glNewList(self.clnum,GL_COMPILE)
        for sphere in spheres: draw_sphere(*sphere)
        for cyl in cyls: draw_cylinder(*cyl)
        for line in lines: draw_line(*line)
        glEndList()
        return

    def on_resize(self, width, height):
        self.width = width
        self.height = height
        glViewport(0,0,self.width,self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective( 
            40.0,                            # Field Of View
            float(self.width)/float(self.height),  # aspect ratio
            1.0,                             # z near
            100.0)                           # z far
        self.tb.update_modelview() # init modview matrix for trackball
        return

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glCallList(self.clnum)
        return

    def on_mouse_press(self, x, y, button, modifiers):
        if button == window.mouse.LEFT:
            self.tb.mouse_roll(
                norm1(x, self.width),
                norm1(y,self.height),
                False)
        elif button == window.mouse.RIGHT:
            self.tb.mouse_zoom(
                norm1(x, self.width),
                norm1(y,self.height),
                False)
        return

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & window.mouse.LEFT:
            self.tb.mouse_roll(
                norm1(x,self.width),
                norm1(y,self.height))
        elif buttons & window.mouse.RIGHT:
            self.tb.mouse_zoom(
                norm1(x,self.width),
                norm1(y,self.height))
        return

def main():
    win = TBWindow()
    spheres = [(-1,-1,0.,1.,0.,0.,1.),
               (1,1,1.,0.,0.,1.,1.)]
    cyls = [(-1,-1,0,1,1,1,0.5,0.5,0.5,0.2)]
    win.calllist(spheres,cyls)
    win.run()
    return

if __name__=="__main__": main()
