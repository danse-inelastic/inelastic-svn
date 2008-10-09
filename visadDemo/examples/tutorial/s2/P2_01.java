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
  Enhanced version of program P1_01.
  Draw function height = 45 - 5 * time^2
  Rename RealTypes and attach units to them.
  Draw scales on display to show the RealTypes names.
  Run program with java P2_01
 */


public class P2_01{

  // Declare variables
  // The quantities to be displayed in x- and y-axes

  private RealType time, height;


  // The function height = f( time ), represented by ( time -> height )

  private FunctionType func_t_h;


  // Our Data values for time are represented by the set

  private Set time_set;


  // The Data class FlatField, which will hold time and height data.
  // time data are implicitly given by the Set time_set

  private FlatField h_vals_ff;


  // The DataReference from the data to display

  private DataReferenceImpl data_ref;


  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap timeMap, heightMap;

  // The constructor for our example class

  public P2_01 (String []args)
    throws RemoteException, VisADException {

    // Create the quantities
    // time and height are measured in SI seconds and SI meters, respectively
    // Use RealType(String name, Unit u,  Set set), set is null

    time = RealType.getRealType("time", SI.second, null);
    height = RealType.getRealType("height", SI.meter, null);


    // Create a FunctionType, that is the class which represents the function
    // height = f(time), that is the MathType ( time -> height )
    // Use FunctionType(MathType domain, MathType range)

    func_t_h = new FunctionType(time, height);


    // These are our actual data values

    // Create the time_set, with 5 integer values, ranging from 0 to 4.
    // That means, that there should be 5 values for height.
    // Use Integer1DSet(MathType type, int length)

    time_set = new Integer1DSet(time, 5);

    // ...the height values

    float[][] h_vals = new float[][]{{0.0f, 33.75f, 45.0f, 33.75f, 0.0f,} };


    // Create a FlatField, that is the class for the samples
    // Use FlatField(FunctionType type, Set domain_set)

    h_vals_ff = new FlatField( func_t_h, time_set);


    // and put the height values above in it

    h_vals_ff.setSamples( h_vals );


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


    // Create a data reference and set the FlatField as our data

    data_ref = new DataReferenceImpl("data_ref");

    data_ref.setData( h_vals_ff );


    // Add reference to display

    display.addReference( data_ref );


    // Create application window, put display into it

    JFrame jframe = new JFrame("My second VisAD application");
    jframe.getContentPane().add(display.getComponent());


    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);

  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P2_01(args);
  }

} //end of Visad Tutorial Program 2_01
