# Copyright 2004-2007 Brandon Keith  See LICENSE file for details. 
"""
$Id: Ui_DimensionsMenu.py,v 1.3 2007/07/01 17:27:32 emessick Exp $
"""

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import Qt
from Utility import geticon


def setupUi(win):
    
    MainWindow = win
    
    #####Dimensions menu start#####
    
    #measurement jigs moved from jigs menu to Tools> dimensionsMenu
    win.jigsDistanceAction = QtGui.QWidgetAction(MainWindow)
    win.jigsDistanceAction.setIcon(geticon("ui/actions/Tools/Dimensions/Measure_Distance"))
    win.jigsDistanceAction.setObjectName("jigsDistanceAction")

    win.jigsAngleAction = QtGui.QWidgetAction(MainWindow)
    win.jigsAngleAction.setIcon(geticon("ui/actions/Tools/Dimensions/Measure_Angle"))
    win.jigsAngleAction.setObjectName("jigsAngleAction")

    win.jigsDihedralAction = QtGui.QWidgetAction(MainWindow)
    win.jigsDihedralAction.setIcon(geticon("ui/actions/Tools/Dimensions/Measure_Dihedral"))
    win.jigsDihedralAction.setObjectName("jigsDihedralAction")
    
    
    win.dimensionsMenu.addAction(win.jigsDistanceAction)
    win.dimensionsMenu.addAction(win.jigsAngleAction)
    win.dimensionsMenu.addAction(win.jigsDihedralAction)
    #####Dimensions menu end##### 
    
    
def retranslateUi(win):
    
    win.dimensionsMenu.setTitle(QtGui.QApplication.translate("MainWindow", "&Dimensions", None, QtGui.QApplication.UnicodeUTF8))
    
    #TOOLS > DIMENSIONS MENU
    win.jigsDistanceAction.setText(QtGui.QApplication.translate("MainWindow", "Measure Distance", None, QtGui.QApplication.UnicodeUTF8))
    win.jigsDistanceAction.setIconText(QtGui.QApplication.translate("MainWindow", "Measure Distance", None, QtGui.QApplication.UnicodeUTF8))
    win.jigsAngleAction.setText(QtGui.QApplication.translate("MainWindow", "Measure Angle", None, QtGui.QApplication.UnicodeUTF8))
    win.jigsAngleAction.setIconText(QtGui.QApplication.translate("MainWindow", "Measure Angle", None, QtGui.QApplication.UnicodeUTF8))
    win.jigsDihedralAction.setText(QtGui.QApplication.translate("MainWindow", "Measure Dihedral", None, QtGui.QApplication.UnicodeUTF8))
    win.jigsDihedralAction.setIconText(QtGui.QApplication.translate("MainWindow", "Measure Dihedral", None, QtGui.QApplication.UnicodeUTF8))
    
