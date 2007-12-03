#!/usr/bin/env python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#Created by:  Jiwu Liu (jliu@pa.msu.edu)
#description:  Declare a class called Curve, which is used by Plot2D to describe a curve in the graph
#<LicenseText>
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Curve:
    """This class holds a common data structure for drawing a 
       curve in a graph. It keeps reference to plotting data as 
       well as plotting option"""
    def __init__(self, name, **properties ):
        """#name is a unique identifier to the curve being plotted.
           #properties is used for passing the plotting options
           
           A quick usage:
           with = {lines|linespoints|points|sticks|steps|dots}
           color = {red|green|blue|black|yellow|...}
           symbol ={diamond|square|cross|star|circle|...}
           line ={solid|dash|dot|dashDot|dashDotDot}
           """
        self.name = name
        
        #should do deepCopy?
        self.style = properties.copy()
        self.data = {'x':None,'y':None,'error':None}
        
        #set default value for common properties
        if not self.style.has_key('color') : self.style['color']='black'
        if not self.style.has_key('width') : self.style['width']=1
        if not self.style.has_key('line')  : self.style['line']='solid'
        if not self.style.has_key('symbol'): self.style['symbol']='diamond'
        if not self.style.has_key('symbolSize'): self.style['symbolSize']=2
        if not self.style.has_key('symbolColor'): self.style['symbolColor']='black'
        if not self.style.has_key('with')  : self.style['with']='lines'  
        if not self.style.has_key('legend'): self.style['legend']=name
    
    def changeStyle(self, properties):
        self.style.update(properties)
    
    def setX(self, xData):
        self.data['x'] = xData
    
    def setY(self, yData):
        self.data['y'] = yData
    
    def setError(self, errorData):
        self.data['error'] = errorData
        
#version
__id__ = '$Id: curve.py,v 1.3 2005/09/01 14:47:19 jwliu Exp $'
        
