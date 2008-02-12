#!/usr/bin/env python

"""
Basic interactor for Reflectometry profile.
"""

import numpy as nx
nx.seterr(invalid='raise')  # Make numpy errors raise exceptions

from reflutils  import active_color
from matplotlib import transforms


# ============== Base interactors ==============================
# GUI starts here
# Other interactor will inherit this

class _BaseInteractor:
    """
    Abstract base class for someone who use interactor
    
    Share some functions between the interface interactor and various layer
    interactors.
    
    Individual interactors need the following functions:
    
        save(ev)  - save the current state for later restore
        restore() - restore the old state
        move(x,y,ev) - move the interactor to position x,y
        moveend(ev) - end the drag event
        update() - draw the interactors
        
    The following are provided by the base class:
    
        connect_markers(markers) - register callbacks for all markers
        clear_markers() - remove all items in self.markers
        onHilite(ev) - enter/leave event processing
        onLeave(ev) - enter/leave event processing
        onClick(ev) - mouse click: calls save()
        onRelease(ev) - mouse click ends: calls moveend()
        onDrag(ev) - mouse move: calls move() or restore()
        onKey(ev) - keyboard move: calls move() or restore()
        
    Interactor attributes:
    
        base  - model we are operating on
        axes  - axes holding the interactor
        color - color of the interactor in non-active state
        markers - list of handles for the interactor
    """
    def __init__(self,base,axes,color='black'):
        self.base  = base
        self.axes  = axes
        self.color = color
        self._save_n       = 0
        self._save_depth_n = 0 
        self.infopanel = base.parent.infopanel
        self.model     = base.model
        self.click_flag = 0
        
    def clear_markers(self):
        '''
        Clear old markers and interfaces.
        '''
        for h in self.markers:
            h.remove()
        if self.markers:
            self.base.connect.clear(*self.markers)
        self.markers = []


    #======================================
    def save(self, ev):
        pass
    
    def restore(self, ev):
        pass
    
    def move(self, x, y, ev):
        pass
    
    def moveend(self, ev):
        pass

    def updateValue(self, event):
        pass

    def setValue(self, event):
        pass

    def Artist2Name(self, event):
        pass    
    #=====================================

         
    def  BestDepthLayerNum(self, x):
         n = self.model.find( x )
         if abs(self.model.offset[n+1]-x)<3:
             ret = n
         else:
             ret = n-1
         if ret < 0 : return 0
         else:        return ret


    def connect_markers(self,markers):
        """
        Connect markers to callbacks
        """
        for h in markers:
            connect = self.base.connect
            connect('enter',   h, self.onHilite)
            connect('leave',   h, self.onLeave)
            connect('click',   h, self.onClick)
            connect('release', h, self.onRelease)
            connect('drag',    h, self.onDrag)
            connect('key',     h, self.onKey)


    def onHilite(self, event):
        """
        Hilite the artist reporting the event, indicating that it is
        ready to receive a click.
        """
        event.artist.set_color(active_color)
        self.base.draw()
        
        return True


    def onLeave(self, event):
        """
        Restore the artist to the original colour when the cursor leaves.
        """
        event.artist.set_color(self.color)
        self.base.draw()
        self.click_flag = 0  
        
        return True
            

    def onClick(self, event):
        """
        Prepare to move the artist.  Calls save() to preserve the state for
        later restore().
        """
        self.click_flag = 1
        self.clickx = event.xdata
        self.clicky = event.ydata
        self.save(event)

        # update the parameter name in info panel if necessary
        transform = event.artist.get_transform()
        x = event.x
        y = event.y
        x,y = transform.inverse_xy_tup( (x,y) )
        event.xdata = x
        event.ydata = y
        #============================================ 

        # Here we just show the parameter. Change nothing to model
        self._save_n = self.base.model.find( event.xdata )
        self.showValue(event)

        
        return True



    def onRelease(self, event):
        #self.updateValue(event)

        self.moveend(event)
        self.click_flag = 0   
        return True



    def onDrag(self, event):
        """
        Move the artist.  Calls move() to update the state, or restore() if
        the mouse leaves the window.
        """
        inside,prop = self.axes.contains(event)
        if inside:
            self.clickx = event.xdata
            self.clicky = event.ydata
            
            if self.click_flag ==0:
               self._save_depth_n =  self.BestDepthLayerNum(event.xdata) 

            self.move(event.xdata, event.ydata, event)

            # update the parameter name in info panel if necessary
            #self.updatePN(event)

            # set the parameter            
            self.setValue(event)
        else:
            self.restore()
            
        self.base.update()
        self.base.parent.modelPanel.OnUpdateModelMenu(event) 
        self.click_flag ==0
        
        return True

    

    def onKey(self, event):
        '''
        Respond to keyboard events.  Arrow keys move the widget.  Escape
        restores it to the position before the last click.
        
        Calls move() to update the state.  Calls restore() on escape.
        '''
        if event.key == 'escape':
            self.restore()
        elif event.key in ['up', 'down', 'right', 'left']:
            dx,dy = self.dpixel(self.clickx,self.clicky,nudge=event.control)
            if   event.key == 'up':    self.clicky += dy
            elif event.key == 'down':  self.clicky -= dy
            elif event.key == 'right': self.clickx += dx
            else: self.clickx -= dx
            self.move(self.clickx, self.clicky, event)
        else:
            return False
        
        self.base.update()
        
        return True



    def dpixel(self,x,y,nudge=False):
        '''
        Return the step size in data coordinates for a small
        step in screen coordinates.  If nudge is False (default)
        the step size is one pixel.  If nudge is True, the step
        size is 0.2 pixels.
        '''
        ax = self.axes
        px,py = ax.transData.inverse_xy_tup((x,y))
        if nudge:
            nx,ny = ax.transData.xy_tup((px+0.2,py+0.2))
        else:
            nx,ny = ax.transData.xy_tup((px+1.,py+1.))
        dx = nx-x
        dy = ny-y
        return dx,dy

