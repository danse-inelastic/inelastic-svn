#!/usr/bin/python

import numpy
from struct import pack,unpack,calcsize

version=1

intSize = calcsize('<i')
dubSize = calcsize('<d')
strSize = calcsize('<s')

class PolarizationIO:
    
    def __init__(self, filename='Polarizations', comment='',
                 dimension=3, numAtoms=1, numks=1):
        self.f=open(filename,'w')
        self.f.write(pack('<64s','Polarizations'))
        self.f.write(pack('<i',version))
        self.f.write(pack('<1024s',comment))
        self.f.write(pack('<i',dimension))
        self.f.write(pack('<i',numAtoms))
        self.f.write(pack('<i',numks))

    def writeVec(self,vec):
        """Takes numpy Polarizations with shape (N_b,D) and writes \n
to binary file."""
    
        res = numpy.zeros( vec.shape + (2,) )
        res[:,:,0] = numpy.real(vec)
        res[:,:,1] = numpy.imag(vec)
        res = tuple( res.reshape( (-1) ) )
        self.f.write( pack('<%id' % len(res),*res) )
        return

    def read(self,filename='Polarizations'):
        """Takes filename, returns a tuple with information and Polarizations \n
as a numpy."""
        f=open(filename,'r').read()
        i = 0
        filetype, = unpack('<64s',f[i:i+64*strSize])          ; i += 64*strSize
        version,  = unpack('<i',f[i:i+intSize])               ; i += intSize
        comment,  = unpack('<1024s',f[i:i+1024*strSize])      ; i += 1024*strSize
        D,N_b,N_q = unpack('<3i',f[i:i+3*intSize])            ; i += 3*intSize
        res       = unpack('<%id' % (N_q*N_b*D*N_b*D*2),f[i:])
        res = numpy.array(res)
        res.shape = (N_q,N_b*D,N_b,D,2)
        Pols = res[:,:,:,:,0] + 1j*res[:,:,:,:,1]
        return (filetype.strip('\x00'),version,comment.strip('\x00')),Pols

