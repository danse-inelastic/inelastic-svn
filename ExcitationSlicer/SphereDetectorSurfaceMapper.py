from DetectorSurfaceMapper import DetectorSurfaceMapper
import numpy as np

class SphereDetectorSurfaceMapper(DetectorSurfaceMapper):
    """A spherical detector surface mapper."""

    def __init__(self, Ei=50, Etransfer=0, sphRadius=4,
                 phiMin=0, phiMax=120,
                 thetaMax=120, thetaMin=60):
        DetectorSurfaceMapper.__init__(self, Ei=50, Etransfer=0)
        self.sphRadius = sphRadius
        self.phiMin = phiMin
        self.phiMax = phiMax
        self.thetaMin = thetaMin
        self.thetaMax = thetaMax

    def setPhiMin(self, phiMin):
        self.phiMin = phiMin

    def setPhiMax(self, phiMax):
        self.phiMax = phiMax

    def setThetaMin(self, thetaMin):
        self.thetaMin = thetaMin

    def setThetaMax(self, thetaMax):
        self.thetaMax = thetaMax

    def getPhiMin(self):
        return self.phiMin
    
    def getPhiMax(self):
        return self.phiMax

    def getThetaMin(self):
        return self.thetaMin

    def getThetaMax(self):
        return self.thetaMax
        
    def getKf(self, Etransfer=None):
        """Returns the magnitude of k_f for an energy transfer (to the sample) Etransfer.
        Return kf in inverse Angstroems if Ei and Etransfer are in meV."""
        if Etransfer == None:
            Etransfer = self.e
        DetectorSurfaceMapper._checkEtransfer(Etransfer)
        ef = self.ei - Etransfer
        kf = np.sqrt(ef/2.072)  # Squires (1.9)
        return kf

    def getVf(self, Etransfer=None):
        """Returns the final neutron velocity, vf, for an energy transfer (to the sample) Etransfer.
        For energies in meV, returns a velociy in (m/s)."""
        kf = self.getKf(Etransfer)
        vf = kf / (1.588E-3)
        return vf

    def getTf(self, Etransfer=None):
        """Returns the time-of-flight for the final neutron, Tf, for an energy transfer (to the sample) Etransfer.
        For energies in meV, and detector radius in meters, Tf is in seconds."""
        vf = self.getVf(Etransfer)
        tf = self.sphRadius / vf

    
    pass # End of class SphereDetectorSurfaceMapper
