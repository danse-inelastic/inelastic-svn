#!/usr/bin/env python

import os, wx, wx.aui
import numpy as nx

import matplotlib
from matplotlib.figure   import Figure
from matplotlib.axes     import Subplot
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import FigureManager
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg

from datadQ import DatadQ
from reflInteractor import  ReflectometryInteractor, Listener
from Fit      import Fit
from listener import Listener
from profile  import Profile

from reflutils import CheckValid, showErrorMsg, clear_axes, tFloat, isfactory
from reflutils import bspline, isvector, BSpline, spline, slope, Slope, \
                      decodeP, filterP

from addLayerDialog        import AddLayerDialog
from changeProfileDialog   import ChangeProfileDialog
from changeLayernameDialog import ChangeLayernameDialog
from changeMetaDataDialog  import ChangeMetaDataDialog
from initModelDialog       import InitModelDialog,InitModelDialogNM
from removeLayerDialog     import RemoveLayerDialog
from saveModelDialog       import SaveModelDialog, SaveModelDialog2
from addData2XML    import addStrData
from getData2XML    import getStrData
from str2Data       import load_inline, Data2Str
from parseReflModel import ReflModel, ParkFit
from layer import Layer

import parseReflModel


from auiPanel import AuiPanel

# Translate  STAJ file into model
from staj2model import Staj2Model, Staj2MModel

from miscRefl import lookUpModelName, parseProfile, parseProfileValue, \
     parseStaj, getDataTxt, parseMStaj, _toPyScriptM, _toPyScript, \
     isStajModelType

from reflTheory import ReflParameter, ReflParameterMag
from modelEvent  import MODEL_UPDATE, MODEL_ADD, MODEL_REMOVE, MODEL_UPDATE_META
 
#=================================================================
# TODO: Add other layer operation, eg: layerFine
[
 wxID_Init_Model,
 wxID_Init_Model_NM,  
 wxID_Load_Model,
 wxID_Load_Model_From_XML,   
 wxID_Add_Layer,
 wxID_Remove_Layer,
 wxID_Save_Model,
 wxID_Export_Model,
 wxID_Export_Model_Staj,
 wxID_Update_Model,
 wxID_Clear_Model,
 wxID_Save_Fig,
 wxID_Change_LayerName,
 wxID_Change_Profile,
 wxID_Change_MetaData,
 wxID_Load_Staj,
 
] = [ wx.NewId() for item in range(16) ]



#==================================================================
class ReflPanel(AuiPanel):

    def __init__( self, parent, size=(400,300) ):
        
        super(ReflPanel, self).__init__(parent, id=-1, size=size)

        # This make sure we can communicate between different panels.  
        self.parent = parent      
    
        # Turn the model into a user interface
        self.listener = Listener()
        
        self.fig = Figure( figsize   = (8,6),
                           dpi       = 75,
                           facecolor = 'white',
                           edgecolor = 'white',
                           )
        self.canvas   = FigureCanvas(self, -1, self.fig)
        self.fig.set_canvas(self.canvas)        
        self.fig.add_axes( Subplot(self.fig, 111) )

        # Create a figure manager to manage things
        self.figmgr = FigureManager( self.canvas, 1, self )
           
        self.sizer = wx.BoxSizer( wx.VERTICAL )
        self.sizer.Add( self.canvas,1, border=2, flag= wx.LEFT|wx.TOP|wx.GROW)
        self.SetSizer( self.sizer)  
        self.Fit()

        self._createMenu()
            
        self.canvas.Bind( wx.EVT_LEFT_DCLICK, self.OnLeftDClick     )
        self.canvas.Bind( wx.EVT_RIGHT_DOWN,  self.OnPanelRightDown )

        # Model Data
        self._data    = None
        self._dataStr = ""
        self.current_layer = None

        #meta data
        self.wavelength= 4.75
        self.wavelengthDiv= 0.021
        self.angularDiv = 7e-4
        self.background = 1.0e-10
        self.dtheta1 = 7e-4
        self.dtheta2 = 7e-4
        self.dvtheta = 7e-4
        self.Q1 = 0.0
        self.Q2 = 10000
        #Staj
        self.nTLayers = 2
        self.nMLayers = 7
        self.nBLayers = 1
         
        # Show toolbar or not?
        self.toolbar = NavigationToolbar2WxAgg( self.canvas )
        self.toolbar.Show(False)
        self.LoadJobFlag=0
 
        
    def _initModel( self,
                    names = None,
                    depth = None,
                    rough = None,
                    rho   = None,
                    mu    = None,
                    phi   = None,
                    theta = None
                    ):
        """
        Initialize mode by profile
        """
        if len(names) == 0: 
            raise ValueError("must support the incident and substrate layer")
       
        self.model = Profile( names = names,
                              depth = depth,
                              rough = rough,
                              rho   = rho,
                              mu    = mu,
                              phi   = phi,
                              theta = theta
                              )
    
        # Turn the model into a user interface
        self.axes    = self.fig.get_axes()[0]

        self.profile = ReflectometryInteractor( self.axes,
                                                self.model,
                                                self.listener,
                                                self.parent
                                               )
        fit = Fit( [self.profile] )
        self.listener.connect("update", self.profile, fit.update)

        # Need update 
        self.model.refresh()
        self.profile.interface.refresh()
        self.profile.update()
        

    def _Disable(self):
        """ Disable some menu choices """
        self.editMenu.Enable(wxID_Add_Layer,        False)
        self.editMenu.Enable(wxID_Remove_Layer,     False)
        self.editMenu.Enable(wxID_Save_Model,       False)
        self.editMenu.Enable(wxID_Clear_Model,      False)
        self.editMenu.Enable(wxID_Change_LayerName, False)
        self.editMenu.Enable(wxID_Change_MetaData,  False)
        self.editMenu.Enable(wxID_Change_Profile,   False)
        self.editMenu.Enable(wxID_Save_Fig,         False)

        
    def _createMenu(self):
        """  popup menus """        
        menu = wx.Menu(title=u'Edit Model')

        menu.Append( help='',  id=wxID_Init_Model_NM,    kind=wx.ITEM_NORMAL,
                     text=u'&Init Model(Non Magnetic)...' )
        menu.Append( help='',  id=wxID_Init_Model,       kind=wx.ITEM_NORMAL,
                     text=u'&Init Model(Magnetic)...' )

        menu.AppendSeparator()
        
        menu.Append( help='',  id=wxID_Add_Layer,        kind=wx.ITEM_NORMAL,
                     text=u'&Add Layer ...' )
        menu.Append( help='',  id=wxID_Remove_Layer,     kind=wx.ITEM_NORMAL,
                     text = u'&Remove Layer ...')

        menu.AppendSeparator()
        
        menu.Append( help='',  id=wxID_Change_Profile,   kind=wx.ITEM_NORMAL,
                     text=u'&Change Profile Within Layer...')                 
        menu.Append( help='',  id=wxID_Change_LayerName, kind=wx.ITEM_NORMAL,
                     text=u'&Change Layer Name ...')
        menu.Append( help='',  id=wxID_Change_MetaData,  kind=wx.ITEM_NORMAL,
                     text=u'&Change MetaData...')

        menu.AppendSeparator()
        
        menu.Append( help='',  id=wxID_Load_Model,       kind=wx.ITEM_NORMAL,
                     text=u'&Load Model ...')
        menu.Append( help='',  id=wxID_Load_Staj,        kind=wx.ITEM_NORMAL,
                     text=u'&Load Staj ...')
        
        menu.AppendSeparator()
        
        menu.Append( help='',  id=wxID_Save_Model,       kind=wx.ITEM_NORMAL,
                     text=u'&Save Model(python)...')
        menu.Append( help='',  id=wxID_Clear_Model,      kind=wx.ITEM_NORMAL,
                     text=u'&Clear Model ...')

        menu.AppendSeparator()
        
        menu.Append( help='',  id=wxID_Save_Fig,         kind=wx.ITEM_NORMAL,
                     text=u'&Save Figure ...')
        
        menu.AppendSeparator()

        #===================
        self.Bind(wx.EVT_MENU, self.OnInitModelMenu,   id=wxID_Init_Model)
        self.Bind(wx.EVT_MENU, self.OnInitModelNMMenu, id=wxID_Init_Model_NM)
        self.Bind(wx.EVT_MENU, self.OnAddLayerMenu,    id=wxID_Add_Layer)
        self.Bind(wx.EVT_MENU, self.OnRemoveLayerMenu, id=wxID_Remove_Layer)
        self.Bind(wx.EVT_MENU, self.OnSaveFigureMenu,  id=wxID_Save_Fig)
        self.Bind(wx.EVT_MENU, self.OnLoadModelMenu,   id=wxID_Load_Model)
        self.Bind(wx.EVT_MENU, self.OnLoadStajMenu,    id=wxID_Load_Staj)
        self.Bind(wx.EVT_MENU, self.OnSaveModelMenu,   id=wxID_Save_Model)
        self.Bind(wx.EVT_MENU, self.OnClearModelMenu,  id=wxID_Clear_Model)

        self.Bind(wx.EVT_MENU, self.OnChangeLayerNameMenu,
                  id=wxID_Change_LayerName)
        
        self.Bind(wx.EVT_MENU, self.OnChangeProfileLayerMenu,
                  id=wxID_Change_Profile)

        self.Bind(wx.EVT_MENU, self.OnChangeMetaDataMenu,
                  id=wxID_Change_MetaData)

        
        self.editMenu = menu

        self._Disable()


    def _updateScalarValue(self, pm, Pname, val):

        if   Pname == "depth":
             if pm.depth  != val:    pm.depth = val
        elif Pname == "rough":            
             if  pm.rough != val:    pm.rough = val
        elif Pname == "rho":            
             if  pm.rho   != val:    pm.rho = val
        elif Pname == "mu":
             if  pm.mu    != val:    pm.mu = val
        elif Pname == "phi":
             if  pm.phi   != val:    pm.phi = val
        elif Pname == "theta":
             if  pm.theta != val:    pm.theta = val
        else:
            pass
        
    

    def _updateFactoryValue(self, pm, Pname, idx, val):

        if   Pname == "rho":
             _pm = decodeP( pm.rho )
             _pm._valList[idx] = val
             pm.rho  = _pm.build()
             
        elif Pname == "mu":
             _pm = decodeP( pm.mu )
             _pm._valList[idx] = val
             pm.mu  = _pm.build()
             
        elif Pname == "phi":
             _pm = decodeP( pm.phi )
             _pm._valList[idx] = val
             pm.phi  = _pm.build()

        elif Pname == "theta":
             _pm = decodeP( pm.theta )
             _pm._valList[idx] = val
             pm.theta  = _pm.build()
             
        else:  pass
        
    
    def _updateScalarViewer( self, Pname, nLayer, val):

        n = nLayer
        if   Pname == "depth":  self.model.depth[ n]      = val
        elif Pname == "rough":  self.model.rough[ n]      = val
        elif Pname == "rho":    self.model.Lrho[  n]._val = val
        elif Pname == "mu":     self.model.Lmu[   n]._val = val
        elif Pname == "phi":    self.model.Lphi[  n]._val = val
        elif Pname == "theta":  self.model.Ltheta[n]._val = val
        else:  pass 

        
    def _updateFactoryViewer( self, Pname, nLayer, idx, val):

        n = nLayer
        if   Pname == "rho":    self.model.Lrho[  n]._val[idx] = val
        elif Pname == "mu":     self.model.Lmu[   n]._val[idx] = val
        elif Pname == "phi":    self.model.Lphi[  n]._val[idx] = val
        elif Pname == "theta":  self.model.Ltheta[n]._val[idx] = val
        else:  pass


    def UpdateViewer(self, names, value):
        ( LName, PName ) = names
        for i in xrange(len(self.model.names)):
            if LName == self.model.names[i]:
                nLayer = i
                break
            
        pm = self.parent.model.getChild( LName  )
         
        _pars = PName.split('_')
        if len(_pars) == 1:
            self._updateScalarValue( pm, PName, value)
            self._updateScalarViewer( _pars[0].strip(), nLayer, value)

        else:
            self._updateFactoryValue(pm,
                                     _pars[0].strip(),
                                     int( _pars[-1].strip() ),
                                     value
                                     )
            self._updateFactoryViewer(_pars[0].strip(),
                                      nLayer,
                                      int( _pars[1].strip() ), 
                                      value
                                      )
        #update refl builder
        self.model.refresh()
        self.profile.update()

    
    def SetModel(self, model):
    
        if self.LoadJobFlag == 1 : return
        
        try:
            _pms =  model.getXmlParameters()
        except:
            return

        if _pms == None or len(_pms) == 0:   return
        
        self.LoadJobFlag = 1
        
        _names=[]; _depth=[]; _rough=[]; _rho=[]; _mu=[]; _phi=[]; _theta=[]
        for i in xrange( len(_pms) ):
            pm = _pms[i]
            _names.append(pm.name)
            _depth.append(pm.depth)
            _rough.append(pm.rough)
            _rho.append( decodeP( pm.rho) )
            _mu.append(  decodeP( pm.mu )  )
            if hasattr(pm, 'phi'):
                _phi.append(   decodeP( pm.phi   ) )
                _theta.append( decodeP( pm.theta ) )

        if _phi==[]:
            _phi   = None
            _theta = None
            self.magnetic = False
        else:
            self.magnetic = True
               
        self._initModel(names = _names,
                        depth = _depth,
                        rough = _rough,
                        rho   = _rho,
                        mu    = _mu,
                        phi   = _phi,
                        theta = _theta
                        )

        self.editMenu.Enable(wxID_Init_Model,    False)
        self.editMenu.Enable(wxID_Load_Model,    False)
        self.editMenu.Enable(wxID_Init_Model_NM, False)
        self.editMenu.Enable(wxID_Load_Staj,     False)
        
        self.editMenu.Enable(wxID_Add_Layer,        True)
        self.editMenu.Enable(wxID_Save_Model,       True)
        self.editMenu.Enable(wxID_Remove_Layer,     True)
        self.editMenu.Enable(wxID_Clear_Model,      True)
        self.editMenu.Enable(wxID_Change_LayerName, True)
        self.editMenu.Enable(wxID_Change_MetaData,  True)
        self.editMenu.Enable(wxID_Change_Profile,   True)

        
    
    def _setModel(self):
        pass

    
    def OnPanelRightDown(self, event ):
        """ On touch the right mouse """
        self._current_rightdown_layer = self.current_layer
        self.PopupMenu(self.editMenu)


    def UpdateModel(self, event):
        self.parent.OnUpdateModel(event)


    def OnUpdateModelMenu(self, event):
        pass


    def OnClearModelMenu(self, event):
        """ Clear the model """
        if hasattr(self, 'profile'):
           self.profile.roughness.clear()
           self.profile.interface.clear()
           self.profile.hrho.remove()
           self.profile.hmu.remove()

           if self.model.magnetic:
              self.profile.hP.remove()
              self.profile.htheta.remove()

           self.profile.hlegend.texts=[]
           del self.profile.hlegend
        
           for interactor in self.profile.profiles:
               interactor.clear_markers()
           self.profile.connect.clearall()
        
           clear_axes( self.profile.ax )
           if self.model.magnetic:
              clear_axes( self.profile.ax2 )
           
           # Remove pars
           for i in xrange( len(self.model.names) ):
               nameID = self.model.names[i]
               self.parent.model.removeChild( nameID  )
               
           self.parent._fireModelEvent(MODEL_ADD)
 

           #TODO: Clear the info panel
           self._Disable()
           self.editMenu.Enable(wxID_Load_Model,      True)
           self.editMenu.Enable(wxID_Init_Model_NM,   True)
           self.editMenu.Enable(wxID_Init_Model,      True)
           self.editMenu.Enable(wxID_Load_Staj,       True)



    def OnInitModelMenu(self, event):
        """ Init the magnetic model Menu """
        dlg = InitModelDialog(self.parent,
                              -1,
                              "Init incident and substrate",
                              size    = (300,300),
                              style   = wx.DEFAULT_DIALOG_STYLE,
                              useMetal= False,
                             )
        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        if val == wx.ID_CANCEL:   return  # Do nothing
        if val == wx.ID_OK:
	    ret1 = dlg.getIncidentInfo()
            ret2 = dlg.getSubstrateInfo()
        else:
            ret1 = None
            ret2 = None
        
        names = [ret1[0],ret2[0]]
        depth = [30.0, 30.0]
        rough = [5.0]
        rho   = [ ret1[1],ret2[1] ]
        mu    = [ ret1[2],ret2[2] ]
        phi   = [ ret1[3],ret2[3] ]
        theta = [ ret1[4],ret2[4] ]

        self.magnetic = True 
        self._initModel(names = names,
                        depth = depth,
                        rough = rough,
                        rho   = rho,
                        mu    = mu,
                        phi   = phi,
                        theta = theta
                        )

        for x in xrange( len(depth) ):
            _refl       = ReflParameterMag()  
            _refl.name  = names[x] 
            _refl.depth = tFloat( depth[x] )
            _refl.rho   = rho[x]
            _refl.mu    = mu[x]
            _refl.phi   = phi[x]
            _refl.theta = theta[x]
            if x < len(depth)-1:
                _refl.rough = rough[x]
            self.parent.model.addChild( _refl )
            
        self.parent._fireModelEvent(MODEL_ADD)
        
        self.editMenu.Enable(wxID_Init_Model,    False)
        self.editMenu.Enable(wxID_Load_Model,    False)
        self.editMenu.Enable(wxID_Init_Model_NM, False)
        self.editMenu.Enable(wxID_Load_Staj,     False)
        
        self.editMenu.Enable(wxID_Add_Layer,        True)
        self.editMenu.Enable(wxID_Save_Model,       True)
        self.editMenu.Enable(wxID_Remove_Layer,     True)
        self.editMenu.Enable(wxID_Clear_Model,      True)
        self.editMenu.Enable(wxID_Change_LayerName, True)
        self.editMenu.Enable(wxID_Change_MetaData,  True)
        self.editMenu.Enable(wxID_Change_Profile,   True)
        
	return True


    def OnInitModelNMMenu(self, event):
        """ Init the non magnetic model Menu """
        dlg = InitModelDialogNM(self.parent,
                                -1,
                                "Init incident and substrate",
                                size    = (300,240),
                                style   = wx.DEFAULT_DIALOG_STYLE,
                                useMetal= False,
                                )
        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        if  val == wx.ID_CANCEL:  return  #Do nothing
        if  val == wx.ID_OK:
	    ret1 = dlg.getIncidentInfo()
            ret2 = dlg.getSubstrateInfo()
        else:
            ret1 = None
            ret2 = None
     
        names = [ ret1[0], ret2[0] ]
        depth = [ 30,30 ]
        rough = [ 5 ]
        rho   = [ ret1[1], ret2[1] ]
        mu    = [ ret1[2], ret2[2] ]

        self.magnetic  = False 
        self._initModel( names = names,
                         depth = depth,
                         rough = rough,
                         rho   = rho,
                         mu    = mu
                         )
        
        for x in xrange( len(depth) ):
            _refl = ReflParameter()  
            _refl.name  = names[x] 
            _refl.depth = tFloat( depth[x] )
            _refl.rho   = rho[x]
            _refl.mu    = mu[x]
            if x < len(depth)-1:
                _refl.rough = rough[x]
            self.parent.model.addChild( _refl )
            
        self.parent._fireModelEvent(MODEL_ADD)

        #print self.model.Lrho[0]._val
        self.editMenu.Enable(wxID_Init_Model,    False)
        self.editMenu.Enable(wxID_Init_Model_NM, False)
        self.editMenu.Enable(wxID_Load_Model,    False)
        self.editMenu.Enable(wxID_Load_Staj,     False)
        
        self.editMenu.Enable(wxID_Add_Layer,        True)
        self.editMenu.Enable(wxID_Save_Model,       True)
	self.editMenu.Enable(wxID_Add_Layer,        True)
        self.editMenu.Enable(wxID_Remove_Layer,     True)
        self.editMenu.Enable(wxID_Clear_Model,      True)
        self.editMenu.Enable(wxID_Change_LayerName, True)
        self.editMenu.Enable(wxID_Change_MetaData,  True)
        self.editMenu.Enable(wxID_Change_Profile,   True)

        return True


    def _parseDepth(self):
        """  parse the depth of model """
        ret = []
        for i in xrange( len(self.model.depth) ):
            ret.append( self.model.depth[i] )  

        return ret

    
    def _parseRough(self):
        """ parse the rough of model """
        ret = []
        for i in xrange( len(self.model.rough) ):
            ret.append( self.model.rough[i] )  

        return ret


    def _parseRho(self):
        """ parse the Rho of model """
        return  parseProfile( self.model.Lrho, self.model.rho )

    def _parseMu(self):
        """ parse the mu of model """
        return  parseProfile( self.model.Lmu, self.model.mu )

    def _parsePhi(self):
        """ parse the phi of model """
        return  parseProfile( self.model.Lphi, self.model.phi )

    def _parseTheta(self):
        """ parse the theta of model """
        return  parseProfile( self.model.Ltheta, self.model.theta )



    def _parseDepthValue(self):
        """parse the depth value of model ( reflPARK) """
        ret = []
        n = len(self.model.depth)
        for i in xrange(n):
            ret.append( self.model.depth[i] )  

        return ret


    def _parseRhoValue(self):
        """ parse the Rho of model """
        return parseProfileValue( self.model.Lrho, self.model.rho )

    def _parseMuValue(self):
        """ parse the mu of model """
        return parseProfileValue( self.model.Lmu, self.model.mu )

    def _parsePhiValue(self):
        """ parse the phi of model """
        return parseProfileValue( self.model.Lphi, self.model.phi )

    def _parseThetaValue(self):
        """ parse the theta  of model """
        return parseProfileValue( self.model.Ltheta, self.model.theta )


    def OnSaveModelMenu(self, evt ):
        """ Save the model as python script """
        rough = self.model.rough
        name  = self.model.names
        depth = self._parseDepth()
        rho   = self._parseRho()
        mu    = self._parseMu()
        if self.model.magnetic:
           phi   = self._parsePhi()
           theta = self._parseTheta()
           
        dlg = SaveModelDialog(self.parent,
                              -1,
                              "Save Model Info",
                              size    = (300,200),
                              style   = wx.DEFAULT_DIALOG_STYLE,
                              useMetal= False,
                             )
        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        if val == wx.ID_CANCEL:  return   # Do nothing
        if val == wx.ID_OK:
            [modelname,  filename, outfile] = dlg.getOutPutInfo()

        if self.model.magnetic:   
           txts = _toPyScriptM("parseReflModel", 0, modelname,filename,name,
                               depth, rough, rho, mu, phi, theta,
                               self.wavelength,    self.background,
                               self.wavelengthDiv, self.angularDiv)
        else:
           txts = _toPyScript("parseReflModel", 0, modelname,filename,name,
                              depth, rough, rho, mu,
                              self.wavelength,    self.background,
                              self.wavelengthDiv, self.angularDiv)
        
        try:
            fd = open( outfile,  'w' )
            fd.writelines( txts )
            fd.close()
        except:
            showErrorMsg(self, 'Error in saving model XML file:',
                                'model File  Error')




    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def parseDictLayers(self):

        n = len(self.dictLayers)
        names=[]; roughs=[]; depths=[]; rhos=[];  mus=[];  phis=[];  thetas=[]
        for i in xrange(n):
            names.append( self.dictLayers[i]["name"] )
            depths.append( self.dictLayers[i]["depth"] )
            rhos.append( self.dictLayers[i]["rho"] )
            mus.append( self.dictLayers[i]["mu"] )
            phis.append( self.dictLayers[i]["phi"] )
            thetas.append( self.dictLayers[i]["theta"] )
       
        n = len(self.dictInterfaces)
        for i in xrange(n):
            roughs.append( self.dictInterfaces[i]["interface"] )
            
        return [names,depths, roughs, rhos, mus,phis,thetas ]


    def parseStajLayerName(self, pLists, nT, nM, nB ):

         _name = []    
         for x in xrange( len(pLists) ):
             if    x <= nT: 
                 _name.append( 'T%d'%(x) )
             elif  x >nT and x <= nT + nM:
                 _name.append( 'M%d'%(x-nT) )
             else:
                 _name.append( 'B%d'%(x-nT-nM) )
                 
         return _name



    def OnLoadStajMenu(self, evt ):
        """ Load the model from staj ( magnetic case ) """
        dlg=wx.FileDialog(self,
                          message="Load a build model from Staj file",
                          wildcard="Staj file(*.staj)|*.staj|Staj file (*.sta)|*.sta|Any file(*.*)|*.*",
                          style=wx.OPEN
                          )
        fname = ''
        _val  = dlg.ShowModal()
        if  _val == wx.ID_CANCEL:  return #Do nothing
        if  _val == wx.ID_OK:
            dir0  = dlg.GetDirectory()
            fname = dlg.GetFilename()
        dlg.Destroy()

        if fname == '':
            showErrorMsg(self, 'Error in load file:'+fname,'py file Error')

        _fullFileName = os.path.join(dir0,fname)          
        fin           = open(_fullFileName,'r')
        _FirstLine    = fin.readlines()[0].strip().split()
        fin.close()

        # FIXME: Need more robust way to test it is magnetic or not?
        if( len(_FirstLine) == 4  ):    #Magnetic Case
            
            self.magnetic  = True
            self._LoadMStajFile( _fullFileName, dir0 )
            
        elif( len(_FirstLine) == 6  ):  #NonMagnetic Case
            
            self.magnetic  = False
            self._LoadNMStajFile( _fullFileName, dir0 )
            
        else:                           #Other Format
            pass
        

        self.editMenu.Enable(wxID_Load_Model,        False)
        self.editMenu.Enable(wxID_Load_Staj,         False)
        self.editMenu.Enable(wxID_Save_Model,        True)
        self.editMenu.Enable(wxID_Init_Model,        False)
        self.editMenu.Enable(wxID_Init_Model_NM,     False)
         
        self.editMenu.Enable(wxID_Add_Layer,         True)
        self.editMenu.Enable(wxID_Remove_Layer,      True)
        self.editMenu.Enable(wxID_Clear_Model,       True)
        self.editMenu.Enable(wxID_Change_LayerName,  True)
        self.editMenu.Enable(wxID_Change_Profile,    True)
        self.editMenu.Enable(wxID_Change_MetaData,   True)



    def _LoadNMStajFile(self, fname, dir0 ):
        """ Load the model from staj """
        s2m  = Staj2Model( fname, scale=True )._toModel()
        ( self.wavelength, self.wavelengthDiv,  self.angularDiv,
          self.intensity,  self.background ) = s2m[1]
          
        ( _nTLayer, _nMLayer, _nBLayer, _nRepeat, _nFit, self._nRough )=s2m[2]
        (_d, _rough, _rho, _mu, _rhom) = s2m[0]

        _names = self.parseStajLayerName( _d, _nTLayer, _nMLayer, _nBLayer)
        ( qmin,  qmax,  npnts)  =  s2m[3]
        ( self._proftyp,  self._stajdatafile,  outfile)  =  s2m[4]

        self.Q1 = 0.0
        self.Q2 = 0.0


        if _d[0] < 0.00001:
           _d[0] = 100
           
        _rough_ = []
        for x in xrange( len(_rough)-1  ):
            _rough_.append( _rough[x+1] )
        _rough_.append(  _rough[ len(_rough) -1 ] )
        
        self._initModel(names = _names,
                        depth = _d,
                        rough = _rough_,
                        rho   = _rho,
                        mu    = _mu
                        )
          
        for x in xrange( len(_d) ):
            
            _refl       = ReflParameter()
            _refl.name  = _names[x]
            _refl.depth = tFloat( _d[x] )
            _refl.rho   = _rho[x]
            _refl.mu    = _mu[x]
               
            if x < len(_d)-1:
                _refl.rough = _rough_[x]
                             
            self.parent.model.addChild( _refl )

        try:
            _meta = self.parent.parent.datasetPanel.GetDataset().getXmlData()[0].getXmlMetaData()
        except:
            showErrorMsg(self,
                         'Error in change metadata:','meta data Error')
            return
        
        _meta.angularDiv    = self.angularDiv
        _meta.background    = self.background
        _meta.wavelength    = self.wavelength
        _meta.wavelengthDiv = self.wavelengthDiv
        
        self.parent._fireModelEvent(MODEL_ADD)




    def _LoadMStajFile(self, fname, dir0 ):
        """ Load the model from staj ( magnetic case ) """
        # Load model infos from staj file
        s2m  = Staj2MModel( fname, scale=True )._toModel()
        
        (self.wavelength, self.wavelengthDiv, self.angularDiv,   
         self.intensity,  self.background,    self.Aguide ) =  s2m[0]

        self.Q1 = 0.0
        self.Q2 = 0.0
        self.dtheta1 = self.angularDiv
        self.dtheta2 = self.angularDiv

        ( _rho,_phi, _depth,_depthm, _rough,_roughm, _mu,_the)= s2m[1]
        _Qranges                     = s2m[2]
        (_nLayer, _nRough , _nFit  ) = s2m[3]
        (_type,  _suffix,  _outfile) = s2m[4]

        self._stajdatafile = _outfile+_suffix[0]
        
        _names = []
        for x in xrange( len(_depth) ):
           if    x ==0:   _names.append( 'MV' )
           else:          _names.append( 'M%d'%(x) )


        if _depth[0] < 0.00001:
           _depth[0] = 100
           
        _rough_ = []
        for x in xrange( len(_rough)-1  ):
            _rough_.append( _rough[x+1] )
        _rough_.append(  _rough[ len(_rough) -1 ] )

        self._initModel(names = _names,
                        depth = _depth,
                        rough = _rough_,
                        rho   = _rho,
                        mu    = _mu,
                        phi   = _phi,
                        theta = _the
                        ) 

        for x in xrange( len(_depth) ):
            
            _refl       = ReflParameterMag()  
            _refl.name  = _names[x]
            _refl.depth = tFloat( _depth[x] )
            _refl.rho   = _rho[x]
            _refl.mu    = _mu[x]
            _refl.phi   = _phi[x]
            _refl.theta = _the[x]
               
            if x < len(_depth)-1:
                _refl.rough = _rough_[x]

            self.parent.model.addChild( _refl )

        try:
            _meta = self.parent.parent.datasetPanel.GetDataset().getXmlData()[0].getXmlMetaData()
        except:
            showErrorMsg(self,
                         'Error in change metadata:','meta data Error')
            return
        
        _meta.angularDiv    = self.angularDiv
        _meta.background    = self.background
        _meta.wavelength    = self.wavelength
        _meta.wavelengthDiv = self.wavelengthDiv
        
        self.parent._fireModelEvent(MODEL_ADD)

        

    def OnLoadModelMenu(self, evt ):
        """ Load the model """
        dlg=wx.FileDialog(self,
                          message ="Load a build model python script",
                          wildcard="python file (*.py)|*.py|Any file(*.*)|*.*",
                          style   =wx.OPEN
                          )
        fname=''
        _val = dlg.ShowModal()
        if  _val == wx.ID_CANCEL:  return  #Do nothing
        if  _val == wx.ID_OK:
            dir0  = dlg.GetDirectory()
            fname = dlg.GetFilename()
            _inFullName = os.path.join(dir0, fname)
        dlg.Destroy()
        
        txts = ''
        if fname != '':
            fd = open( _inFullName )
            for txt in fd:
                if not txt.isspace():  txts += txt    
            fd.close()               

        #If empty file, do nothing 
        if txts == '':  return
        
        M_n  = lookUpModelName( txts )  
        cmd  = txts + 'self.dictLayers='    + M_n + '.DictLayers\n'+ \
                      'self.dictInterfaces='+ M_n + '.DictInterfaces\n' + \
                      'self.magnetic = '    + M_n + '.magnetic\n' + \
                      'self.wavelength='    + M_n + '.wavelength\n' + \
                      'self.wavelengthDiv=' + M_n + '.wavelengthdivergence\n'+\
                      'self.angularDiv='    + M_n + '.angulardivergence\n' + \
                      'self.background='    + M_n + '.background'
        exec cmd
        
        (_names,_depth,_rough,_rho,_mu, _phi, _theta ) = self.parseDictLayers()
        if not self.magnetic:
            _phi   = None
            _theta = None
            
        self._initModel(names = _names,
                        depth = _depth,
                        rough = _rough,
                        rho   = _rho,
                        mu    = _mu,
                        phi   = _phi,
                        theta = _theta
                        )

        for x in xrange( len(_depth) ):
            
            if not self.magnetic:  _refl = ReflParameter()
            else:                  _refl = ReflParameterMag()  

            _refl.name  = _names[x]
            _refl.depth = tFloat( _depth[x] )
            _refl.rho   = filterP( _rho[x] )
            _refl.mu    = filterP( _mu[x]  )
            if  self.magnetic:
                _refl.phi   = filterP( _phi[x]   )
                _refl.theta = filterP( _theta[x] )
               
            if x < len(_depth)-1:
                _refl.rough = _rough[x]

            self.parent.model.addChild( _refl )
               
        self.parent._fireModelEvent(MODEL_ADD)

        self.editMenu.Enable(wxID_Load_Model,    False)
        self.editMenu.Enable(wxID_Load_Staj,     False)
        self.editMenu.Enable(wxID_Init_Model,    False)
        self.editMenu.Enable(wxID_Init_Model_NM, False)
         
        self.editMenu.Enable(wxID_Add_Layer,    True)
        self.editMenu.Enable(wxID_Remove_Layer, True)
        self.editMenu.Enable(wxID_Clear_Model,  True)
        self.editMenu.Enable(wxID_Change_LayerName, True)
        self.editMenu.Enable(wxID_Change_Profile,   True)
        self.editMenu.Enable(wxID_Change_MetaData,  True)
        self.editMenu.Enable(wxID_Save_Model,    True)



    def OnSaveFigureMenu(self, evt ):
        """ Save the current figure """
        dlg = wx.FileDialog(self,
                       message="Save Figure as ...",
                       defaultDir=os.getcwd(), 
                       defaultFile="",
                       wildcard="image file (*.png)|*.fig|Any file(*.*)|*.*",
                       style=wx.SAVE
                      )

        _val = dlg.ShowModal()
        if  _val == wx.ID_CANCEL:  return  #Do nothing
        if  _val == wx.ID_OK:
            outfile = dlg.GetPath()
            
        dlg.Destroy()

        try:
            self.fig.savefig( outfile )
        except:
            showErrorMsg(self, 'Error in save the figure:','model File  Error')



    def OnChangeMetaDataMenu(self, event):
        """ Change MetaData """

        try:
            _meta = self.parent.parent.datasetPanel.GetDataset().getXmlData()[0].getXmlMetaData()
        except:
            showErrorMsg(self,
                         'Error in change metadata:','meta data Error')
            return

            
        #return
        dlg = ChangeMetaDataDialog(self,
                                   -1,
                                   "Meta Data",
                                   size    = (360,240),
                                   style   = wx.DEFAULT_DIALOG_STYLE,
                                   useMetal= False,
                                   pm = _meta
                                   )
        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        if  val == wx.ID_CANCEL:  return   #Do nothing
        if  val == wx.ID_OK:
	    ret = dlg.getOutPutInfo()
        else:
            pass

        _meta.angularDiv    = ret[0] 
        _meta.background    = ret[3]
        _meta.wavelength    = ret[1]
        _meta.wavelengthDiv = ret[2]
        self.parent._fireModelEvent(MODEL_UPDATE_META)

    

    def change_a_profile(self, idx, mL, mP, b ):
        """ Change  a profile in a  layer """
        if  isfactory( b ):
            mL[idx] = Layer( b )  
            mP[idx] = b 
        else:
            val = CheckValid(b)
            mL[idx] = Layer( val )
            mP[idx] = val  



    def OnChangeProfileLayerMenu(self, event ):
        """ Change a profile from  a layer """
        idx = self.current_layer
        dlg = ChangeProfileDialog(self.parent,
                             -1,
                             "Change a profile within layer(%d)"%(idx),
                             size    = (500,200),
                             style   = wx.DEFAULT_DIALOG_STYLE,
                             useMetal= False,
                             model   = self.model,
                             layer_num = idx
                             )

        # this does not return until the dialog is closed.
        
        val = dlg.ShowModal()
        if  val == wx.ID_CANCEL:  return   # Do nothing
        if  val == wx.ID_OK:
	    ret = dlg.getLayerInfo()
        else:
            ret = [1]  # error happer

        # check return right or not
        if ret[-1] != 0:  
           showErrorMsg(self,
                        "Wrong input format(invalid layer), try again",
                        "Add Layer Error message"
                        )
           return False  # error happen

        # At this stage, no error happen 
        _type     = ret[0]
        _nProfile = ret[2]

        nameID = self.model.names[idx]
        _pm    = self.parent.model.getChild( nameID  )
        
        if _type == "rho":
            self.change_a_profile( idx, self.model.Lrho, self.model.rho,
                                   _nProfile )
            _pm.rho =  _nProfile
            
        if _type == "mu":
            self.change_a_profile( idx, self.model.Lmu,  self.model.mu,
                                   _nProfile )
            _pm.mu =  _nProfile
            
        if _type == "phi":
            self.change_a_profile( idx, self.model.Lphi, self.model.phi,
                                   _nProfile )
            _pm.phi =  _nProfile
            
        if _type == "theta":
            self.change_a_profile(idx,self.model.Ltheta, self.model.theta,
                                  _nProfile )
            _pm.theta = _nProfile
              
        self.parent._fireModelEvent(MODEL_UPDATE)
        
        # Update the profile
        self.model.refresh()
        self.profile.interface.refresh()
        self.profile.set_layer(idx)  
        self.profile.update()

        self.editMenu.Enable(wxID_Remove_Layer, True)           

	return True


    
    def add_a_layer(self, idx, mL, mP, b ):
        """ Add a profile in a  layer """
        if  isfactory( b ):          

            mL.insert(idx, Layer( b ) ) 
            mP.insert(idx, b )   #mP.insert(idx, b.build() )

        else:
            val = CheckValid(b)
            mL.insert(idx, Layer( val) )
            mP.insert(idx,        val  )



    def OnAddLayerMenu(self, event ):
        """ On add a layer """
        idx = self._current_rightdown_layer
         
        if self.model.magnetic:  sizes = (500,300)
        else:                    sizes = (500,240)

        # check the position is OK for add a layer or not
        if idx <=0:
           showErrorMsg(self,
                        "Can't add a layer before incident layer(%s)"%(self.model.names[0]), "Add Layer Error message" )
           return

        if idx >= len(self.model.names):
           showErrorMsg(self,
                        "Can't add a layer before substrate layer(%s)"%(self.model.names[-1]), "Add Layer Error message" )
           return


        #input 
        dlg = AddLayerDialog(self.parent,
                             -1,
                             "Add a layer between layer(%s) and layer(%s)"%(self.model.names[idx-1], self.model.names[idx]),
                             size    = sizes,
                             style   = wx.DEFAULT_DIALOG_STYLE,
                             useMetal= False,
                             model   = self.model
                             )
        val = dlg.ShowModal()
        if  val == wx.ID_CANCEL:   return # Do nothing
        if  val == wx.ID_OK:
	    ret = dlg.getLayerInfo()
        else:
            ret = [1]  # error happen

        # If error happen. FIXME, give info about what error happen?
        if ret[-1] != 0:
           showErrorMsg(self, "Wrong input format(invalid layer), try again",
                              "Add Layer Error message" )
           return


        if self.model.names.count( ret[0] ) >=1:
           showErrorMsg(self,
                        "The layer name %s exists( not unique )"%( ret[0] ), 
                        "Add Layer Error message" )
           return

        # Remove
        for i in xrange( len(self.model.names) ):
            nameID = self.model.names[i]
            self.parent.model.removeChild( nameID  )


        self.model.names.insert(idx, ret[0])
        self.model.depth   = nx.insert( self.model.depth,   idx, ret[1])
        print  self.model.depth
        self.model.rough   = nx.insert( self.model.rough,   idx, ret[2])
        self.add_a_layer(idx, self.model.Lrho, self.model.rho, ret[3] )
        self.add_a_layer(idx, self.model.Lmu,  self.model.mu,  ret[4] )
        if self.magnetic:
           self.add_a_layer(idx, self.model.Lphi,  self.model.phi,   ret[5] )
           self.add_a_layer(idx, self.model.Ltheta,self.model.theta, ret[6] )

        # Add on order    
        for x in xrange( len(self.model.depth) ):
            
            if not self.magnetic:  _refl = ReflParameter()
            else:                  _refl = ReflParameterMag()  

            _refl.name  = self.model.names[x]
            _refl.depth = self.model.depth[x] 
            _refl.rho   = filterP(self.model.rho[x])
            _refl.mu    = filterP(self.model.mu[x])
            if  self.magnetic:
                _refl.phi   = filterP(self.model.phi[x])
                _refl.theta = filterP(self.model.theta[x])
                    
            if x < len(self.model.depth)-1:
                _refl.rough = self.model.rough[x]

            self.parent.model.addChild( _refl )
               
        self.parent._fireModelEvent(MODEL_ADD)


        # Update the profile
        self.model.refresh()
        self.profile.interface.refresh()
        #self.profile.set_layer(idx+1)  
        self.profile.update()

        self.editMenu.Enable(wxID_Remove_Layer, True)           

        return True    



    def OnRemoveLayerMenu(self, event ):
        """ On Remove a layer """
        dlg = RemoveLayerDialog(self.parent,
                                -1,
                                title    = "Remove a layer",
                                size     = (360,160),
                                style    = wx.DEFAULT_DIALOG_STYLE,
                                useMetal = False,
                                model    = self.model
                                )
        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        if   val == wx.ID_CANCEL:  return   # Do nothing
        if   val == wx.ID_OK:
	     ret = dlg.getLayerInfo()
        else:
             ret = [1]  # error happen 

        if  ret[-1] != 0 :
            showErrorMsg(self, "We can't remove a invalid Layer",
                               "Remove Layer Error message")
            return False

           
        # At this stage, no error happen     
        idx = ret[0]

        nameID = self.model.names[idx]
        self.parent.model.removeChild( nameID  )
        self.parent._fireModelEvent(MODEL_ADD)
        
        self.model.names.pop( idx )        
        self.model.depth = nx.delete( self.model.depth, idx )
        self.model.rough = nx.delete( self.model.rough, idx )

        self.model.Lrho.pop( idx )
        self.model.rho.pop( idx )
        self.model.Lmu.pop( idx )
        self.model.mu.pop( idx )
        if self.magnetic:
            self.model.Lphi.pop( idx )
            self.model.phi.pop( idx )
            self.model.Ltheta.pop( idx )
            self.model.theta.pop( idx )
            
        # update profile   
        self.model.refresh()
        self.profile.interface.refresh()
        self.profile.update()

	return True



    def OnChangeLayerNameMenu(self, event ):
        """ Change layer name """ 
        idx    = self.current_layer
        nameID = self.model.names[idx]
        
        dlg = ChangeLayernameDialog(self.parent,
                                    -1,
                                    "Change a profile within layer(%d)"%(idx),
                                    size    = (500,200),
                                    style   = wx.DEFAULT_DIALOG_STYLE,
                                    useMetal= False,
                                    layer_name = nameID
                                    )
        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        if  val == wx.ID_CANCEL:  return   # Do nothing
        if  val == wx.ID_OK:
	    ret = dlg.getLayerInfo()

        # At this stage, no error happen 
        _newName = ret[0]

        # Here we check the "name" is unique or not?
        if self.model.names.count( _newName ) >=1:
           showErrorMsg(self,
                        "The layer name %s exists( not unique )"%(_newName),
                        "Change layer name Error message" )
           return

        
        OLD = self.parent.model.getChild( nameID  )
        OLD.name = _newName
        
        self.parent._fireModelEvent(MODEL_UPDATE)

        self.model.names[ idx ] = _newName
        self.model.refresh()
        self.profile.interface.refresh()
        self.profile.update()
        
	return True


    def update(self, n):
        """ Update current layer number """
        self.current_layer = n


    def GetToolBar(self):
        """ backend_wx call this function. KEEP it """
        return None

    
    def OnLeftDClick(self, event):
        """
        FIXME, Do some meaningful things here. 
        print 'Left double click from canvas
        """
        pass


    def OnPanelFrameClose(self, event):
        """ On Close this Frame """
        self.Destroy()
        event.Skip()

