import CifFile,re,math
from my import ind,listToLine,flatten
from pyre.components.Component import Component

class Translator(Component):
    '''translates from cif into various other formats'''
    
    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        filename = inv.str( "filename", default = "")
        filename.meta['tip'] = ".cif file to be translated."
        
    def __init__(self, file=''):
        Component.__init__(self, 'Translator', facility='Translator')
        self.filenameIn=file
        
    def _configure(self):
        Component._configure(self)
        self.filenameIn = self.inventory.filename
        return
    
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
        for i in ind(atomTypes):
            listOut.append([atomTypes[i],self._removeParens(atomXs[i]),
            self._removeParens(atomYs[i]),self._removeParens(atomZs[i])])
        return listOut
    
    def _cifToAtomCoordString(self):
        atomNCoords=self.cifToAtomAndCoordinateList(self.filenameIn)
        stringOut=''
        for entry in atomNCoords:
            stringOut += listToLine(entry)
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

    def evaluateCrystOperation(self,opString,xyzVal):
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
        
    def _unique(self,list):
        '''removes nonunique entries in a list'''
        newList=[]
        # first go through list
        for vector in list:
            # then go through the new list to see if it's already there
            alreadythere=False
            for entry in newList:
                difference=[vector[i]-entry[i] for i in range(3)]
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
                newEntryPositions.append(newPosition)
            # remove the non-_unique ones
            uniqueEntryPositions=self._unique(newEntryPositions)
            # add these to the total number of atoms in the unit cell
            newPositions.append(uniqueEntryPositions)
        return flatten(newPositions)