/*
VisAD Tutorial
Copyright (C) 2000 Ugo Taddei
*/

package tutorial.s2;

// Import needed classes

import visad.*;
import visad.java2d.DisplayImplJ2D;
import java.rmi.RemoteException;
import java.awt.*;
import javax.swing.*;

/**
VisAD Tutorial example 2_04
  Simple extension of example P2_03
  We link a ConstantMap to our DataReference, in order to
  get large red points.
  Data is organized as MathType (  index -> ( time, height ) )
  Run program with java P2_04
 */


public class P2_04{

  // Declare variables
  // The quantities to be displayed in x- and y-axes: time and height, respectively
  // Our index is alos a RealType

  private RealType time, height, index;


  // A Tuple, to pack time and height together

  private RealTupleType t_h_tuple;


  // The function ( time(i), height(i) ), where i = index,
  // represented by ( index -> ( time, height) )
  // ( time, height) are a Tuple, so we have a FunctionType
  // from index to a tuple

  private FunctionType func_i_tuple;


  // Our Data values, the points, are now indexed by the Set

  private Set index_set;


  // The Data class FlatField, which will hold time and height data.
  // time data are implicitely given by the Set time_set

  private FlatField vals_ff;


  // The DataReference from the data to display

  private DataReferenceImpl data_ref;


  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap timeMap, heightMap;


  public P2_04 (String []args)
    throws RemoteException, VisADException {

    // Create the quantities
    // x and y are measured in SI meters
    // Use RealType(String name, Unit u,  Set set), set is null

    time = RealType.getRealType("time", SI.second, null);
    height = RealType.getRealType("height", SI.meter, null);


    // Organize time and height in a Tuple

    t_h_tuple = new RealTupleType( time, height);


    // Index has no unit, just a name

    index = RealType.getRealType("index");


    // Create a FunctionType ( index -> ( time, height) )
    // Use FunctionType(MathType domain, MathType range)

    func_i_tuple = new FunctionType( index, t_h_tuple);

    // Create the x_set, with 5 values, but this time using a
    // Integer1DSet(MathType type, int length)

    index_set = new Integer1DSet(index, 5);


    // These are our actual data values for time and height
    // Note that these values correspond to the parabola of the
    // previous examples. The y (height) values are the same, but the x (time)
    // are now given given.

    float[][] point_vals = new float[][]{{-3.0f, -1.5f, 0.0f, 1.5f, 3.0f,},
    					 {0.0f, 33.75f, 45.0f, 33.75f, 0.0f,} };

    // Create a FlatField, that is the Data class for the samples
    // Use FlatField(FunctionType type, Set domain_set)

    vals_ff = new FlatField( func_i_tuple, index_set);


     // and put the height values above in it

    vals_ff.setSamples( point_vals );


    // Create Display and its maps

    // A 2D display

    display = new DisplayImplJ2D("display1");


    // Get display's graphics mode control and draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();
    dispGMC.setScaleEnable(true);


    // Create the ScalarMaps: quantity time is to be displayed along XAxis
    // and height along YAxis
    // Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

    timeMap = new ScalarMap( time, Display.XAxis );
    heightMap = new ScalarMap( height, Display.YAxis );


    // Add maps to display

    display.addMap( timeMap );
    display.addMap( heightMap );


    // Scale heightMap. This will scale the y-axis, because heightMap has DisplayRealType YAXIS
    // We simply choose the range from -4 to 4 for the x-axis
    // and -10.0 to 50.0 for

    timeMap.setRange( -4.0, 4.0);
    heightMap.setRange( -10.0, 50.0);


    // Create a data reference and set the FlatField as our data

    data_ref = new DataReferenceImpl("data_ref");

    data_ref.setData( vals_ff );


    // Only change from the previous version
    // Define a ConstantMap to draw large red points

    ConstantMap[] pointsCMap = {   new ConstantMap( 1.0f, Display.Red),
        	     new ConstantMap( 0.0f, Display.Green),
        	     new ConstantMap( 0.0f, Display.Blue),
        	     new ConstantMap( 3.50f, Display.PointSize)};


    // Add reference to display, and link DataReference to ConstantMap

    display.addReference( data_ref, pointsCMap );


    // Create application window, put display into it

    JFrame jframe = new JFrame("VisAD Tutorial example 2_04");
    jframe.getContentPane().add(display.getComponent());


    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P2_04(args);
  }

} //end of Visad Tutorial example 2_04
