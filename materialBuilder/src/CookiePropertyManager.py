# Copyright 2004-2007 Brandon Keith  See LICENSE file for details. 
"""
$Id: CookiePropertyManager.py,v 1.6 2007/07/01 17:27:31 emessick Exp $
"""

from PyQt4 import QtCore, QtGui
from Ui_CookiePropertyManager import Ui_CookiePropertyManager
from PropertyManagerMixin import PropertyManagerMixin, pmSetPropMgrIcon, pmSetPropMgrTitle
from PyQt4.Qt import Qt, SIGNAL

class CookiePropertyManager(QtGui.QWidget, 
                            PropertyManagerMixin, 
                            Ui_CookiePropertyManager):
    
    # <title> - the title that appears in the property manager header.
    title = "Build Cystal"
    # <iconPath> - full path to PNG file that appears in the header.
    iconPath = "ui/actions/Tools/Build Structures/Build Crystal.png"
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.setupUi(self)
        self.retranslateUi(self)
        
        # setupUi() did not add the icon or title. We do that here.
	pmSetPropMgrIcon( self, self.iconPath )
        pmSetPropMgrTitle( self, self.title )
        
        # Connect widget signals to slots
        self.connect(self.cookieSpec_groupBoxButton, 
                     SIGNAL("clicked()"),
                     self.toggle_cookieSpec_groupBox)      
        self.connect(self.layerProperties_groupBoxButton, 
                     SIGNAL("clicked()"), 
                     self.toggle_layerProperties_groupBox)        
        self.connect(self.displayOptions_groupBoxButton, 
                     SIGNAL("clicked()"),
                     self.toggle_displayOptions_groupBox)      
        self.connect(self.advancedOptions_groupBoxButton, 
                     SIGNAL("clicked()"),
                     self.toggle_advancedOptions_groupBox)    
        
    def toggle_cookieSpec_groupBox(self):
        self.toggle_groupbox(self.cookieSpec_groupBoxButton, self.latticeCBox, self.latticeLabel, self.surface100_btn,
                         self.surface110_btn, self.surface111_btn, self.gridOrientation_label,
                         self.rotateGrid_label, self.gridRotateAngle, self.antiRotateButton, self.rotateButton)
        
    def toggle_advancedOptions_groupBox(self):
        self.toggle_groupbox(self.advancedOptions_groupBoxButton, self.snapGridCheckBox, self.freeViewCheckBox)
        
    def toggle_displayOptions_groupBox(self):
        self.toggle_groupbox(self.displayOptions_groupBoxButton, self.dispTextLabel, self.dispModeCBox, 
                             self.fullModelCheckBox, self.gridLineCheckBox)
        
    def toggle_layerProperties_groupBox(self):
        self.toggle_groupbox(self.layerProperties_groupBoxButton, self.currentLayer_label, self.currentLayerCBox, 
                             self.addLayerButton,
                             self.latticeCells_label,  self.layerCellsSpinBox,
                             self.layerThickness_label, self.layerThicknessLineEdit)   
