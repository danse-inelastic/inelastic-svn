#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="XiaoliTang"
__date__ ="$Dec 7, 2009 10:53:38 AM$"

class Vibrations(object):
    def __init__(self, qpoints=None, frequency=None, polarization=None):

        self.qpoints = qpoints
        self.frequency = frequency
        self.polarization = polarization

    def add_info(self):
        pass
        
    def print_info(self):
        'Will need to change this to pickle data to files'
        print 'number of qpoints is', len(self.qpoints)
        print 'the correspondent qpoints are', self.qpoints
        print 'the eigenvalues are', self.eigenval
        print 'the eigenvectors are', self.eigenvec

    def savetofile(self,phononfile=None):
        if phononfile is None:
            phononfile = 'phonon.dat'
        output = open(phononfile,'w')
        for i in range(0,len(self.qpoints)):
            output.write('qpoint:              '+ str(self.qpoints[i])+'\n')
            output.write('frequency:           '+str(self.frequency[i])+'\n')
            output.write('polarization vector: '+str(self.polarization[i])+'\n')
        output.close()

#-----------------------------Seperator-----------------------------------------
class DynamicalMatrix(object):
    def __init__(self, qpoints=None, dynamicalmatrix=None):
        if qpoints is None:
            raise ValueError('No valid value for qpoints')
        else:
            self.qpoints = qpoints
        if dynamicalmatrix is None:
            raise ValueError('No valid value for dynamicalmatrix')
        else:
            self.dynamicalmatrix=dynamicalmatrix


    def savetofile(self,filename=None):
	if filename is None:
            output = open('dynamicalmatrix.dat','w')
	else:
	    self.filename = filename
            output = open(self.filename,'w')
        for i in range(0,len(self.qpoints)):
            output.write('qpoints:          ' + str(self.qpoints[i])+'\n')
            output.write('dynamical matrix: '+str(self.dynamicalmatrix[i])+'\n')
        output.close()

#-----------------------------Seperator-----------------------------------------
class AnharmonicTensor(object):
    """only for qe now
    q1=0
    q2 = qpoints here
    q3 = -qpoints here
    anharmonictensor = d3(q1,q2,q3)
    need to generalize to q1,q2,q3
    """

    def __init__(self, qpoints=None, anharmonictensor=None):
        if qpoints is None:
            raise ValueError('No valid value for qpoints')
        else:
            self.qpoints = qpoints
        if anharmonictensor is None:
            raise ValueError('No valid value for dynamicalmatrix')
        else:
            self.anharmonictensor=anharmonictensor

    def savetofile(self,filename=None):
	if filename is None:
            output = open('d3tensor.dat','w')
	else:
	    self.filename=filename
 	    output = open(self.filename)
        for i in range(0,len(self.qpoints)):
            output.write('qpoints:           ' + str(self.qpoints[i])+'\n')
            output.write('anharmonic tensor: '+str(self.anharmonictensor[i])+'\n')
        output.close()
        
#-----------------------------Seperator-----------------------------------------
def test_vib():

    qpoints=[[0,0,0],[1,1,1]]
    freqs=[2,4]
    eigenvecs=[[1+1j,2+2j,3+3j],[4+4j,5+5j,6+6j]]
    phonon = Vibrations(qpoints=qpoints,frequency=freqs,polarization=eigenvecs)
    phonon.savetofile()

def test_dm():
    qpoints=[[0,0,0],[1,1,1]]
    dynmat=[[2,4],[6,8]]
    d2matrix = DynamicalMatrix(qpoints=qpoints,dynamicalmatrix=dynmat)
    d2matrix.savetofile()
    d2matrix.savetofile(filename='temp.dat')

def test_d3():
    qpoints=[[0,0,0],[1,1,1]]
    dynmat=[[2,4],[6,8]]
    d3tensor = AnharmonicTensor(qpoints=qpoints,anharmonictensor=dynmat)
    d3tensor.savetofile()

if __name__ == '__main__':
    print "Hello World";
    test_d3()

