#!/usr/bin/python

import numpy
from numpy import array
from struct import pack,unpack,calcsize

version=1

intSize = calcsize('<i')
dubSize = calcsize('<d')
strSize = calcsize('<s')

def write(Sq,filename='Sq',comment=''):
  """Takes numpy Sq in with shape (N_q) and writes to binary file."""
  f=open(filename,'w')
  f.write(pack('<64s','Sq'))
  f.write(pack('<i',version))
  f.write(pack('<1024s',comment))
  f.write(pack('<i',Sq.shape[0]))
  Sq = numpy.asarray(Sq.reshape(-1), dtype="<d")
  f.write(Sq.tostring())
  return

def read(filename='Sq'):
  """Takes filename, returns a tuple with information and Sq as a numpy."""
  f=open(filename,'r')
  filetype, = unpack('<64s',f.read(64*strSize))
  version,  = unpack('<i',f.read(intSize))
  comment,  = unpack('<1024s',f.read(1024*strSize))
  N_q,      = unpack('<i',f.read(intSize))
  Sq        = numpy.fromstring(f.read(), dtype="<d")[:N_q]
  Sq.shape = (N_q)
  return (filetype.strip('\x00'),version,comment.strip('\x00')),Sq

