#!/usr/bin/env python

"""
layer interactor.
"""

import numpy as nx
nx.seterr(invalid='raise')  # Make numpy errors raise exceptions

from layer import FlatLayer, SlopeLayer, SplineLayer, JoinLayer, NoLayer
from baseInteractor import _BaseInteractor

# ============== Layer interactors ==============================
# GUI starts here
#================================================================
class LayerInteractor(_BaseInteractor):
    """
    Abstract base class for the layer interactors.
    
    Layers should define:
       set_layer
       move
       save
       restore
       update
    """
    def __init__(self,
                 base,
                 axes,
                 layer,
                 par,
                 color='black'
                 ):
        _BaseInteractor.__init__(self, base, axes, color=color)
        self.layer   = layer
        self.markers = []
        self.par     = par  # The name of the par of this profile



    def Artist2Name( self, label):
        # Obtain Artist name
        ValidParNames = ["mu","rho","theta","phi"]
        name =  label.split("[")[0].strip()

        if name in ValidParNames:
            return  label 
        else:
            return  ""
        

    def  _lookupIndex( self, event ):
    
        try:    idx = self.layerMarker.index(event.artist)
        except: idx = None

        return idx

    
    def  updateRhoValue(self, name, event):
         """ Update the rho layer """
         n = self._save_n
         self.infopanel.updateNLayer( n )
         
         idx = self._lookupIndex( event )
         self.infopanel.updateRhoValue(  event.ydata, idx=idx )


    def  updateMuValue(self, name, event):
         """ Update the mu layer """
         n = self._save_n
         self.infopanel.updateNLayer( n )
         
         idx = self._lookupIndex( event )
         self.infopanel.updateMuValue(  event.ydata, idx=idx )


    def  updatePhiValue(self, name, event):
         """ Update the phi layer """
         n = self._save_n
         self.infopanel.updateNLayer( n )
         
         idx = self._lookupIndex( event )
         self.infopanel.updatePhiValue(  event.ydata, idx=idx )


    def updateThetaValue( self, name, event):

         """ Update the theta layer """
         n = self._save_n
         self.infopanel.updateNLayer( n )
         
         idx = self._lookupIndex( event )
         self.infopanel.updateThetaValue(  event.ydata, idx=idx )


    def setValue(self, event):
        """ Update the layer value """
        _pn = self.Artist2Name( event.artist.get_label() )

        if len(_pn) > 0:
            
           if    _pn[:3] == "rho":   self.updateRhoValue(   _pn, event)
           elif  _pn[:2] == "mu":    self.updateMuValue(    _pn, event)
           elif  _pn[:3] == "phi":   self.updatePhiValue(   _pn, event)
           elif  _pn[:5] == "theta": self.updateThetaValue( _pn, event)
           else:
                raise ValueError("Invalid parmeter")



    def  showRhoValue(self, event):
         """ Show the rho layer """
         n = self._save_n
         self.infopanel.updateNLayer( n )
         
         idx = self._lookupIndex( event )
         self.infopanel.showRhoValue( idx=idx )


    def  showMuValue(self, event):
         """ show the mu layer """
         n = self._save_n
         self.infopanel.updateNLayer( n )
         
         idx = self._lookupIndex( event )
         self.infopanel.showMuValue( idx=idx )


    def  showPhiValue(self, event):
         """ show the phi layer """
         n = self._save_n
         self.infopanel.updateNLayer( n )
         
         idx = self._lookupIndex( event )
         self.infopanel.showPhiValue( idx=idx )


    def  showThetaValue( self, event):
         """ show the theta layer """
         n = self._save_n
         self.infopanel.updateNLayer( n )
         
         idx = self._lookupIndex( event )
         self.infopanel.showThetaValue( idx=idx )


    def showValue(self, event):
        """ Update the layer value """
        _pn = self.Artist2Name( event.artist.get_label() )
 
        if len(_pn) > 0:
             
           if    _pn[:3] == "rho":   self.showRhoValue(  event)
           elif  _pn[:2] == "mu":    self.showMuValue(   event)
           elif  _pn[:3] == "phi":   self.showPhiValue(  event)
           elif  _pn[:5] == "theta": self.showThetaValue(event)
           else:
                raise ValueError("Invalid parmeter name")


            
    #=============================================================        
    def get_Marker(self, i ):
        filled_markers =[ 'o', # '_draw_circle',
                          's', # '_draw_square',
                          'p', # '_draw_pentagon',
                          'd', # '_draw_thin_diamond',
                          'h', # '_draw_hexagon1',
                          '+', # '_draw_plus',
                          'x', # '_draw_x',
                          'D', # '_draw_diamond',
                          'H', # '_draw_hexagon2',
                          'v', #'_draw_triangle_down',
                          '^', # '_draw_triangle_up',
                          '<', # '_draw_triangle_left',
                          '>', # '_draw_triangle_right',
                          '1', # '_draw_tri_down',
                          '2', # '_draw_tri_up',
                          '3', # '_draw_tri_left',
                          '4', # '_draw_tri_right',
                        ]
        return filled_markers[ i%len(filled_markers) ] 
    


#=============================================================
class FlatLayerInteractor(LayerInteractor):
    """
    Interactor for FlatLayer to handle flat slabs.
    """
    def set_layer(self, n):
        """
        Setup the widgets required to edit layer n.
        """
        self.layernum = n
        v  = self.layer._val
        ax = self.axes

        self.layerMarker = ax.plot( [], [],
                                    '--',
                                    label      = self.par,
                                    linewidth  = 2,
                                    color      = self.color, 
                                    pickradius = 5,
                                    zorder     = 5
                                    )[0]
        self.markers = [ self.layerMarker ]

        self.connect_markers(self.markers)
        self.update()


    def update(self):
        """
        Draw the widgets in their new positions.
        """
        model = self.base.model
        n = self.layernum
        x = [ model.offset[n], model.offset[n+self.layer.span] ]
        y = [self.layer._val]*2
        
        #print "x: ", x
        #print "y: ", y
        h = self.markers[0]
        
        h.set_data(x,y)


    def move(self, x, y, ev):
        """
        Update the model with the new widget position.
        """
        self.layer._val = y
        

    def save(self, ev):
        """
        Save the current state of the model represented by the widget.
        """
        self._saved_v = self.layer._val
        

    def restore(self):
        """
        Restore the widget and model to the saved state.
        """
        self.layer._val = self._saved_v



#==============================================================
class SlopeLayerInteractor(LayerInteractor):
    """
    Interactor for SlopeLayer to handle the line control points.

    For slope layer, we use 'p' marker
    """
    def set_layer(self, n):
        """
        Setup the widgets required to edit layer n.
        """
        self.layernum = n

        left, right = self.layer._val
        ax = self.axes

        self.layerMarker = [ ax.plot( [], [],
                       linestyle  = '',
                       markersize = 10,
                       label      = "%s[%d]"%(self.par,i),
                       linewidth  = 2,
                       color      = self.color, 
                       pickradius = 10,
                       zorder     = 3,
                       alpha      = 0.6,
                       marker     = 'p',
                       visible    = False
                       )[0]  for i in xrange( 2 ) ]
        
        slopeLine = ax.plot( [], [],
                       '--',
                       label      = 'slope::line::'+self.par,
                       linewidth  = 2,
                       color      = self.color, 
                       pickradius = 0,
                       zorder     = 5,
                       visible = False
                       )[0]
        

        self.markers = [self.layerMarker[0], self.layerMarker[1]]
        
        self.connect_markers(self.markers)
        self.markers.append( slopeLine )
        
        self.update()



    def update(self):
        """
        Draw the widgets in their new positions.
        """
        model = self.base.model
        n = self.layernum

        # We shift 5 point to avoid overlapping with depth marker
        left_x  = [ model.offset[n]]
        right_x = [ model.offset[n+self.layer.span] ]
        
        left_y  = [self.layer._val[0] ]
        right_y = [self.layer._val[1] ]
        
        leftMarker  = self.markers[0]
        rightMarker = self.markers[1]
        lineMarker  = self.markers[2]

        leftMarker.set( visible=(n>0))
        lineMarker.set( visible=(n>0))
        rightMarker.set(visible=(n>0))
        
        m_x =  [ model.offset[n], model.offset[n+self.layer.span] ]
        m_y =  [self.layer._val[0],  self.layer._val[1] ]
        
        leftMarker.set_data( left_x,  left_y )
        rightMarker.set_data(right_x, right_y)
        lineMarker.set_data( m_x,     m_y    )
        


    def move(self, x, y, ev):
        """
        Update the model with the new widget position.
        """
        model   = self.base.model
        n       = self.layernum
        left_x  = model.offset[n]
        right_x = model.offset[n+self.layer.span] 
        span    = right_x - left_x

        # update left 
        if abs(left_x -x ) / span  <  0.02 :
            self.layer._val[0] = y 

        # update right  
        if abs(right_x -x ) / span  <  0.02 :
           self.layer._val[1] = y 

        # Otherwise: Do Nothing.



    def save(self, ev):
        """
        Save the current state of the model represented by the widget.
        """
        self._saved_v = self.layer._val
        


    def restore(self):
        """
        Restore the widget and model to the saved state.
        """
        self.layer._val = self._saved_v




############################################################################
class SplineLayerInteractor(LayerInteractor):
    """
    Interactor for SplineLayer to handle bspline control points.

    For spline layer, we use "circle" marker
    """
    def set_layer(self, n):
        """
        Setup the widgets required to edit layer n.
        """
        self.layernum = n

        ax = self.axes

        splineLines = [ ax.plot( [], [],
                               '--',
                               label      = 'slope::line::'+self.par,
                               linewidth  = 2,
                               color      = self.color, 
                               pickradius = 0,
                               zorder     = 5,
                               visible = False
                               )[0]  for i in xrange(len(self.layer._val)-1) ]
          
        self.layerMarker = [ax.plot( [], [],
                                 linestyle='',
                                 markersize = 10,
                                 label      = "%s[%d]"%(self.par,i),
                                 linewidth  = 2,
                                 color      = self.color, 
                                 pickradius = 5,
                                 zorder     = 3,
                                 alpha  = 0.6,
                                 marker = 'o',
                                 visible = False
                       )[0]  for i in xrange( len(self.layer._val) ) ]


        # FIXME: use fast way to combine two lists into a single list
        self.markers = []
        for i in xrange( len(self.layerMarker) ):
            self.markers.append(self.layerMarker[i])
        for i in xrange( len(splineLines) ):
            self.markers.append( splineLines[i] )

            
        
        self.connect_markers(self.markers)
        self.update()


    def update(self):
        """
        Draw the widgets in their new positions.
        """
        model = self.base.model
        n = self.layernum
        
        left_x  = model.offset[n]
        right_x = model.offset[n+self.layer.span] 
        span = right_x - left_x

        nv = len( self.layer._val )
        control_z = nx.arange(0.0, nv)/(nv-1.0)*span + left_x
 
        for i in xrange(nv*2-1):
            self.markers[i].set(visible=(n>0))

        #spline Markers      
        for i in xrange(nv):         
            self.markers[i].set_data(control_z[i], self.layer._val[i])

        #spline line
        for i in xrange(nv-1):
            m_x = [ control_z[i],        control_z[i+1]       ]
            m_y = [ self.layer._val[i],  self.layer._val[i+1] ]
            self.markers[i+nv].set_data(m_x, m_y)      

           
    #================================================================
    def move(self, x, y, ev):
        """
        Update the model with the new widget position.
        """
        model = self.base.model
        n = self.layernum
        left_x  = model.offset[n]
        right_x = model.offset[n+self.layer.span] 
        span = right_x - left_x

        nv = len( self.layer._val )
        control_z = nx.arange(0.0, nv)/(nv-1.0)*span + left_x

        idx = -1 
        for i in xrange(nv):        
            if abs(control_z[i]-x ) / span < 0.01 :
                idx = i
                break

        if idx != -1 :
           self.layer._val[idx] = y 


    def save(self, ev):
        """
        Save the current state of the model represented by the widget.
        """
        self._saved_v = self.layer._val
        

    def restore(self):
        """
        Restore the widget and model to the saved state.
        """
        self.layer._val = self._saved_v



###########################################################################
class NoLayerInteractor(LayerInteractor):
    """
    Null Interactor for undefined layers.
    """
    def set_layer(self, n):
        pass

    def update(self):
        pass

    def move(self, x, y):
        pass

    def save(self):
        pass

    def restore(self):
        pass



# ======================== LayerInteractor factory ====================
# Associate layers with layer interactors through function
#     interactor(layer)
            
class _LayerInteractorFactory:
    """
    Given a layer, find the associated interactor.
    """
    def __init__(self):
        self.template = {FlatLayer: FlatLayerInteractor,
                         SlopeLayer: SlopeLayerInteractor,
                         SplineLayer: SplineLayerInteractor,
                         JoinLayer: NoLayerInteractor,
                         NoLayer: NoLayerInteractor
                         }
    def __call__(self,
                 base,
                 axes,
                 layer,
                 par,
                 **kw
                 ):
        if layer.__class__ in self.template:
            return self.template[layer.__class__](base, axes, layer, par,**kw)
        else:
            return NoLayerInteractor(base, axes, layer, par,**kw)
        
Interactor = _LayerInteractorFactory()
