#!/usr/bin/python

import numpy
from struct import pack,unpack,calcsize

version=1

intSize = calcsize('<i')
dubSize = calcsize('<d')
strSize = calcsize('<s')

def write(FQ,filename='FractionalQs',comment=''):
  """Takes numpy fractional Q with shape (N_q,D) and writes to binary file."""
  f=open(filename,'w')
  f.write(pack('<64s','FractionalQs'))
  f.write(pack('<i',version))
  f.write(pack('<1024s',comment))
  f.write(pack('<i',FQ.shape[1]))
  f.write(pack('<i',FQ.shape[0]))
  FQ = numpy.asarray( FQ.reshape(-1), dtype="<d" )
  f.write(FQ.tostring())
  return

def read(filename='FractionalQs'):
  """Takes filename, returns a tuple with information and fractional Q as a \n
     numpy."""
  f=open(filename,'r')
  filetype, = unpack('<64s',f.read(64*strSize))
  version,  = unpack('<i',f.read(intSize))
  comment,  = unpack('<1024s',f.read(1024*strSize))
  D,N_q     = unpack('<2i',f.read(2*intSize))
  FQ        = numpy.fromstring(f.read(), dtype="<d")[:D*N_q]
  FQ.shape = (N_q,D)
  return (filetype.strip('\x00'),version,comment.strip('\x00')),FQ

