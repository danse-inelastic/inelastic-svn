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
  VisAD Tutorial example 2_05
  Combine examples 2_03 and 2_04, to display the continuous function
  height = 45 - 5 * time^2 as a green line and the point of
  example 2_04 as red dots. The line values are generated with a for-loop
  Add a ScalarMap with SelectRange as DisplayRealType, in order to
  select a range in which the RealTypes can be displayed.
  This will cut the parabola and prevent the first data point to be
  dislayed , that is, data ouside the range don't get drawn
  Run program with java P2_05
 */


public class P2_05{

// Declare variables
  // The quantities to be displayed in x- and y-axes: time and height, respectively
  // Our index is also a RealType

  private RealType time, height, index;


  // A Tuple, to pack time and height together

  private RealTupleType t_h_tuple;


  // The function ( elevation(i), height(i) ), where i = index,
  // represented by ( index -> ( elevation, height) )
  // ( elevation, height) are a Tuple, so we have a FunctionType
  // from index to a tuple

  private FunctionType func_i_tuple,  func_time_height;


  // Our Data values: the domain Set time_set for ( time -> height )
  // and the Set index_set for the indexed points

  private Set time_set, index_set;


  // The Data class FlatField, which will hold time and height data.
  // time Data for line is implicitely given by the Set time_set
  // point_vals_ff holds the point values

  private FlatField line_ff, points_ff;


  // The DataReference from the data to display

  private DataReferenceImpl points_ref, line_ref;


  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap timeMap, heightMap, timeRangeMap;



  public P2_05 (String []args)
    throws RemoteException, VisADException {

    // Create the quantities
    // x and y are measured in SI meters
    // Use RealType(String name, Unit u,  Set set), set is null

    time = RealType.getRealType("time", SI.second, null);
    height = RealType.getRealType("height", SI.meter, null);

   // Code for setting POINT data

    // Organize time and height in a Tuple

    t_h_tuple = new RealTupleType( time, height);

    // Index has no unit, just a name

    index = RealType.getRealType("index");

    // Create a FunctionType ( index -> ( time, height) ), for points
    // Use FunctionType(MathType domain, MathType range)

    func_i_tuple = new FunctionType( index, t_h_tuple);

    // Create index_set, but this time using a
    // Integer1DSet(MathType type, int length)

    index_set = new Integer1DSet(index, 5);


    // These are our actual data values for time and height
    // Note that these values correspond to the parabola of the
    // previous examples. The y (height) values are the same, but the x (time)
    // values are explicitely given.

    float[][] point_vals = new float[][]{{-3.0f, -1.5f, 0.0f, 1.5f, 3.0f,},
                                         {0.0f, 33.75f, 45.0f, 33.75f, 0.0f,} };


    // Create a FlatField, that is the Data class for the samples
    // Use FlatField(FunctionType type, Set domain_set)

    // for the (time, height) points

    points_ff = new FlatField( func_i_tuple, index_set);


    // and finally put the points and height values above into the points FlatField

    points_ff.setSamples( point_vals );



   // Code for setting LINE data


    // the FunctionType for the line, function ( time -> height)

    func_time_height = new FunctionType(time, height);

    // Create a time_set, with LENGTH = 25 values, for continuous line

    int LENGTH = 25;
    time_set = new Linear1DSet(time, -3.0, 3.0, LENGTH );

    // Generate some (25) points with a for-loop for the line
    // Note that we have the parabola height = 45 - 5 * time^2
    // But first we create a float array for the values

    float[][] h_vals = new float[1][LENGTH];

    // ...then we use a method of Set to get the samples from time_set;
    // this call will get the time values
    // "true" means we get a copy from the samples

    float[][] d_vals  = time_set.getSamples( true);

    for(int i = 0; i < LENGTH; i++)
      h_vals[0][i] =  45.0f - 5.0f * (float) (d_vals[0][i]*d_vals[0][i]);

    // Create a FlatField, that is the Data class for the samples
    // Use FlatField(FunctionType type, Set domain_set)
    // for the line

    line_ff = new FlatField( func_time_height, time_set);

    // and finally put the points and height values into the line FlatField

    line_ff.setSamples( h_vals );


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
    heightMap = new ScalarMap( height,   Display.YAxis );

    // We create a new ScalarMap, with time as RealType and SelectRange as DisplayRealType

    timeRangeMap = new ScalarMap( time, Display.SelectRange );

    // Add maps to display

    display.addMap( timeMap );
    display.addMap( heightMap );
    display.addMap( timeRangeMap );

    // Scale heightMap. This will scale the y-axis, because heightMap has DisplayRealType YAXIS
    // We simply choose the range from -4 to 4 for the x-axis
    // and -10.0 to 50.0 for


    timeMap.setRange( -4.0, 4.0);
    heightMap.setRange( -10.0, 50.0);

    // Select the range of RealType time

    RangeControl timeRangeControl = (RangeControl) timeRangeMap.getControl();

    float[] timeRange = {  -2.0f, 4.0f };
    timeRangeControl.setRange( timeRange );


    // Create a data reference and set the FlatField as our data

    points_ref = new DataReferenceImpl("points_ref");
    line_ref = new DataReferenceImpl("line_ref");

    points_ref.setData( points_ff );
    line_ref.setData( line_ff );


    // Only change from the previous version
    // Define a ConstantMap to draw large red points

    ConstantMap[] pointsCMap = {     new ConstantMap( 1.0f, Display.Red),
        			     new ConstantMap( 0.0f, Display.Green),
        			     new ConstantMap( 0.0f, Display.Blue),
        			     new ConstantMap( 4.50f, Display.PointSize)};

    ConstantMap[] lineCMap = {       new ConstantMap( 0.0f, Display.Red),
        			     new ConstantMap( 0.8f, Display.Green),
        			     new ConstantMap( 0.0f, Display.Blue),
        			     new ConstantMap( 1.50f, Display.LineWidth)};


    // Add reference to display, and link DataReference to ConstantMap

    display.addReference( points_ref, pointsCMap );
    display.addReference( line_ref , lineCMap);


    // Create application window, put display into it

    JFrame jframe = new JFrame("VisAD Tutorial example 2_05");
    jframe.getContentPane().add(display.getComponent());

    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P2_05(args);
  }

} //end of Visad Tutorial example 2_05
