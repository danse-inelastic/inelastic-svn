# Copyright 2004-2007 Brandon Keith  See LICENSE file for details. 
"""
Ui_PartWindow.py provides the part window class.

$Id: Ui_PartWindow.py,v 1.6 2007/07/01 17:27:32 emessick Exp $

History: 

- PartWindow and GridPosition classes moved here from MWSemantics.py.
  Mark 2007-06-27
"""

from PyQt4.Qt import Qt, QWidget, QHBoxLayout, QVBoxLayout, QSplitter
from PyQt4.Qt import QTabWidget, QScrollArea, QSizePolicy
from GLPane import GLPane
from PropMgr_Constants import pmDefaultWidth, pmMaxWidth, pmMinWidth
from Utility import geticon
from modelTree import modelTree
from qt4transition import qt4warnDestruction, qt4todo
import platform, env
from PropMgrBaseClass import printSizePolicy, printSizeHints, getPalette
from debug import print_compact_traceback #bruce 070627 bugfix

class PartWindow(QWidget):
    """A part window composed of the model tree/property manager (tabs)
    on the left (referred to as the "left channel") and the glpane
    (with a history widget below) on the right. A resizable splitter 
    separates the left channel and the 3D graphics area.
    """
    widgets = [] # For debugging purposes.
    
    def __init__(self, assy, parent):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle("My Part Window")
	
	# The main layout for the part window is an HBoxLayout <pwHBoxLayout>.
	pwHBoxLayout = QHBoxLayout(self)
	pwHBoxLayout.setMargin(3) # Makes a difference; I like 3. -- Mark
        pwHBoxLayout.setSpacing(0)
	
	# ################################################################
	# <pwHSplitter> is the "main splitter" bw the MT/PropMgr and the 
	# glpane with the following children:
	# - <leftChannelWidget> (QWidget)
	# - <pwVSplitter> (QSplitter)
	
        self.pwHSplitter = pwHSplitter = QSplitter(Qt.Horizontal)
	pwHSplitter.setObjectName("main splitter")
	pwHSplitter.setHandleWidth(3) # The splitter handle is 3 pixels wide.
        pwHBoxLayout.addWidget(pwHSplitter)
	
	# ##################################################################
	# <leftChannelWidget> - the container of all widgets left of the 
	# main splitter:
	# - <featureManager> (QTabWidget), with children:
	#    - <modelTreeTab> (QWidget)
	#    - <propertyManagerScrollArea> (QScrollArea), with the child:
	#       - <propertyManagerTab> (QWidget)
	
        leftChannelWidget = QWidget(parent)
	leftChannelWidget.setObjectName("leftChannelWidget")
        leftChannelWidget.setMinimumWidth(pmMinWidth)
	leftChannelWidget.setMaximumWidth(pmMaxWidth)
	leftChannelWidget.setSizePolicy(
	    QSizePolicy(QSizePolicy.Policy(QSizePolicy.Fixed),
			QSizePolicy.Policy(QSizePolicy.Expanding)))
        
        # This layout will contain only the featureManager (done below).
        leftChannelVBoxLayout = QVBoxLayout(leftChannelWidget)
        leftChannelVBoxLayout.setMargin(0)
        leftChannelVBoxLayout.setSpacing(0)
        
	pwHSplitter.addWidget(leftChannelWidget)
	
	# Makes it so leftChannelWidget is not collapsible.
	pwHSplitter.setCollapsible (0, False)
	
        # Feature Manager - the QTabWidget that contains the MT and PropMgr.
	# I'll rename this later since this isn't a good name. It is also
	# used in other files. --Mark
        self.featureManager = QTabWidget()
	self.featureManager.setObjectName("featureManager")
        self.featureManager.setCurrentIndex(0)
	self.featureManager.setAutoFillBackground(True)
	
	# Create the model tree "tab" widget. It will contain the MT GUI widget.
	# Set the tab icon, too.
        self.modelTreeTab = QWidget()
	self.modelTreeTab.setObjectName("modelTreeTab")
        self.featureManager.addTab(self.modelTreeTab,
				   geticon("ui/modeltree/Model_Tree"), "") 
	
        modelTreeTabLayout = QVBoxLayout(self.modelTreeTab)
        modelTreeTabLayout.setMargin(0)
        modelTreeTabLayout.setSpacing(0)
	
	# Create the model tree (GUI) and add it to the tab layout.
        self.modelTree = modelTree(self.modelTreeTab, parent)
	self.modelTree.modelTreeGui.setObjectName("modelTreeGui")
        modelTreeTabLayout.addWidget(self.modelTree.modelTreeGui)
	
	# Create the property manager "tab" widget. It will contain the PropMgr
	# scroll area, which will contain the property manager and all its 
	# widgets.
        self.propertyManagerTab = QWidget()
	self.propertyManagerTab.setObjectName("propertyManagerTab")
	
	self.propertyManagerScrollArea = QScrollArea(self.featureManager)
	self.propertyManagerScrollArea.setObjectName("propertyManagerScrollArea")
	self.propertyManagerScrollArea.setWidget(self.propertyManagerTab)
	self.propertyManagerScrollArea.setWidgetResizable(True) 
	# Eureka! 
	# setWidgetResizable(True) will resize the Property Manager (and its contents)
	# correctly when the scrollbar appears/disappears. It even accounts correctly for 
	# collapsed/expanded groupboxes! Mark 2007-05-29
	
	# Add the property manager scroll area as a "tabbed" widget. 
	# Set the tab icon, too.
	self.featureManager.addTab(self.propertyManagerScrollArea, 
				   geticon("ui/modeltree/Property_Manager"), "")
	
	# Finally, add the "featureManager" to the left channel layout.
        leftChannelVBoxLayout.addWidget(self.featureManager)
	
	# ##################################################################
	# <pwVSplitter> - a splitter comprising of all widgets to the right
	# of the main splitter with children:
	# - <glpane> (GLPane)
	# - <history_object> (HistoryWIdget)
	
	self.pwVSplitter = pwVSplitter = QSplitter(Qt.Vertical, pwHSplitter)
	pwVSplitter.setObjectName("pwVSplitter")
	
	# Create the glpane and make it a child of the (vertical) splitter.
        self.glpane = GLPane(assy, self, 'glpane name', parent)
	qt4warnDestruction(self.glpane, 'GLPane of PartWindow')
        pwVSplitter.addWidget(self.glpane)
			
	from HistoryWidget import HistoryWidget
	
        histfile = platform.make_history_filename() #@@@ ninad 061213 This is likely a new bug for multipane concept 
	#as each file in a session will have its own history widget
	qt4todo('histfile = platform.make_history_filename()')
	
        #bruce 050913 renamed self.history to self.history_object, and deprecated direct access
        # to self.history; code should use env.history to emit messages, self.history_widget
        # to see the history widget, or self.history_object to see its owning object per se
        # rather than as a place to emit messages (this is rarely needed).
        self.history_object = HistoryWidget(self, filename = histfile, mkdirs = 1)
            # this is not a Qt widget, but its owner;
            # use self.history_widget for Qt calls that need the widget itself.
        self.history_widget = self.history_object.widget
	self.history_widget.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
	
            #bruce 050913, in case future code splits history widget (as main window subwidget)
            # from history message recipient (the global object env.history).
        
        env.history = self.history_object #bruce 050727, revised 050913
	
	pwVSplitter.addWidget(self.history_widget)
	
	pwHSplitter.addWidget(pwVSplitter)
	
	if 0: #@ Debugging code related to bug 2424. Mark 2007-06-27.
	    self.widgets.append(self.pwHSplitter)
	    self.widgets.append(leftChannelWidget)
	    self.widgets.append(self.featureManager)
	    self.widgets.append(self.modelTreeTab)
	    self.widgets.append(self.modelTree.modelTreeGui)
	    self.widgets.append(self.propertyManagerScrollArea)
	    self.widgets.append(self.propertyManagerTab)
	    self.widgets.append(self.pwVSplitter)
	    
	    print "PartWindow.__init__() ============================================"
	    self.printSizeInfo()
	    
	    # The following call to the QSplitter.sizes() function returns zero for 
	    # the width of the glpane. I consider this "our bug". It should be looked
	    # into at later time. Mark 2007-06-27.
	    print "MAIN HSPLITTER SIZES: ", pwHSplitter.sizes()
	    
    def printSizeInfo(self):
	"""Used to print the sizeHints and sizePolicy of left channel widgets.
	I'm using this to help resolve bug 2424:
	"Allow resizing of splitter between Property Manager and Graphics window."
	-- Mark
	"""
	for widget in self.widgets:
	    printSizePolicy(widget)
	    #printSizeHints(widget)
	    #print "\n"

    def setRowCol(self, row, col):
        self.row, self.col = row, col
	
    def updatePropertyManagerTab(self, tab): #Ninad 061207
	"Update the Properties Manager tab with 'tab' "

	self.parent.glpane.gl_update_confcorner() #bruce 070627, since PM affects confcorner appearance
	
	if self.propertyManagerScrollArea.widget():
	    #The following is necessary to get rid of those c object deleted errors (and the resulting bugs)
	    lastwidgetobject = self.propertyManagerScrollArea.takeWidget() 
	    if lastwidgetobject:
		try:
		    lastwidgetobject.update_props_if_needed_before_closing()
		except:
		    if platform.atom_debug:
			msg1 = "Last PropMgr doesn't have method updatePropsBeforeClosing."
			msg2 =  " That is OK (for now,only implemented in GeometryGenerators)"
			msg3 = "Ignoring Exception"
			print_compact_traceback(msg1 + msg2 + msg3)
					    
	    lastwidgetobject.hide() # @ ninad 061212 perhaps hiding the widget is not needed
	       
	self.featureManager.removeTab(self.featureManager.indexOf(self.propertyManagerScrollArea))

	#Set the PropertyManager tab scroll area to the appropriate widget .at
	self.propertyManagerScrollArea.setWidget(tab)
		
	self.featureManager.addTab(self.propertyManagerScrollArea, 
				   geticon("ui/modeltree/Property_Manager"), "")
				   
	self.featureManager.setCurrentIndex(self.featureManager.indexOf(self.propertyManagerScrollArea))
	
    def KLUGE_current_PropertyManager(self): #bruce 070627
        """Return the current Property Manager widget (whether or not its tab is showing),
        or None if there is not one.
           WARNING: This method's existence (not only its implementation) is a kluge,
        since the right way to access that would be by asking the "command stack";
        but that's not yet implemented, so this is the best we can do for now.
        Also, it would be better to get the top command and talk to it, not its PM
        (a QWidget). Also, whatever calls this will be making assumptions about that PM
        which are really only the command's business. So in short, every call of this is
        in need of cleanup once we have a working "command stack". (That's true of many
        things related to PMs, not only this method.)
           WARNING: The return values are (presumably) widgets, but they can also be mode objects
        and generator objects, due to excessive use of multiple inheritance in the current PM code.
        So be careful what you do with them -- they might have lots of extra methods/attrs,
        and setting your own attrs in them might mess things up.
        """
        res = self.propertyManagerScrollArea.widget()
        if hasattr(res, 'done_btn'):
            return res
        # not sure what widget this is otherwise, but it is one (rather than None) for the default mode,
        # at least on startup, so just return None in this case
        return None

    def dismiss(self):
        self.parent.removePartWindow(self)
	
class GridPosition:
    def __init__(self):
        self.row, self.col = 0, 0
        self.availableSlots = [ ]
        self.takenSlots = { }

    def next(self, widget):
        if len(self.availableSlots) > 0:
            row, col = self.availableSlots.pop(0)
        else:
            row, col = self.row, self.col
            if row == col:
                # when on the diagonal, start a new self.column
                self.row = 0
                self.col = col + 1
            elif row < col:
                # continue moving down the right edge until we're about
                # to hit the diagonal, then start a new bottom self.row
                if row == col - 1:
                    self.row = row + 1
                    self.col = 0
                else:
                    self.row = row + 1
            else:
                # move right along the bottom edge til you hit the diagonal
                self.col = col + 1
        self.takenSlots[widget] = (row, col)
        return row, col

    def removeWidget(self, widget):
        rc = self.takenSlots[widget]
        self.availableSlots.append(rc)
        del self.takenSlots[widget]
	


