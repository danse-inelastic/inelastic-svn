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

//	    // Get the Set samples to facilitate the calculations
//
//	    float[][] set_samples = domain_set.getSamples( true );
//
//
//	    // We create another array, with the same number of elements of
//	    // z and temperature, but organized as
//	    // float[2][ number_of_samples ]
//
//	    float[][] flat_samples = new float[2][NCOLS * NROWS];
//
//	    // ...and then we fill our 'flat' array with the generated values
//	    // by looping over NCOLS and NROWS
//
//	    for(int c = 0; c < NCOLS; c++)
//
//	      for(int r = 0; r < NROWS; r++){
//
//		// ...z
//		flat_samples[0][ c * NROWS + r ] = 01.0f / (float)( (set_samples[0][ c * NROWS + r ] *
//							     set_samples[0][ c * NROWS + r ]) +
//							     (set_samples[1][ c * NROWS + r ] *
//							     set_samples[1][ c * NROWS + r ]) + 1.0f );
//
//		// ...temperature
//		flat_samples[1][ c * NROWS + r ] = (float)( (Math.sin( 0.50*(double) set_samples[0][ c * NROWS + r ])  ) * Math.cos( (double) set_samples[1][ c * NROWS + r ] ) ) ;
//
//
//	    }

	    // Create a FlatField
	    // Use FlatField(FunctionType type, Set domain_set)

	    FlatField vals_ff = new FlatField( func_domain_range, domain_set);

	    // ...and put the values above into it

	    // Note the argument false, meaning that the array won't be copied

	    vals_ff.setSamples( flat_samples , false );

	    // Create Display and its maps

	    // A 2D display

	    DisplayImplJ3D display = new DisplayImplJ3D("display1");

	    // Get display's graphics mode control and draw scales

	    GraphicsModeControl dispGMC = (GraphicsModeControl)  display.getGraphicsModeControl();
	    dispGMC.setScaleEnable(true);


	    // Create the ScalarMaps: y to YAxis, x to XAxis and
	    // z to ZAxis and temperature to RGB
	    // Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

	    ScalarMap latMap = new ScalarMap( y,    Display.YAxis );
	    ScalarMap lonMap = new ScalarMap( x, Display.XAxis );

	    // Add maps to display

	    display.addMap( latMap );
	    display.addMap( lonMap );

	     // z to z-axis and temperature to color

	    ScalarMap altZMap = new ScalarMap( z,  Display.ZAxis );
//	    tempRGBMap = new ScalarMap( temperature,  Display.RGB );
	    // Add maps to display
	    display.addMap( altZMap );
//	    display.addMap( tempRGBMap );


	    // Uncomment following lines to have different data depiction
	    // temperature to z-axis and z to color

	    //altRGBMap = new ScalarMap( z,  Display.RGB );
	    //tempZMap = new ScalarMap( temperature,  Display.ZAxis );
	    //display.addMap( altRGBMap );
	    //display.addMap( tempZMap );


	    // Create a data reference and set the FlatField as our data

	    DataReferenceImpl data_ref = new DataReferenceImpl("data_ref");

	    data_ref.setData( vals_ff );

	    // Add reference to display

	    display.addReference( data_ref );
		
		
	}

	DisplayImpl getDisplay(){
		return display;
	}
	
}
