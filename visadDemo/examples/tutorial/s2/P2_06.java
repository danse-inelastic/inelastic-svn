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
  VisAD Tutorial example 2_06
  The same old parabola, but with a different look.
  We use a MathType ( time -> (height, speed) ),
  draw time and height along the x- and y-axis, respectively, and
  map the speed to the line colour. For that we use a ScalarMap with
  speed as RealType and Display.RGB as DisplayRealType
  Use the GraphicsModeControl to change line thickness of
  display
  Run program with java P2_06
 *
 */


public class P2_06{

  // Declare variables
  // The quantities to be displayed in x- and y-axes

  private RealType time, height, speed;

  // height and speed are organized in a Tuple

  private RealTupleType h_s_tuple;


  // The function height = f(time) and speed = f(time)
  // as ( time -> (height, speed) )

  private FunctionType func_t_tuple;


  // Our Data values for time are represented by the set

  private Set time_set;


  // The Data class FlatField, which will hold data.

  private FlatField h_s_ff;

  // The DataReference from the data to display

  private DataReferenceImpl h_s_ref;

  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap timeMap, heightYMap, speedRGBMap;


  public P2_06 (String []args)
    throws RemoteException, VisADException {

    // Create the quantities
    // Use RealType(String name, Unit u,  Set set), set is null

    time = RealType.getRealType("time", SI.second, null);
    height = RealType.getRealType("height", SI.meter, null);

    // Create speed, but without a unit

    speed = RealType.getRealType("speed");

    // Pack height and speed in a Tuple

    h_s_tuple = new RealTupleType(height, speed);


    // Create a FunctionType
    // Use FunctionType(MathType domain, MathType range)


    func_t_tuple = new FunctionType(time, h_s_tuple);


    // Create the time_set, with 5 values, but this time using a
    // Linear1DSet(MathType type, double first, double last, int length)

    int LENGTH = 32;
    time_set = new Linear1DSet(time, -3.0, 3.0, LENGTH);


    // Generate some points with a for-loop for the line
    // Note that we have the parabola height = 45 - 5 * time^2
    // But first we create a float array for the values
    // Note the dimensions of the array:
    //   float[ number_of_range_components ][ number_of_range_samples]


    float[][] h_s_vals = new float[2][LENGTH];


    // ...then we use a method of Set to get the samples from time_set;
    // this call will get the time values
    // "true" means we get a copy from the samples

    float[][] t_vals  = time_set.getSamples( true);

    // finally generate height and speed values
    // height is given by the parabola height = 45 - 5 * time^2
    // and speed by its first derivative speed = -10 * time

    for(int i = 0; i < LENGTH; i++){
      h_s_vals[0][i] =  45.0f - 5.0f * (float) (t_vals[0][i]*t_vals[0][i]);
      h_s_vals[1][i] =  - 10.0f * (float) t_vals[0][i];
    }


    // Create a FlatField
    // Use FlatField(FunctionType type, Set domain_set)


     h_s_ff = new FlatField( func_t_tuple, time_set);


     // and put the height values above in it

     h_s_ff.setSamples(h_s_vals );


    // Create Display and its maps

    // A 2D display

    display = new DisplayImplJ2D("display1");

    // Get display's graphics mode control draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();

    dispGMC.setScaleEnable(true);


    // Create the ScalarMaps: quantity time is to be displayed along XAxis
    // and height along YAxis; speed is mapped to RGB color
    // Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

    timeMap = new ScalarMap( time, Display.XAxis );

    heightYMap = new ScalarMap( height, Display.YAxis );
    speedRGBMap = new ScalarMap( speed, Display.RGB );


    // Add maps to display

    display.addMap( timeMap );
    display.addMap( heightYMap );
    display.addMap( speedRGBMap );


    // Scale yMap. This will scale the y-axis, because heightYMap
    // has DisplayRealType YAxis
    // we simply choose the range from 0.0 to 50.0

    heightYMap.setRange( 0.0, 50.0);


    // Create a data reference and set the FlatField as our data

    h_s_ref = new DataReferenceImpl("h_s_ref");

    h_s_ref.setData( h_s_ff );

    // Add reference to display

    display.addReference( h_s_ref );


    // Create application window, put display into it

    JFrame jframe = new JFrame("VisAD Tutorial example 2_06");
    jframe.getContentPane().add(display.getComponent());

    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P2_06(args);
  }

} //end of Visad Tutorial Program 2_06
