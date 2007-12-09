# Copyright 2006-2007 Brandon Keith  See LICENSE file for details. 
"""
CylinderChunks.py -- define a new whole-chunk display mode,
which shows a chunk as a single opaque bounding cylinder of the chunk's color.

$Id: CylinderChunks.py,v 1.5 2007/07/01 17:27:31 emessick Exp $

This is mainly intended as an example of how to use class ChunkDisplayMode,
though it might be useful as a fast-rendering display mode too.
"""

__author__ = 'bruce'

from Numeric import dot, argmax, argmin, sqrt

import env
import drawer
import geometry
from VQT import V, norm
from debug import print_compact_traceback
from displaymodes import ChunkDisplayMode
from constants import ave_colors
from prefs_constants import atomHighlightColor_prefs_key

chunkHighlightColor_prefs_key = atomHighlightColor_prefs_key # initial kluge

class CylinderChunks(ChunkDisplayMode):
    "example chunk display mode, which draws the chunk as a cylinder, aligned to the chunk's axes, of the chunk's color"
    mmp_code = 'cyl' # this must be a unique 3-letter code, distinct from the values in constants.dispNames or in other display modes
    disp_label = 'CylinderChunks' # label for statusbar fields, menu text, etc
    icon_name = "displayCylinder.png"
    hide_icon_name = "displayCylinder-hide.png"
    featurename = "Set Display Cylinder" #mark 060611
    ##e also should define icon as an icon object or filename, either in class or in each instance
    ##e also should define a featurename for wiki help
    def drawchunk(self, glpane, chunk, memo, highlighted):
        """Draw chunk in glpane in the whole-chunk display mode represented by this ChunkDisplayMode subclass.
        Assume we're already in chunk's local coordinate system
        (i.e. do all drawing using atom coordinates in chunk.basepos, not chunk.atpos).
           If highlighted is true, draw it in hover-highlighted form (but note that it may have
        already been drawn in unhighlighted form in the same frame, so normally the highlighted form should
        augment or obscure the unhighlighted form).
           Draw it as unselected, whether or not chunk.picked is true. See also self.drawchunk_selection_frame.
        (The reason that's a separate method is to permit future drawing optimizations when a chunk is selected
        or deselected but does not otherwise change in appearance or position.)
           If this drawing requires info about chunk which it is useful to precompute (as an optimization),
        that info should be computed by our compute_memo method and will be passed as the memo argument
        (whose format and content is whatever self.compute_memo returns). That info must not depend on
        the highlighted variable or on whether the chunk is selected.
        """
        if not chunk.atoms:
            return
        end1, end2, radius, color = memo
        if highlighted:
            color = ave_colors(0.5, color, env.prefs[chunkHighlightColor_prefs_key]) #e should the caller compute this somehow?
        drawer.drawcylinder(color, end1, end2, radius, capped = True)
        return
    def drawchunk_selection_frame(self, glpane, chunk, selection_frame_color, memo, highlighted):
        """Given the same arguments as drawchunk, plus selection_frame_color, draw the chunk's selection frame.
        (Drawing the chunk itself as well would not cause drawing errors
         but would presumably be a highly undesirable slowdown, especially if redrawing
         after selection and deselection is optimized to not have to redraw the chunk at all.)
           Note: in the initial implementation of the code that calls this method,
        the highlighted argument might be false whether or not we're actually hover-highlighted.
        And if that's fixed, then just as for drawchunk, we might be called twice when we're highlighted,
        once with highlighted = False and then later with highlighted = True.
        """
        if not chunk.atoms:
            return
        end1, end2, radius, color = memo
        color = selection_frame_color
        # make it a little bigger than the cylinder itself
        axis = norm(end2 - end1)
        alittle = 0.01
        end1 = end1 - alittle * axis
        end2 = end2 + alittle * axis
        drawer.drawcylinder_wireframe(color, end1, end2, radius + alittle)
        return
    def compute_memo(self, chunk):
        """If drawing chunk in this display mode can be optimized by precomputing some info from chunk's appearance,
        compute that info and return it.
           If this computation requires preference values, access them as env.prefs[key],
        and that will cause the memo to be removed (invalidated) when that preference value is changed by the user.
           This computation is assumed to also depend on, and only on, chunk's appearance in ordinary display modes
        (i.e. it's invalidated whenever havelist is). There is not yet any way to change that,
        so bugs will occur if any ordinarily invisible chunk info affects this rendering,
        and potential optimizations will not be done if any ordinarily visible info is not visible in this rendering.
        These can be fixed if necessary by having the real work done within class Chunk's _recompute_ rules,
        with this function or drawchunk just accessing the result of that (and sometimes causing its recomputation),
        and with whatever invalidation is needed being added to appropriate setter methods of class Chunk.
        If the real work can depend on more than chunk's ordinary appearance can, the access would need to be in drawchunk;
        otherwise it could be in drawchunk or in this method compute_memo.
        """
        # for this example, we'll turn the chunk axes into a cylinder.
        # Since chunk.axis is not always one of the vectors chunk.evecs (actually chunk.poly_evals_evecs_axis[2]),
        # it's best to just use the axis and center, then recompute a bounding cylinder.
        if not chunk.atoms:
            return None
        axis = chunk.axis
        axis = norm(axis) # needed (unless we're sure it's already unit length, which is likely)
        center = chunk.center
        points = chunk.atpos - center # not sure if basepos points are already centered
        # compare following Numeric Python code to findAtomUnderMouse and its caller
        matrix = geometry.matrix_putting_axis_at_z(axis)
        v = dot( points, matrix)
        # compute xy distances-squared between axis line and atom centers
        r_xy_2 = v[:,0]**2 + v[:,1]**2
        ## r_xy = sqrt(r_xy_2) # not needed

        # to get radius, take maximum -- not sure if max(r_xy_2) would use Numeric code, but this will for sure:
        i = argmax(r_xy_2)
        max_xy_2 = r_xy_2[i]
        radius = sqrt(max_xy_2)
        # to get limits along axis (since we won't assume center is centered between them), use min/max z:
        z = v[:,2]
        min_z = z[argmin(z)]
        max_z = z[argmax(z)]
        bcenter = chunk.abs_to_base(center)
        # return, in chunk-relative coords, end1, end2, and radius of the cylinder, and color.
        color = chunk.color
        if color is None:
            color = V(0.5,0.5,0.5)
        # make sure it's longer than zero (in case of a single-atom chunk); in fact, add a small margin all around
        # (note: this is not sufficient to enclose all atoms entirely; that's intentional)
        margin = 0.2
        min_z -= margin
        max_z += margin
        radius += margin
        return (bcenter + min_z * axis, bcenter + max_z * axis, radius, color)
    pass # end of class CylinderChunks

ChunkDisplayMode.register_display_mode_class(CylinderChunks)

# end
