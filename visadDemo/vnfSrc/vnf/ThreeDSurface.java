package vnf;

import java.rmi.RemoteException;

import visad.DisplayImpl;
import visad.VisADException;

public class ThreeDSurface {

	DisplayImpl display;
	
	public ThreeDSurface(float[][] samples, int numXData, int numYData) throws VisADException, RemoteException {
		
		
		
	}

	DisplayImpl getDisplay(){
		return display;
	}
	
}
