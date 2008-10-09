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
  Somewhat different version of program P2_07
  We reorganize the MathType of example P2_07 ( time -> (height, speed) )
  as
   ( time -> height )
  and
   ( time -> speed )
  When then plot time (along x-axis) against height and speed, both (along y-axis)
  The color of speed display is changed to match the line color os speed
 */


public class P2_08{

  // Declare variables
  // The quantities to be displayed in x- and y-axes

  private RealType time,height,speed;


  // The functions ( time -> height )
  // and ( time -> speed )

  private FunctionType func_t_h, func_t_s;


  // Our Data values for x are represented by the set

  private Set time_set;


  // A new unit, to measure speed

  private Unit mps;


  // The Data class FlatField, which will hold time and height data
  // and the same for speed

  private FlatField height_ff, speed_ff;

  // The DataReference from the data to display

  private DataReferenceImpl t_h_ref, t_s_ref;

  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap timeMap, heightYMap, hcMap, speedYMap, scMap;


  public P2_08 (String []args)
    throws RemoteException, VisADException {

    // Create the quantities
    // x and y are measured in SI meters
    // Use RealType(String name, Unit u,  Set set), set is null

    time = RealType.getRealType("time", SI.second, null);
    height = RealType.getRealType("height", SI.meter, null);

    // Create a new unit for speed, meters per seconds

    mps = SI.meter.divide( SI.second );

    speed = RealType.getRealType("speed", mps, null);


   // Create a FunctionType, that is the class which represents the function y = f(x)
   // Use FunctionType(MathType domain, MathType range)

    func_t_h = new FunctionType( time, height );
    func_t_s = new FunctionType( time, speed );


    // Create the time_set, with 5 values, but this time using a
    // Linear1DSet(MathType type, double first, double last, int length)

    int LENGTH = 32;
    time_set = new Linear1DSet(time, -3.0, 3.0, LENGTH);

        // Generate some points with a for-loop for the line
    // Note that we have the parabola height = 45 - 5 * time^2
    // But first we create a float array for the values

    float[][] h_vals = new float[1][LENGTH];
    float[][] s_vals = new float[1][LENGTH];

    // ...then we use a method of Set to get the samples from time_set;
    // this call will get the time values
    // "true" means we get a copy from the samples

    float[][] t_vals  = time_set.getSamples( true);


    // finally generate height and speed values
    // height is given by the parabola height = 45 - 5 * time^2
    // and speed by its first derivative speed = -10 * time

    for(int i = 0; i < LENGTH; i++){

     // height values...
      h_vals[0][i] =  45.0f - 5.0f * (float) (t_vals[0][i]*t_vals[0][i]);

     // ...and speed values: the derivative of the above function
      s_vals[0][i] =  - 10.0f * (float) t_vals[0][i];
    }


    // Create the FlatFields
    // Use FlatField(FunctionType type, Set domain_set)

     height_ff = new FlatField( func_t_h, time_set);
     speed_ff = new FlatField( func_t_s, time_set);


     // and put the y values above in it

    height_ff.setSamples( h_vals );
    speed_ff.setSamples( s_vals );

    // Create Display and its maps

    // A 2D display

    display = new DisplayImplJ2D("display1");

    // Get display's graphics mode control and draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();
    dispGMC.setScaleEnable(true);
    dispGMC.setLineWidth( 2.0f );

    // Create the ScalarMaps: quantity time is to be displayed along XAxis,
    // and height and speed along YAxis
    // Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

    timeMap = new ScalarMap( time, Display.XAxis );

    heightYMap = new ScalarMap( height, Display.YAxis );

    speedYMap = new ScalarMap( speed, Display.YAxis );


    // Add maps to display

    display.addMap( timeMap );
    display.addMap( heightYMap );
    display.addMap( speedYMap );


    // Scale heightYMap
    // we simply choose the range from 0.0 to 50.0

    heightYMap.setRange( 0.0, 50.0);

    // Choose yellow as the color for the speed curve

    float speedRed = 1.0f;
    float speedGreen = 1.0f;
    float speedBlue = 0.0f;


    float[] speedColor = new float[]{speedRed, speedGreen, speedBlue};

    // ...and color the axis with the same yellow

    speedYMap.setScaleColor( speedColor );

    // uncomment the following line if you don't want speed axis to be drawn

    // speedYMap.setScaleEnable(false);

    // Create a data reference and set the FlatField as our data

    t_h_ref = new DataReferenceImpl("t_h_ref");
    t_s_ref = new DataReferenceImpl("t_s_ref");

    t_h_ref.setData( height_ff );
    t_s_ref.setData( speed_ff );

    // Add reference to display

    display.addReference( t_h_ref );

    // Create Constantmaps for speed and add its reference to display

    ConstantMap[] speedCMap = {  new ConstantMap( speedRed, Display.Red),
        		        new ConstantMap( speedGreen, Display.Green),
        		        new ConstantMap( speedBlue, Display.Blue),
        		        new ConstantMap( 1.50f, Display.LineWidth)};

    display.addReference( t_s_ref, speedCMap );


    // Create application window, put display into it

    JFrame jframe = new JFrame("VisAD Tutorial example 2_08");
    jframe.getContentPane().add(display.getComponent());

    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P2_08(args);
  }

} //end of Visad Tutorial Program 2_08
