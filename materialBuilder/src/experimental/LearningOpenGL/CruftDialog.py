# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CruftDialog.ui'
#
# Created: Wed Feb 6 21:51:13 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.16
#
# WARNING! All changes made in this file will be lost!


from qt import *


class CruftDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Cruft")



        self.frame1 = QFrame(self,"frame1")
        self.frame1.setGeometry(QRect(20,20,640,450))
        self.frame1.setMinimumSize(QSize(400,300))
        self.frame1.setFrameShape(QFrame.StyledPanel)
        self.frame1.setFrameShadow(QFrame.Raised)

        self.pushButton1 = QPushButton(self,"pushButton1")
        self.pushButton1.setGeometry(QRect(280,480,111,41))

        self.languageChange()

        self.resize(QSize(689,541).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton1,SIGNAL("clicked()"),self.pushButton1_clicked)


    def languageChange(self):
        self.setCaption(self.__tr("Cruft"))
        self.pushButton1.setText(self.__tr("Quit"))


    def pushButton1_clicked(self):
        print "CruftDialog.pushButton1_clicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("CruftDialog",s,c)
