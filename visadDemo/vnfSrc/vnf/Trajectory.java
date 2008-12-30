package vnf;

import java.rmi.RemoteException;

import visad.DataReferenceImpl;
import visad.Display;
import visad.DisplayImpl;
import visad.FlatField;
import visad.FunctionType;
import visad.GraphicsModeControl;
import visad.Gridded2DSet;
import visad.RealTupleType;
import visad.RealType;
import visad.ScalarMap;
import visad.VisADException;
import visad.java2d.DisplayImplJ2D;

public class Trajectory {
	private DisplayImpl display;

	public Trajectory(float[][] xy_vals) throws VisADException, RemoteException{
		// The 2D display, and its the maps
		RealType x = RealType.getRealType("x");
		RealType y = RealType.getRealType("y");			
	    RealType path = RealType.getRealType("path");
		
		// Create the domain tuple
		RealTupleType domain_tuple = new RealTupleType(y, x);				
		FunctionType func_domain_range = new FunctionType( domain_tuple, path);
		Gridded2DSet domain_set = new Gridded2DSet(domain_tuple, xy_vals, xy_vals[0].length);
		// redo the flatfield to contain image data
		// Use FlatField(FunctionType type, Set domain_set)
		FlatField data_ff = new FlatField( func_domain_range, domain_set);

		// ...and put the z values above into it
		// Note the argument false, meaning that the array won't be copied
		//data_ff.setSamples( z_vals);

		// The DataReference from the data to display
		DataReferenceImpl data_ref = new DataReferenceImpl("data_ref");
		
		display = new DisplayImplJ2D("display1");
		GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();
		dispGMC.setScaleEnable(true);
		// Create the ScalarMaps: 
		ScalarMap xMap = new ScalarMap(x, Display.XAxis);
		ScalarMap yMap = new ScalarMap(y, Display.YAxis);
		ScalarMap trajectoryMap = new ScalarMap( path, Display.RGB );
		display.addMap( trajectoryMap );

		display.addMap(xMap);
		display.addMap(yMap);
		// set the display with the new data
		//display.removeReference(data_ref);
		data_ref.setData( data_ff );
		// Add reference to display
		display.addReference(data_ref);

	}

	DisplayImpl getDisplay(){
		return display;
	}
	
}
