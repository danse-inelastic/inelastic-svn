import CifFile,re,math
from os import linesep
#from pyre.components.Component import Component


#class CifParser(Component):
class CifParser:
    '''translates from cif into various other formats'''
    
#    class Inventory(Component.Inventory):
#        import pyre.inventory as inv
#        filename = inv.str( "filename", default = "")
#        filename.meta['tip'] = ".cif file to be translated."
        
    def __init__(self, file=''):
        self.filenameIn = file
#        Component.__init__(self, 'CifParser', facility='CifParser')

    def listToLine(self,list):
        """takes a list and changes it to a line (with newline at end)
        as a string"""
        string=''
        for entry in list:
            string+=entry+" "
        string=string[:-1]+linesep
        return string
    
    def flatten(self,xList,whereto=1):
        """flattens a multidimensional list to a specified extent
        starting from the outer dimension"""
        temp1=xList
        while whereto>0:
            temp2=[]
            for x in temp1:
                temp2=temp2+x
            temp1=temp2
            whereto=whereto-1
        return temp1
    
#    def vecsToParams(self,vecs):
#        """takes lattice vectors in cartesian coordinates with origin at {0,0,0}
#        and returns lattice parameters"""
#        conv=math.pi/180
#        [a,b,c]=vecs
#        ma=math.sqrt(dot(a,a))
#        mb=math.sqrt(dot(b,b))
#        mc=math.sqrt(dot(c,c))
#        al=1/conv*math.acos(dot(b,c)/mb/mc)
#        be=1/conv*math.acos(dot(a,c)/ma/mc)
#        ga=1/conv*math.acos(dot(a,b)/ma/mb)
#        return [ma,mb,mc,al,be,ga]

    def _removeParens(self,numString):
        numString=numString.replace('(','')
        numString=numString.replace(')','')
        return numString
    
    def _removeLabels(self,listOAtomLabels):
        '''takes a list of atom labels and extracts a list of atoms'''
        listOAtoms=[]
        p=re.compile('\d')
        for entry in listOAtomLabels:
            listOAtoms.append(p.sub('',entry))
        return listOAtoms
    
    def cifToAtomAndCoordinateList(self):
        listOut=[]
        cifObj=CifFile.CifFile(self.filenameIn)
        keys=cifObj.keys()
        #for key in keys:
        #    if cifObj[key]['_atom_site_label']
        cifBlock=cifObj[keys[0]] # for now just assume the data is in the first block
        #deal with the fact that many cif's are incomplete or are not done correctly
        if cifBlock.has_key('_atom_site_type_symbol'):
            atomTypes=cifBlock['_atom_site_type_symbol']
        elif cifBlock.has_key('_atom_site_label'):
            atomTypes=cifBlock['_atom_site_label']
            atomTypes=self._removeLabels(atomTypes)
        atomXs=cifBlock['_atom_site_fract_x']
        atomYs=cifBlock['_atom_site_fract_y']
        atomZs=cifBlock['_atom_site_fract_z']
        for i in range(len(atomTypes)):
            listOut.append([atomTypes[i],self._removeParens(atomXs[i]),
            self._removeParens(atomYs[i]),self._removeParens(atomZs[i])])
        return listOut
    
    def _cifToAtomCoordString(self):
        atomNCoords=self.cifToAtomAndCoordinateList(self.filenameIn)
        stringOut=''
        for entry in atomNCoords:
            stringOut += self.listToLine(entry)
        return stringOut
        
    def _norm(self,vec):
        """gives the Euclidean _norm of a vector"""
        temp=sum([el**2. for el in vec])
        return math.sqrt(temp)
        
    def _evaluateSimpleAlgebra(self,left,operand,right):
        num=0.0
        if operand=='+':
            num=float(left)+float(right)
        elif operand=='-':
            num=float(left)-float(right)
        elif operand=='/':
            num=float(left)/float(right)
        return num

    def evaluateCrystOperationOld(self,opString,xyzVal):
        #FIXME: this does not work on mof-74; investigate soon
        '''apply a string representation crystallographic operation to 
        three values'''
        def _operationOnFloatVec():                
            '''if there is a num,operator,num sequence in the float vector,
            perform the operation and collapse the last three entries'''
            if operationSequence[-2:]==['operator','num']:
                    result=self._evaluateSimpleAlgebra(floats[-2], operationHolder[0], floats[-1])
                    floats.pop();floats.pop() #take off the last two numbers
                    floats.append(result) #replace them with the result
                    operationHolder.pop() #remove the operation
                    operationSequence.pop();operationSequence.pop() #remove the metadata
        floatComponents=[]
        components=opString.split(',')
        for component in components:
            chars=[i for i in component]
            '''seed with zero so can deal with expressions that 
            have operators at beginning'''
            floats=[0.0]
            operationHolder=[] # place to save exact operator
            operationSequence=[] #meta data about the types of chars
            for char in chars:
                # see if there are any pending operations and
                # execute them if so
                _operationOnFloatVec()
                # deal with the next character
                if char in ['0','1','2','3','4','5','6','7','8','9']:
                    floats.append(float(char))
                    operationSequence.append('num')
                elif char in ['+','-','/']:
                    operationHolder.append(char)
                    operationSequence.append('operator')
                elif char=='x':
                    floats.append(float(xyzVal[0]))
                    operationSequence.append('num')
                elif char=='y':
                    floats.append(float(xyzVal[1])) 
                    operationSequence.append('num')  
                elif char=='z':
                    floats.append(float(xyzVal[2]))
                    operationSequence.append('num')  
            # see if there are any pending operations and
            # execute them if so
            _operationOnFloatVec()
            floatComponents.append(floats[-1])
        return floatComponents
    
    def evaluateCrystOperation(self,opString,xyzVal):
        components=opString.split(',')
        floatComponents=[self.evaluateAlgebraicExpression(components[i],xyzVal) for i in range(3)]
        return floatComponents
        
    def evaluateAlgebraicExpression(self,expression,xyzVal):
        #break apart into characters
        chars=[i for i in expression]
        
        #put floats back together
        newChars=[]
        newChars.append(chars[0])
        ints=['0','1','2','3','4','5','6','7','8','9']
        floatMaterial=ints+['.']
        for char in chars[1:]:
            # if two consecutive chars are ints, concatenate
            if char in floatMaterial and newChars[-1][-1] in floatMaterial:
                #newChars[-1]=char+newChars[-1]
                newChars[-1]=newChars[-1]+char
            else:
                newChars.append(char)
        chars=newChars
        
        #convert ints to floats
        newChars=[]
        for char in chars:
            if char in ints:
                newChars.append(char+'.')
            else:
                newChars.append(char)
        chars=newChars
        
        #substitute in x, y, z values
        newChars=[]
        for char in chars:
            if char=='x':
                newChars.append(xyzVal[0])
            elif char=='y':
                newChars.append(xyzVal[1])
            elif char=='z':
                newChars.append(xyzVal[2])  
            else:    
                newChars.append(char)
        chars=newChars
                      
        #perform divisions
        newChars=[]
        newChars.append(chars[0])
        i=0
        while True:
            i=i+1
            if i >= len(chars): break
            if chars[i]=='/':
                i=i+1
                newChars[-1]=str(float(newChars[-1])/float(chars[i]))
            else:
                newChars.append(chars[i])
        chars=newChars
        
        #perform additions, subtractions
#        newChars=[]
#        newChars.append(chars[0])
#        foundOperator=False
#        op=''
#        for char in chars[1:]:
#            if char=='+' or char=='-':
#                foundOperator=True
#                op=char
#                continue
#            else:
#                newChars.append(char)
#            
#            if foundOperator:
#                newChars[-1]=str(eval(newChars[-1]+op+char))
#        chars=newChars   
        
        #easier cop out 
        stringRep=''
        for char in chars:
            stringRep+=char
        floatRep=eval(stringRep)    
        
        #return final number
        return floatRep
        
    
    def evaluateCrystOperationNewerButNoGood(self,opString,xyzVal):
        '''apply a string representation crystallographic operation to 
        three values'''
        # substitute x, y, and z into the string represention
        opString = opString.replace('x',xyzVal[0])
        opString = opString.replace('y',xyzVal[1])
        opString = opString.replace('z',xyzVal[2])
        # evaluate it
        newPos = eval(opString)
        return newPos
        
    def _unique(self,list):
        '''removes nonunique entries in a list'''
        newList=[]
        # first go through list
        for vector in list:
            # then go through the new list to see if it's already there
            alreadythere=False
            for entry in newList:
                difference = [vector[i]-entry[i] for i in range(1,4)]
                norm = self._norm(difference)
                if norm < math.pow(10,-3):
                    alreadythere=True
                    break
            if not alreadythere:
                newList.append(vector)
        return newList
        
    def _backInUnitCell(self,coordinates):
        """takes fractional unit cell coordinates and brings them back 
        into the base unit cell"""
        return [x % 1 for x in coordinates]
    
    def getUnitCellAsParameters(self):
        '''gets the unit cell as parameters'''
        cifObj=CifFile.CifFile(self.filenameIn)
        keys=cifObj.keys()
        #for key in keys:
        #    if cifObj[key]['_atom_site_label']
        cifBlock=cifObj[keys[0]] # for now just assume the data is in the first block
        #deal with the fact that many cif's are incomplete or are not done correctly
        try:
            a = float(self._removeParens(cifBlock['_cell_length_a']))
            b = float(self._removeParens(cifBlock['_cell_length_b']))
            c = float(self._removeParens(cifBlock['_cell_length_c']))
            alpha = float(self._removeParens(cifBlock['_cell_angle_alpha']))
            beta = float(self._removeParens(cifBlock['_cell_angle_beta']))
            gamma = float(self._removeParens(cifBlock['_cell_angle_gamma']))
            return (a,b,c,alpha,beta,gamma)
        except:
            print 'the cif file has no unit cell information'
            import sys 
            sys.exit()
    
    def MInv(self, uc):
        """gives the Cartesian normalization with respect the x axis of an arbitrary unit cell uc input as a tuple. Implicit assumption is that a_vector is along x and b_vector in the (x,y) plane."""
        conv=math.pi/180.
        # a=uc[0];b=uc[1];c=uc[2];al=uc[3];be=uc[4];ga=uc[5]
        (a,b,c,al,be,ga)=uc
        cosAlStar=(math.cos(conv*be)*math.cos(conv*ga) - math.cos(conv*al))/(math.sin(conv*be)*math.sin(conv*ga))
        V = a*b*c*(1 - math.cos(conv*al)**2. - math.cos(conv*be)**2. - math.cos(conv*ga)**2. + 2.*math.cos(conv*al)*math.cos(conv*be)*math.cos(conv*ga))**(1/2.)
        cStar = a*b*math.sin(conv*ga)/V
        return [[a, 0, 0], [b*math.cos(conv*ga), b*math.sin(conv*ga), 0], [c*math.cos(conv*be), -c*math.sin(conv*be)*cosAlStar, 1/cStar]]
    
    def getUnitCellAsVectors(self):
        '''gets the unit cell as vectors'''
        return self.MInv(self.getUnitCellAsParameters())
        
    def generateAllCoordinates(self):
        atomNCoords=self.cifToAtomAndCoordinateList()
        cifObj=CifFile.CifFile(self.filenameIn)
        keys=cifObj.keys()
        cifBlock=cifObj[keys[0]] # for now just assume the data is in the first block
        ops=cifBlock['_symmetry_equiv_pos_as_xyz']
        newPositions=[]
        for entry in atomNCoords:
            newEntryPositions=[]
            #operate on all these atoms with the symmetry operations
            for op in ops:
                # first parse the expressions
                newPosition=self.evaluateCrystOperation(op,entry[1:4])
                # now bring it back inside the unit cell
                newPosition=self._backInUnitCell(newPosition)
                # add it to the list and move on
                newEntryPositions.append([entry[0]]+newPosition)
            # remove the non-_unique ones
            uniqueEntryPositions=self._unique(newEntryPositions)
            # add these to the total number of atoms in the unit cell
            newPositions.append(uniqueEntryPositions)
        # now make sure the total number of atoms is unique
        uniqueNewPositions=self._unique(self.flatten(newPositions))
        return uniqueNewPositions