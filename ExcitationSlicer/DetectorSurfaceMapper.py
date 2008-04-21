__doc__ = """A module to map a t-o-f chopper detector surface in reciprocal space"""


#from pyre.components.Component import Component


class DetectorSurfaceMapper:
    """Base class for detector surface mapper."""

    def __init__(self, Ei=50, Etransfer=0):
        self.Ei = Ei
        self.Etransfer  = Etransfer

    def setEi(self, Ei):
        self.Ei = Ei

    def getEi(self):
        return self.Ei

    def setEtransfer(self, Etransfer):
        self.Etransfer = Etransfer

    def getEtransfer(self):
        return self.Etransfer

    def _checkEtransfer(self, Etransfer):
        """Checks that energy transfer input is compatible with incident E."""
        if (Etransfer > self.Ei):
            raise ValueError, 'Energy transfer larger than incident E.'
        pass

    def getDetectorSurface(self, Etransfer=0):
        self._checkEtransfer(Etransfer)
        raise NotImplementedError

        
    pass # End of class DetectorSurfaceMapper
