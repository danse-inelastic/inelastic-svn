#from ASE.ChemicalElements.ChemicalElements import Element, numbers
#__import__('pkg_resources').declare_namespace(__name__)

import sys
vinfo =  sys.version_info
if vinfo[0] != 2: raise NotImplementedError
METACLASS_CTOR_NEEDS_TYPE = vinfo[1]>5


import crystalIO
import atomic_properties
from matter.StructureErrors import StructureFormatError,LatticeError,SymmetryError,IsotropyError
from matter.Atom import Atom
from matter.Lattice import Lattice
from matter.Structure import Structure

# obtain version information
from matter.version import __version__


