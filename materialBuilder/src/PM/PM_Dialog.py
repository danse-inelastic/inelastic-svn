# Copyright 2006-2007 Brandon Keith  See LICENSE file for details. 
"""
PM_Dialog.py

@author: Mark
@version: $Id: PM_Dialog.py,v 1.5 2007/08/09 16:09:20 polosims Exp $
@copyright: 2006-2007 Brandon Keith  All rights reserved.

History:

mark 2007-07-22: Split PropMgrBaseClass out of PropMgrBaseClass.py into this 
file and renamed it PM_Dialog.
"""

from debug import print_compact_traceback

from Utility import geticon
from Utility import getpixmap

from PM_Colors import pmColor
from PM_Colors import pmHeaderFrameColor
from PM_Colors import pmHeaderTitleColor

from PM_Constants import pmMainVboxLayoutMargin
from PM_Constants import pmMainVboxLayoutSpacing
from PM_Constants import pmHeaderFrameMargin
from PM_Constants import pmHeaderFrameSpacing
from PM_Constants import pmHeaderFont
from PM_Constants import pmHeaderFontPointSize
from PM_Constants import pmHeaderFontBold
from PM_Constants import pmSponsorFrameMargin
from PM_Constants import pmSponsorFrameSpacing
from PM_Constants import pmTopRowBtnsMargin
from PM_Constants import pmTopRowBtnsSpacing
from PM_Constants import pmGroupBoxSpacing
from PM_Constants import pmGrpBoxVboxLayoutMargin
from PM_Constants import pmGrpBoxVboxLayoutSpacing
from PM_Constants import pmGridLayoutMargin
from PM_Constants import pmGridLayoutSpacing
from PM_Constants import pmLeftAlignment

from PM_Constants import pmAllButtons
from PM_Constants import pmDoneButton
from PM_Constants import pmCancelButton
from PM_Constants import pmRestoreDefaultsButton
from PM_Constants import pmPreviewButton
from PM_Constants import pmWhatsThisButton

from PyQt4.Qt import SIGNAL
from PyQt4.Qt import QDialog
from PyQt4.Qt import QFont
from PyQt4.Qt import QFrame
from PyQt4.Qt import QGridLayout
from PyQt4.Qt import QLabel
from PyQt4.Qt import QPushButton
from PyQt4.Qt import QPalette
from PyQt4.Qt import QToolButton
from PyQt4.Qt import QSpacerItem
from PyQt4.Qt import QHBoxLayout
from PyQt4.Qt import QVBoxLayout
from PyQt4.Qt import QSize
from PyQt4.Qt import QSizePolicy
from PyQt4.Qt import QWhatsThis

from PM_GroupBox         import PM_GroupBox
from PM_MessageGroupBox  import PM_MessageGroupBox

from Sponsors import SponsorableMixin

class PM_Dialog( QDialog, SponsorableMixin ):
    """
    The PM_Dialog class is the base class for Property Manager dialogs.
    
    [To make a PM class from this mixin-superclass, subclass it to customize
    the widget set and add behavior.
    You must also provide certain methods provided by GeneratorBaseClass
    (either by inheriting it -- not sure if superclass order matters for that --
    or by defining them yourself), including ok_btn_clicked and several others,
    including at least some defined by SponsorableMixin (open_sponsor_homepage, setSponsor).
    This set of requirements may be cleaned up.]
    [Note: Technically, this is not a "base class" but a "mixin class".]    
    """
    
    headerTitleText  = ""  # The header title text.
    
    _widgetList = [] # A list of all group boxes in this PM dialog, 
                     # including the message group box.
                     # (but not header, sponsor button, etc.)
    _groupBoxCount = 0 # Number of PM_GroupBoxes in this PM dialog.
    _lastGroupBox = None # The last PM_GroupBox in this PM dialog. 
                        # (i.e. the most recent PM_GroupBox added).
    
    def __init__(self, 
                 name,
                 iconPath = "",
                 title    = ""
                 ):
        """
        Property Manager constructor.
        
        @param name: the name to assign the property manager dialog object.
        @type  name: str
        
        @param iconPath: the relative path for the icon (PNG image) that 
                         appears in the header.
        @type  iconPath: str
        
        @param title: the title that appears in the header.
        @type  title: str
        """
        
        QDialog.__init__(self)
        
        self.setObjectName(name)
        self._widgetList = [] 
        
        # Main pallete for PropMgr.
        
        self.setPalette(QPalette(pmColor))
        
        # Main vertical layout for PropMgr.
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setMargin(pmMainVboxLayoutMargin)
        self.vBoxLayout.setSpacing(pmMainVboxLayoutSpacing)

        # Add PropMgr's header, sponsor button, top row buttons and (hidden) message group box.
        self._createHeader(iconPath, title)
        self._createSponsorButton()
        self._createTopRowBtns() # Create top buttons row
        
        self.MessageGroupBox = PM_MessageGroupBox(self)
        
        # Keep the line below around; it might be useful.
        # I may want to use it now that I understand it.
        # Mark 2007-05-17.
        #QMetaObject.connectSlotsByName(self)
            
    def show(self):
        """
        Show this Property Manager.
        """
        self.setSponsor()
        
        if not self.pw or self:            
            self.pw = self.win.activePartWindow()
            
        self.pw.updatePropertyManagerTab(self)
        self.pw.featureManager.setCurrentIndex(self.pw.featureManager.indexOf(self))
        
        # Show the default message whenever we open the Property Manager.
        self.MessageGroupBox.MessageTextEdit.restoreDefault()
    
    def _createHeader(self, iconPath, title):
        """
        Creates the Property Manager header, which contains an icon
        (a QLabel with a pixmap) and white text (a QLabel with text).
        
        @param iconPath: the relative path for the icon (PNG image) that 
                         appears in the header.
        @type  iconPath: str
        
        @param title: the title that appears in the header.
        @type  title: str
        """
        
        # Heading frame (dark gray), which contains 
        # a pixmap and (white) heading text.
        self.headerFrame = QFrame(self)
        self.headerFrame.setFrameShape(QFrame.NoFrame)
        self.headerFrame.setFrameShadow(QFrame.Plain)
        
        self.headerFrame.setPalette(QPalette(pmHeaderFrameColor))
        self.headerFrame.setAutoFillBackground(True)

        # HBox layout for heading frame, containing the pixmap
        # and label (title).
        HeaderFrameHLayout = QHBoxLayout(self.headerFrame)
        HeaderFrameHLayout.setMargin(pmHeaderFrameMargin) # 2 pixels around edges.
        HeaderFrameHLayout.setSpacing(pmHeaderFrameSpacing) # 5 pixel between pixmap and label.

        # PropMgr icon. Set image by calling setHeaderIcon().
        self.headerIcon = QLabel(self.headerFrame)
        self.headerIcon.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy(QSizePolicy.Fixed),
                              QSizePolicy.Policy(QSizePolicy.Fixed)))
            
        self.headerIcon.setScaledContents(True)
        
        HeaderFrameHLayout.addWidget(self.headerIcon)
        
        # PropMgr header title text (a QLabel).
        self.headerTitle = QLabel(self.headerFrame)
        headerTitlePalette = self._getHeaderTitlePalette()
        self.headerTitle.setPalette(headerTitlePalette)
        self.headerTitle.setAlignment(pmLeftAlignment)

        # Assign header title font.
        self.headerTitle.setFont(self._getHeaderFont())
        HeaderFrameHLayout.addWidget(self.headerTitle)
        
        self.vBoxLayout.addWidget(self.headerFrame)
        
        # Set header icon and title text.
        self.setHeaderIcon(iconPath)
        self.setHeaderTitle(title)
        
    def _getHeaderFont(self):
        """
        Returns the QFont used for all PropMgr headers.
        
        @return: the header font
        @rtype:  QFont
        """
        font = QFont()
        font.setFamily(pmHeaderFont)
        font.setPointSize(pmHeaderFontPointSize)
        font.setBold(pmHeaderFontBold)
        return font
        
    def setHeaderTitle(self, title):
        """
        Set the Propery Manager header title to string <title>.
        
        @param title: the title to insert in the header.
        @type  title: str
        """
        self.headerTitleText = title
        self.headerTitle.setText(title)
    
    def setHeaderIcon(self, iconPath):
        """
        Set the Propery Manager header icon.
        
        @param iconPath: the relative path to the PNG file containing the icon image.
        @type  iconPath: str
        """
        
        if not iconPath:
            return
        
        self.headerIcon.setPixmap(getpixmap(iconPath))
        
    def _createSponsorButton(self):
        """
        Creates the Property Manager sponsor button, which contains
        a QPushButton inside of a QGridLayout inside of a QFrame.
        The sponsor logo image is not loaded here.
        """
        
        # Sponsor button (inside a frame)
        self.sponsor_frame = QFrame(self)
        self.sponsor_frame.setFrameShape(QFrame.NoFrame)
        self.sponsor_frame.setFrameShadow(QFrame.Plain)

        SponsorFrameGrid = QGridLayout(self.sponsor_frame)
        SponsorFrameGrid.setMargin(pmSponsorFrameMargin)
        SponsorFrameGrid.setSpacing(pmSponsorFrameSpacing) # Has no effect.

        self.sponsor_btn = QPushButton(self.sponsor_frame)
        self.sponsor_btn.setAutoDefault(False)
        self.sponsor_btn.setFlat(True)
        self.connect(self.sponsor_btn,
                     SIGNAL("clicked()"),
                     self.open_sponsor_homepage)
        
        SponsorFrameGrid.addWidget(self.sponsor_btn,0,0,1,1)
        
        self.vBoxLayout.addWidget(self.sponsor_frame)

        button_whatsthis_widget = self.sponsor_btn
            #bruce 070615 bugfix -- put tooltip & whatsthis on self.sponsor_btn, not self.
            # [self.sponsor_frame might be another possible place to put them.]
        
        button_whatsthis_widget.setWhatsThis("""<b>Sponsor Button</b>
            <p>When clicked, this sponsor logo will display a short 
            description about a Sample Builder sponsor. This can 
            be an official sponsor or credit given to a contributor 
            that has helped code part or all of this command. 
            A link is provided in the description to learn more 
            about this sponsor.</p>""")
        
        button_whatsthis_widget.setToolTip("Sample Builder Sponsor Button")
        
        return

    def _createTopRowBtns(self):
        """
        Creates the Done, Cancel, Preview, Restore Defaults and What's This 
        buttons row at the top of the Property Manager.
        """        
        
        # Main "button group" widget (but it is not a QButtonGroup).
        self.pmTopRowBtns = QHBoxLayout()
        # This QHBoxLayout is (probably) not necessary. Try using just the frame for
        # the foundation. I think it should work. Mark 2007-05-30
        
        # Horizontal spacer
        horizontalSpacer = QSpacerItem(1, 1, 
                                QSizePolicy.Expanding, 
                                QSizePolicy.Minimum)
        
        # Frame containing all the buttons.
        self.topRowBtnsFrame = QFrame()
                
        self.topRowBtnsFrame.setFrameShape(QFrame.NoFrame)
        self.topRowBtnsFrame.setFrameShadow(QFrame.Plain)
        
        # Create Hbox layout for main frame.
        topRowBtnsHLayout = QHBoxLayout(self.topRowBtnsFrame)
        topRowBtnsHLayout.setMargin(pmTopRowBtnsMargin)
        topRowBtnsHLayout.setSpacing(pmTopRowBtnsSpacing)
        
        topRowBtnsHLayout.addItem(horizontalSpacer)
        
        # Set button type.
        if 1: # Mark 2007-05-30
            # Needs to be QToolButton for MacOS. Fine for Windows, too.
            buttonType = QToolButton 
            # May want to use QToolButton.setAutoRaise(1) below. Mark 2007-05-29
        else:
            buttonType = QPushButton # Do not use.
        
        # Done (OK) button.
        self.done_btn = buttonType(self.topRowBtnsFrame)
        self.done_btn.setIcon(
            geticon("ui/actions/Properties Manager/Done.png"))
        self.done_btn.setIconSize(QSize(22,22))  
        self.connect(self.done_btn,
                     SIGNAL("clicked()"),
                     self.doneButtonClicked)
        self.done_btn.setToolTip("Done")
        
        topRowBtnsHLayout.addWidget(self.done_btn)
        
        # Cancel (Abort) button.
        self.cancel_btn = buttonType(self.topRowBtnsFrame)
        self.cancel_btn.setIcon(
            geticon("ui/actions/Properties Manager/Abort.png"))
        self.cancel_btn.setIconSize(QSize(22,22))
        self.connect(self.cancel_btn,
                     SIGNAL("clicked()"),
                     self.cancelButtonClicked)
        self.cancel_btn.setToolTip("Cancel")
        
        topRowBtnsHLayout.addWidget(self.cancel_btn)
        
        #@ abort_btn depreciated. We still need it because modes use it. 
        self.abort_btn = self.cancel_btn
        
        # Restore Defaults button.
        self.restore_defaults_btn = buttonType(self.topRowBtnsFrame)
        self.restore_defaults_btn.setIcon(
            geticon("ui/actions/Properties Manager/Restore.png"))
        self.restore_defaults_btn.setIconSize(QSize(22,22))
        self.connect(self.restore_defaults_btn,
                     SIGNAL("clicked()"),
                     self.restoreDefaultsButtonClicked)
        self.restore_defaults_btn.setToolTip("Restore Defaults")
        topRowBtnsHLayout.addWidget(self.restore_defaults_btn)
        
        # Preview (glasses) button.
        self.preview_btn = buttonType(self.topRowBtnsFrame)
        self.preview_btn.setIcon(
            geticon("ui/actions/Properties Manager/Preview.png"))
        self.preview_btn.setIconSize(QSize(22,22))
        self.connect(self.preview_btn,
                     SIGNAL("clicked()"),
                     self.previewButtonClicked)
        self.preview_btn.setToolTip("Preview")
        
        topRowBtnsHLayout.addWidget(self.preview_btn)        
        
        # What's This (?) button.
        self.whatsthis_btn = buttonType(self.topRowBtnsFrame)
        self.whatsthis_btn.setIcon(
            geticon("ui/actions/Properties Manager/WhatsThis.png"))
        self.whatsthis_btn.setIconSize(QSize(22,22))
        self.connect(self.whatsthis_btn,
                     SIGNAL("clicked()"),
                     self.whatsThisButtonClicked)
        self.whatsthis_btn.setToolTip("What\'s This Help")
        
        topRowBtnsHLayout.addWidget(self.whatsthis_btn)
        
        topRowBtnsHLayout.addItem(horizontalSpacer)
        
        # Create Button Row
        self.pmTopRowBtns.addWidget(self.topRowBtnsFrame)
        
        self.vBoxLayout.addLayout(self.pmTopRowBtns)
        
        # Add What's This for buttons.
        
        self.done_btn.setWhatsThis("""<b>Done</b>
            <p><img source=\"ui/actions/Properties Manager/Done.png\"><br>
            Completes and/or exits the current command.</p>""")
        
        self.cancel_btn.setWhatsThis("""<b>Cancel</b>
            <p><img source=\"ui/actions/Properties Manager/Abort.png\"><br>
            Cancels the current command.</p>""")
        
        self.restore_defaults_btn.setWhatsThis("""<b>Restore Defaults</b>
            <p><img source=\"ui/actions/Properties Manager/Restore.png\"><br>
            Restores the defaut values of the Property Manager.</p>""")
        
        self.preview_btn.setWhatsThis("""<b>Preview</b>
            <p><img source=\"ui/actions/Properties Manager/Preview.png\"><br>
            Preview the structure based on current Property Manager settings.</p>""")

        self.whatsthis_btn.setWhatsThis("""<b>What's This</b> 
            <p><img source=\"ui/actions/Properties Manager/WhatsThis.png\"><br>
            Click this option to invoke a small question mark that is attached to the mouse pointer, 
            then click on an object which you would like more information about. 
            A pop-up box appears with information about the object you selected.</p>""")
        
        return

    def hideTopRowButtons(self, pmButtonFlags = None):
        """
        Hides one or more top row buttons using <pmButtonFlags>.
        Button flags not set will cause the button to be shown
        if currently hidden.
        
        @param pmButtonFlags: this enumerator describes the which buttons to hide, where:
        
            - pmDoneButton            =  1
            - pmCancelButton          =  2
            - pmRestoreDefaultsButton =  4
            - pmPreviewButton         =  8
            - pmWhatsThisButton       = 16
            - pmAllButtons            = 31
            
        @type  pmButtonFlags: int
        """
        
        if pmButtonFlags & pmDoneButton: 
            self.done_btn.hide()
        else: 
            self.done_btn.show()
            
        if pmButtonFlags & pmCancelButton: 
            self.cancel_btn.hide()
        else: 
            self.cancel_btn.show()
            
        if pmButtonFlags & pmRestoreDefaultsButton: 
            self.restore_defaults_btn.hide()
        else: 
            self.restore_defaults_btn.show()
            
        if pmButtonFlags & pmPreviewButton: 
            self.preview_btn.hide()
        else: 
            self.preview_btn.show()
            
        if pmButtonFlags & pmWhatsThisButton: 
            self.whatsthis_btn.hide()
        else: 
            self.whatsthis_btn.show()
        
    def showTopRowButtons(self, pmButtonFlags = pmAllButtons):
        """
        Shows one or more top row buttons using <pmButtonFlags>.
        Button flags not set will cause the button to be hidden
        if currently displayed.
        
        @param pmButtonFlags: this enumerator describes which buttons to display, where:
        
            - pmDoneButton            =  1
            - pmCancelButton          =  2
            - pmRestoreDefaultsButton =  4
            - pmPreviewButton         =  8
            - pmWhatsThisButton       = 16
            - pmAllButtons            = 31
            
        @type  pmButtonFlags: int
        """
        
        self.hideTopRowButtons(pmButtonFlags ^ pmAllButtons)
        
    def _getHeaderTitlePalette(self):
        """
        Return a palette for header title (text) label. 
        """
        palette = QPalette()
        palette.setColor(QPalette.WindowText, pmHeaderTitleColor)
        return palette
        
    def doneButtonClicked(self):
        """
        Slot for the What's This button.
        """
        self.ok_btn_clicked()
    
    def cancelButtonClicked(self):
        """
        Slot for the What's This button.
        """
        self.cancel_btn_clicked()
    
    def restoreDefaultsButtonClicked(self):
        """
        Slot for "Restore Defaults" button in the Property Manager.
        It is called each time the button is clicked.
        """
        for widget in self._widgetList:
            if isinstance(widget, PM_GroupBox):
                widget.restoreDefault()
                         
    def previewButtonClicked(self):
        """
        Slot for the What's This button.
        """
        self.preview_btn_clicked()
        
    def whatsThisButtonClicked(self):
        """
        Slot for the What's This button.
        """
        QWhatsThis.enterWhatsThisMode()
                
# End of PropMgrBaseClass ############################