#!/usr/bin/python

import numpy
from struct import pack,unpack,calcsize

version=1

intSize = calcsize('<i')
dubSize = calcsize('<d')
strSize = calcsize('<s')

def write(Q,filename='Q',comment=''):
  """Takes numpy Q in with shape (N_q,D) and writes to binary file."""
  f=open(filename,'w')
  f.write(pack('<64s','Q'))
  f.write(pack('<i',version))
  f.write(pack('<1024s',comment))
  f.write(pack('<i',Q.shape[1]))
  f.write(pack('<i',Q.shape[0]))
  Q = numpy.asarray( Q.reshape(-1), dtype="<d")
  f.write(Q.tostring())
  return

def read(filename='Q'):
  """Takes filename, returns a tuple with information and Q as a numpy."""
  f=open(filename,'r')
  filetype,= unpack('<64s',f.read(64*strSize))
  version, = unpack('<i',f.read(intSize))
  comment, = unpack('<1024s',f.read(1024*strSize))
  D,N_q    = unpack('<2i',f.read(2*intSize))
  Q        = numpy.fromstring(f.read(), dtype="<d")[:N_q*D]
  Q.shape = (N_q,D)
  return (filetype.strip('\x00'),version,comment.strip('\x00')),Q

