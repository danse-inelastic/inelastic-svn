import  wx.grid as gridlib
#from MainPlotWindow.MainPlotWindow import backend


#data types
edBoolean = gridlib.GRID_VALUE_CHOICE + ':true,false' 
edString = gridlib.GRID_VALUE_STRING
edFloat = gridlib.GRID_VALUE_FLOAT
edBool = gridlib.GRID_VALUE_BOOL
edInt = gridlib.GRID_VALUE_NUMBER
edCapstyle = gridlib.GRID_VALUE_CHOICE + ':butt,round,projecting'
edJoinstyle = gridlib.GRID_VALUE_CHOICE + ':miter,round,bevel'
edLinestyle = gridlib.GRID_VALUE_CHOICE + ':-,--,-.,:,steps,None'
edMarker = gridlib.GRID_VALUE_CHOICE + ':+,.,1,2,3,4'
edAdjustable = gridlib.GRID_VALUE_CHOICE + ':box,datalim'
edAnchor = gridlib.GRID_VALUE_CHOICE + ':C,SW,S,SE,E,NE,N,NW,W'
edAspect = gridlib.GRID_VALUE_CHOICE + ':auto,equal'#also can do float
edColor = gridlib.GRID_VALUE_CHOICE + ':blue,green,red,cyan,magenta,yellow,black,white'
edNumpy = gridlib.GRID_VALUE_STRING
edScale = gridlib.GRID_VALUE_CHOICE + ':linear,log'

class VtkPropertyModel:
    
    #plt = VtkBackend() # Create backend instance
#use(plt, globals()) # Export public namespace of plt to globals()

#class PropertyModel:
#    
#    def __init__(self,parent):
#        self.parent=parent

#TODO: way to fix those properties that don't have a get method but do have a set method
#TODO: add item type (validate_...) to check value input to make sure it is correct
#TODO eventually use wxwindows color picker for colors


# order of the properties is: label, value, format, apiKeyword

# this is what used to be uncommented in 'trunk'
#from graphics.common import Figure
#figureProps = Figure._props.items()
    
    def __init__(self,parent):
        self.parent=parent
        # DESIGN FLAW: go to VtkPropertyTable->PropertyEditor->MainPanel (IntegratedWindow or AUI)-> VtkWrapper
        self.vtkBackend = self.parent.parent.parent.backendWrap.vtkBackend
        self.figureProps = self.vtkBackend.gcf()._prop.items()
        self.figurePropDataTypes = {'axshape':edString, 'axes':edString, 'curax':edString, 'size': edString}


#        [['alpha transparency', 1.0, edFloat, 'alpha'],
#                ['animated', False, edBoolean, 'animated'],
#                #  axes: an axes instance
#                #  canvas: a FigureCanvas instance
#                #  clip_box: a matplotlib.transform.Bbox instance
#                #  clip_on: [True | False]
#                #  clip_path: an agg.path_storage instance
#                ['figure dpi', 80, edFloat, 'dpi'],
#                ['edge color', '', edColor, 'edgecolor'],
#                ['face color', '', edColor, 'facecolor'],
#                ['figure height', '', edFloat, 'figheight'],
#                #  figsize_inches: unknown
#                #  figure: a matplotlib.figure.Figure instance
#                ['figure width', '', edFloat, 'figwidth'],
#                #  frameon: boolean
#                #  label: any string
#                #  lod: [True | False]
#                #  picker: [None|float|boolean|callable]
#                #  size_inches: a w,h tuple with w,h in inches
#                #  transform: a matplotlib.transform transformation instance
#                ['visible', True, edBoolean, 'visible'],
#                ['z order', 2, edInt, 'zorder']  
#                ]

#
#        # figure props
#        # figure size in inches: width by height
#        figure = {'figure.figsize'    : [ (8,6), validate_nseq_float(2)],
#        'figure.dpi'        : [ 80, validate_float],   # DPI
#        'figure.facecolor'  : [ '0.75', validate_color], # facecolor; scalar gray
#        'figure.edgecolor'  : [ 'w', validate_color],  # edgecolor; white
#    
#        'figure.subplot.left'   : [0.125, ValidateInterval(0, 1, closedmin=False, closedmax=False)],
#        'figure.subplot.right'  : [0.9, ValidateInterval(0, 1, closedmin=False, closedmax=False)],
#        'figure.subplot.bottom' : [0.1, ValidateInterval(0, 1, closedmin=False, closedmax=False)],
#        'figure.subplot.top'    : [0.9, ValidateInterval(0, 1, closedmin=False, closedmax=False)],
#        'figure.subplot.wspace' : [0.2, ValidateInterval(0, 1, closedmin=False, closedmax=True)],
#        'figure.subplot.hspace' : [0.2, ValidateInterval(0, 1, closedmin=False, closedmax=True)]}    
#
#        savefig = {'savefig.dpi'       : [ 150, validate_float],   # DPI
#        'savefig.facecolor' : [ 'w', validate_color],  # facecolor; white
#        'savefig.edgecolor' : [ 'w', validate_color],  # edgecolor; white
#        'savefig.orientation' : [ 'portait', validate_orientation]}  # edgecolor; white

#from graphics.common import Axis
        self.axesProps = self.vtkBackend.gca()._prop.items()
        self.axesPropDataTypes={'zmax':edString, 'xlim':edString, 'diffusecolor':edString, 'zmin':edString, 
                           'plotitems':edString, 'visible':edString, 'numberofitems':edString, 
                           'xmin':edString, 'speculartcolor':edString, 'ymin':edString, 'ylim':edString, 
                           'fontname':edString, 'scale':edString, 'ymax':edString, 'bgcolor':edString, 
                           'lights':edString, 'camera':edString, 'ylabel':edString, 
                           'hidden':edString, 'method':edString, 'cameramode':edString, 'colormap':edString, 
                           'zlabel':edString, 'caxismode':edString, 'ambientcolor':edString, 'daspect':edString, 
                           'grid':edString, 'axiscolor':edString, 'shading':edString, 'hold':edString, 
                           'fgcolor':edString, 'viewport':edString, 'box':edString, 'zlim':edString,
                           'center':edString, 'title':edString, 'caxis':edString, 
                           'colorbar':edString, 'xlabel':edString, 'mode':edString, 
                           'xmax':edString, 'fontsize':edString, 'daspectmode':edString}

        [['adjustable', 1.0, edAdjustable, 'adjustable'],
             ['alpha transparency', 1.0, edFloat, 'alpha'],
             ['anchor', 1.0, edAnchor, 'anchor'],
             ['animated', False, edBoolean, 'animated'],
             ['aspect', 'auto', edAspect, 'aspect'],
             ['autoscale_on', True, edBoolean, 'autoscale_on'],
             #  axes: an axes instance
             ['axis background color', 'white', edColor, 'axis_bgcolor'],
            #  axis_off: void
            #  axis_on: void
            #  axisbelow: True|False
            #  clip_box: a matplotlib.transform.Bbox instance
            #  clip_on: [True | False]
            #  clip_path: an agg.path_storage instance
            #  cursor_props: a (float, color) tuple
            #  figure: a Figure instance
            #  frame_on: True|False
            ['label', '', edString, 'label'],
            #  lod: [True | False]
            #  navigate: True|False
            #  navigate_mode: unknown
            #  picker: [None|float|boolean|callable]
            ['position', '[0.125, 0.1, 0.775, 0.8]', edString, 'position'],
            ['title', '', edString, 'title'],# need special provision for getting this--no get method
            # since matplotlib has no get_title (just catch 'exceptions.AttributeError'
            # and make current value None or '')
            #  transform: a matplotlib.transform transformation instance
            ['visible', True, edBoolean, 'visible'], 
            ['x label', '', edString, 'xlabel'], 
            ['x limits', '(0.0, 1.0)', edString, 'xlim'],
            ['x scale', 'linear', edScale, 'xscale'],
            ['x tick labels',"['0.0','0.2','0.4','0.6','0.8','1.0']", edString,'xticklabels'],
            ['x ticks', 'array([ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ])', edString, 'xticks'],
            ['y label', '', edString, 'ylabel'], 
            ['y scale', 'linear', edScale, 'yscale'],
            ['y tick labels',"['0.0','0.2','0.4','0.6','0.8','1.0']", edString,'yticklabels'],
            ['y ticks', 'array([ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ])', edString, 'yticks'],
            ['z order', 2, edInt, 'zorder'] 
            ]



#        axes = {'axes.axisbelow'         : [False, validate_bool],
#        'axes.hold'         : [True, validate_bool],
#        'axes.facecolor'    : ['w', validate_color],    # background color; white
#        'axes.edgecolor'    : ['k', validate_color],    # edge color; black
#        'axes.linewidth'    : [1.0, validate_float],    # edge linewidth
#        'axes.titlesize'    : ['large', validate_fontsize], # fontsize of the axes title
#        'axes.grid'         : [False, validate_bool],   # display grid or not
#        'axes.labelsize'    : ['medium', validate_fontsize], # fontsize of the x any y labels
#        'axes.labelcolor'   : ['k', validate_color],    # color of axis label
#    
#        'polaraxes.grid'         : [True, validate_bool]}   # display polar grid or not
#
#        grid = {'grid.color'       :   ['k', validate_color],       # grid color
#        'grid.linestyle'   :   [':', str],       # dotted
#        'grid.linewidth'   :   [0.5, validate_float]}     # in points

#        'xtick.major.size'   : [5, validate_float],      # major xtick size in points
#        'xtick.minor.size'   : [2, validate_float],      # minor xtick size in points
#        'xtick.major.pad'   : [3, validate_float],      # distance to label in points
#        'xtick.minor.pad'   : [3, validate_float],      # distance to label in points
#        'xtick.color'        : ['k', validate_color],    # color of the xtick labels
#        'xtick.labelsize'    : ['small', validate_fontsize], # fontsize of the xtick labels
#        'xtick.direction'    : ['in', str],            # direction of xticks
#        'ytick.major.size'   : [5, validate_float],      # major ytick size in points
#        'ytick.minor.size'   : [2, validate_float],      # minor ytick size in points
#        'ytick.major.pad'   : [3, validate_float],      # distance to label in points
#        'ytick.minor.pad'   : [3, validate_float],      # distance to label in points
#        'ytick.color'        : ['k', validate_color],    # color of the ytick labels
#        'ytick.labelsize'    : ['small', validate_fontsize], # fontsize of the ytick labels
#        'ytick.direction'    : ['in', str]}            # direction of yticks

        self.plottableProps = [['line width', 0.5, edFloat, 'linewidth'],     # line width in points
                      ['line style', '-', edString, 'linestyle'],
                      #['line color', 'b', edString, 'color']
                      ['line color', 0, edInt, 'color']]
        
        
        #dictionary of line property data types
        # have put line properties elsewhere as a temporary hack
        self.linePropDataTypes={'function':edString,'linecolor':edString,'zlim':edString,'description':edString,'xlim':edString,
                           'material':edString,'ylim':edString,'dims':edString,'ydata':edString,'xdata':edString,
                           'linetype':edString,'numberofpoints':edString,'pointsize':edString, 
                           'linemarker':edString, 'linewidth':edString, 'legend':edString, 'zdata':edString}

        [['alpha transparency', 1.0, edFloat, 'alpha'],
            ['animated', False, edBoolean, 'animated'],
            ['line antialiasing', True, edBoolean, 'antialiased'],
            #['axes', instance, edString, 'axes'],
            #['clip_box', instance, edString, 'clip_box'],
            #['clip_on', True, edBoolean, 'clip_on'],
            #['clip_path', instance, edString, 'clip_path'],
            ['line color', 'blue', edColor, 'color'],#eventually use wx color selector
            ['dash capstyle', 'butt', edCapstyle, 'dash_capstyle'],
            ['dash joinstyle', 'miter', edJoinstyle, 'dash_joinstyle'],
            #  dashes: sequence of on/off ink in points
            #  data: (array xdata, array ydata)
            #  figure: a matplotlib.figure.Figure instance
            ['label', '_line0', edString, 'label'],
            ['line style', '-', edLinestyle, 'linestyle'],
            ['line width', 0.5, edFloat, 'linewidth'],  
            #  lod: [True | False]   
            ['line marker', 'None', edString, 'marker'],  
            ['marker edge color', 'auto', edString, 'markeredgecolor'],
            ['marker edge width', 0.5, edFloat, 'markeredgewidth'],
            ['marker face color', 'auto', edInt, 'markerfacecolor'],
            ['marker size', 6, edFloat, 'markersize'], 
            #['picker', 6, edFloat, 'picker'],#  picker: [None|float|boolean|callable]
            ['solid capstyle', 'projecting', edCapstyle, 'solid_capstyle'],
            ['solid joinstyle', 'miter', edJoinstyle, 'solid_joinstyle'],
            #  transform: a matplotlib.transform transformation instance
            ['visible', True, edBoolean, 'visible'],
            ['x data', '', edString, 'xdata'],
            ['y data', '', edString, 'ydata'],
            ['z order', 2, edInt, 'zorder']   
]




#    
#        # patch props
#        patch = {'patch.linewidth'   : [0.5, validate_float], # line width in points
#        'patch.edgecolor'   : ['k', validate_color], # black
#        'patch.facecolor'   : ['b', validate_color], # blue
#        'patch.antialiased' : [True, validate_bool]} # antialised (no jaggies)
#    
#    
#        # font props
#        font = {'font.family'       : ['serif', str],            # used by text object
#        'font.style'        : ['normal', str],           #
#        'font.variant'      : ['normal', str],           #
#        'font.stretch'      : ['normal', str],           #
#        'font.weight'       : ['normal', str],           #
#        'font.size'         : [12.0, validate_float], #
#        'font.serif'        : ['serif', validate_comma_sep_str],
#        'font.sans-serif'   : ['sans-serif', validate_comma_sep_str],
#        'font.cursive'      : ['cursive', validate_comma_sep_str],
#        'font.fantasy'      : ['fantasy', validate_comma_sep_str],
#        'font.monospace'    : ['monospace', validate_comma_sep_str]}
#    
#        # text props
#        text = {'text.color'        : ['k', validate_color],     # black
#        'text.usetex'       : [False, validate_usetex],
#        'text.dvipnghack'    : [False, validate_bool],
#        'text.fontstyle'    : ['normal', str],
#        'text.fontangle'    : ['normal', str],
#        'text.fontvariant'  : ['normal', str],
#        'text.fontweight'   : ['normal', str],
#        'text.fontsize'     : ['medium', validate_fontsize],
#        # mathtext settings
#        'mathtext.mathtext2'  :   [False, validate_bool], # Needed to enable Unicode
#        # fonts used by mathtext. These ship with matplotlib
#        'mathtext.rm'       :   ['cmr10.ttf', str], # Roman (normal)
#        'mathtext.it'       :   ['cmmi10.ttf', str], # Italic
#        'mathtext.tt'       :   ['cmtt10.ttf', str],  # Typewriter (monospaced)
#        'mathtext.mit'       :   ['cmmi10.ttf', str], # Math italic
#        'mathtext.cal'      :   ['cmsy10.ttf', str], # Caligraphic
#        'mathtext.nonascii' :   ['cmex10.ttf', str]} # All other nonascii fonts
#    
#        image = {'image.aspect' : ['equal', validate_aspect],  # equal, auto, a number
#        'image.interpolation'  : ['bilinear', str],
#        'image.cmap'   : ['jet', str],        # one of gray, jet, etc
#        'image.lut'    : [256, validate_int],  # lookup table
#        'image.origin'    : ['upper', str],  # lookup table
#    
#        'contour.negative_linestyle' : [(6.0,6.0), validate_nseq_float(2)]}
#    
    legendProps = [['legend fontsize', "small", edString, 'legend.fontsize']
               ]
#        legend = {'legend.isaxes'    :       [True,validate_bool],
#        'legend.numpoints'         :       [ 4,validate_int],      # the number of points in the legend line
#        'legend.fontsize' : ["small",validate_fontsize],
#        'legend.pad'       :       [ 0.2, validate_float],         # the fractional whitespace inside the legend border
#        'legend.markerscale'       :       [ 0.6, validate_float],    # the relative size of legend markers vs. original
#    
#        # the following dimensions are in axes coords
#        'legend.labelsep'  :       [ 0.005, validate_float],    # the vertical space between the legend entries
#        'legend.handlelen'         :       [ 0.05, validate_float],  # the length of the legend lines
#        'legend.handletextsep'     :       [ 0.02, validate_float], # the space between the legend line and legend text
#        'legend.axespad'   :       [ 0.02, validate_float], # the border between the axes and legend edge
#    
#        'legend.shadow' : [ False, validate_bool ]}
#    

#    
#        # a map from key -> value, converter
#        misc={'backend'           : ['GTK', validate_backend],
#        'numerix'           : ['Numeric', validate_numerix],
#        'datapath'          : [get_data_path(), validate_path_exists],
#        'interactive'       : [False, validate_bool],
#        'timezone'          : ['UTC', str]}
#    
#        # the verbosity setting
#        verbosity = {'verbose.level'           : ['silent', validate_verbose],
#        'verbose.fileo'           : ['sys.stdout', validate_verbose_fileo]}
#    
#        moreMisc = {'tk.window_focus'   : [ False, validate_bool],  # Maintain shell focus for TkAgg
#        'tk.pythoninspect'   : [ False, validate_bool],  # Set PYTHONINSPECT
#        'ps.papersize'      : [ 'letter', validate_ps_papersize], # Set the papersize/type
#        'ps.useafm'   : [ False, validate_bool],  # Set PYTHONINSPECT
#        'ps.usedistiller'   : [ False, validate_ps_distiller],  # use ghostscript or xpdf to distill ps output
#        'ps.distiller.res'  : [6000, validate_int],       # dpi
#        'pdf.compression'   : [6, validate_int],            # compression level from 0 to 9; 0 to disable
#        'svg.image_inline'  : [True, validate_bool],        # write raster image data directly into the svg file
#        'svg.image_noscale'  : [False, validate_bool],        # suppress scaling of raster data embedded in SVG
#        'plugins.directory' : ['.matplotlib_plugins', str]} # where plugin directory is locate
        
 
