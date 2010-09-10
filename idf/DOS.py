#!/usr/bin/python

import numpy
from struct import pack,unpack,calcsize

version=1

intSize = calcsize('<i')
dubSize = calcsize('<d')
strSize = calcsize('<s')

def write(E,DOS,filename='DOS',comment=''):
  """Takes numpy DOS in with shape (N_e) and writes to binary file."""
  f=open(filename,'w')
  f.write(pack('<64s','DOS'))
  f.write(pack('<i',version))
  f.write(pack('<1024s',comment))
  f.write(pack('<i',DOS.shape[0]))
  f.write(pack('<d',E[1]-E[0]))
  DOS = numpy.asarray( DOS, dtype="<d" )
  f.write(DOS.tostring())
  return

def read(filename='DOS'):
  """Takes filename, returns a tuple with information and DOS as a numpy."""
  f=open(filename,'r')
  filetype, = unpack('<64s',f.read(64*strSize))
  version,  = unpack('<i',f.read(intSize))
  comment,  = unpack('<1024s',f.read(1024*strSize))
  N_Bins,   = unpack('<i',f.read(intSize))
  dE,       = unpack('<d',f.read(dubSize))
  DOS       = numpy.fromstring(f.read(), dtype="<d")[:N_Bins]
  E = numpy.arange(0,N_Bins*dE,dE)
  return (filetype.strip('\x00'),version,comment.strip('\x00')),E,DOS

