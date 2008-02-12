
#!/usr/bin/env python

"""
Reflectometry profile interactor.
"""

import numpy as nx
nx.seterr(invalid='raise')  # Make numpy errors raise exceptions

from reflutils import twinx, interface_color, disable_color, active_color, \
                      rho_color, mu_color, P_color, theta_color, \
                      profile_colors, profile_pars

from binder              import BindArtist
from layerInteractor     import Interactor
from interfaceInteractor import InterfaceInteractor
from roughnessInteractor import RoughnessInteractor
from listener   import Listener
from Fit        import Fit


# ================== Main profile interactor =====================
class ReflectometryInteractor:
    """Reflectometry profile editor"""

    def __init__(self,
                 ax,
                 model,
                 listener,
                 parent
                 ):
        self.listener = listener
        self.ax       = ax
        self.parent   = parent
        
        # Theta needs a separate axis, we put these two axes into a figure
        if model.magnetic:
            self.ax2 = twinx( self.ax )
        else:
            self.ax2 = None
      
        self.ax.set_xlabel( r'$\rm{z}\ (\angstrom)$' )
        if model.magnetic:
            self.ax.set_ylabel( r'$\rm{Density}\ \times 10^{-6}\ \ \rho,\  \mu,\  \rho_M$')
        else:
            self.ax.set_ylabel(r'$\rm{Density}\ \times 10^{-6}\ \ \rho,\  \mu$')
        
        if model.magnetic:
           self.ax2.set_ylabel(r'$\rm{Magnetic\ Angle\ (\ ^\circ)}$')

        # TODO: the connect mechanism needs to be owned by the canvas rather
        # than the axes --- cannot have multiple profiles on the same canvas
        # until connect is in the right place.
        
       
        self.connect = BindArtist( ax.figure )
       
        #Clear connections to all artists.
        self.connect.clearall()
        self.connect('motion',ax,         self.onMotion )
        self.connect('click', ax.figure,  self.onContext)

        #ax.figure.canvas.mpl_connect('motion_notify_event',self.onMotion)

        # Add model 
        self.model = model

        # Add interactor for Interface
        self.interface = InterfaceInteractor(self,ax)
        
        # Add interactor for Roughness
        self.roughness = RoughnessInteractor(self,ax)
        
        self.profiles    = []
        self.layernum    = None
        self.axes_frozen = False
        
        # Add some plots
        [self.hrho] = ax.plot([],[],'-',color=rho_color,label=r'$\rho$')
        [self.hmu ] = ax.plot([],[],'-',color=mu_color, label=r'$\mu$' )

        # Add some legend
        if self.model.magnetic:
            #More plots in magnetic case
            [self.hP    ] = self.ax.plot(  [], [], '-', color=P_color,
                                           label = r'$\rho_M$')
            [self.htheta] = self.ax2.plot( [], [], '-', color=theta_color,
                                           label = r'$\theta$')
            
            self.hlegend = self.ax.legend(
                               (self.hrho, self.hmu, self.hP, self.htheta),
                               #('SLD','Absorption','Mag. SLD','Mag. angle'),
                               (r'$\rho$', r'$\mu$', r'$\rho_M$', r'$\theta$'),
                               loc='upper right'
                               )
        else:
            self.hlegend = self.ax.legend( (self.hrho, self.hmu),
                                           (r'$\rho$', r'$\mu$'),
                                           loc='upper right'
                                           )
        self.hlegend.get_frame().set( alpha=0.2, facecolor='yellow' )

        # update the figure 
        self.update()
        

    def onMotion(self, event):
        """Respond to motion events by changing the active layer."""
        # Find the layer containing the  event.xdata 
        Layer_num = self.model.find(event.xdata)
        
        #self.parent.infopanel.update(Layer_num)
        self.parent.modelPanel.update(Layer_num)
        
        self.set_layer( Layer_num )
        
        return False


    def onContext(self, ev):
        """Context menu (eventually ...)."""
        return False


    def set_layer(self, n):
        """Make layer n the active layer."""
        # Check if the markers are already set
        if n == self.layernum:
            return
        self.layernum = n
        
        # Clear the old markers
        for interactor in self.profiles:
            interactor.clear_markers()
        
        # Reset the profile interactors to those appropriate for the layer type
        if self.model.magnetic:
           axes = [self.ax]*3 + [self.ax2]  # ax ax ax ax2
        else:  #nonmagnetic case
           axes = [self.ax]*2  
        self.profiles = [ Interactor(self,ax,L,p, color=c) 
                              for ax,c,p, L in zip(axes,
                                                   profile_colors,
                                                   profile_pars,
                                                   self.model[n])
                         ]
        #print len(self.profiles)
        for interactor in self.profiles:
            interactor.set_layer(n)

        # Move  the roughness markers for the interface
        self.roughness.set_layer(n)
        #self.ylim = 0, 100
        self.draw()


    def update(self):
        """
        Respond to changes in the model by recalculating the profiles and
        resetting the widgets.
        """
        # We are done the manipulation; let the model send its update signal
        # to whomever is listening.
        self.listener.signal('update',self)

        # Update locations
        self.model.calc_offsets()
        for interactor in self.profiles:
            interactor.update()
        self.interface.update()
        self.roughness.update()

        # Update profile
        z,p = self.model.calc(n=400)
        self.hrho.set_data(z,p[0])
        self.hmu.set_data(z,p[1])
        self.hmu.set_visible(self.model.absorbing)
        
        if self.model.magnetic:
            self.hP.set_data(z,p[2])
            self.htheta.set_data(z,p[3])
            self.hP.set_visible(self.model.magnetic)
            self.htheta.set_visible(self.model.magnetic)

        
        # Compute automatic y limits
        # Note: theta limits are on ax2

        # The ylim of marker for spline layer, etc
        m = self.model.calcMarker()

        if self.model.magnetic:
           lo = min( p[0].min(), p[1].min(), p[2].min(), m[0] )
           hi = max( p[0].max(), p[1].max(), p[2].max(), m[1] )
           fluff     = 0.1*(hi-lo)
           self.ylim = lo-fluff, hi+fluff
        else:
           lo = min( p[0].min(), p[1].min(), m[0] )
           hi = max( p[0].max(), p[1].max(), m[1] )
           fluff     = 0.05*(hi-lo)
           self.ylim = lo-fluff, hi+fluff 

        self.ax.set_ylim(lo-fluff, hi+fluff)
        
        # Compute reflectivity
        self.draw()


    def freeze_axes(self):
        self.axes_frozen = True
        

    def thaw_axes(self):
        self.axes_frozen = False
        

    def draw(self):
        """Set the limits and tell the canvas to render itself."""
        # TODO: Stop doing surprising things with limits
        # TODO: Detect if user is zoomed, and freeze limits if that is the case

        if not self.axes_frozen:
            #_xspans = self.model.offset[-1] - self.model.offset[0] 
            #self.ax.set_xlim(self.model.offset[0 ] - _xspans*0.05,
            #                 self.model.offset[-1] + _xspans*0.05
            #                 )
            self.ax.set_xlim(self.model.offset[0 ],
                             self.model.offset[-1]
                             )
            self.ax.set_ylim(*self.ylim)
            if self.model.magnetic:
               self.ax2.set_ylim(0,360)

        self.ax.figure.canvas.draw_idle()




# ================ Example program ===========================
def demo():
    import pylab
    # Names for the layers, including incident medium and substrate
    names = [ r"Si", r"Fe_2O_3", r"Fe", r"Thiol", r"D_2O" ]
    
    # Depths for the layers, excluding incident medium and substrate
    d = [100, 120, 180]
    
    # Profile definitions
    rho   = [2.07, 3, 8, -1, 5.76]
    mu    = [0, 0, 2, 0, 1]
    P     = [0, 0, 5, 0, 0]
    theta = [0, 0, 270, 0, 0]
    rough = [30,10,20,30]
    
    model = Profile(depth=d,
                    rho=rho,
                    mu=mu,
                    phi=P,
                    theta=theta,
                    rough=rough,
                    names=names
                    )
    
    # Turn the model into a user interface
    listener = Listener()
    profile = ReflectometryInteractor(pylab.subplot(111), model, listener)
    fit = Fit([profile])
    listener.connect("update",profile,fit.update)
    pylab.show()
    print "d2 = ",model.depth[2]
    
if __name__ == "__main__": demo()
