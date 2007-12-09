# Copyright 2006-2007 Brandon Keith  See LICENSE file for details. 
"""
dimensions.py - code to help draw dimensions

$Id: dimensions.py,v 1.25 2007/07/01 17:27:32 emessick Exp $

History (most recent first):

wware 060324 - created this file
"""

__author__ = "Will"

import math
import types
import Numeric
from Numeric import dot

from OpenGL.GL import glVertex

import platform
from VQT import cross
from VQT import vlen
from VQT import norm
from drawer import drawline
from Utility import Node

"""
The font is a vector-drawing thing. The entries in the font are
integer coordinates. The drawing space is 5x7.
"""

_font = {
    ' ': ( ),
    'A': (((0, 0),
           (0, 4),
           (1, 6),
           (3, 6),
           (4, 4),
           (4, 0)),
          ((0, 3),
           (4, 3))),
    'B': (((0, 6),
           (3, 6),
           (4, 5),
           (4, 4),
           (3, 3),
           (1, 3)),
          ((3, 3),
           (4, 2),
           (4, 1),
           (3, 0),
           (0, 0)),
          ((1, 6),
           (1, 0))),
    'C': ((4, 5),
          (3, 6),
          (1, 6),
          (0, 5),
          (0, 1),
          (1, 0),
          (3, 0),
          (4, 1)),
    'D': (((0, 6),
           (3, 6),
           (4, 5),
           (4, 1),
           (3, 0),
           (0, 0)),
          ((1, 6),
           (1, 0))),
    'E': (((4, 6),
           (0, 6),
           (0, 0),
           (4, 0)),
          ((0, 3),
           (3, 3))),
    'F': (((4, 6),
           (0, 6),
           (0, 0)),
          ((0, 3),
           (3, 3))),
    'G': ((4, 5),
          (3, 6),
          (1, 6),
          (0, 5),
          (0, 1),
          (1, 0),
          (3, 0),
          (4, 1),
          (4, 3),
          (2, 3)),
    'H': (((0, 6),
           (0, 0)),
          ((4, 6),
           (4, 0)),
          ((0, 3),
           (4, 3))),
    'I': (((1, 6),
           (3, 6)),
          ((1, 0),
           (3, 0)),
          ((2, 6),
           (2, 0))),
    'J': (((3, 6),
           (3, 1),
           (2, 0),
           (1, 0),
           (0, 1),
           (0, 2)),
          ((2, 6),
           (4, 6))),
    'K': (((0, 0),
           (0, 6)),
          ((0, 2),
           (4, 6)),
          ((2, 4),
           (4, 0))),
    'L': ((0, 6),
          (0, 0),
          (4, 0)),
    'M': ((0, 0),
          (0, 6),
          (2, 2),
          (4, 6),
          (4, 0)),
    'N': ((0, 0),
          (0, 6),
          (4, 0),
          (4, 6)),
    'O': ((4, 5),
          (3, 6),
          (1, 6),
          (0, 5),
          (0, 1),
          (1, 0),
          (3, 0),
          (4, 1),
          (4, 5)),
    'P': ((0, 3),
          (3, 3),
          (4, 4),
          (4, 5),
          (3, 6),
          (0, 6),
          (0, 0)),
    'Q': (((4, 5),
           (3, 6),
           (1, 6),
           (0, 5),
           (0, 1),
           (1, 0),
           (3, 0),
           (4, 1),
           (4, 5)),
          ((2, 2),
           (4, 0))),
    'R': (((0, 3),
           (3, 3),
           (4, 4),
           (4, 5),
           (3, 6),
           (0, 6),
           (0, 0)),
          ((2, 3),
           (4, 0))),
    'S': ((4, 5),
          (3, 6),
          (1, 6),
          (0, 5),
          (0, 4),
          (1, 3),
          (3, 3),
          (4, 2),
          (4, 1),
          (3, 0),
          (1, 0),
          (0, 1)),
    'T': (((0, 6),
           (4, 6)),
          ((2, 6),
           (2, 0))),
    'U': ((0, 6),
          (0, 1),
          (1, 0),
          (3, 0),
          (4, 1),
          (4, 6)),
    'V': ((0, 6),
          (2, 0),
          (4, 6)),
    'W': ((0, 6),
          (1, 0),
          (2, 4),
          (3, 0),
          (4, 6)),
    'X': (((0, 0),
           (4, 6)),
          ((0, 6),
           (4, 0))),
    'Y': (((0, 6),
           (2, 3),
           (4, 6)),
          ((2, 3),
           (2, 0))),
    'Z': ((0, 6),
          (4, 6),
          (0, 0),
          (4, 0)),
    # do we need lowercase? not yet
    '.': ((2, 0),
          (3, 0),
          (3, 1),
          (2, 1),
          (2, 0)),
    '/': ((0, 0),
          (3, 6)),
    '#': (((1, 0),
           (2, 6)),
          ((2, 0),
           (3, 6)),
          ((0, 4),
           (4, 4)),
          ((0, 2),
           (4, 2))),
    '+': (((0, 3),
           (4, 3)),
          ((2, 5),
           (2, 1))),
    '-': ((0, 3),
          (4, 3)),
    '*': (((0, 3),
           (4, 3)),
          ((1, 1),
           (3, 5)),
          ((1, 5),
           (3, 1))),
    # Still need: ~ ` ! @ $ % ^ & ( ) _ = [ ] { } ; : ' " | < > , ?
    '0': (((0, 6),
           (4, 0)),
          ((1, 0),
           (0, 1),
           (0, 5),
           (1, 6),
           (3, 6),
           (4, 5),
           (4, 1),
           (3, 0),
           (1, 0))),
    '1': ((1, 0),
          (3, 0),
          (2, 0),
          (2, 6),
          (1, 5)),
    '2': ((0, 5),
          (1, 6),
          (3, 6),
          (4, 5),
          (4, 3),
          (0, 1),
          (0, 0),
          (4, 0)),
    '3': ((0, 5),
          (1, 6),
          (3, 6),
          (4, 5),
          (4, 4),
          (3, 3),
          (1, 3),
          (3, 3),
          (4, 2),
          (4, 1),
          (3, 0),
          (1, 0),
          (0, 1)),
    '4': ((1, 6),
          (0, 3),
          (4, 3),
          (4, 6),
          (4, 0)),
    '5': ((4, 6),
          (0, 6),
          (0, 3),
          (3, 3),
          (4, 2),
          (4, 1),
          (3, 0),
          (0, 0)),
    '6': ((3, 6),
          (0, 4),
          (0, 1),
          (1, 0),
          (3, 0),
          (4, 1),
          (4, 2),
          (3, 3),
          (1, 3),
          (0, 2)),
    '7': ((0, 6),
          (4, 6),
          (2, 0)),
    '8': ((1, 3),
          (0, 4),
          (0, 5),
          (1, 6),
          (3, 6),
          (4, 5),
          (4, 4),
          (3, 3),
          (1, 3),
          (0, 2),
          (0, 1),
          (1, 0),
          (3, 0),
          (4, 1),
          (4, 2),
          (3, 3)),
    '9': ((1, 0),
          (4, 3),
          (4, 5),
          (3, 6),
          (1, 6),
          (0, 5),
          (0, 4),
          (1, 3),
          (3, 3),
          (4, 4)),
    }

WIDTH = 5
HEIGHT = 7
SCALE = 0.08

class Font3D:

    def __init__(self, xpos=0, ypos=0, right=None, up=None, rot90=False, glBegin=False):

        self.glBegin = glBegin
        if right is not None and up is not None:
            # The out-of-screen direction for text should always agree with
            # the "real" out-of-screen direction.
            self.outOfScreen = cross(right, up)

            if rot90:
                self.xflip = xflip = right[1] < 0.0
            else:
                self.xflip = xflip = right[0] < 0.0

            xgap = WIDTH
            halfheight = 0.5 * HEIGHT

            if xflip:
                xgap *= -SCALE
                def fx(x): return SCALE * (WIDTH - 1 - x)
            else:
                xgap *= SCALE
                def fx(x): return SCALE * x

            if rot90:
                ypos += xgap
                xpos -= halfheight * SCALE
                def tfm(x, y, yoff1, yflip):
                    if yflip:
                        y1 = SCALE * (HEIGHT - 1 - y)
                    else:
                        y1 = SCALE * y
                    return Numeric.array((xpos + yoff1 + y1, ypos + fx(x), 0.0))
            else:
                xpos += xgap
                ypos -= halfheight * SCALE
                def tfm(x, y, yoff1, yflip):
                    if yflip:
                        y1 = SCALE * (HEIGHT - 1 - y)
                    else:
                        y1 = SCALE * y
                    return Numeric.array((xpos + fx(x), ypos + yoff1 + y1, 0.0))
            self.tfm = tfm

    def drawString(self, str, yoff=1.0, color=None, tfm=None, _font_X=_font['X']):
        n = len(str)
        if not self.glBegin:
            assert color is not None
        if hasattr(self, 'tfm'):
            assert tfm is None
            if self.xflip:
                def fi(i): return i - (n + 1)
            else:
                def fi(i): return i
            # figure out what the yflip should be
            p0 = self.tfm(0, 0, yoff, False)
            textOutOfScreen = cross(self.tfm(1, 0, yoff, False) - p0,
                                    self.tfm(0, 1, yoff, False) - p0)
            yflip = dot(textOutOfScreen, self.outOfScreen) < 0.0
            def tfmgen(i):
                def tfm2(x, y):
                    return self.tfm(x + (WIDTH+1) * fi(i), y, yoff, yflip)
                return tfm2
        else:
            assert tfm is not None
            def tfmgen(i):
                def tfm2(x, y):
                    return tfm(x + i * (WIDTH+1), y)
                return tfm2
        for i in range(n):
            # A pen-stroke is a tuple of 2D vectors with integer
            # coordinates. Each character is represented as a stroke,
            # or a tuple of strokes e.g. '+' or 'X' or '#'.
            def drawSequence(seq, tfm=tfmgen(i)):
                if len(seq) == 0:
                    return  # a space character has an empty sequence
                if type(seq[0][0]) is not types.IntType:
                    # handle multi-stroke characters
                    for x in seq:
                        drawSequence(x)
                    return
                seq = map(lambda tpl: apply(tfm,tpl), seq)
                for i in range(len(seq) - 1):
                    pos1, pos2 = seq[i], seq[i+1]
                    if self.glBegin:
                        # This is what we do for grid planes, where "somebody"
                        # is drawGPGrid in drawers.py.
                        # Somebody has already taken care of glBegin(GL_LINES).
                        glVertex(pos1[0], pos1[1], pos1[2])
                        glVertex(pos2[0], pos2[1], pos2[2])
                        # Somebody has already taken care of glEnd().
                    else:
                        # This is what we do for dimensions.
                        drawline(color, seq[i], seq[i+1])
            drawSequence(_font.get(str[i], _font_X))

class ZeroLengthCylinder(Exception):
    pass

class CylindricalCoordinates:
    def __init__(self, point0, z, uhint, uhint2):
        # u and v and zn are unit vectors
        # z is NOT a unit vector
        self.p0 = point0
        self.p1 = point1 = point0 + z
        self.z = z
        zlen = vlen(z)
        if zlen < 1.0e-6:
            raise ZeroLengthCylinder()
        self.zinv = 1.0 / zlen
        self.zn = zn = norm(z)
        u = norm(uhint - (dot(uhint, z) / zlen**2) * z)
        if vlen(u) < 1.0e-4:
            u = norm(uhint2 - (dot(uhint2, z) / zlen**2) * z)
        v = cross(zn, u)
        self.u = u
        self.v = v
    def __repr__(self):
        def vecrepr(v):
            return "[%g %g %g]" % tuple(v)
        return ("<CylindricalCoordinates p0=%s p1=%s\n  z=%s u=%s v=%s>" %
                (vecrepr(self.p0), vecrepr(self.p1), vecrepr(self.z),
                 vecrepr(self.u), vecrepr(self.v)))
    def rtz(self, pt):
        d = pt - self.p0
        z = dot(d, self.zn)
        d = d - z * self.zn
        r = vlen(d)
        theta = Numeric.arctan2(dot(d, self.v), dot(d, self.u))
        return Numeric.array((r, theta, z), 'd')
    def xyz(self, rtz):
        r, t, z = rtz
        du = (r * math.cos(t)) * self.u
        dv = (r * math.sin(t)) * self.v
        dz = z * self.z
        return self.p0 + du + dv + dz
    def drawLine(self, color, rtz1, rtz2, width=1):
        drawline(color, self.xyz(rtz1), self.xyz(rtz2), width=width)
    def drawArc(self, color, r, theta1, theta2, z,
                width=1, angleIncrement = math.pi / 50):
        n = int(math.fabs(theta2 - theta1) / angleIncrement + 1)
        step = (1.0 * theta2 - theta1) / n
        for i in range(n):
            t = theta1 + step
            self.drawLine(color, (r, theta1, z), (r, t, z), width=width)
            theta1 = t

THICKLINEWIDTH = 20

def drawLinearDimension(color,      # what color are we drawing this in
                        right, up,  # screen directions mapped to xyz coordinates
                        bpos,       # position of the handle for moving the text
                        p0, p1,     # positions of the ends of the dimension
                        text, highlighted=False):
    outOfScreen = cross(right, up)
    bdiff = bpos - 0.5 * (p0 + p1)
    csys = CylindricalCoordinates(p0, p1 - p0, bdiff, right)
    # This works OK until we want to keep the text right side up, then the
    # criterion for right-side-up-ness changes because we've changed 'up'.
    br, bt, bz = csys.rtz(bpos)
    e0 = csys.xyz((br + 0.5, 0, 0))
    e1 = csys.xyz((br + 0.5, 0, 1))
    drawline(color, p0, e0)
    drawline(color, p1, e1)
    v0 = csys.xyz((br, 0, 0))
    v1 = csys.xyz((br, 0, 1))
    if highlighted:
        drawline(color, v0, v1, width=THICKLINEWIDTH)
    else:
        drawline(color, v0, v1)
    # draw arrowheads at the ends
    a1, a2 = 0.25, 1.0 * csys.zinv
    arrow00 = csys.xyz((br + a1, 0, a2))
    arrow01 = csys.xyz((br - a1, 0, a2))
    drawline(color, v0, arrow00)
    drawline(color, v0, arrow01)
    arrow10 = csys.xyz((br + a1, 0, 1-a2))
    arrow11 = csys.xyz((br - a1, 0, 1-a2))
    drawline(color, v1, arrow10)
    drawline(color, v1, arrow11)
    # draw the text for the numerical measurement, make
    # sure it goes from left to right
    xflip = dot(csys.z, right) < 0
    # then make sure it's right side up
    theoreticalRight = (xflip and -csys.z) or csys.z
    theoreticalOutOfScreen = cross(theoreticalRight, bdiff)
    yflip = dot(theoreticalOutOfScreen, outOfScreen) < 0
    if platform.atom_debug:
        print "DEBUG INFO FROM drawLinearDimension"
        print csys
        print theoreticalRight, theoreticalOutOfScreen
        print xflip, yflip
    if yflip:
        def fx(y):
            return br + 1.5 - y / (1. * HEIGHT)
    else:
        def fx(y):
            return br + 0.5 + y / (1. * HEIGHT)
    if xflip:
        def fz(x):
            return 0.9 - csys.zinv * x / (1. * WIDTH)
    else:
        def fz(x):
            return 0.1 + csys.zinv * x / (1. * WIDTH)
    def tfm(x, y, fx=fx, fz=fz):
        return csys.xyz((fx(y), 0, fz(x)))
    f3d = Font3D()
    f3d.drawString(text, tfm=tfm, color=color)

def drawAngleDimension(color, right, up, bpos, p0, p1, p2, text, minR1=0.0, minR2=0.0, highlighted=False):
    z = cross(p0 - p1, p2 - p1)
    try:
        csys = CylindricalCoordinates(p1, z, up, right)
    except ZeroLengthCylinder:
        len0 = vlen(p1 - p0)
        len2 = vlen(p1 - p2)
        # make sure it's really a zero-degree angle
        assert len0 > 1.0e-6
        assert len2 > 1.0e-6
        assert vlen(cross(p1 - p2, p1 - p0)) < 1.0e-6
        # For an angle of zero degrees, there is no correct way to
        # orient the text, so just draw a line segment
        if len0 > len2:
            L = len0
            end = p0
        else:
            L = len2
            end = p2
        Lb = vlen(bpos - p1)
        if Lb > L:
            L = Lb
            end = p1 + (Lb / L) * (end - p1)
        drawline(color, p1, end)
        return
    br, bt, bz = csys.rtz(bpos)
    theta1 = csys.rtz(p0)[1]
    theta2 = csys.rtz(p2)[1]
    if theta2 < theta1 - math.pi:
        theta2 += 2 * math.pi
    elif theta2 > theta1 + math.pi:
        theta2 -= 2 * math.pi
    if theta2 < theta1:
        theta1, theta2 = theta2, theta1
    e0 = csys.xyz((max(vlen(p0 - p1), br, minR1) + 0.5, theta1, 0))
    e1 = csys.xyz((max(vlen(p2 - p1), br, minR2) + 0.5, theta2, 0))
    drawline(color, p1, e0)
    drawline(color, p1, e1)
    if highlighted:
        csys.drawArc(color, br, theta1, theta2, 0, width=THICKLINEWIDTH)
    else:
        csys.drawArc(color, br, theta1, theta2, 0)
    # draw some arrowheads
    e00 = csys.xyz((br, theta1, 0))
    e10 = csys.xyz((br, theta2, 0))
    dr = 0.25
    dtheta = 1 / br
    e0a = csys.xyz((br + dr, theta1 + dtheta, 0))
    e0b = csys.xyz((br - dr, theta1 + dtheta, 0))
    e1a = csys.xyz((br + dr, theta2 - dtheta, 0))
    e1b = csys.xyz((br - dr, theta2 - dtheta, 0))
    drawline(color, e00, e0a)
    drawline(color, e00, e0b)
    drawline(color, e10, e1a)
    drawline(color, e10, e1b)
    midangle = (theta1 + theta2) / 2
    tmidpoint = csys.xyz((br + 0.5, midangle, 0))
    h = 1.0e-3
    textx = norm(csys.xyz((br + 0.5, midangle + h, 0)) - tmidpoint)
    texty = norm(csys.xyz((br + 0.5 + h, midangle, 0)) - tmidpoint)

    # make sure the text runs from left to right
    if dot(textx, right) < 0:
        textx = -textx

    # make sure the text isn't upside-down
    outOfScreen = cross(right, up)
    textForward = cross(textx, texty)
    if dot(outOfScreen, textForward) < 0:
        tmidpoint = csys.xyz((br + 1.5, midangle, 0))
        texty = -texty

    textxyz = tmidpoint - (0.5 * len(text)) * textx

    def tfm(x, y):
        x = (x / (1. * WIDTH)) * textx
        y = (y / (1. * HEIGHT)) * texty
        return textxyz + x + y
    f3d = Font3D()
    f3d.drawString(text, tfm=tfm, color=color)

def drawDihedralDimension(color, right, up, bpos, p0, p1, p2, p3, text, highlighted=False):
    # Draw a frame of lines that shows how the four atoms are connected
    # to the dihedral angle
    csys = CylindricalCoordinates(p1, p2 - p1, up, right)
    r1, theta1, z1 = csys.rtz(p0)
    r2, theta2, z2 = csys.rtz(p3)
    e0a = csys.xyz((r1, theta1, 0.5))
    e1a = csys.xyz((r2, theta2, 0.5))
    drawline(color, p1, p0)
    drawline(color, p0, e0a)
    drawline(color, p3, e1a)
    drawline(color, p2, p3)
    drawline(color, p1, p2)
    # Use the existing angle drawing routine to finish up
    drawAngleDimension(color, right, up, bpos,
                       e0a, (p1 + p2) / 2, e1a, text,
                       minR1=r1, minR2=r2, highlighted=highlighted)
