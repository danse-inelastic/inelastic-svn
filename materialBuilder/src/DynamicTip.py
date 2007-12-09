# Copyright 2004-2007 Brandon Keith  See LICENSE file for details. 
"""
DynamicTip.py 

For the support of dynamic, informative tooltips of a highligthed object in the GLPane. 

History: 
060817 Mark created dynamicTip class
060818 Ninad moved DynamiceTip class into this file DynamicTip.py and added more

$Id: DynamicTip.py,v 1.16 2007/07/01 17:27:31 emessick Exp $


"""

import math
import time

from PyQt4.Qt import QToolTip, QRect

import env
from chem import atom
from elements import Singlet
from bonds import Bond
from jigs import Jig
from VQT import vlen
from platform import fix_plurals

from prefs_constants import dynamicToolTipWakeUpDelay_prefs_key
from prefs_constants import dynamicToolTipAtomDistancePrecision_prefs_key
from prefs_constants import dynamicToolTipBendAnglePrecision_prefs_key
from prefs_constants import dynamicToolTipTorsionAnglePrecision_prefs_key
from prefs_constants import dynamicToolTipAtomChunkInfo_prefs_key
from prefs_constants import dynamicToolTipBondChunkInfo_prefs_key
from prefs_constants import dynamicToolTipAtomPosition_prefs_key
from prefs_constants import dynamicToolTipAtomDistanceDeltas_prefs_key
from prefs_constants import dynamicToolTipBondLength_prefs_key
from prefs_constants import dynamicToolTipAtomMass_prefs_key



class DynamicTip: # Mark and Ninad 060817.
    """For the support of dynamic, informative tooltips of a highligthed object in the GLPane. 
    """
    def __init__(self, glpane):
        
        self.glpane = glpane       
        
        # <toolTipShown> is a flag set to True when a tooltip is currently displayed for the 
        # highlighted object under the cursor.
        self.toolTipShown = False
     
    def maybeTip(self, helpEvent):
        """Determines if this tooltip should be displayed. The tooltip will be displayed at
        <cusorPos> if an object is highlighted and the mouse hasn't moved for 
        some period of time, called the "wake up delay" period, which is a user pref
        (not yet implemented in the Preferences dialog) currently set to 1 second.
        
        <cursorPos> is the current cursor position in the GLPane's local coordinates.
        
        maybeTip() is called by GLPane.timerEvent() whenever the cursor is not moving to 
        determine if the tooltip should be displayed.
        
        For more details about this member, see Qt documentation on QToolTip.maybeTip().
        """
        
        # <motionlessCursorDuration> is the amount of time the cursor (mouse) has been motionless.
        motionlessCursorDuration = time.time()- self.glpane.cursorMotionlessStartTime
        
        # Don't display the tooltip yet if <motionlessCursorDuration> hasn't exceeded the "wake up delay".
        # The wake up delay is currently set to 1 second in prefs_constants.py. Mark 060818.
        if motionlessCursorDuration < env.prefs[dynamicToolTipWakeUpDelay_prefs_key]:
            self.toolTipShown = False
            return
        
        selobj = self.glpane.selobj
        
        # If an object is not currently highlighted, don't display a tooltip.
        if not selobj:
            return
        
        # If the highlighted object is a singlet, don't display a tooltip for it.
        if isinstance(selobj, atom) and (selobj.element is Singlet):
            return
            
        if self.toolTipShown:
            # The tooltip is already displayed, so return. Do not allow tip() to be called again or it will "flash".
            return
                   
  
        tipText = self.getToolTipText()
        
        if not tipText:            
            tipText = "" #This makes sure that dynamic tip is not displayed 
            #when the highlightable object is 'unknown' to the dynamic tip class
            
        
        QToolTip.showText(helpEvent.globalPos(), tipText)  #@@@ ninad061107 works fine but need code review
               
        self.toolTipShown = True
                            
                            
    def getToolTipText(self): # Mark 060818, Ninad 060818
        """Return the tooltip text to display, which depends on what is selected and what is highlighted.
        Fetures implemented --
        If nothing is selected, return the name of the highlighted object.
        If one atom is selected, return the distance between it and the highlighted atom.
        If two atoms are selected, return the angle between them and the highlighted atom.
        Preferences for setting the precision (decimal place) for each measurement
        Preferences for displaying atom chunk info, bond chunk info, Atom distance Deltas, 
        atom coordinates, bond length (nuclear distance), bond type.
        Displays Jig info 
        
        For later:
        If three atoms are selected, return the torsion angle between them and the highlighted atom.
        We also need to truncate long item info strings(e.g. if an item has a very long name it should
        truncate it with 3 dots : "item na...")
        """
                
        from ops_select import ops_select_Mixin 
        
        glpane = self.glpane
        
        #ninad060831 - First I defined the following in the _init method of this class. But the prefeences were 
        #not updated immediately when changed from prefs dialog. So I moved those definitions below and now it works fine
        
        self.atomDistPrecision = env.prefs[dynamicToolTipAtomDistancePrecision_prefs_key] #int
        self.bendAngPrecision = env.prefs[dynamicToolTipBendAnglePrecision_prefs_key] #int
        self.torsionAngPrecision = env.prefs[dynamicToolTipTorsionAnglePrecision_prefs_key] #int
        self.isAtomChunkInfo = env.prefs[dynamicToolTipAtomChunkInfo_prefs_key]#boolean
        self.isBondChunkInfo = env.prefs[dynamicToolTipBondChunkInfo_prefs_key]#boolean
        self.isAtomPosition = env.prefs[dynamicToolTipAtomPosition_prefs_key]#boolean
        self.isAtomDistDeltas = env.prefs[dynamicToolTipAtomDistanceDeltas_prefs_key]#boolean
        self.isBondLength = env.prefs[dynamicToolTipBondLength_prefs_key] #boolean
        self.isAtomMass = env.prefs[dynamicToolTipAtomMass_prefs_key] #boolean
        
        
        objStr = self.getHighlightedObjectInfo(self.atomDistPrecision)
                               
        selectedAtomList = glpane.assy.getOnlyAtomsSelectedByUser()
        selectedJigList = glpane.assy.getSelectedJigs()
        
        ppa2 = glpane.assy.ppa2 # previously picked atom
        ppa2Exists = self.lastPickedInSelAtomList(ppa2, selectedAtomList)
        
        ppa3 = glpane.assy.ppa3 #atom picked before ppa2
        ppa3Exists = self.lastTwoPickedInSelAtomList(ppa2, ppa3, selectedAtomList) #checks if *both* ppa2 and ppa3 exist
                
        if len(selectedAtomList) == 0: 
            return objStr
            
        #ninad060818 Give the distance info if only one atom is selected in the glpane (and is not the highlighted one)
        #If a 'last picked' atom exists (and is still selected, then it returns distance between that last picked and highlighted
        #If the highlighted atom is also selected/last picked , only give atom info don't give '0' distance info" 
        #Known bug: If many atoms selected, if ppa2 and ppa2 exists and if ppa2 is deleted, it doesn't display the distance between 
        #highlighted and ppa3. (as of 060818 it doesn't even display the atom info ..but thats not a bug just NIY that I need to 
        #handle somewhere else. 
        
        elif isinstance(glpane.selobj, atom) and (len(selectedAtomList) == 1 ):
            if self.getDistHighlightedAtomAndSelectedAtom(selectedAtomList, ppa2,self.atomDistPrecision):
                distStr = self.getDistHighlightedAtomAndSelectedAtom(selectedAtomList, ppa2,self.atomDistPrecision)
                return objStr + "<br>" + distStr
            else:
                return objStr
                
        #ninad060821 Give the angle info if only 2 atoms are selected (and the selection doesn't include highlighted atom)
        #if ppa2 and ppa3 both exist (and still selected) then it returns angle between them 
        #If the highlighted atom is also selected/last picked/lasttolastpicked , only give atom and distance info don't give angle info
        #If distance info is not available for some reasons (e.g. no ppa2 or more than 2 atoms region selected  etc, return Distance info only)
        
        elif  isinstance(glpane.selobj, atom) and ( len(selectedAtomList) == 2 or len(selectedAtomList) == 3):
            if self.getAngleHighlightedAtomAndSelAtoms(ppa2, ppa3,selectedAtomList,self.bendAngPrecision):
                angleStr = self.getAngleHighlightedAtomAndSelAtoms(ppa2, ppa3,selectedAtomList,self.bendAngPrecision)
                return objStr + "<br>" + angleStr
            else:
                if self.getDistHighlightedAtomAndSelectedAtom(selectedAtomList, ppa2,self.atomDistPrecision):
                    distStr = self.getDistHighlightedAtomAndSelectedAtom(selectedAtomList, ppa2,self.atomDistPrecision)
                    return objStr + "<br>" + distStr
                else:
                    return objStr
        
        #ninad060822 For all other cases, simply return the object info. 
        else:
            return objStr #@@@ ninad060818 ...if we begin to support other objects (other than jig/chunk/bonds/atoms)
                                #then we need to retirn glpane.selobj
                
        """elif "three atoms are selected":
            self
            torsionStr = self.getTorsionHighlightedAtomAndSelAtoms()
            angleStr = self.getAngleHighlightedAtomAndSelAtoms()
            distStr = self.getDistHighlightedAtomAndSelectedAtom()
            return torsionStr + "<br>" + angleStr + "<br>" + distStr"""
            
        
    def getHighlightedObjectInfo(self, atomDistPrecision): 
        "Returns the info such as name, id, xyz coordinates etc of the highlighed object"
        from bond_constants import describe_atom_and_atomtype
        #from chem import Atom
        
        glpane = self.glpane
        atomposn = None
        atomChunkInfo = None
                
        #      ---- Atom Info ----
        if isinstance(glpane.selobj, atom):
            selAtom  = glpane.selobj
            atomInfoStr = selAtom.getToolTipInfo(glpane, self.isAtomPosition,self.isAtomChunkInfo, self.isAtomMass, atomDistPrecision)
            return atomInfoStr
           
        #       ----Bond Info----
        if isinstance(glpane.selobj, Bond):
            selBond = glpane.selobj
            bondInfoStr = selBond.getToolTipInfo(glpane, self.isBondChunkInfo, self.isBondLength, atomDistPrecision)
            return  bondInfoStr
            
        #          ---- Jig Info ----
        if isinstance(glpane.selobj, Jig):
            jig = glpane.selobj
            jigStr = jig.getToolTipInfo()
            return jigStr
        
        #@@@ninad060818 In future if we support other object types in glpane, do we need a check for that? 
        # e.g. else: return "unknown object" .
            
        
    def getDistHighlightedAtomAndSelectedAtom(self, selectedAtomList, ppa2, atomDistPrecision): 
        
        from VQT import vlen
        """
        Returns the distance between the selected atom  and the highlighted atom. 
        If there is only one atom selected and is same as highlighed atom, then it returns None.  (then the function calling this 
        routine needs to handle that case.) 
        """
       
        glpane = self.glpane
               
        selectedAtom = None
        
        atomDistDeltas =None
        
        if len(selectedAtomList) > 2: # ninad060824 don't show atom distance info when there are more than 2 atoms selected. Fixes bug2225 
            return False
        
        #ninad060821 It is posible that 2 atoms are selected and one is highlighted. This condition allows the function use in the conditional loop that shows angle between the selkected and highlighted atoms
        if  len(selectedAtomList) ==2 and glpane.selobj in selectedAtomList: #this means the highlighted object is also in this list
            i = selectedAtomList.index(glpane.selobj)
            if i == 0: #ninad060821 This is a clumsy way of knowing which atom is which. Okay for now since there are only 2 atoms 
                selectedAtom = selectedAtomList[1]
            else:
                selectedAtom = selectedAtomList[0]
                
        if len(selectedAtomList) == 1:
            #ninad060821 disabled the case where many atoms are selected and there still exists a last picked.  I did this becasue
            #it is confusing. Example: I picked an atom. Now I region selected another atom (after pick operation) then I highlight an atom. 
            #it shows the distance between the highlighed and the picked and not highlighted and region selected. This is not good
            #If we have a way to know when region select operation was performed (before or after) then we can implement it 
            #again. Probably selectedAtomList maintains this record? Should we check the list to see if ppa2 comes before or after the 
            # region selection?  It is complecated. Need to discuss with Bruce and Mark. Not implementing it right now. 
            #This also invalidates the need to pass ppa2 as an arg to this function. Still keeping it until I hear back from Bruce/Mark
            
            #if ppa2:
                #selectedAtom = ppa2 #ninad060818 This handles a case when there are many atoms selected and there still exists a 'last picked' one
            #else:
                #selectedAtom = selectedAtomList[0] #buggy if there are more than 2 atoms selected. But its okay because I am handling it correctly elsewhere where (I am calling this function) ninad060821
            selectedAtom = selectedAtomList[0]
            
        xyz = glpane.selobj.posn()
        
         # round the distance value using atom distance precision preference ninad 060822
         
         #ninad060822: Note: In prefs constant.py, I am using for example--
         # ('atom_distance_precision', 'int', dynamicToolTipAtomDistancePrecision_prefs_key, 3)
         #Notice that the digit is not 3.0  but is simply 3 as its an integer. 
         #I changed to to plain 3 because I got a Deprecation warning: integer arg expected, got float 
         
        roundedDist = str(round(vlen(xyz - selectedAtom.posn()),atomDistPrecision))
        
        #ninad060818 No need to display disance info if highlighed object and lastpicked/ only selected object are identical
        if selectedAtom:
            if selectedAtom is not glpane.selobj: 
                distStr = ("<font color=\"#0000FF\">Distance %s-%s :</font> %s A"%(glpane.selobj, selectedAtom,roundedDist))
                atomDistDeltas = self.getAtomDistDeltas(self.isAtomDistDeltas, atomDistPrecision,selectedAtom)
                if atomDistDeltas:
                    distStr += "<br>" + atomDistDeltas
                
                return distStr
            else:
                return False
        else:
            return False
    
    def getAngleHighlightedAtomAndSelAtoms(self,ppa2, ppa3,selectedAtomList,bendAngPrecision):
        
        """
        Returns the angle between the last two selected atoms and the current highlighted atom. 
        If the highlighed atom is also one of the selected atoms and there are only 2 selected  atoms other than 
         the highlighted one then it returns None.(then the function calling this routine needs to handle that case.) 
        
        """
        from chem import atom_angle_radians
        
        glpane = self.glpane
        lastSelAtom = None
        secondLastSelAtom = None
               
        ppa3Exists = self.lastTwoPickedInSelAtomList(ppa2, ppa3, selectedAtomList) #checks if *both* ppa2 and ppa3 exist
        
        if  len(selectedAtomList) ==3 and glpane.selobj in selectedAtomList:
            if ppa3Exists and not (glpane.selobj is ppa2 or glpane.selobj is ppa3):
                lastSelAtom = ppa2
                secondLastSelAtom = ppa3
            else:
                #ninad060825 revised the following. Earlier code in v1.8 was correct but this one is simpler. Suggested by Bruce. I have tested it and is safe.
                tempAtomList =list(selectedAtomList)
                tempAtomList.remove(glpane.selobj)
                lastSelAtom = tempAtomList[0]
                secondLastSelAtom = tempAtomList[1]
            
        if len(selectedAtomList) == 2: #here I (ninad) don't care about whether itselected atom is also highlighted. It is handled below. 
            if ppa3Exists:
                lastSelAtom = ppa2
                secondLastSelAtom = ppa3
            else:
                 lastSelAtom = selectedAtomList[0]
                 secondLastSelAtom = selectedAtomList[1]
            #ninad060821 No need to display angle info if highlighed object and lastpicked or secondlast picked
            #  object are identical
            if glpane.selobj in selectedAtomList: 
                return False
        
        if lastSelAtom and secondLastSelAtom:
            angle = atom_angle_radians( glpane.selobj, lastSelAtom,secondLastSelAtom ) * 180/math.pi
            roundedAngle = str(round(angle,bendAngPrecision))
            angleStr = fix_plurals("<font color=\"#0000FF\">Angle %s-%s-%s:</font> %s degree(s)"
            %(glpane.selobj, lastSelAtom,secondLastSelAtom,roundedAngle))
            return angleStr
        else:
            return False
    
    def getTorsionHighlightedAtomAndSelAtoms(self):
        """
        Return the torsion angle between the last 3 selected atoms and the highlighed atom, 
        If the highlighed atom is also selected, it excludes it while finding the last 3 selected atoms. 
        If the highlighed atom is also one of the selected atoms and there are only 2 selected  atoms other than 
        the highlighted one then it returns None. (then the function calling this routine needs to handle that case.) 
        """
        return False
        
    def lastPickedInSelAtomList(self, ppa2,selectedAtomList):
        '''Checks whether the last atom picked (ppa2) exists in the atom list
           Returns True of False. 
        '''
        if ppa2 in selectedAtomList:
            return True
        else:
            return False
    
    def lastTwoPickedInSelAtomList(self, ppa2,ppa3,selectedAtomList):
        '''Checks whether *both* the last two picked atoms (ppa2 and ppa3) exist in the atom list
           Returns True of False. 
        '''
        if (ppa2 and ppa3) in selectedAtomList:
            return True
        else:
            return False
    
    def lastThreePickedInSelAtomList(self, ppa2, ppa3, ppa4):
        '''Checks whether *all*  the three picked atoms (ppa2 , ppa3 and ppa4) exist in the atom list
           Returns True of False.  Note: there is no ppa4 yet - ninad060818
        '''
        
    def getAtomDistDeltas(self, isAtomDistDeltas, atomDistPrecision,selectedAtom):
        ''' returns atom distance deltas (delX, delY, delZ) string  if the 'show atom distance delta info' in dynamic toooltip is checked from
         the user prefs otherwise returns None
        '''
        glpane = self.glpane
        if isAtomDistDeltas:
            
            xyz = glpane.selobj.posn()
            xyzSelAtom = selectedAtom.posn()
            deltaX = str(round(vlen(xyz[0]- xyzSelAtom[0]),atomDistPrecision))
            deltaY = str(round(vlen(xyz[1]- xyzSelAtom[1]),atomDistPrecision))
            deltaZ  = str(round(vlen(xyz[2]- xyzSelAtom[2]),atomDistPrecision))
            atomDistDeltas = "<font color=\"#0000FF\">DeltaX:</font> " + deltaX + "<br>" + "<font color=\"#0000FF\">DeltaY:</font> " + deltaY + "<br>" +  "<font color=\"#0000FF\">DeltaZ:</font> " + deltaZ
            return atomDistDeltas
        else:
            return None
                        
# end
