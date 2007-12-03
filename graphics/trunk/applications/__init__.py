def pylab():
    from matplot import matplot as matplotFactory
    return matplotFactory()

def IDL():
    from PyIDL import rsiIDL as IDLFactory
    return IDLFactory()

def Matlab():
    from Matlab import Matlab as MatlabFactory
    return MatlabFactory()

def grace():
    from PyGrace import PyGrace as PyGraceFactory
    return PyGraceFactory()
