package vnf;

import java.rmi.RemoteException;

import visad.DataReferenceImpl;
import visad.Display;
import visad.DisplayImpl;
import visad.FlatField;
import visad.FunctionType;
import visad.GraphicsModeControl;
import visad.Integer2DSet;
import visad.Linear2DSet;
import visad.RealTupleType;
import visad.RealType;
import visad.ScalarMap;
import visad.VisADException;
import visad.java2d.DisplayImplJ2D;

public class Image {
	
	private DisplayImpl display;

	public Image(float[][] flat_samples, int numXData, int numYData) 
		throws VisADException, RemoteException{
		// Declare variables for 1D Plotter
		RealType x = RealType.getRealType("x");
		RealType y = RealType.getRealType("y");
	    
//		// Create the domain tuple
	    RealTupleType domain_tuple = new RealTupleType(y, x);				
	    RealType z = RealType.getRealType("z");
	    FunctionType func_domain_range = new FunctionType( domain_tuple, z);
//		//Gridded2DSet domain_set = new Gridded2DSet(domain_tuple, xy_vals, xy_vals[0].length);
		//Integer2DSet domain_set = new Integer2DSet(domain_tuple, numYData, numXData);
	    Linear2DSet domain_set = new Linear2DSet(domain_tuple, 0.0, (double)(numXData-1), 
	    		numXData, 0.0, (double)(numYData), numYData);
//		// redo the flatfield to contain image data
//		// Use FlatField(FunctionType type, Set domain_set)				
		FlatField data_ff = new FlatField( func_domain_range, domain_set);

		// ...and put the z values above into it
		// Note the argument false, meaning that the array won't be copied
		data_ff.setSamples(flat_samples);

		display = new DisplayImplJ2D("display1");
		DataReferenceImpl data_ref = new DataReferenceImpl("data_ref");

		// Get display's graphics mode control and draw scales
		GraphicsModeControl dispGMC = display.getGraphicsModeControl();
		dispGMC.setScaleEnable(true);
		dispGMC.setLineWidth(2.0f);
		// Create the ScalarMaps: 
		ScalarMap xMap = new ScalarMap(x, Display.XAxis);
		ScalarMap yMap = new ScalarMap(y, Display.YAxis);
		ScalarMap imageMap = new ScalarMap( z, Display.RGB );
		display.addMap(xMap);
		display.addMap(yMap);
		display.addMap( imageMap );
		//set the new FlatField as our data
		data_ref.setData( data_ff );
		// Add reference to display
		display.addReference(data_ref);
	}
	
	DisplayImpl getDisplay(){
		return display;
	}

}
