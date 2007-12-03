#!/usr/bin/env python
##
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 4/17/2006 version 0.1a
# mmckerns@caltech.edu
# (C) 2006 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
__author__ = 'Mike McKerns'
__doc__ = '''...
'''

from graphics.gnuplot.gnuprompt import gnuplot

class gnuplotAPI(gnuplot):
    ''' ... '''
    # currently assumes a single plot window
    sessiontype = 'gnuplot'
    style = {'symbolshape':None, 'linestyle':None, 'symbolsize':None,
             'linewidth':None, 'symbolcolor':None, 'linecolor':None}
    color = {'none':-2,'black':-1,'dots':0,'red':1,'green':2,'blue':3,
             'magenta':4,'cyan':5,'brown':6,'yellow':7,'orange':8}
    shape = {'none':-1,'dot':0,'plus':1,'cross':2,'star':3,'square':4,
              'filledsquare':5,'circle':6,'filledcircle':7,'triangle':8,
              'filledtriangle':9,'downtriangle':10,'filleddowntriangle':11,
              'diamond':12,'filleddiamond':13}
    #plotref = {} # format: {0:'sin(x)'}

    #def __init__(self):
    #    from graphics.gnuplot import gnuplot
    #    self.session = gnuplot()
    #    return

    # create a blank canvas
    def blank(self):
        self.clear()
        return

    # destroy the plot window (preserving session variables)
    def destroy(self):
        self.restart()
        return

    # set the xlabel for the plot window
    #def xlabel(self,name):
    #    return

    # set the ylabel for the plot window
    #def ylabel(self,name):
    #    return

    # set the title for the plot window
    #def title(self,name):
    #    return

    # set the range for the x-axis
    def xrange(self,min='',max=''):
        if min is '' and max is '': value = '[-10:10]'
        else: value = (min,max)
        self.session.set_range('xrange',value)
        return

    # set the range for the y-axis
    def yrange(self,min='',max=''):
        if min is '' and max is '': value = '[*:*]'
        else: value = (min,max)
        self.session.set_range('yrange',value)
        return

    # toggle the x-axis to logscale
    def xlogscale(self,status=True,base=10):
        if status is False:
            self.session('unset logscale x')
            return
        base = str(base)
        command = 'set logscale x '+base
        self.session(command)
        return

    # toggle the y-axis to logscale
    def ylogscale(self,status=True,base=10):
        if status is False:
            self.session('unset logscale y')
            return
        base = str(base)
        command = 'set logscale y '+base
        self.session(command)
        return

    # set the x-axis tics
    # NOTE: gnuplot will extend the range to match the tics
    def xtics(self,interval='*'):
        if interval is '*':
            self.session('set xtics autofreq')
            return
        if interval is None:
            self.session('unset xtics')
            return
        interval = str(interval)
        command = 'set xtics '+interval
        self.session(command)
        return

    # set the y-axis tics
    # NOTE: gnuplot will extend the range to match the tics
    def ytics(self,interval='*'):
        if interval is '*':
            self.session('set ytics autofreq')
            return
        if interval is None:
            self.session('unset ytics')
            return
        interval = str(interval)
        command = 'set ytics '+interval
        self.session(command)
        return

    # get plot item
    def _getItem(self,id):
        return self.session.itemlist[id]

    def _getStyleStr(self,id):
        item = self._getItem(id)
        rawstyle = item.get_option('with')
        return rawstyle

    def _fromStyleStr(self,rawstr):
        style = self.style.copy() #get defaults
        if not rawstr: #there are no modifiers (using defaults)
            return style #return defaults
        rawlist = rawstr.split()
        style['linestyle'] = rawlist.pop(0)
        # FIXME: allow for errorbars/errorlines
        while rawlist:
        #XXX: what about setting keys like 'color','size',...
            if rawlist[0] in ['lt','linetype']:
                rawlist.pop(0)
                color = rawlist.pop(0)
                color = int(color)
                colorindex = self.color.values().index(color)
                style['linecolor'] = self.color.keys()[colorindex]
                style['symbolcolor'] = style['linecolor']
            elif rawlist[0] in ['lw','linewidth']:
                rawlist.pop(0)
                width = rawlist.pop(0)
                style['linewidth'] = int(width)
            elif rawlist[0] in ['pt','pointtype']:
                rawlist.pop(0)
                shape = rawlist.pop(0)
                shape = int(shape)
                shapeindex = self.shape.values().index(shape)
                style['symbolshape'] = self.shape.keys()[shapeindex]
            elif rawlist[0] in ['ps','pointsize']:
                rawlist.pop(0)
                size = rawlist.pop(0)
                style['symbolsize'] = int(size)
            else:
                pass #XXX: should this raise a warning? 
        return style

    # get style for plot item:
    #   linestyle, linetype (color), linewidth, pointtype (shape), pointsize
    # NOTE: linecolor & pointcolor are always the same
    def getStyle(self,id):
        stylestr = self._getStyleStr(id)
        style = self._fromStyleStr(stylestr)
        #FIXME: when using automatic settings, return actual setting
        #FIXME: (i.e. 'green' instead of None == automatic linecolor #2)
        #XXX: allow select one item?
        return style

    # send Gnuplot style string to Gnuplot bindings
    def _toBindingsStyleStr(self,id,style):
        item = self._getItem(id)
        item.set_option(with=style)
        self.refresh()
        return

    # compose Gnuplot style string from API style options:
    #   linestyle = {solid|dotted|sticks|data},
    #   linecolor = <API standard>,
    #   linewidth = INT >= 1,
    #   symbolshape = <API standard>,
    #   symbolsize = INT >= 0
    # NOTE: symbolcolor removed; to set symbolcolor, use linecolor
    def _toStyleStr(self,style):
        base = ''
        if style['linestyle'] is 'dotted': # = l lt 0
            base = 'linespoints'
            style['linecolor'] = 'dots'
        elif style['linestyle'] is 'sticks': # = impulse
            base = 'impulses'
        elif style['linestyle'] is 'data': # = p, eb, xeb, yeb, xyeb
            base = 'points'
        elif style['linestyle'] is 'solid': # = lp, el, xel, yel, xyel
            base = 'linespoints'
        else: 
            print style; raise "Unsupported style"
            #base = None
            #base = 'linespoints'
        # FIXME: need to handle errorbars/errorlines here
        options = ''
        if style['linecolor'] in self.color.keys(): #also symbolcolor
            options += ' lt '+str(self.color[style['linecolor']])
        if style['linewidth'] > 0:
            options += ' lw '+str(style['linewidth'])
        if base not in ['linespoints','points']:
            return base,options
        if style['symbolshape'] in self.shape.keys():
            options += ' pt '+str(self.shape[style['symbolshape']])
        if style['symbolsize'] >= 0:
            options += ' ps '+str(style['symbolsize'])
        return base,options

    # modify API style dict:
    #   linestyle (style) ==> style for plotting line or data
    #   symbolshape (shape) ==> symbol type for data point
    #   linewidth (width) ==> width of plotted line
    #   symbolsize (size) ==> size of plotted data point
    #   linecolor (color) ==> color of plotted line
    #   symbolcolor (color) ==> color of plotted symbol
    # NOTE: symbolcolor and linecolor are not independent
    def _setStyleDict(self,style,kwds):
        #get existing style for plot
        #process kwds to build API style dict
        for setting in self.style.keys():
            if kwds.has_key(setting):
                style[setting] = kwds.pop(setting)
        if kwds.has_key('style'):
            style['linestyle'] = kwds.pop('style')
        if kwds.has_key('color'):
            style['symbolcolor'] = kwds['color']
            style['linecolor'] = kwds.pop('color')
        if kwds.has_key('width'):
            style['linewidth'] = kwds.pop('width')
        if kwds.has_key('shape'):
            style['symbolshape'] = kwds.pop('shape')
        if kwds.has_key('size'):
            style['symbolsize'] = kwds.pop('size')
        # XXX: Allow gnuplot shortcut (i.e 'with') syntax ?
        return style

    # set line and/or symbol style for plot item
    def setStyle(self,id,**kwds):
        #get existing style for plot
        style = self.style.copy() # set to defaults
        #FIXME: style = getStyle(id) #allow for existing style
        #build API style dict
        style = self._setStyleDict(style,kwds)
        #compose style string
        base,options = self._toStyleStr(style)
        withstr = base+options
        #send style string to bindings
        self._toBindingsStyleStr(id,withstr)
        return

    # get label for plot item from legend
    def getLabel(self,id):
        item = self._getItem(id)
        return item.get_option('title')

    # set label for plot item in legend
    def setLabel(self,id,name):
        item = self._getItem(id)
        item.set_option(title=name)
        self.refresh()
        return

    # remove plot item
    def remove(self,id):
        item = self._getItem(id)
        self.session.itemlist.remove(item)        
        self.refresh()
        return





'''
    def _PlotFile(self,name,**kwds):
        self.plot(self.File(name,**kwds))
        return

    def _PlotFunc(self,func,**kwds):
        self.plot(self.Func(func,**kwds))
        return

    def _PlotData(self,*set,**kwds):
        self.plot(self.Data(*set,**kwds))
        return

    def _PlotGridData(self,set,**kwds):
        self.plot(self.GridData(set,**kwds))
        return

    # add new plot item:
    #   data = tuple (x,y,e)  *OR*  string 'f(x)'
    #   style = string # change from gnuplot to API style
    #   label = string
    def plot2D(self,data,style=None,label=None):
        if isinstance(data,(tuple,list)): #array?
            data = str(data)[1:-1]
            type = 'Data'
        else: #isinstance(data,str)
            type = 'Func'
        command = "self.plot(self."+type+"("+data
        if style: command += ",with="+style
        if label: command += ",title="+label
        command += ")"
        exec command
        return
'''


