from DetectorSurfaceMapper import DetectorSurfaceMapper
import numpy as np

# Load VTK stuff up here for now, but maybe should only load pieces needed in specific methods
from vtk import *
# load VTK extensions
from libvtkCommonPython import *
from libvtkGraphicsPython import *

class SphereDetectorSurfaceMapper(DetectorSurfaceMapper):
    """A spherical detector surface mapper."""

    def __init__(self, Ei=50, Etransfer=0, sphRadius=4,
                 phiMin=0, phiMax=120,
                 thetaMax=120, thetaMin=60):
        #DetectorSurfaceMapper.__init__(self, Ei=50, Etransfer=0)
        self.Ei = Ei
        self.Etransfer = Etransfer
        self.sphRadius = sphRadius
        self.phiMin = phiMin
        self.phiMax = phiMax
        self.thetaMin = thetaMin
        self.thetaMax = thetaMax

        print "Ei = %f, Etransfer= %f" % (self.Ei, self.Etransfer)

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
            Etransfer = self.getEtransfer()
        DetectorSurfaceMapper._checkEtransfer(self, Etransfer)
        Ei = self.getEi()
        Ef = Ei  - Etransfer
        kf = np.sqrt(Ef/2.072)  # Squires (1.9)
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

    def getKi(self):
        """Returns incident neutron wavevector MAGNITUDE k_i (in Angstroems-1 if E_i is in meV)."""
        Ei = self.Ei
        ki = np.sqrt(Ei / 2.072)
        return ki

    def getKiVector(self):
        """Returns incident neutron wavevector k_i (in Angstroems-1 if E_i is in meV)."""
        kivec = np.zeros(3,dtype='float')
        ki = self.getKi()
        # the ki wavevector should be determined from the orientation of the single crystal...
        kivec[0] = ki
        return kivec

    def getVtkMapper(self):
        #from vtk import vtkSphereSource,vtkPolyDataMapper,vtkActor
        sph = vtkSphereSource()

        # We switch theta and phi in VTK interface for more usual spherical notation

        #sph.SetStartPhi(self.phiMin)
        #sph.SetEndPhi(self.phiMax)
        #sph.SetStartTheta(self.thetaMin)
        #sph.SetEndTheta(self.thetaMax)

        sph.SetStartPhi(self.thetaMin)
        sph.SetEndPhi(self.thetaMax)
        sph.SetStartTheta(self.phiMin)
        sph.SetEndTheta(self.phiMax)
        sph.SetPhiResolution(int((self.phiMax-self.phiMin+0.001)/10)+1)
        sph.SetThetaResolution(int((self.thetaMax-self.thetaMin+0.001)/10)+1)

        sph.LatLongTessellationOn()
        sph.SetRadius(self.getKf())
        sph.SetCenter(self.getKiVector().tolist())
        sphMapper = vtkPolyDataMapper()
        sphMapper.SetInput(sph.GetOutput())
        #sphActor = vtkActor()
        #sphActor.SetMapper(sphMapper)
        return sphMapper
        
    pass # End of class SphereDetectorSurfaceMapper
