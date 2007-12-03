#!/usr/bin/env python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#Created by:  Jiwu Liu (jliu@pa.msu.edu)
#description:  Plotting class based on pyre.component using different graphic library
#<LicenseText>
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from pyre.components.Component import Component
    
class Plot2D(Component):
    """This class is the base class for 2D real time plotting. 
    User should, however, implement one's own plot component
    based on this.
    It already has a internal structure #curveMap to manage
    all the curves added to it, and a set of interface to 
    communicate with the underlying graphics class, all of 
    which have names ended with #View
    This is a thread-safe class
    """
    symbolStyleIndex = 0
    lineStyleIndex = 0
    colors = ("red","blue","black","magenta","cyan","green","yellow")
    lines = ('solid','dash','dot','dashDot')
    symbols = ("circle","square","triangle","diamond","cross","xCross")
    
    def buildSymbolStyle ( self, index = -1 ):
        i = index
        if i == -1:
            i = Plot2D.symbolStyleIndex
            Plot2D.symbolStyleIndex += 1
        
        symbolIndex = (i // len(Plot2D.colors)) %len(Plot2D.symbols)
        colorIndex = i % len(Plot2D.colors) 
        return {'with':'points',
             'color':Plot2D.colors[colorIndex],
             'symbolColor':Plot2D.colors[colorIndex],
             'symbol':Plot2D.symbols[symbolIndex],
             'symbolSize':8}
                 
    def buildLineStyle ( self, index = -1 ):
        i = index
        if i == -1:
            i = Plot2D.lineStyleIndex
            Plot2D.lineStyleIndex += 1
        
        lineIndex = ( i // len(Plot2D.colors)) %len(Plot2D.lines)
        colorIndex = i % len(Plot2D.colors)
        return {'with':'lines',
             'color':Plot2D.colors[colorIndex],
             'line':Plot2D.lines[lineIndex],
             'width':2}
                 
    def __init__(self, name): 
        if name is None: name = 'Plot2D'
        
        Component.__init__(self, name, facility = 'plotlib' )
        import threading
        self.lock = threading.RLock()
        self.curveMap = {}
    
    def setLabels(self, title, xlabel, ylabel):
        #No need to copy. String is constant
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title  = title
        
    def setSize(self, width, height):
        self.width = width
        self.height = height
    
    def display ( self ):
        """This is a funtion to be called to start the window 
           event loop"""
        raise NotImplementedError("class %s must override function 'display'"  
                                  % self.__class__.__name__)
    
    def addCurve (self, curve ):
        try:
            self.lock.acquire()
                  
            # Plot library will return a internal reference to the curve inserted.
            self.curveMap[curve.name] = self._insert(curve.data,curve.style)
        finally:
            self.lock.release()
            
    def removeCurve ( self, curve ):
        try:
            self.lock.acquire()
            
            # remove the curve from the map first
            curveRef = self.curveMap.pop(curve.name, None)
            if curveRef is None : return 
            self._remove(curveRef)
        
        finally:
            self.lock.release()
    
    def updateCurveData ( self, curve ):
        """When this function is called, it will inform the associated
           graph to update its appearance"""
        try:
            self.lock.acquire()
            
            curveRef = self.__findCurve(curve.name)
            if curveRef is None: return
            
            # With the new curve, we can ask for replotting.
            self._updateData(curveRef, curve.data)
        finally:
            self.lock.release()
    
    def changeCurveStyle (self, curve):
        """Function will change the looking of specified curve and 
           update the view"""
        try: 
            self.lock.acquire()
            curveRef = self.__findCurve(curve.name)
            if curveRef is None: return
            
            self._changeStyle(curveRef, curve.style)
            
        finally:
            self.lock.release()
    
    def __findCurve ( self, curveName ):
        """Private function access critical data without lock"""
        try:
            return self.curveMap[curveName]
        except KeyError:
            return None
            
    # Function provided to interface with graphic library uniformly
    def _insert(self, data, style ):
        """Must be implemented by child class"""
        raise NotImplementedError("class %s must override function 'insertToView'"  
                                  % self.__class__.__name__)

    # Function provided to interface with graphic library uniformly
    def _remove(self, curveRef):
        """Must be implemented by child class"""
        raise NotImplementedError("class %s must override function 'removeFromView'"  
                                  % self.__class__.__name__)
    
    # Function provided to interface with graphic library uniformly
    def _updateData(self, curveRef, data ):
        """Must be implemented by child class"""
        raise NotImplementedError("class %s must override function 'updateDataInView'"  
                                  % self.__class__.__name__)
    
    # Function provided to interface with graphic library uniformly
    def _changeStyle(self, curveRef, style):
        """Must be implemented by child class"""
        raise NotImplementedError("class %s must override function 'changeStyleInView'"  
                                  % self.__class__.__name__)
        
# version
__id__ ='$Id: plot2d.py,v 1.8 2006/01/24 16:06:50 jwliu Exp $'
        
        
