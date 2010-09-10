#!/usr/bin/python

import numpy
from numpy import array
from struct import pack,unpack,calcsize

version=1

intSize = calcsize('<i')
dubSize = calcsize('<d')
strSize = calcsize('<s')

def write(Sqe,filename='Sqe',comment=''):
  """Takes numpy Sqe in with shape (N_e,N_q) and writes to binary file."""
  f=open(filename,'w')
  f.write(pack('<64s','Sqe'))
  f.write(pack('<i',version))
  f.write(pack('<1024s',comment))
  f.write(pack('<i',Sqe.shape[0]))
  f.write(pack('<i',Sqe.shape[1]))
  Sqe = numpy.asarray(Sqe.reshape(-1), dtype="<d")
  f.write(Sqe.tostring())
  return

def read(filename='Sqe'):
  """Takes filename, returns a tuple with information and Sqe as a numpy."""
  f=open(filename,'r')
  filetype, = unpack('<64s',f.read(64*strSize))
  version,  = unpack('<i',f.read(intSize))
  comment,  = unpack('<1024s',f.read(1024*strSize))
  N_e,N_q   = unpack('<2i',f.read(2*intSize))
  Sqe = numpy.fromstring(f.read(),dtype="<d")
  Sqe.shape = (N_e,N_q)
  return (filetype.strip('\x00'),version,comment.strip('\x00')),Sqe

