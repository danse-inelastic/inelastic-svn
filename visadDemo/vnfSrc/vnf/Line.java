package vnf;

import java.rmi.RemoteException;

import visad.DataReferenceImpl;
import visad.Display;
import visad.DisplayImpl;
import visad.FlatField;
import visad.FunctionType;
import visad.GraphicsModeControl;
import visad.Gridded1DSet;
import visad.RealType;
import visad.ScalarMap;
import visad.VisADException;
import visad.java2d.DisplayImplJ2D;

public class Line {

	private DisplayImpl display;

	public Line(float[][]x_vals, float[][]y_vals)
	throws VisADException, RemoteException {
		// Declare variables for 1D Plotters
		RealType x = RealType.getRealType("x", null, null);
		RealType y = RealType.getRealType("y", null, null);
		FunctionType func_domain_range = new FunctionType(x, y);
		// Our Data values for x are represented by the set
		Gridded1DSet x_set = new Gridded1DSet(x, x_vals, x_vals.length);
		// The Data class FlatField, which will hold time and height data
		// and the same for speed
		FlatField data_ff = new FlatField(func_domain_range, x_set);
		// and put the y values above in it
		data_ff.setSamples(y_vals);
		display = new DisplayImplJ2D("display1");
		// Get display's graphics mode control and draw scales
		GraphicsModeControl dispGMC = display.getGraphicsModeControl();
		dispGMC.setScaleEnable(true);
		dispGMC.setLineWidth(2.0f);
		
		
		// The DataReference from the data to display
		DataReferenceImpl data_ref = new DataReferenceImpl("data_ref");
		// Create the ScalarMaps: 
		ScalarMap xMap = new ScalarMap(x, Display.XAxis);
		ScalarMap yMap = new ScalarMap(y, Display.YAxis);
		// Add maps to display
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
