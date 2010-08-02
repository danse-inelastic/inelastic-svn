#!/usr/bin/env python
#
# a test of the trackball_camera class, showing basic usage in pyglet.
#
# by Roger Allen, July 2008
# roger@rogerandwendy.com
#
from pyglet.gl import *
from pyglet import window
from trackball_camera import TrackballCamera

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
g_width  = 800
g_height = 600
# >>>> INITIALIZE THE TRACKBALL CAMERA
g_tbcam  = TrackballCamera(20.0)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def to_glfloat_array(x):
    return (GLfloat * len(x))(*x)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def init_gl():
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
                        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def on_resize(width, height):
    g_width = width
    g_height = height
    glViewport(0,0,g_width,g_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective( 
        40.0,                            # Field Of View
        float(g_width)/float(g_height),  # aspect ratio
        1.0,                             # z near
        100.0)                           # z far
    # >>>> INITIALIZE THE MODELVIEW MATRIX FOR THE TRACKBALL CAMERA
    g_tbcam.update_modelview()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def draw_sphere():
    glColor3f(1.0, 1.0, 0.0)
    q = gluNewQuadric()
    gluQuadricDrawStyle(q,GLU_LINE)
    #gluQuadricDrawStyle(q,GLU_FILL)
    glPushMatrix()
    glTranslatef(10.0, 0.0, 0.0)
    gluSphere(q,5.0,20,20)
    glPopMatrix()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def draw_grid():
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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def redraw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_grid()
    draw_sphere()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def norm1(x,maxx):
    """given x within [0,maxx], scale to a range [-1,1]."""
    return (2.0 * x - float(maxx)) / float(maxx)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def on_mouse_press(x, y, button, modifiers):
    if button == window.mouse.LEFT:
        g_tbcam.mouse_roll(
            norm1(x, g_width),
            norm1(y,g_height),
            False)
    elif button == window.mouse.RIGHT:
        g_tbcam.mouse_zoom(
            norm1(x, g_width),
            norm1(y,g_height),
            False)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & window.mouse.LEFT:
        g_tbcam.mouse_roll(
            norm1(x,g_width),
            norm1(y,g_height))
    elif buttons & window.mouse.RIGHT:
        g_tbcam.mouse_zoom(
            norm1(x,g_width),
            norm1(y,g_height))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    config = Config(double_buffer=True, depth_size=24)
    win = window.Window(visible=False,resizable=True,config=config)
    win.on_mouse_press   = on_mouse_press
    win.on_mouse_drag    = on_mouse_drag
    win.on_resize        = on_resize
    global g_width, g_height
    win.set_size(g_width,g_height)
    init_gl()
    win.set_visible()
    while not win.has_exit:
        win.dispatch_events()
        redraw()
        win.flip()

if __name__=="__main__":
    main()
