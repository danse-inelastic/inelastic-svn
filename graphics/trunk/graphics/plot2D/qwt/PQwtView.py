# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jwliu/test/pythontest/pdffit2/utils/graphics/plot/pqwtview.ui'
#
# Created: Tue May 17 18:27:18 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
# WARNING! All changes made in this file will be lost!
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#Modified by:  Jiwu Liu (jliu@pa.msu.edu)
#description: This is a class implemented with Qwt lib to plot.
#<LicenseText>
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys
from qt import *
from qwt import *

class PQwtView(QDialog):
    def __init__(self, parent = None,name = None,modal=0,fl=0):
        QDialog.__init__(self,parent,name,modal,fl)
        
        if not name: self.setName("PQwtView")

        self.setSizeGripEnabled(1)
        
        ##LayoutWidget = QWidget(self,"layout1")
        ##LayoutWidget.setGeometry(QRect(22,22,500,280))
        # Inorder to resize the dialog without messing up the form appearance, we must set:
        LayoutWidget = self
        
        layout1 = QVBoxLayout(LayoutWidget,11,6,"layout1")

        self.qwtPlot1 = QwtPlot(LayoutWidget,"qwtPlot1")
        self.qwtPlot1.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,255,255,self.qwtPlot1.sizePolicy().hasHeightForWidth()))
        self.qwtPlot1.setMinimumSize(QSize(450,234))
        self.qwtPlot1.setAxisAutoScale(QwtPlot.yLeft)
        self.qwtPlot1.setAxisAutoScale(QwtPlot.xBottom)
        self.qwtPlot1.setCanvasBackground(Qt.white)
        self.qwtPlot1.setAutoLegend(True)
        layout1.addWidget(self.qwtPlot1)

        layout2 = QHBoxLayout(None,0,6,"layout2")

        self.buttonHelp = QPushButton(LayoutWidget,"buttonHelp")
        self.buttonHelp.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.buttonHelp.sizePolicy().hasHeightForWidth()))
        self.buttonHelp.setMinimumSize(QSize(80,32))
        self.buttonHelp.setAutoDefault(1)
        layout2.addWidget(self.buttonHelp)
        Horizontal_Spacing2 = QSpacerItem(238,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(Horizontal_Spacing2)

        self.buttonOk = QPushButton(LayoutWidget,"buttonOk")
        self.buttonOk.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.buttonOk.sizePolicy().hasHeightForWidth()))
        self.buttonOk.setMinimumSize(QSize(80,32))
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        layout2.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton(LayoutWidget,"buttonCancel")
        self.buttonCancel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.buttonCancel.sizePolicy().hasHeightForWidth()))
        self.buttonCancel.setMinimumSize(QSize(80,32))
        self.buttonCancel.setAutoDefault(1)
        layout2.addWidget(self.buttonCancel)
        layout1.addLayout(layout2)

        self.languageChange()

        self.resize(QSize(555,331).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.buttonOk,SIGNAL("clicked()"),self.accept)
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self.reject)

    def languageChange(self):
        self.setCaption(self.__tr("Pdffit2 2D Plotting"))
        self.buttonHelp.setText(self.__tr("&Help"))
        self.buttonHelp.setAccel(self.__tr("F1"))
        self.buttonOk.setText(self.__tr("&OK"))
        self.buttonOk.setAccel(QString.null)
        self.buttonCancel.setText(self.__tr("&Cancel"))
        self.buttonCancel.setAccel(QString.null)

    def __tr(self,s,c = None):
        # qApp is a global instance from qt. It must have been created at this moment.
        return qApp.translate("PQwtView",s,c)
        
if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = PQwtView()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()

#version
__id__ = '$Id: pqwtview.py,v 1.6 2005/08/31 19:51:12 jwliu Exp $'
