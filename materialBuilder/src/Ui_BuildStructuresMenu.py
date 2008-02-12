# Copyright 2004-2007 Brandon Keith  See LICENSE file for details. 
"""
$Id: Ui_BuildStructuresMenu.py,v 1.6 2007/07/01 17:27:32 emessick Exp $
"""

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import Qt
from Utility import geticon

def setupUi(win):
    """Construct the QWidgetActions for the Build menu and buttons on the 
    Command Manager toolbar (and main menu bar).
    """
    
    MainWindow = win

    ###Build Structures Menu start###
    win.toolsDepositAtomAction = QtGui.QWidgetAction(MainWindow)
    win.toolsDepositAtomAction.setCheckable(1) # make the build button checkable
    win.toolsDepositAtomAction.setIcon(geticon("ui/actions/Tools/Build Structures/Build Atoms"))
    
    win.toolsCookieCutAction = QtGui.QWidgetAction(MainWindow)
    win.toolsCookieCutAction.setCheckable(1) # make the cookie cutter button checkable
    win.toolsCookieCutAction.setIcon(geticon("ui/actions/Tools/Build Structures/Build Crystal"))
        
    win.insertGrapheneAction = QtGui.QWidgetAction(MainWindow)
    win.insertGrapheneAction.setIcon(geticon("ui/actions/Tools/Build Structures/Graphene"))
    win.insertGrapheneAction.setObjectName("insertGrapheneAction")
    
    win.insertNanotubeAction = QtGui.QWidgetAction(MainWindow)
    win.insertNanotubeAction.setIcon(geticon("ui/actions/Tools/Build Structures/Nanotube"))
    win.insertNanotubeAction.setObjectName("insertNanotubeAction")

    win.buildDnaAction = QtGui.QWidgetAction(MainWindow)
    win.buildDnaAction.setIcon(geticon("ui/actions/Tools/Build Structures/DNA"))
    win.buildDnaAction.setObjectName("buildDnaAction")
    
    win.buildDnaOrigamiAction = QtGui.QWidgetAction(MainWindow)
    win.buildDnaOrigamiAction.setIcon(geticon(
        "ui/actions/Tools/Build Structures/DNA_Origami"))
    win.buildDnaOrigamiAction.setObjectName("buildDnaOrigamiAction")
    
    # Create the Build menu.
    win.buildStructuresMenu.addAction(MainWindow.toolsDepositAtomAction)
    win.buildStructuresMenu.addAction(win.buildDnaAction)
    #win.buildStructuresMenu.addAction(win.buildDnaOrigamiAction)    
    win.buildStructuresMenu.addAction(win.insertNanotubeAction)
    win.buildStructuresMenu.addAction(win.insertGrapheneAction)
    win.buildStructuresMenu.addAction(MainWindow.toolsCookieCutAction)
    
    # Atom Generator (Developer Example). Mark 2007-06-08
    win.insertAtomAction = QtGui.QWidgetAction(MainWindow)
    win.insertAtomAction.setIcon(geticon("ui/actions/Toolbars/Smart/Deposit_Atoms.png"))
    win.insertAtomAction.setObjectName("insertAtomAction")
    win.buildStructuresMenu.addAction(win.insertAtomAction)
    
    # End of Build Structures Menu
    
def retranslateUi(win):
    
    win.buildStructuresMenu.setTitle(QtGui.QApplication.translate(
         "MainWindow", 
         "Build Structures", 
         None, 
         QtGui.QApplication.UnicodeUTF8))
    
    # TOOLS > BUILD STRUCTURES MENU ITEMS
    win.toolsDepositAtomAction.setText(QtGui.QApplication.translate(
         "MainWindow", 
         "Atoms", 
         None, 
         QtGui.QApplication.UnicodeUTF8))
    win.toolsDepositAtomAction.setToolTip(QtGui.QApplication.translate(
         "MainWindow", 
         "Build Atoms", 
         None, 
         QtGui.QApplication.UnicodeUTF8))
    win.buildDnaOrigamiAction.setText(QtGui.QApplication.translate(
         "MainWindow", 
         "Origami",
         None,
         QtGui.QApplication.UnicodeUTF8))
    win.buildDnaOrigamiAction.setToolTip(QtGui.QApplication.translate(
         "MainWindow",
         "Build DNA Origami", 
         None, 
         QtGui.QApplication.UnicodeUTF8))
     
    win.toolsCookieCutAction.setText(QtGui.QApplication.translate(
         "MainWindow", 
         "Crystal",
         None, 
         QtGui.QApplication.UnicodeUTF8))
    win.toolsCookieCutAction.setToolTip(QtGui.QApplication.translate(
         "MainWindow", 
         "Build Crystal",
         None, 
         QtGui.QApplication.UnicodeUTF8))
    win.insertNanotubeAction.setIconText(QtGui.QApplication.translate(
         "MainWindow",
         "Nanotube",
         None, 
         QtGui.QApplication.UnicodeUTF8))
    win.insertNanotubeAction.setToolTip(QtGui.QApplication.translate(
         "MainWindow", 
         "Build Nanotube", 
         None,
         QtGui.QApplication.UnicodeUTF8))
    win.insertGrapheneAction.setIconText(QtGui.QApplication.translate(
         "MainWindow", 
         "Graphene", 
         None, 
         QtGui.QApplication.UnicodeUTF8))
    win.insertGrapheneAction.setToolTip(QtGui.QApplication.translate(
        "MainWindow", 
        "Build Graphene Sheet", 
        None, 
        QtGui.QApplication.UnicodeUTF8))
    win.buildDnaAction.setText(QtGui.QApplication.translate(
         "MainWindow", 
         "DNA", 
         None, 
         QtGui.QApplication.UnicodeUTF8))
    win.buildDnaAction.setIconText(QtGui.QApplication.translate(
         "MainWindow", 
         "DNA",
         None,
         QtGui.QApplication.UnicodeUTF8))
    win.buildDnaAction.setToolTip(QtGui.QApplication.translate(
         "MainWindow",
         "Build DNA", 
         None, 
         QtGui.QApplication.UnicodeUTF8))
     
      
    # Atom Generator example for developers. Mark and Jeff. 2007-06-13
    #@ Jeff - add a link to the public wiki page when ready. Mark 2007-06-13.
    win.insertAtomAction.setIconText(QtGui.QApplication.translate(
        "MainWindow", 
        "Atom", 
        None, 
        QtGui.QApplication.UnicodeUTF8))
    win.insertAtomAction.setToolTip(QtGui.QApplication.translate(
        "MainWindow", 
        "Atom Generator (Developer Example)", 
        None, 
        QtGui.QApplication.UnicodeUTF8))
