package vnf;

import java.rmi.RemoteException;

import visad.DataReferenceImpl;
import visad.Display;
import visad.DisplayImpl;
import visad.FlatField;
import visad.FunctionType;
import visad.GraphicsModeControl;
import visad.Linear2DSet;
import visad.RealTupleType;
import visad.RealType;
import visad.ScalarMap;
import visad.VisADException;
import visad.java3d.DisplayImplJ3D;

public class ThreeDSurface {

	DisplayImpl display;
	
	public ThreeDSurface(float[][] flat_samples, int numXData, int numYData) throws VisADException, RemoteException {
		RealType y = RealType.getRealType("y");
		RealType x = RealType.getRealType("x");
		RealType z = RealType.getRealType("z");

		RealTupleType domain_tuple = new RealTupleType(y, x);
		FunctionType func_domain_range = new FunctionType( domain_tuple, z);

	    Linear2DSet domain_set = new Linear2DSet(domain_tuple, 0.0, (double)(numXData-1), 
	    		numXData, 0.0, (double)(numYData), numYData);

	    FlatField vals_ff = new FlatField( func_domain_range, domain_set);
	    vals_ff.setSamples( flat_samples , false );

	    // Create Display and its maps

	    display = new DisplayImplJ3D("display1");

	    // Get display's graphics mode control and draw scales

	    GraphicsModeControl dispGMC = (GraphicsModeControl)  display.getGraphicsModeControl();
	    dispGMC.setScaleEnable(true);

	    // Create the ScalarMaps
	    ScalarMap yMap = new ScalarMap( y, Display.YAxis );
	    ScalarMap xMap = new ScalarMap( x, Display.XAxis );
	    ScalarMap zMap = new ScalarMap( z,  Display.ZAxis );
	    display.addMap( yMap );
	    display.addMap( xMap );
	    display.addMap( zMap );

	    DataReferenceImpl data_ref = new DataReferenceImpl("data_ref");
	    data_ref.setData( vals_ff );
	    display.addReference( data_ref );
	}

	DisplayImpl getDisplay(){
		return display;
	}
	
}
