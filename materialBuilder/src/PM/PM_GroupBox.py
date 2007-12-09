# Copyright 2006-2007 Brandon Keith  See LICENSE file for details. 
"""
PM_GroupBox.py

@author: Mark
@version: $Id: PM_GroupBox.py,v 1.7 2007/08/09 16:19:26 polosims Exp $
@copyright: 2006-2007 Brandon Keith  All rights reserved.

History:

mark 2007-07-22: Split PropMgrGroupBox out of PropMgrBaseClass.py into this 
file and renamed it PM_GroupBox.
"""

import platform

from debug import print_compact_traceback

from PM_Colors import getPalette
from PM_Colors import pmGrpBoxButtonBorderColor
from PM_Colors import pmGrpBoxButtonTextColor
from PM_Colors import pmGrpBoxExpandedIconPath
from PM_Colors import pmGrpBoxCollapsedIconPath
from PM_Colors import pmGrpBoxColor
from PM_Colors import pmGrpBoxBorderColor
from PM_Colors import pmGrpBoxButtonColor

from PM_Constants import pmGroupBoxSpacing
from PM_Constants import pmGrpBoxVboxLayoutMargin
from PM_Constants import pmGrpBoxVboxLayoutSpacing
from PM_Constants import pmGrpBoxGridLayoutMargin
from PM_Constants import pmGrpBoxGridLayoutSpacing

from PM_Constants import pmGridLayoutMargin
from PM_Constants import pmGridLayoutSpacing

from PM_Constants import pmLeftAlignment, pmRightAlignment
from PM_Constants import pmLeftColumn, pmRightColumn

from PyQt4.Qt import Qt
from PyQt4.Qt import QGroupBox
from PyQt4.Qt import QGridLayout
from PyQt4.Qt import QLabel
from PyQt4.Qt import QPushButton
from PyQt4.Qt import QPalette
from PyQt4.Qt import QSizePolicy
from PyQt4.Qt import QSpacerItem
from PyQt4.Qt import QVBoxLayout
from PyQt4.Qt import QWidget
from PyQt4.Qt import SIGNAL

from Utility import geticon

class PM_GroupBox( QGroupBox ):
    """
    The PM_GroupBox widget provides a group box container with a 
    collapse/expand button and a title button.
    
    PM group boxes can be nested by supplying an existing PM_GroupBox as the 
    parentWidget of a new PM_GroupBox (as an argument to its constructor).
    If the parentWidget is a PM_GroupBox, no title button will be created
    for the new group box.
    
    @cvar setAsDefault: Determines whether to reset the value of all
                        widgets in the group box when the user clicks
                        the "Restore Defaults" button. If set to False,
                        no widgets will be reset regardless thier own 
                        I{setAsDefault} value.
    @type setAsDefault: bool
       
    @cvar labelWidget: The Qt label widget of this group box.
    @type labelWidget: U{B{QLabel}<http://doc.trolltech.com/4/qlabel.html>}
    
    @cvar expanded: Expanded flag.
    @type expanded: bool
    
    @cvar _title: The group box title.
    @type _title: str
    
    @cvar _widgetList: List of widgets in the group box (except the title button).
    @type _widgetList: list
    
    @cvar _rowCount: Number of rows in the group box.
    @type _rowCount: int
    
    @cvar _groupBoxCount: Number of group boxes in this group box.
    @type _groupBoxCount: int
    
    @cvar _lastGroupBox: The last group box in this group box (i.e. the
                         most recent PM group box added).
    @type _lastGroupBox: PM_GroupBox
    """
    
    setAsDefault = True
    labelWidget  = None
    expanded     = True
    
    _title         = ""
    _widgetList    = []
    _rowCount      = 0
    _groupBoxCount = 0
    _lastGroupBox  = None
    
    def __init__(self, 
                 parentWidget, 
                 title          = '', 
                 setAsDefault   = True
                 ):
        """
        Appends a PM_GroupBox widget to I{parentWidget}, a L{PM_Dialog} or a 
        L{PM_GroupBox}.
        
        If I{parentWidget} is a L{PM_Dialog}, the group box will have a title 
        button at the top for collapsing and expanding the group box. If 
        I{parentWidget} is a PM_GroupBox, the title will simply be a text 
        label at the top of the group box.
        
        @param parentWidget: The parent dialog or group box containing this
                             widget.
        @type  parentWidget: L{PM_Dialog} or L{PM_GroupBox}
        
        @param title: The title (button) text. If empty, no title is added.
        @type  title: str
        
        @param setAsDefault: If False, no widgets in this group box will have 
                             thier default values restored when the B{Restore 
                             Defaults} button is clicked, regardless thier own 
                             I{setAsDefault} value.
        @type  setAsDefault: bool
        
        @see: U{B{QGroupBox}<http://doc.trolltech.com/4/qgroupbox.html>}
        """
      
        QGroupBox.__init__(self)
        
        self.parentWidget = parentWidget
        parentWidget._groupBoxCount += 1
        _groupBoxCount = 0
    
        self._title = title
        self.setAsDefault = setAsDefault
        
        # Calling addWidget() here is important. If done at the end,
        # the title button does not get assigned its palette for some 
        # unknown reason. Mark 2007-05-20.
        parentWidget.vBoxLayout.addWidget(self) # Add self to PropMgr's vBoxLayout
        
        self._widgetList = []
        parentWidget._widgetList.append(self)
        
        self.setAutoFillBackground(True) 
        self.setPalette(self._getPalette())
        self.setStyleSheet(self._getStyleSheet())
        
        # Create vertical box layout which will contain two widgets:
        # - the group box title button (or title) on row 0.
        # - the container widget for all PM widgets on row 1.
        self._vBoxLayout = QVBoxLayout(self)
        self._vBoxLayout.setMargin(0)
        self._vBoxLayout.setSpacing(0)
        
        # _containerWidget contains all PM widgets in this group box.
        # Its sole purpose is to easily support the collapsing and
        # expanding of a group box by calling this widget's hide()
        # and show() methods.
        self._containerWidget = QWidget()
        self._vBoxLayout.insertWidget(0, self._containerWidget)
        
        # Create vertical box layout
        self.vBoxLayout = QVBoxLayout(self._containerWidget)
        self.vBoxLayout.setMargin(pmGrpBoxVboxLayoutMargin)
        self.vBoxLayout.setSpacing(pmGrpBoxVboxLayoutSpacing)
        
        # Create grid layout
        self.gridLayout = QGridLayout()
        self.gridLayout.setMargin(pmGridLayoutMargin)
        self.gridLayout.setSpacing(pmGridLayoutSpacing)

        # Insert grid layout in its own vBoxLayout
        self.vBoxLayout.addLayout(self.gridLayout)
        
        # Add title button (or just a title if the parent is not a PM_Dialog).
        if isinstance(parentWidget, PM_GroupBox):
            self.setTitle(title)
        else: # Parent is a PM_Dialog, so add a title button.
            self.titleButton = self._getTitleButton(self, title)
            self._vBoxLayout.insertWidget(0, self.titleButton)
            self.connect( self.titleButton, 
                          SIGNAL("clicked()"),
                          self.toggleExpandCollapse)
            
        # Fixes the height of the group box. Very important. Mark 2007-05-29
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy(QSizePolicy.Preferred),
                        QSizePolicy.Policy(QSizePolicy.Fixed)))
        
        self._addBottomSpacer()
        
    def _addBottomSpacer(self):
        """
        Add a vertical spacer below this group box.
        
        Method: Assume this is going to be the last group box in the PM, so set
        its spacer's vertical sizePolicy to MinimumExpanding. We then set the 
        vertical sizePolicy of the last group box's spacer to Fixed and set its
        height to pmGroupBoxSpacing.
        """
        # Spacers are only added to groupboxes in the PropMgr, not
        # nested groupboxes.
        from PM_Dialog import PM_Dialog
        if not isinstance(self.parentWidget, PM_Dialog):
            self.verticalSpacer = None
            return
        
        if self.parentWidget._lastGroupBox:
            # _lastGroupBox is no longer the last one. <self> will be the
            # _lastGroupBox, so we must change the verticalSpacer height 
            # and sizePolicy of _lastGroupBox to be a fixed
            # spacer between it and <self>.
            defaultHeight = pmGroupBoxSpacing
            self.parentWidget._lastGroupBox.verticalSpacer.changeSize(
                10, defaultHeight, 
                QSizePolicy.Fixed,
                QSizePolicy.Fixed)
            self.parentWidget._lastGroupBox.verticalSpacer.defaultHeight = defaultHeight
            
        # Add a 1 pixel high, MinimumExpanding VSpacer below this group box.
        # This keeps all group boxes in the PM layout squeezed together as 
        # group boxes  are expanded, collapsed, hidden and shown again.
        defaultHeight = 1
        self.verticalSpacer = QSpacerItem(10, defaultHeight, 
                                        QSizePolicy.Fixed,
                                        QSizePolicy.MinimumExpanding)
        
        self.verticalSpacer.defaultHeight = defaultHeight
        
        self.parentWidget.vBoxLayout.addItem(self.verticalSpacer)
        
        # This groupbox is now the last one in the PropMgr.
        self.parentWidget._lastGroupBox = self
        
    def restoreDefault (self):
        """
        Restores the default values for all widgets in this group box.
        """
        for widget in self._widgetList:
            if platform.atom_debug:
                print "PM_GroupBox.restoreDefault(): widget =", widget.objectName()
            widget.restoreDefault()
    
    def getTitle(self):
        """
        Returns the group box title.
        
        @return: The group box title.
        @rtype:  str
        """
        return self._title
    
    def setTitle(self, title):
        """
        Sets the groupbox title to <title>.
        
        @param title: The group box title.
        @type  title: str
        
        @attention: This overrides QGroupBox's setTitle() method.
        """
        
        if not title:
            return
        
        # Create QLabel widget.
        if not self.labelWidget:
            self.labelWidget = QLabel()
            self.vBoxLayout.insertWidget(0, self.labelWidget)
            labelAlignment = pmLeftAlignment
            self.labelWidget.setAlignment(labelAlignment)
        
        self._title = title
        self.labelWidget.setText(title)
        
    def getPmWidgetPlacementParameters(self, pmWidget):
        """
        Returns all the layout parameters needed to place 
        a PM_Widget in the group box grid layout.
        
        @param pmWidget: The PM widget.
        @type  pmWidget: PM_Widget
        """
        
        label       = pmWidget.label
        labelColumn = pmWidget.labelColumn
        spanWidth   = pmWidget.spanWidth
        row         = self._rowCount
        
        if not spanWidth: 
            # This widget and its label are on the same row
            labelRow       = row
            labelSpanCols  = 1
            labelAlignment = pmRightAlignment
            # Set the widget's row and column parameters.
            widgetRow      = row
            widgetColumn   = 1
            widgetSpanCols = 1
            widgetAlignment = pmLeftAlignment
            rowIncrement   = 1
            
            if labelColumn == 1:
                widgetColumn   = 0
                labelAlignment = pmLeftAlignment
                widgetAlignment = pmRightAlignment
            
        else: 
            # This widget spans the full width of the groupbox           
            if label: 
                # The label and widget are on separate rows.
                    
                # Set the label's row, column and alignment.
                labelRow       = row
                labelColumn    = 0
                labelSpanCols  = 2
                    
                # Set this widget's row and column parameters.
                widgetRow      = row + 1 # Widget is below the label.
                widgetColumn   = 0
                widgetSpanCols = 2
                
                rowIncrement   = 2
            else:  # No label. Just the widget.
                labelRow       = 0
                labelColumn    = 0
                labelSpanCols  = 0

                # Set the widget's row and column parameters.
                widgetRow      = row
                widgetColumn   = 0
                widgetSpanCols = 2
                rowIncrement   = 1
                
            labelAlignment = pmLeftAlignment
            widgetAlignment = pmLeftAlignment
                
        return widgetRow, \
               widgetColumn, \
               widgetSpanCols, \
               widgetAlignment, \
               rowIncrement, \
               labelRow, \
               labelColumn, \
               labelSpanCols, \
               labelAlignment
    
    def addPmWidget(self, pmWidget):
        """
        Add a PM widget and its label to this group box.
        
        @param pmWidget: The PM widget to add.
        @type  pmWidget: PM_Widget
        """
        
        # Get all the widget and label layout parameters.
        widgetRow, \
        widgetColumn, \
        widgetSpanCols, \
        widgetAlignment, \
        rowIncrement, \
        labelRow, \
        labelColumn, \
        labelSpanCols, \
        labelAlignment = \
            self.getPmWidgetPlacementParameters(pmWidget)
        
        if pmWidget.labelWidget:            
            self.gridLayout.addWidget( pmWidget.labelWidget,
                                       labelRow, 
                                       labelColumn,
                                       1, 
                                       labelSpanCols,
                                       labelAlignment )
        
        # The following is a workaround for a Qt bug. If addWidth()'s 
        # <alignment> argument is not supplied, the widget spans the full 
        # column width of the grid cell containing it. If <alignment> 
        # is supplied, this desired behavior is lost and there is no 
        # value that can be supplied to maintain the behavior (0 doesn't 
        # work). The workaround is to call addWidget() without the <alignment>
        # argument. Mark 2007-07-27.
        if widgetAlignment == pmLeftAlignment:
            self.gridLayout.addWidget( pmWidget,
                                       widgetRow, 
                                       widgetColumn,
                                       1, 
                                       widgetSpanCols ) 
                                       # aligment = 0 doesn't work.
        else:
            self.gridLayout.addWidget( pmWidget,
                                       widgetRow, 
                                       widgetColumn,
                                       1, 
                                       widgetSpanCols, 
                                       widgetAlignment )
        
        self._widgetList.append(pmWidget)
        
        self._rowCount += rowIncrement
        
    def addQtWidget(self, qtWidget, column, spanWidth):
        """
        Add a Qt widget to this group box.
        
        @param qtWidget: The Qt widget to add.
        @type  qtWidget: QWidget
        
        @warning: this method has not been tested yet.
        """
        # Set the widget's row and column parameters.
        widgetRow      = self._rowCount
        widgetColumn   = column
        if spanWidth:
            widgetSpanCols = 2
        else:
            widgetSpanCols = 1
        
        self.gridLayout.addWidget( qtWidget,
                                   widgetRow, 
                                   widgetColumn,
                                   1, 
                                   widgetSpanCols )
        
        self._rowCount += 1

    def hide(self):
        """
        Hides the group box .
        
        @see: L{show}
        """
        QWidget.hide(self)
        if self.labelWidget:
            self.labelWidget.hide() 
        
        # Change the spacer height to zero to "hide" it unless
        # self is the last GroupBox in the Property Manager.
        if self.parentWidget._lastGroupBox is self:
            return
        
        if self.verticalSpacer:
            self.verticalSpacer.changeSize(10, 0)
            
    def show(self):
        """
        Unhides the group box.
        
        @see: L{hide}
        """
        QWidget.show(self)
        if self.labelWidget:
            self.labelWidget.show() 
        
        if self.parentWidget._lastGroupBox is self:
            return
        
        if self.verticalSpacer:
            self.verticalSpacer.changeSize(10, self.verticalSpacer.defaultHeight)

    # Title Button Methods #####################################
    
    def _getTitleButton(self, 
                        parentWidget = None,
                        title        = '', 
                        showExpanded = True ):
        """
        Return the group box title push button. The push button is customized 
        such that it appears as a title bar at the top of the group box. 
        If the user clicks on this 'title bar' it sends a signal to open or close
        the group box.
        
        @param parentWidget: The parent dialog or group box containing this widget.
        @type  parentWidget: PM_Dialog or PM_GroupBox
        
        @param title: The button title.
        @type  title: str 
        
        @param showExpanded: dDetermines whether the expand or collapse image is 
                             displayed on the title button.
        @type  showExpanded: bool
                             
        @see: L{_getTitleButtonStyleSheet()}
        
        @Note: Including a title button should only be legal if the parentWidget
               is a PM_Dialog.
        """
        
        button  = QPushButton(title, parentWidget)
        button.setFlat(False)
        button.setAutoFillBackground(True)
        
        button.setStyleSheet(self._getTitleButtonStyleSheet(showExpanded))     
        
        self.titleButtonPalette = self._getTitleButtonPalette()
        button.setPalette(self.titleButtonPalette)
        
        # ninad 070221 set a non-existant 'Ghost Icon' for this button.
        # By setting this icon, the button text left aligns! 
        # (which what we want :-) )
        # So this might be a bug in Qt4.2.  If we don't use the following kludge, 
        # there is no way to left align the push button text but to subclass it. 
        # (could means a lot of work for such a minor thing).  So OK for now.
        
        button.setIcon(geticon("ui/actions/Properties Manager/GHOST_ICON"))
        
        return button
    
    def _getTitleButtonPalette(self):
        """
        Return a palette for the title button. 
        """
        return getPalette(None, QPalette.Button, pmGrpBoxButtonColor)
    
    
    def _getTitleButtonStyleSheet(self, showExpanded = True):
        """
        Returns the style sheet for a group box title button (or checkbox).
        
        @param showExpanded: Determines whether to include an expand or
                             collapse icon.
        @type  showExpanded: bool
        
        @return: The title button style sheet.
        @rtype:  str
        """
        
        # Need to move border color and text color to top (make global constants).
        if showExpanded:        
            styleSheet = "QPushButton {border-style:outset;\
            border-width: 2px;\
            border-color: " + pmGrpBoxButtonBorderColor + ";\
            border-radius:2px;\
            font:bold 12px 'Arial'; \
            color: " + pmGrpBoxButtonTextColor + ";\
            min-width:10em;\
            background-image: url(" + pmGrpBoxExpandedIconPath + ");\
            background-position: right;\
            background-repeat: no-repeat;\
            }"       
        else:
            
            styleSheet = "QPushButton {border-style:outset;\
            border-width: 2px;\
            border-color: " + pmGrpBoxButtonBorderColor + ";\
            border-radius:2px;\
            font: bold 12px 'Arial'; \
            color: " + pmGrpBoxButtonTextColor + ";\
            min-width:10em;\
            background-image: url(" + pmGrpBoxCollapsedIconPath + ");\
            background-position: right;\
            background-repeat: no-repeat;\
            }"
            
        return styleSheet
            
    def toggleExpandCollapse(self):
        """
        Slot method for the title button to expand/collapse the group box.
        """
        if self._widgetList:
            if self.expanded:
                self.vBoxLayout.setMargin(0)
                self.vBoxLayout.setSpacing(0)
                self.gridLayout.setMargin(0)
                self.gridLayout.setSpacing(0)
                # The styleSheet contains the expand/collapse.
                styleSheet = self._getTitleButtonStyleSheet(showExpanded = False)
                self.titleButton.setStyleSheet(styleSheet)
                # Why do we have to keep resetting the palette?
                # Does assigning a new styleSheet reset the button's palette?
                # If yes, we should add the button's color to the styleSheet.
                # Mark 2007-05-20
                self.titleButton.setPalette(self._getTitleButtonPalette())
                self.titleButton.setIcon(
                    geticon("ui/actions/Properties Manager/GHOST_ICON"))
                self._containerWidget.hide()
                self.expanded = False 
            else: # Expand groupbox by showing all widgets in groupbox.
                from PM_MessageGroupBox import PM_MessageGroupBox
                if isinstance(self, PM_MessageGroupBox):
                    # If we don't do this, we get a small space b/w the 
                    # title button and the MessageTextEdit widget.
                    # Extra code unnecessary, but more readable. 
                    # Mark 2007-05-21
                    self.gridLayout.setMargin(0)
                    self.gridLayout.setSpacing(0)
                else:
                    self.vBoxLayout.setMargin(pmGrpBoxVboxLayoutMargin)
                    self.vBoxLayout.setSpacing(pmGrpBoxVboxLayoutSpacing)
                    self.gridLayout.setMargin(pmGrpBoxGridLayoutMargin)
                    self.gridLayout.setSpacing(pmGrpBoxGridLayoutSpacing)
                    
                # The styleSheet contains the expand/collapse.
                styleSheet = self._getTitleButtonStyleSheet(showExpanded = True)
                self.titleButton.setStyleSheet(styleSheet)
                # Why do we have to keep resetting the palette?
                # Does assigning a new styleSheet reset the button's palette?
                # If yes, we should add the button's color to the styleSheet.
                # Mark 2007-05-20
                self.titleButton.setPalette(self._getTitleButtonPalette())
                self.titleButton.setIcon(
                    geticon("ui/actions/Properties Manager/GHOST_ICON"))
                self._containerWidget.show()
                self.expanded = True         
        else:
            print "Clicking on the group box button has no effect \
                   since it has no widgets."
    
    # GroupBox palette and stylesheet methods. ##############################
    
    def _getPalette(self):
        """
        Return a palette for this group box. The color should be slightly 
        darker (or lighter) than the property manager background.
        
        @return: The group box palette.
        @rtype:  U{B{QPalette}<http://doc.trolltech.com/4/qpalette.html>}
        """
        return getPalette( None, QPalette.Window, pmGrpBoxColor )
    
    def _getStyleSheet(self):
        """
        Return the style sheet for the groupbox. This sets the following 
        properties only:
         - border style
         - border width
         - border color
         - border radius (on corners)
        The background color for a groupbox is set using getPalette().
        
        @return: The group box style sheet.
        @rtype:  str
        
        """
        
        styleSheet = \
                   "QGroupBox {border-style:solid;\
                   border-width: 1px;\
                   border-color: " + pmGrpBoxBorderColor + ";\
                   border-radius: 0px;\
                   min-width: 10em; }" 
        
        ## For Groupboxs' Pushbutton : 
        ##Other options not used : font:bold 10px;  
        
        return styleSheet

# End of PM_GroupBox ############################