# Written by Mikkel Bollinger email: mbolling@fysik.dtu.dk
"""Module containing additional methods for NumPy arrays

The methods in this module are used by 'Structures.Grid' and classes related 
to it by inheritance.
"""

def Transpose_SquareMatrix(matrix):
	import lapack
	return lapack.TransposeSquareMatrix(matrix)

def HermitianConjugate_SquareMatrix(matrix):
	import Numeric
	# Transposed matrix:
	matrix_h=Transpose_SquareMatrix(matrix=matrix)
	# Complex conjugating
	Numeric.multiply(matrix_h.imag,-1,matrix_h.imag)
	return matrix_h

def HermitianEigensystem(matrix,eigenvalues=None):
	import lapack
	import Numeric
	# If eigenvalues have not been specied calculate all
	if eigenvalues is None:
		eigenvalues=(1,matrix.shape[0])
	eigval,eigvec=lapack.Zheevx(matrix,eigenvalues[0],eigenvalues[1])
	# The eigenvectors must be complex conjugated (!?)
	eigvec=Numeric.conjugate(eigvec)
	return (eigval,eigvec)

def GeneralizedHermitianEigensystem(matrix1,matrix2,eigenvalues=None):
	import lapack
	import Numeric
	# If eigenvalues have not been specified calculate all
	if eigenvalues is None:
		eigenvalues=(1,matrix1.shape[0])
	eigval,eigvec=lapack.Zhegvx(matrix1,matrix2,eigenvalues[0],eigenvalues[1])
	# The eigenvectors must be complex conjugated (?!)
	eigvec=Numeric.conjugate(eigvec)
	return (eigval,eigvec)

def Inverse(matrix,copymatrix=1):
	import lapack
	import Numeric
	import copy
	if copymatrix:
		matrix=copy.copy(matrix)
	return lapack.Zgetri(matrix)

def UpperMatrix2HermitianMatrix(uppermatrix):
	import Numeric
	for i in range(0,len(uppermatrix)-1):
		# copying each row in uppermatrix to the lower part
		uppermatrix[i+1:,i]=Numeric.conjugate(uppermatrix[i,i+1:])
	return uppermatrix	

def SolveLinearEquations(A,B,copy_a=1):
	import lapack
	import Numeric
	# Solves the linear system: A X = B
	# In Lapack array are input as column,row
	if copy_a: # Non-contiguous array that is copied in Zgesv
		A=Numeric.transpose(A)
	else:
		A=Transpose_SquareMatrix(A)
	# Non-contiguous array that is copied in Zgesv	
	B=Numeric.transpose(B)
	X=Numeric.transpose(lapack.Zgesv(A,B))
	# asarray makes transposed array contiguous
	return Numeric.array(X) 

def SolveLinearEquations_SquareMatrices(A,B,copy_a=1,copy_b=1):
	import lapack
	import Numeric
	# Solves the linear system: A X = B
	# In Lapack arrays are input as column,row
	if copy_a: # Produces a non-contiguous array that is copied in Zgesv
		A=Numeric.transpose(A)
	else: 
		A=Transpose_SquareMatrix(matrix=A)
	if copy_b: # Produces a non-contiguous array that is copied in Zgesv
		B=Numeric.transpose(B)
	else: 
		B=Transpose_SquareMatrix(matrix=B)
	X=lapack.Zgesv(A,B)
	# X should also be transposed (no copying done):
	return Transpose_SquareMatrix(X)
	
def MatrixMultiplication(matrixa,matrixb,alpha=1.0,atype='NoTranspose',btype='NoTranspose'):
	import lapack
	import Numeric
	# Use complex or double BLAS routine ?
	if matrixa.typecode()=='D' or matrixb.typecode()=='D': # Complex
		matrixtypes={"NoTranspose":0,"Transpose":1,"ConjugateTranspose":2}
		# Setting the correct dimensions of output array C
		Cdim1=matrixa.shape[0]
		if atype in ['Transpose','ConjugateTranspose']:
			Cdim1=matrixa.shape[1]
		Cdim2=matrixb.shape[1]
		if btype in ['Transpose','ConjugateTranspose']:
			Cdim2=matrixb.shape[0]	
		# Converting alpha to complex variable (if necessary):
		alpha=complex(alpha)
		matrixc=Numeric.zeros((Cdim1,Cdim2),Numeric.Complex)
		return lapack.BLAS_zgemm(matrixa,matrixb,matrixc,alpha.real,alpha.imag,0.0,0.0,matrixtypes[atype],matrixtypes[btype])
	else: # Double
		matrixtypes={"NoTranspose":0,"Transpose":1}
		return lapack.BLAS_dgemm(matrixa,matrixb,alpha,matrixtypes[atype],matrixtypes[btype])


def SliceArray(array,slicelist):
	"""Method for slicing an array
	This method can be used for slicing an array by specifying the array
	and a slicelist. The slicelist should have the same length as the
	number of axes in the array.

	**An example:**

	To slice an array having three axes with (12:17,:,[13,26]):

	'SliceArray(array,[range(12,17),None,(13,26)])'

	Note that 'None' implies that all the values along the given axis are
	retained. The output array will have the same number of axes as the
	input array.
	"""
	from Numeric import take
	for i in range(len(slicelist)):
		if slicelist[i]==None:
			pass
		elif type(slicelist[i])==type(1):
			array=take(array,[slicelist[i]],i)
		else:
			array=take(array,slicelist[i],i)
	return array

def RepeatArray(array,periods):
	"""Method for repeating an array according to periods
	
	This method is used for repeating an array according to the specified
	periods. 'periods' should be a sequence having the same length as the
	number of indices in 'array'. 

	**An example:**

	To repeat an array having three axis by (2,1,3) use:
	
	'RepeatArray(array,(2,1,3))' 

	"""
	from Numeric import concatenate
	import copy
	repeatarray=copy.copy(array)
	for i in range(len(periods)):
		repeatarray=concatenate(periods[i]*[repeatarray],axis=i)
	# the array is copied to make it contiguous
	return copy.copy(repeatarray)

def TranslateAlongAxis0NonPeriodic(array,translation,type):
	"""Optimized method for translating along axis o"""
	import Numeric
	import copy
	if translation==0:
	    return copy.copy(array)
	newarray=Numeric.zeros(array.shape,type)
	if translation>0:
	    newarray[translation:]=array[:-translation]
	else:
	    newarray[:translation]=array[-translation:]
	return newarray

def FFTShift(array):
	return TranslateAlongAxis0(array,len(array)-len(array)/2)

def TranslateAlongAxis0(array,translation):
	"""Optimized method for translating along axis o"""
	from Numeric import concatenate,take
	import copy
	if translation==0:
	    return copy.copy(array)
	newarray=copy.copy(array)
	newarray[:translation]=array[-translation:]
	newarray[translation:]=array[:-translation]
	return newarray


def Translate(array,translation):
	"""Method for translating an array used by Simulations.Dacapo.Grid"""
	from Numeric import concatenate,take
	import copy
	newarray=array
	size=array.shape
	for dim in range(len(translation)):
		axis=dim-len(translation)
		newarray=concatenate((take(newarray,range(translation[dim],size[axis]),axis),take(newarray,range(translation[dim]),axis)),axis)
	# the array is copied to make it contiguous
	return copy.copy(newarray)

def FindValue(array,value,axis):
	"""Returns an array with the position of value in array.

	This method can be used for finding the position of value along a given
	axis in 'array'.  
	"""
	from Numeric import argmin
	return argmin(abs(array-value),axis)

def FindValueInterpolate(array,value,axis,delta=1.0e-10):
	"""Returns an with the position of value in array using linear interpolation
	This method can be used for finding the position of value along a given
	axis in 'array' . The values are found by using linear interpolation
	between neighboring points in the array.
	"""
	from Numeric import zeros,Float
	shape=array.shape
	otheraxes=range(3)
	del otheraxes[axis]
	contoursurface=zeros((shape[otheraxes[0]],shape[otheraxes[1]]),Float)
	for axis0 in range(shape[otheraxes[0]]):
		for axis1 in range(shape[otheraxes[1]]):
			slice=[None,None,None]
			slice[otheraxes[0]]=axis0
			slice[otheraxes[1]]=axis1
			arrayslice=SliceArray(array,slice).flat
			#for normalaxis in range(interval[1],interval-1,-1):
			# Counting down from above.
			# 2 is subtracted since the surface cannot be
			# outside the searchinterval
			for normalaxis in range(shape[axis]-2,-1,-1):
				rel_deviation=(value-arrayslice[normalaxis])/(arrayslice[normalaxis+1]-arrayslice[normalaxis]+delta)
				if (rel_deviation>= 0.0 and rel_deviation<1.0):
					contoursurface[axis0,axis1]=normalaxis+rel_deviation
					break
	return contoursurface

def Map(function,array,coordinates):
	"""Return a mapped array

	This method can be used to map an array along with the coordinates
	corresponding to each grid point. The arrangement of the arguments
	in the input function is expected to be of the form 
	'function(' *arrayvalue* , *coordinate* ')' where *coordinate* is a 
	NumPy array having a length correspoding to the dimension.
	"""
	from Numeric import reshape,swapaxes,asarray

	# Finding the dimension of the array
	dim=coordinates.shape[0]
	spatialshape=array.shape[-dim:]

	# Reshaping array shape=(indices,) 
	flatarray=reshape(array,(array.shape[:-dim]+(-1,)))
	# Reshaping coordinates (indices,dim)
	flatcoordinates=swapaxes(reshape(coordinates,(dim,-1)),0,1)

	maparray=asarray(map(function,flatarray,flatcoordinates))

	# Reshaping back again
	return reshape(maparray,spatialshape)

def DerivativeXYZ(array,reciprocal,componentlist,kpoint=[0,0,0]):
	"""Returns the derivative of an array

	This method returns the derivative of an array. Note that the method
	implicitly assumes the array to be periodically repeated. However,
	if the spatial variation of the array can be written on the form
	'exp(ikr)*array' the derivative may still be obtained by specifying a
	'kpoint' given in cartesiancoordinates.

	**An example:** 

	To obtain the x,y derivative of array:

	'DerivativeXYZ(array,reciprocal,("x","y"))'

	where 'reciprocal' is an array representing the reciprocal unit cell 
	of the space in which 'array' is defined. 
	"""
	from Numeric import fromfunction

	# Using the following procedure (with i=x,y,z)
	# di f = sum_G prefactor*c_G*exp(i*(k+G)*r), where
	# prefactor = i*G_i

	# Generates a list with numbers 0,1,...,range/2,-(range/2-1),...,-1
	indexfunction=lambda i,length:(i+(length/2-1))%length-(length/2-1)

	components={'x':0,'y':1,'z':2}
	rec_coordinates=CoordinateArrayFromUnitVectors(array.shape,reciprocal,kpoint,indexfunction)
	prefactor=1.0

	for component in componentlist:
		prefactor=-1.0j*rec_coordinates[components[component]]*prefactor
	# Finding c_G
	c_G=InverseFFT(array)
	return FFT3D(prefactor*c_G)

def FFT3D(array):
	"""Returns the FFT of a three dimensional array
	
	This method can be used to obtain the FFT of a three dimensional array.
	"""
	import FFT
	N1,N2,N3=array.shape
	return FFT.fft(FFT.fft2d(array,(N1,N2),axes=(0,1)),N3,axis=2)

def FFT(array):
	"""Returns the FFT of an array

	This method can be used to obtain the FFT of an array.
	"""
	import FFT
	dim=array.shape
	for i in range(len(dim)):
		array=FFT.fft(array,dim[i],axis=i)
	return array

def InverseFFT(array):
	"""Returns the inverse FFT of an array

	This method can be used to obtain the inverse FFT of an array
	"""
	import FFT
	dim=array.shape
	for i in range(len(dim)):
		array=FFT.inverse_fft(array,dim[i],axis=i)
	return array

def CoordinateArrayFromUnitVectors(shape,gridunitvectors,origin=[0,0,0],indexfunction=lambda i,length:i):
	"""
	This method can be used to obtain an array representing the coordinates
	of a space defined by 'gridunitvecors'. 'gridunitvectors' is in turn a
 	list containing the vectors defining the cells of the grid, i.e. the
	vectors between neighboring grid points. These vectors are spanned
	according to the specified shape. 

	'origin' -- specifies the origin of the returned coordinate array. 
	
	'indexfunction' -- is a lambda expression that defines the indices 
	with which each of the specified gridunitvectors are to be multiplied. 
	'indexfunction' must take two arguments, 'i' and 'length' - default
	is 'lambda i,length:i'. During exection the input index 'i' will run 
	over the interval 0,1,..., 'length' -1.

	**An Example**

	To obtain a coordinate array of shape (10,10) with 
	'gridunitvectors' =[[2,0],[0,1]] and the origin at [10,0] use:

	'CoordinateArrayFromUnitVectors((10,10),[[2,0],[0,1],[10,0])'

	Note that the output array will be of shape 
	(< *dimension* > ,  < *spatialcoordinates* >).
	"""
	from Numeric import add,fromfunction,array,asarray
	coordinatelist=[]
	gridunitvectors=asarray(gridunitvectors)
	# Looping over the dimensionality of the vectors
	for dim in range(gridunitvectors.shape[1]):
		coordinates=origin[dim]
		# Contribution from each unitvector
		for nunitvector in range(gridunitvectors.shape[0]):
			# Finding the indices from which the coordinate grid
			# is spanned
			indices=map(lambda i,f=indexfunction,l=shape[nunitvector]:f(i,l),range(shape[nunitvector]))
			coordinatefunc=lambda i,v=gridunitvectors[nunitvector,dim]:i*v
			coordinates=add.outer(coordinates,map(coordinatefunc,indices))
		coordinatelist.append(coordinates)
	return array(coordinatelist)












