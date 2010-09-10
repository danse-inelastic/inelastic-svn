#!/usr/bin/python

import numpy
from struct import pack,unpack,calcsize

version=1

intSize = calcsize('<i')
dubSize = calcsize('<d')
strSize = calcsize('<s')

def write(E,filename='E',comment=''):
  """Takes numpy E in with shape (N_e) and writes to binary file."""
  f=open(filename,'w')
  f.write(pack('<64s','E'))
  f.write(pack('<i',version))
  f.write(pack('<1024s',comment))
  f.write(pack('<i',E.shape[0]))
  E = numpy.asarray(E, dtype="<d")
  f.write(E.tostring())
  return

def read(filename='E'):
  """Takes filename, returns a tuple with information and E as a numpy."""
  f=open(filename,'r').read()
  i = 0
  filetype, = unpack('<64s',f.read(64*strSize))
  version,  = unpack('<i',f.read(intSize))
  comment,  = unpack('<1024s',f.read(1024*strSize))
  N_e       = unpack('<i',f.read(intSize))
  E         = numpy.fromstring(f.read(), dtype="<d")[:N_e]
  return (filetype.strip('\x00'),version,comment.strip('\x00')),E

