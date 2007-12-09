# Copyright 2005-2007 Brandon Keith  See LICENSE file for details. 
"""
zoomMode.py -- zoom mode.

$Id: zoomMode.py,v 1.38 2007/07/01 17:27:32 emessick Exp $

"""
__author__ = "Mark"

from Numeric import dot

from OpenGL.GL import GL_DEPTH_TEST
from OpenGL.GL import glDisable
from OpenGL.GL import GL_LIGHTING
from OpenGL.GL import glColor3d
from OpenGL.GL import GL_COLOR_LOGIC_OP
from OpenGL.GL import glEnable
from OpenGL.GL import GL_XOR
from OpenGL.GL import glLogicOp
from OpenGL.GL import glFlush
from OpenGL.GL import GL_DEPTH_COMPONENT
from OpenGL.GL import glReadPixelsf
from OpenGL.GLU import gluUnProject

from PyQt4.Qt import Qt

from VQT import V, A
import drawer
from modes import basicMode
from constants import GL_FAR_Z


class zoomMode(basicMode):
    # class constants
    modename = 'ZOOM'
    default_mode_status_text = "Tool: Zoom" # Changed 'Mode' to 'Tool'. Fixes bug 1298. mark 060323
    
    # methods related to entering this mode
    
    def Enter(self):
        basicMode.Enter(self)
        bg = self.o.backgroundColor
                
        # rubber window shows as white color normally, but when the
        # background becomes bright, we'll set it as black.
        brightness = bg[0] + bg[1] + bg[2]
        if brightness > 1.5: self.rbwcolor = bg
        else: self.rbwcolor = A((1.0, 1.0, 1.0)) - A(bg)
        
        self.glStatesChanged = False
        
        
    # init_gui handles all the GUI display when entering this mode [mark 041004
    def init_gui(self):
        self.w.zoomToolAction.setChecked(1) # toggle on the Zoom Tool icon
        self.o.setCursor(self.w.ZoomCursor)
        self.w.zoomDashboard.show()
            
# methods related to exiting this mode

    def haveNontrivialState(self):
        return False

    def StateDone(self):
        return None
        
    # a safe way for now to override Done:
    ## Huaicai: This method must be called to safely exit this mode    
    def Done(self, new_mode = None):
        """[overrides basicMode.Done; this is deprecated, so doing it here
        is a temporary measure for Alpha, to be reviewed by Bruce ASAP after
        Alpha goes out; see also the removal of Done from weird_to_override
        in modes.py. [bruce and mark 050130]
        """
        ## [bruce's symbol to get him to review it soon: ####@@@@]
        if new_mode is None:
            try:
                m = self.o.prevMode # spelling??
                new_mode = m
            except:
                pass
        
        ## If OpenGL states changed during this mode, we need to restore
        ## them before exit. Currently, only the leftDown() will change that.
        if self.glStatesChanged:
            self.o.redrawGL = True
            glDisable(GL_COLOR_LOGIC_OP)
            glEnable(GL_LIGHTING)
            glEnable(GL_DEPTH_TEST)
        
        return basicMode.Done(self, new_mode)
        
            
    # restore_gui handles all the GUI display when leavinging this mode [mark 041004]
    def restore_gui(self):
        self.w.zoomToolAction.setChecked(0) # toggle off the Zoom Tool icon
        self.w.zoomDashboard.hide()

    # mouse and key events
    def leftDown(self, event):
        """Compute the rubber band window starting point, which
             lies on the near clipping plane, projecting into the same 
             point that current cursor points at on the screen plane"""
        self.pWxy = (event.pos().x(), self.o.height - event.pos().y())
        p1 = A(gluUnProject(self.pWxy[0], self.pWxy[1], 0.005)) 
        
        self.pStart = p1
        self.pPrev = p1
        self.firstDraw = True
        
        self.o.redrawGL = False
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glColor3d(self.rbwcolor[0], self.rbwcolor[1], self.rbwcolor[2])
        
        glEnable(GL_COLOR_LOGIC_OP)
        glLogicOp(GL_XOR)
        
        self.glStatesChanged = True
        
        
    def leftDrag(self, event):
        """Compute the changing rubber band window ending point. Erase    the previous window, draw the new window """
        # bugs 1190, 1818 wware 060405 - sometimes Qt neglects to call leftDown before this
        if not hasattr(self, "pWxy") or not hasattr(self, "firstDraw"):
            return
        cWxy = (event.pos().x(), self.o.height - event.pos().y())
        
        if not self.firstDraw: #Erase the previous rubber window
            drawer.drawrectangle(self.pStart, self.pPrev, self.o.up, self.o.right, self.rbwcolor)
        self.firstDraw = False

        self.pPrev = A(gluUnProject(cWxy[0], cWxy[1], 0.005))
        ##draw the new rubber band
        drawer.drawrectangle(self.pStart, self.pPrev, self.o.up, self.o.right, self.rbwcolor)
        glFlush()
        self.o.swapBuffers() #Update display
        
        
    def leftUp(self, event):
        """Erase the final rubber band window and do zoom if user indeed     draws a rubber band window"""
        # bugs 1190, 1818 wware 060405 - sometimes Qt neglects to call leftDown before this
        if not hasattr(self, "pWxy") or not hasattr(self, "firstDraw"):
            return
        cWxy = (event.pos().x(), self.o.height - event.pos().y())
        zoomX = (abs(cWxy[0] - self.pWxy[0]) + 0.0) / (self.o.width + 0.0)
        zoomY = (abs(cWxy[1] - self.pWxy[1]) + 0.0) / (self.o.height + 0.0)

        ##The rubber band window size can be larger than that of glpane.
        ## Limit the zoomFactor to 1.0
        zoomFactor = min(max(zoomX, zoomY), 1.0)
        
        ##Huaicai: when rubber band window is too small,
        ##like a double click, a single line rubber band, skip zoom
        DELTA = 1.0E-5
        if self.pWxy[0] == cWxy[0] or self.pWxy[1] == cWxy[1] or zoomFactor < DELTA: 
                self.o.mode.Done(self.o.prevMode)
                return
        
        ##Erase the last rubber-band window
        drawer.drawrectangle(self.pStart, self.pPrev, self.o.up, self.o.right, self.rbwcolor)
        glFlush()
        self.o.swapBuffers()
        
        winCenterX = (cWxy[0] + self.pWxy[0]) / 2.0
        winCenterY = (cWxy[1] + self.pWxy[1]) / 2.0
        winCenterZ = glReadPixelsf(int(winCenterX), int(winCenterY), 1, 1, GL_DEPTH_COMPONENT)
        
        assert winCenterZ[0][0] >= 0.0 and winCenterZ[0][0] <= 1.0
        if winCenterZ[0][0] >= GL_FAR_Z:  ### window center touches nothing
                 p1 = A(gluUnProject(winCenterX, winCenterY, 0.005))
                 p2 = A(gluUnProject(winCenterX, winCenterY, 1.0))

                 los = self.o.lineOfSight
                 k = dot(los, -self.o.pov - p1) / dot(los, p2 - p1)

                 zoomCenter = p1 + k*(p2-p1)
        else:
                zoomCenter = A(gluUnProject(winCenterX, winCenterY, winCenterZ[0][0]))
        self.o.pov = V(-zoomCenter[0], -zoomCenter[1], -zoomCenter[2]) 
        
        ## The following are 2 ways to do the zoom, the first one 
        ## changes view angles, the 2nd one change viewing distance
        ## The advantage for the 1st one is model will not be clipped by 
        ##  near or back clipping planes, and the rubber band can be 
        ## always shown. The disadvantage: when the view field is too 
        ## small, a selection window may be actually act as a single pick.
        ## rubber ban window will not look as rectanglular any more.
        #zf = self.o.getZoomFactor()
        ##zoomFactor = pow(zoomFactor, 0.25)
        #zoomFactor *= zf
        #self.o.setZoomFactor(zoomFactor)
        
        ##Change viewing distance to do zoom. This works better with
        ##mouse wheel, since both are changing viewing distance, and
        ##it's not too bad of model being clipped, since the near/far clip
        ##plane change as scale too.
        self.o.scale *= zoomFactor
       
        self.Done()

    def keyPress(self,key):
        # ESC - Exit/cancel zoom mode.
        if key == Qt.Key_Escape: 
            self.Done()
            
        basicMode.keyPress(self,key) # Fixes bug 1172. mark 060321
            
    def Draw(self):
        basicMode.Draw(self)
        self.o.assy.draw(self.o)
        ##Make sure this is the last scene draw
        #if self.rbw: 
                #self.RBWdraw() # Draw rubber band window.
     
       
    def RBWdraw(self):
        """Draw the rubber-band window. 
        """
        drawer.drawrectangle(self.pStart, self.pPrev,
                                 self.o.up, self.o.right, self.rbwcolor)
         
    def update_cursor_for_no_MB(self): # Fixes bug 1638. mark 060312.
        '''Update the cursor for 'Zoom' mode.
        '''
        self.o.setCursor(self.w.ZoomCursor)

    pass # end of class zoomMode
