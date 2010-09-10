#!/usr/bin/python

import numpy
from struct import pack,unpack,calcsize

version=1

intSize = calcsize('<i')
dubSize = calcsize('<d')
strSize = calcsize('<s')

def write(Omega2,filename='Omega2',comment='',D=3):
  """Takes numpy Omega2 in with shape (N_q,N_b*D) and writes to binary file."""
  f=open(filename,'w')
  f.write(pack('<64s','Omega2'))
  f.write(pack('<i',version))
  f.write(pack('<1024s',comment))
  #f.write(pack('<i',Omega2.shape[2]))
  f.write(pack('<i',D))
  # maybe there should be some further checking on integer division below:
  f.write(pack('<i',Omega2.shape[1] / D))
  f.write(pack('<i',Omega2.shape[0]))
  Omega2 = numpy.asarray( Omega2.reshape(-1), dtype="<d" )
  f.write(Omega2.tostring())
  return

def read(filename='Omega2'):
  """Takes filename, returns a tuple with information and Omega2 as a numpy."""
  f=open(filename,'r')
  filetype, = unpack('<64s',f.read(64*strSize))
  version,  = unpack('<i',f.read(intSize))
  comment,  = unpack('<1024s',f.read(1024*strSize))
  D,N_b,N_q = unpack('<3i',f.read(3*intSize))
  Omega2    = numpy.fromstring(f.read(), dtype="<d")[:N_q*N_b*D]
  Omega2.shape = (N_q,N_b*D)
  return (filetype.strip('\x00'),version,comment.strip('\x00')),Omega2

