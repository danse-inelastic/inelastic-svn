#!/usr/bin/env python

"""
Reflectometry profile interactor.
"""
from matplotlib import transforms
import numpy as nx
nx.seterr(invalid='raise')  # Make numpy errors raise exceptions

from reflutils import twinx, interface_color, disable_color, active_color, \
                      rho_color, mu_color, P_color, theta_color, profile_colors
from binder         import BindArtist
from baseInteractor import _BaseInteractor


# ============== Interface  interactors ================
# GUI starts here
#=======================================================
class InterfaceInteractor(_BaseInteractor):
    """
    Control the size of the layers.
    """
    def __init__(self, base,axes, color=interface_color):
        _BaseInteractor.__init__(self, base, axes, color=color)
        self.markers  = []
        self.textmark = []
        self.axes     = axes
        self.xcoords  = transforms.blend_xy_sep_transform(axes.transData,
                                                          axes.transAxes)
        self.reset_layers()

        
    def reset_layers(self):
        """Reset all markers."""
        ax    = self.axes
        model = self.base.model

        self._clear_markers()
        self.markers = [ ax.axvline(x=z,
                                    linewidth=1,
                                    linestyle='-',
                                    label='interface %g'%( model.find(z) ),
                                    color=self.color,
                                    alpha=0.5,
                                    pickradius=2
                                    #pickradius=8     # 8  is too big
                                    ) for z in model.offset[1:-1]
                        ]
        self.markers[0].set(linestyle=':')
        self.connect_markers(self.markers[1:])        

        if model.names:
            self._set_text()



    def refresh(self): 
        """
        Refreah all markers.

        Also we clear up all the connects with the markers 
        """
        if  self.markers:
            self.base.connect.clear(*self.markers)

        self.reset_layers()
        

            
    def _set_text(self):
        """
        Place the layer names on the graph mid way between the interfaces.
        The incident layer name is placed just before the first interface,
        and the substrate name is placed just after the last interface.
        """
        ax    = self.axes
        model = self.base.model

        self.textmark = [ ax.text(model.offset[i]+model.depth[i]/2.0, 1.00,
                                  s, 
                                  transform=self.xcoords, 
                                  ha='left',
                                  va='bottom',
                                  rotation=30,
                                  fontsize=10
                                  #bbox=dict(facecolor='yellow', alpha=0.2)
                                  )  for i,s in enumerate(model.names)
                         ]

        pos =  ax.get_xlim()
        ax.set_xlim( (pos[0], pos[1]+200) )
        #self.textmark[ 0].set(x = -10,              ha = 'right')
        #self.textmark[-1].set(x = model.offset[-1], ha = 'left' )


    def _clear_markers(self):
        """Remove interfaces and layer names from the graph."""
        for h in self.markers:
            h.remove()
        for h in self.textmark:
            h.remove()
        self.textmark=[]


    def clear(self):
        """Remove interfaces and layer names from the graph."""
        self.clear_markers()
        for i in xrange( len(self.textmark) ):
             self.textmark[i].remove()
             

    def update(self):
        """Draw the new interfaces on the graph."""
        model = self.base.model
        
        for i,h in enumerate(self.markers):
            h.set_xdata( [ model.offset[i+1], model.offset[i+1] ] )
        if self.textmark:
            for i,h in enumerate( self.textmark[1:-1] ):
                # Note: using i+1 because skipping the incident layer label
                  
                #h.set_x( model.offset[i+1] + model.depth[i+1]/2 )
                if model.depth[i+1] <=8:
                   if  model.depth[i+2] <=8 and  model.depth[i]>=8 :  
                       h.set_x( model.offset[i+1]-6 )
                   else:
                       h.set_x( model.offset[i+1] + model.depth[i+1]/2.0 )
                else:
                   h.set_x( model.offset[i+1] + model.depth[i+1]/2 )
                   
            self.textmark[-1].set_x( model.offset[-2]+5 )


    def save(self, ev):
        """
        Remember the depths for this layer and the next so that we
        can drag interfaces and restore on Esc.
        """
        #self._save_n = self.markers.index(ev.artist)
        #self._save_d = self.base.model.depth[self._save_n]
        #if self._save_n     < self.base.model.numlayers:
        #   self._save_dnext = self.base.model.depth[self._save_n+1]
        self.base.freeze_axes()

            
    def restore(self):
        """Restore the depths for this layer and the next."""
        try:
            model = self.base.model
            model.depth[self._save_n] = self._save_d
            if self._save_n < model.numlayers:
                model.depth[self._save_n+1] = self._save_dnext
        except:
            pass

    
    def move(self, x, y, ev):
        """
        Process move to a new position, making sure that the move is allowed.
        """
        model = self.base.model
        n = self._save_depth_n
        lo = model.offset[n]

        #if ev.shift and n < model.numlayers:
        
        if 0:
            # Drag interface (unless it is the last one)
            hi = model.offset[n+2]
            # Make sure we aren't dragging below the previous or above the next
            if x < lo:
                model.depth[n] = 0
                model.depth[n+1] = self._save_d + self._save_dnext
            elif x > hi:
                model.depth[n]   = self._save_d + self._save_dnext
                model.depth[n+1] = 0
            else:
                model.depth[n  ] = x - lo
                model.depth[n+1] = self._save_d+self._save_dnext-model.depth[n]
        else:
            # Drag layer
            #if  abs(x-lo)< model.rough[n-1]+model.rough[n]:
            min_depth = 5
            max_depth = 10000
            
            if  abs(x-lo) <  min_depth:  # Too samll
                #model.depth[n] = model.depthLo[n]
                return True
            
            if  abs(x-lo) >= max_depth: # Too Big
                model.depth[n] = max_depth
                return True
            
            if x < lo:  model.depth[n] = lo - x
            else:       model.depth[n] = x - lo


    def moveend(self, ev):
        self.base.thaw_axes()



    #=====================================
    def  XData2LayerDepth( self,n, x ):
         # Get the depth of layer n
         val = self.model.offset[n+1] - self.model.offset[n]  
         return val


    def  XData2LayerCoords( self, x, direction ):
         # Translate the xdata into Layer Coords.
         n   = self.base.model.find( x )
         if direction == "right":
            val = abs(  x - self.model.offset[n+1] )
         else:
            val = abs(  x - self.model.offset[n]   )
            
         return val


    def  BestDepthLayerNum(self, x):
         n = self.model.find( x )
         if abs(self.model.offset[n+1]-x)<3:
             ret = n
         else:
             ret = n-1
         if ret < 0 : return 0
         else:        return ret


    def Artist2Name( self, label):
        # Obtain Artist name
        if len(label) > 9:
            return "depth"

        return ""


    def updateValue(self, event):
        """
        Update the depth Value in Infopanel and refresh model
        We don't use this function, keep it for later use
        If we don't use it at final version, just remove it
        """
        n = self.BestDepthLayerNum(event.xdata)
        self._save_depth_n = n
        self.infopanel.updateNLayer( n )

        _pn = self.Artist2Name( event.artist.get_label() )
        if len(_pn) > 0:
            pass 
            self.infopanel.updatePN( _pn )

        val = self.XData2LayerDepth( n, event.xdata )
        self.infopanel.updateDepthValue( val )


    def showValue(self, event):
        """Show the depth Value""" 
        n = self.BestDepthLayerNum(event.xdata)
        self._save_depth_n = n
        self.infopanel.updateNLayer( n )

        self.infopanel.showDepthValue(  )


    def setValue(self, event):
        """ Set the depth Value """
        n = self._save_depth_n
        self.infopanel.updateNLayer( n )

        val = self.XData2LayerDepth( n, event.xdata )
        self.infopanel.updateDepthValue( val )     
