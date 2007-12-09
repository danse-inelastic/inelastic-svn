# Copyright 2005-2007 Brandon Keith  See LICENSE file for details. 
"""
panMode.py -- pan mode.

$Id: panMode.py,v 1.21 2007/07/01 17:27:32 emessick Exp $
"""
__author__ = "Mark"

from PyQt4.Qt import Qt

from modes import basicMode

class panMode(basicMode):

    # class constants
    modename = 'PAN'
    default_mode_status_text = "Tool: Pan" # Changed 'Mode' to 'Tool'. Fixes bug 1298. mark 060323

    # no __init__ method needed
    
    # methods related to entering this mode

    # init_gui handles all the GUI display when entering this mode [mark 041004
    def init_gui(self):
        self.w.panToolAction.setChecked(1) # toggle on the Pan Tool icon
        self.o.setCursor(self.w.MoveCursor)
        self.w.panDashboard.show()
            
# methods related to exiting this mode

    def haveNontrivialState(self):
        return False

    def StateDone(self):
        return None

    # a safe way for now to override Done:
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
        return basicMode.Done(self, new_mode)
        
    # restore_gui handles all the GUI display when leavinging this mode [mark 041004]
    def restore_gui(self):
        self.w.panToolAction.setChecked(0) # toggle off the Pan Tool icon
        self.w.panDashboard.hide()

    # mouse and key events
    
    def leftDown(self, event):
        'Event handler for LMB press event.'
        # Setup pan operation
        farQ_junk, self.movingPoint = self.dragstart_using_GL_DEPTH( event)
            #bruce 060316 replaced equivalent old code with this new method            
        self.startpt = self.movingPoint # Used in leftDrag() to compute move offset during drag op.
        
    def leftDrag(self, event):
        'Event handler for LMB drag event.'
        point = self.dragto( self.movingPoint, event) #bruce 060316 replaced old code with dragto (equivalent)
        self.o.pov += point - self.movingPoint
        self.o.gl_update()

    def keyPress(self,key):
        # ESC - Exit pan mode.
        if key == Qt.Key_Escape: 
            self.Done()
            
        basicMode.keyPress(self,key) # Fixes bug 1172. mark 060321

    def Draw(self):
        basicMode.Draw(self)   
        self.o.assy.draw(self.o)
         
    def update_cursor_for_no_MB(self): # Fixes bug 1638. mark 060312.
        '''Update the cursor for 'Pan' mode.
        '''
        self.o.setCursor(self.w.MoveCursor)
         
    pass # end of class panMode
