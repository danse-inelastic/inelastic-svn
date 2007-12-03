#!/usr/bin/env python
##

class GraphicsAPI():
    ''' '''

    # create a blank canvas
    def blank(self):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)

    # destroy the plot window (preserving session variables)
    def destroy(self):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)

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
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)

    # set the range for the y-axis
    def yrange(self,min='',max=''):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)

    # toggle the x-axis to logscale
    def xlogscale(self,status=True,base=10):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)

    # toggle the y-axis to logscale
    def ylogscale(self,status=True,base=10):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)

    # set the x-axis tics
    # NOTE: gnuplot will extend the range to match the tics
    def xtics(self,interval='*'):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)

    # set the y-axis tics
    # NOTE: gnuplot will extend the range to match the tics
    def ytics(self,interval='*'):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)

    # get style for plot item:
    #   linestyle, linetype (color), linewidth, pointtype (shape), pointsize
    # NOTE: linecolor & pointcolor are always the same
    def getStyle(self,id):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)

    # set line and/or symbol style for plot item
    def setStyle(self,id,**kwds):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)

    # get label for plot item from legend
    def getLabel(self,id):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)

    # set label for plot item in legend
    def setLabel(self,id,name):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)

    # remove plot item
    def remove(self,id):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)





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


